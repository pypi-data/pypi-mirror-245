# %%
import sys
import time
import os

sys.path.append("util")
from read_bam_file import read_bam_file
from get_mutations import get_all_mutations
from refseq import get_reference

import numpy as np
import pandas as pd
import argparse


def humansize(nbytes):
    """
    returns a human-readable string representation of a number of bytes.

    INPUTS:
    nbytes: integer; number of bytes
    OUTPUTS:
    a string with the number of bytes in a human-readable format
    """
    suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


def get_files(fpath):
    """
    get all bam files in a directory if given, if it is a file, return the file name.
    """
    files_to_analyse = []
    isFile = os.path.isfile(fpath)

    # checks if path is a directory
    isDirectory = os.path.isdir(fpath)

    files_to_analyse = []
    if isFile and fpath.endswith(".bam") or fpath.endswith(".cram"):
        files_to_analyse.append(fpath)
    elif isDirectory:
        for file in os.listdir(fpath):
            if file.endswith(".bam") or file.endswith(".cram"):
                files_to_analyse.append(os.path.join(fpath, file))
    else:
        print("The path is invalid.")

    if len(files_to_analyse) == 0:
        print("No files to analyse")
        return None

    files_to_analyse.sort()
    print("Files to analyse: ", *files_to_analyse, sep="\n")
    return files_to_analyse


if __name__ == "__main__":
    # get files to analyse from command line
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument(
        "path",
        help="path to the directory containing bam/cram files or to the bam/cram file directly",
    )
    parser.add_argument("ref", help="path to the reference sequence file")
    parser.add_argument(
        "-o",
        "--output",
        help="path to the output directory (default: current directory)",
        default=os.getcwd(),
    )
    parser.add_argument(
        "-p",
        "--filter_per",
        help="percentage of reads that must contain a mutation to be kept as a mutation",
        type=float,
        default=0.0,
    )
    parser.add_argument(
        "-n",
        "--filter_num",
        help="number of reads that must contain a mutation to be kept as a mutation",
        type=int,
        default=0,
    )

    # parse the arguments
    args = parser.parse_args()

    # access the values of the arguments
    fpath = args.path
    ref_path = args.ref
    output_dir = args.output
    filter_per = args.filter_per
    filter_num = args.filter_num

    files_to_analyse = get_files(fpath)
    if files_to_analyse is None:
        exit()

    global_start_time = time.time()

    REFSEQ = get_reference(ref_path)
    for file_name in files_to_analyse:
        print("Analyzing: ", file_name)
        startTime = time.time()
        print("Strating...")
        readInfoDf = read_bam_file(file_name)
        weights = readInfoDf["Counts"]
        nbReads = readInfoDf.shape[0]
        # print("readInfoDf.shape: ", readInfoDf.shape)
        # print("*-* time for read_bam_file: ", time.time() - startTime)
        # get mutations
        startTime = time.time()
        (
            results_relative_mutation_index,
            results_ablolute_positions,
            mutations_kept,
        ) = get_all_mutations(readInfoDf, REFSEQ, filter_per, filter_num)
        # print("*-* time for get_all_mutations: ", time.time() - startTime)
        # remove invalid mutations (mutations containing 'N' or '=')
        # need to be coded more flexibly if in the future more unexpected errors occur.
        startTime = time.time()
        rand_id = np.random.randint(0, 10000000)

        df_mutations_kept = pd.DataFrame(mutations_kept, columns=["Mutations"])

        # export results
        results_relative_mutation_index[
            ["startIdx_mutations_Based", "endIdx_mutations_Based", "muts"]
        ].to_csv(
            os.path.join(
                output_dir,
                f"Xsparse_relative_{file_name.split('/')[-1]}_filter{filter_per}_{filter_num}_{rand_id}.csv",
            ),
            index=False,
        )
        results_ablolute_positions[["startIdx_0Based", "endIdx_0Based", "muts"]].to_csv(
            os.path.join(
                output_dir,
                f"Xsparse_absolute_{file_name.split('/')[-1]}_filter{filter_per}_{filter_num}_{rand_id}.csv",
            ),
            index=False,
        )
        results_relative_mutation_index["Counts"].to_csv(
            os.path.join(
                output_dir,
                f"Wsparse_relative_{file_name.split('/')[-1]}_filter{filter_per}_{filter_num}_{rand_id}.csv",
            ),
            index=False,
        )
        results_ablolute_positions["Counts"].to_csv(
            os.path.join(
                output_dir,
                f"Wsparse_absolute_{file_name.split('/')[-1]}_filter{filter_per}_{filter_num}_{rand_id}.csv",
            ),
            index=False,
        )
        df_mutations_kept.to_csv(
            os.path.join(
                output_dir,
                f"mutations_index_{file_name.split('/')[-1]}_filter{filter_per}_{filter_num}_{rand_id}.csv",
            ),
            index=False,
        )
    # print("time to save csv file:", time.time() - startTime)
    print("**** total time: ", round(time.time() - global_start_time, 2), "s ****")


# %%
