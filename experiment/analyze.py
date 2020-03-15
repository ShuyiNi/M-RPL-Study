#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument("exp_dir", type=Path)
    args = parser.parse_args()
    exp_dir = args.exp_dir

    bin_width = 10  # s
    df_rpl = measure_metrics(exp_dir / "log/rpl/packet-log.csv", bin_width)
    df_mrpl = measure_metrics(exp_dir / "log/mrpl/packet-log.csv", bin_width)
    make_plots(df_rpl, df_mrpl, exp_dir / "result")


def measure_metrics(log_file, bin_width):
    df = pd.read_csv(log_file)
    t_max = df.dropna()["t_recv"].max()
    n_max = int(t_max / bin_width)
    bins = [bin_width * i for i in range(n_max + 1)]
    grp = df.groupby(pd.cut(df["t_recv"], bins))
    grp_mean = grp.mean()
    grp_count = grp.count()

    data = {}
    data["time"] = grp_mean["t_recv"].values
    data["latency"] = grp_mean["latency"].values
    data["throughput"] = grp_count["t_recv"].values / bin_width

    return pd.DataFrame(data)


def make_plots(df_rpl, df_mrpl, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)

    mpl.rcParams["figure.figsize"] = (3.2, 2.4)
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["font.size"] = 9
    mpl.rcParams["axes.labelsize"] = 9
    mpl.rcParams["xtick.labelsize"] = 9
    mpl.rcParams["ytick.labelsize"] = 9
    mpl.rcParams["legend.fontsize"] = 9

    rpl_style = {"color": "black", "linestyle": "-", "label": "RPL"}
    mrpl_style = {"color": "black", "linestyle": "--", "label": "M-RPL"}
    ylabel = {"throughput": "Throughput (packets/s)", "latency": "Latency (s)"}
    for metric in ["throughput", "latency"]:
        plt.figure()
        plt.plot(df_rpl["time"], df_rpl[metric], **rpl_style)
        plt.plot(df_mrpl["time"], df_mrpl[metric], **mrpl_style)
        plt.legend()
        plt.xlabel("Time (s)")
        plt.ylabel(ylabel[metric])
        plt.xlim(0, None)
        plt.ylim(0, None)
        plt.tight_layout()
        plt.savefig(out_dir / f"{metric}.pdf")
        plt.close()


if __name__ == "__main__":
    main()
