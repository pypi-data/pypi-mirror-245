import os
import argparse
import torch
from sklearn.metrics import roc_auc_score
import numpy as np
from maldi_nn.models import AMRModel
from maldi_nn.utils.data import DRIAMSAMRDataModule
from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping
from lightning.pytorch.loggers import TensorBoardLogger
from lightning.pytorch import Trainer
from importlib.resources import files
import json
import ast
import h5torch


def boolean(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.MetavarTypeHelpFormatter
):
    pass


# eval phase:
def micro_roc_auc(trues, preds, locs, drug_names):
    return roc_auc_score(trues, preds)


def macro_roc_auc(trues, preds, locs, drug_names):
    t = []
    for c in np.unique(drug_names):
        trues_sub = trues[drug_names == c]
        if len(np.unique(trues_sub)) > 1:
            preds_sub = preds[drug_names == c]
            t.append(roc_auc_score(trues_sub, preds_sub))
    return np.mean(t)


def instance_roc_auc(trues, preds, locs, drug_names):
    r, c = np.unique(locs, return_counts=True)
    pos = 0
    total = 0
    for r_ in r[c > 1]:
        trues_sub = trues[locs == r_]
        if len(np.unique(trues[locs == r_])) > 1:
            preds_sub = preds[locs == r_]
            p = preds_sub[trues_sub == 1][:, None] >= preds_sub[trues_sub == 0]
            pos += p.sum()
            total += p.size
    return pos / total


def prec_at_1_neg(trues, preds, locs, drug_names):
    r, c = np.unique(locs, return_counts=True)
    pos = 0
    total = 0
    for r_ in r[c > 1]:
        trues_sub = trues[locs == r_]
        if len(np.unique(trues[locs == r_])) > 1:
            preds_sub = preds[locs == r_]
            pos += trues_sub[np.argmin(preds_sub)]
            total += 1
    return (total - pos) / total


size_to_layer_dims = {
    "S": [256, 128],
    "M": [512, 256, 128],
    "L": [1024, 512, 256, 128],
    "XL": [2048, 1024, 512, 256, 128],
    "Linear": [],
}

drug_encoder_args = {
    "onehot": {},
    "kernel": {},
    "ecfp": {"bits": 512, "diameter": 4},
    "cnn": {"alphabet": "deepsmiles"},
    "trf": {"alphabet": "deepsmiles"},
    "gru": {"alphabet": "deepsmiles"},
    "img": {"size": (128, 128), "normalize": True, "inverse": True},
}


def main():
    parser = argparse.ArgumentParser(
        description="Training script for dual-branch AMR recommender fine-tuning on other DRIAMS hospitals.",
        formatter_class=CustomFormatter,
    )

    parser.add_argument("path", type=str, metavar="path", help="path to h5torch file.")
    parser.add_argument(
        "logs_path", type=str, metavar="logs_path", help="path to logs."
    )
    parser.add_argument(
        "drug_embedder",
        type=str,
        metavar="drug_embedder",
        choices=["ecfp", "onehot", "gru", "cnn", "trf", "img", "kernel"],
        help="Which drug embedder to use, choices: {%(choices)s} Ignored if a ckpt_path is given.",
    )
    parser.add_argument(
        "spectrum_embedder",
        type=str,
        metavar="spectrum_embedder",
        choices=["S", "M", "L", "XL", "Linear"],
        help="Which size spectrum embedder to use, choices: {%(choices)s} Ignored if a ckpt_path is given",
    )
    parser.add_argument(
        "hospital",
        type=str,
        metavar="hospital",
        choices=["B", "C", "D"],
        help="Which DRIAMS hospital to fine-tune on, choices: {%(choices)s}",
    )

    parser.add_argument(
        "percent",
        type=float,
        metavar="percent",
        help="Percentage of training data to use (100percent means 1000 samples)",
    )

    parser.add_argument(
        "--ckpt_path",
        type=str,
        default="None",
        help="Checkpoint from which to start training",
    )

    parser.add_argument(
        "--lr",
        type=float,
        default=5e-4,
        help="Learning rate, Ignored if a ckpt_path is given.",
    )
    parser.add_argument(
        "--logging_file",
        type=str,
        default="res.txt",
        help="Which file to write final performances to.",
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=4,
        help="Number of workers in dataloader. Reduce to alleviate CPU.",
    )

    parser.add_argument(
        "--devices",
        type=ast.literal_eval,
        default=1,
        help="devices to use. Input an integer to specify a number of gpus or a list e.g. [1] or [0,1,3] to specify which gpus.",
    )

    args = parser.parse_args()

    dm = DRIAMSAMRDataModule(
        args.path,
        drug_encoder=args.drug_embedder,
        drug_encoder_args=drug_encoder_args[args.drug_embedder],
        batch_size=128,
        n_workers=args.num_workers,
        preprocessor=None,
        min_spectrum_len=None,
        in_memory=False,
    )
    dm.setup(None)

    split_path = files("maldi_nn.utils").joinpath("hospital_split.json")
    hosp_split = json.load(open(split_path))
    train_locs = np.array(hosp_split[args.hospital + "_train"]).astype(bytes)[
        : int(1000 * args.percent)
    ]
    val_locs = np.array(hosp_split[args.hospital + "_val"]).astype(bytes)
    test_locs = np.array(hosp_split[args.hospital + "_test"]).astype(bytes)

    f = h5torch.File(args.path)
    train_rows = np.where(np.isin(f["0/loc"][:], train_locs))[0]
    train_indices = np.isin(f["central/indices"][:][0], train_rows)
    val_rows = np.where(np.isin(f["0/loc"][:], val_locs))[0]
    val_indices = np.isin(f["central/indices"][:][0], val_rows)
    test_rows = np.where(np.isin(f["0/loc"][:], test_locs))[0]
    test_indices = np.isin(f["central/indices"][:][0], test_rows)

    if dm.min_spectrum_len is not None:
        lens_all = np.array([len(tt) for tt in f["0/intensity"][:]])

        lens = lens_all[f["central"]["indices"][0][train_indices]]
        train_indices = train_indices[lens > dm.min_spectrum_len]

        lens = lens_all[f["central"]["indices"][0][val_indices]]
        val_indices = val_indices[lens > dm.min_spectrum_len]

        lens = lens_all[f["central"]["indices"][0][test_indices]]
        test_indices = test_indices[lens > dm.min_spectrum_len]

    f = f.to_dict()

    dm.train = h5torch.Dataset(
        f,
        sampling="coo",
        subset=train_indices,
        sample_processor=dm.processor,
    )

    dm.val = h5torch.Dataset(
        f,
        sampling="coo",
        subset=val_indices,
        sample_processor=dm.processor,
    )

    dm.test = h5torch.Dataset(
        f,
        sampling="coo",
        subset=test_indices,
        sample_processor=dm.processor,
    )

    print(len(dm.train), len(dm.val), len(dm.test))

    drug_embedder_kwargs = {
        "onehot": {
            "num_drugs": len(dm.drug_encoder.vocab),
            "dim": 64,
        },
        "kernel": {
            "n_inputs": len(dm.drug_encoder.embeds),
            "n_outputs": 64,
            "layer_dims": [],
            "dropout": 0.2,
        },
        "ecfp": {"n_inputs": 512, "n_outputs": 64, "layer_dims": [], "dropout": 0.2},
        "cnn": {
            "vocab_size": len(dm.drug_encoder.alphabet_dict),
            "dim": 64,
            "depth": 4,
            "kernel_size": 5,
        },
        "trf": {
            "vocab_size": len(dm.drug_encoder.alphabet_dict),
            "dim": 64,
            "depth": 4,
            "n_head": 8,
        },
        "gru": {"vocab_size": len(dm.drug_encoder.alphabet_dict), "hidden_dim": 64},
        "img": {"stem_downsample": 2, "kernel_size": 5, "hidden_dim": 32, "depth": 2},
    }

    if args.ckpt_path != "None":
        model = AMRModel.load_from_checkpoint(args.ckpt_path)
    else:
        model = AMRModel(
            spectrum_embedder="mlp",
            drug_embedder=args.drug_embedder,
            spectrum_kwargs={
                "n_inputs": 6000,
                "n_outputs": 64,
                "layer_dims": size_to_layer_dims[args.spectrum_embedder],
                "dropout": 0.2,
            },
            drug_kwargs=drug_embedder_kwargs[args.drug_embedder],
            lr=args.lr,
            weight_decay=0,
            lr_decay_factor=1,
            warmup_steps=250,
            scaled_dot_product=True,
        )

    val_ckpt = ModelCheckpoint(monitor="val_micro_auc", mode="max")
    callbacks = [
        val_ckpt,
        EarlyStopping(monitor="val_micro_auc", patience=10, mode="max"),
    ]
    logger = TensorBoardLogger(
        args.logs_path,
        name="finetunehosp_%s_%s_%s_%s_%s"
        % (
            args.drug_embedder,
            args.spectrum_embedder,
            args.lr,
            args.hospital,
            args.percent,
        ),
    )

    trainer = Trainer(
        accelerator="gpu",
        devices=args.devices,
        strategy="auto",
        max_epochs=250,
        callbacks=callbacks,
        logger=logger,
    )

    trainer.fit(model, dm.train_dataloader(), dm.val_dataloader())

    # validation
    p = trainer.predict(
        model, dataloaders=dm.val_dataloader(), ckpt_path=val_ckpt.best_model_path
    )

    trues = torch.cat([pp[0][:, 0] for pp in p]).numpy()
    preds = torch.cat([pp[0][:, 1] for pp in p]).numpy()
    locs = np.concatenate([pp[1] for pp in p])
    drug_names = np.concatenate([pp[2] for pp in p])

    with open(os.path.join(args.logs_path, args.logging_file), "a") as f:
        f.write(
            "%s\tval\t%.5f\t%.5f\t%.5f\t%.5f\n"
            % (
                val_ckpt.best_model_path,
                micro_roc_auc(trues, preds, locs, drug_names),
                macro_roc_auc(trues, preds, locs, drug_names),
                instance_roc_auc(trues, preds, locs, drug_names),
                prec_at_1_neg(trues, preds, locs, drug_names),
            )
        )

    # test
    p = trainer.predict(
        model, dataloaders=dm.test_dataloader(), ckpt_path=val_ckpt.best_model_path
    )

    trues = torch.cat([pp[0][:, 0] for pp in p]).numpy()
    preds = torch.cat([pp[0][:, 1] for pp in p]).numpy()
    locs = np.concatenate([pp[1] for pp in p])
    drug_names = np.concatenate([pp[2] for pp in p])

    with open(os.path.join(args.logs_path, args.logging_file), "a") as f:
        f.write(
            "%s\ttest\t%.5f\t%.5f\t%.5f\t%.5f\n"
            % (
                val_ckpt.best_model_path,
                micro_roc_auc(trues, preds, locs, drug_names),
                macro_roc_auc(trues, preds, locs, drug_names),
                instance_roc_auc(trues, preds, locs, drug_names),
                prec_at_1_neg(trues, preds, locs, drug_names),
            )
        )


if __name__ == "__main__":
    main()
