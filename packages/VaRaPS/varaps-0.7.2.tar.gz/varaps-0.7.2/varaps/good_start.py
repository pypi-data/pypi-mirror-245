import argparse
import os
import sys
import time

import numpy as np

from util import mode1, mode2


def get_input(prompt, default=None, required=False):
    user_input = input(f"{prompt} (default: {default}): ").strip()
    if required and not user_input:
        print("This input is required")
        return get_input(prompt, default, required)
    return user_input if user_input else default


def get_files(path, mode):
    files = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        ext = ".bam" if mode in [1, 3] else ".csv"
        prefix = "" if mode in [1, 3] else "Xsparse_"
        files = [os.path.join(path, f) for f in os.listdir(path) if f.startswith(prefix) and f.endswith(ext)]
    if not files:
        print("No files found to analyze")
        sys.exit(1)
    print("Files to analyze:")
    [print(f) for f in files]
    return files


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m", "--mode", type=int, choices=[1, 2, 3], help="Analysis mode. 1: Extract variants from BAM. " "2: Get proportions from mode 1 output. " "3: Get proportions directly from BAM."
    )

    parser.add_argument("--path", help="File path or directory")
    parser.add_argument("--ref", help="Reference sequence file")
    parser.add_argument("-o", "--output", help="Output directory")

    parser.add_argument("-p", "--filter_per", type=float, help="Filter percentage")
    parser.add_argument("-n", "--filter_num", type=int, help="Filter read count")

    parser.add_argument("--M", help="Profile mutation matrix file")
    parser.add_argument("--NbBootstraps", type=int, help="Number of bootstraps")

    parser.add_argument("--deconv_method", type=int, choices=[1, 2, 3, 4], help="Deconvolution method")

    parser.add_argument("--optibyAlpha", type=lambda x: (str(x).lower() in ["true", "1"]), help="Optimize by error rate")

    parser.add_argument("--alphaInit", type=float, help="Initial alpha value")

    args = parser.parse_args()

    # Get required args interactively if not provided
    if not args.mode:
        args.mode = int(get_input("Enter analysis mode", required=True))

    if args.mode in [1, 3]:
        if not args.path:
            args.path = get_input("Enter path to BAM file/directory", required=True)
        if not args.ref:
            args.ref = get_input("Enter path to reference file", required=True)

    if args.mode in [2, 3]:
        if not args.path:
            args.path = get_input("Enter path to X files", required=True)
        if not args.M:
            args.M = get_input("Enter path to profile matrix", required=True)
        if not args.output:
            args.output = get_input("Enter output directory", required=True)

    # Set default values
    if not args.filter_per:
        args.filter_per = 0.0
    if not args.filter_num:
        args.filter_num = 0
    if not args.deconv_method:
        args.deconv_method = 1
    if args.optibyAlpha is None:
        args.optibyAlpha = True
    if not args.alphaInit:
        args.alphaInit = 0.01
    if not args.NbBootstraps:
        args.NbBootstraps = 1

    return args


def main():
    args = parse_args()

    files = get_files(args.path, args.mode)

    if args.mode == 1:
        for f in files:
            mode1.analyze_file(f, args.ref, args.filter_per, args.filter_num, args.output)

    elif args.mode == 2:
        mode2.analyze_files(files, args.M, args.output, args.NbBootstraps, args.alphaInit, args.optibyAlpha, args.deconv_method)

    elif args.mode == 3:
        temp_dir = f"temp_{int(time.time())}"
        os.mkdir(os.path.join(args.output, temp_dir))

        for f in files:
            mode1.analyze_file(f, args.ref, args.filter_per, args.filter_num, temp_dir)

        mode2.analyze_files(temp_dir, args.M, args.output, args.NbBootstraps, args.alphaInit, args.optibyAlpha, args.deconv_method)


if __name__ == "__main__":
    main()
