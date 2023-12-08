# %%
import numpy as np
import time
import pandas as pd
import sys
import os
import bisect
from ast import literal_eval

from concurrent.futures import ProcessPoolExecutor

sys.path.append("./")
# from VariantsProportionFreyjaSparse import VariantsProportionFreyjaSparse
from util import VariantsProportionFreyjaSparse


# %%
def get_files(fpath):
    # checks if path is a file
    isFile = os.path.isfile(fpath)

    # checks if path is a directory
    isDirectory = os.path.isdir(fpath)

    files_to_analyse = []
    if isFile and fpath.endswith(".csv"):
        files_to_analyse.append(fpath)
    elif isDirectory:
        for file in os.listdir(fpath):
            if file.startswith("Xsparse_absolute_") and file.endswith(".csv"):
                files_to_analyse.append(os.path.join(fpath, file))
                # files_to_analyse.append(fpath + "/" + file)
    else:
        print("The path is not a file or a directory")

    if len(files_to_analyse) == 0:
        print("No files to analyse")
        # return
    # print("Files to analyse: ", *files_to_analyse, sep="\n")
    files_to_analyse.sort()

    files_to_analyse = np.array(files_to_analyse)
    # reverse the order of the files
    files_to_analyse = files_to_analyse[::-1]
    return files_to_analyse


# %%
def get_sample_bootstrap_weight(weights):
    positions = np.random.choice(
        np.arange(len(weights)),
        size=np.sum(weights),
        replace=True,
        p=weights / np.sum(weights),
    )
    return np.bincount(positions, minlength=len(weights))


def extract_positions(mut_str):
    """
    returns the position (extract digits from a string) in a mutation string
    """
    return int("".join([i for i in mut_str if i.isdigit()]))


PATH_X_MATRIXs = "../../EauDeParis/X_sparse"
PATH_RESULT = "../../EauDeParis/X_sparse_result_freyja"
PATH_M_MATRIX = "../../Arnaud/proposed_lineages_list4SUMMIT.stringent.freyja0001.csv"
NbBootstraps = 10
alphaInit = 0.01
freezeAlpha = False
files_to_analyze = get_files(PATH_X_MATRIXs)


def analyse_file(file):
    M = pd.read_csv(PATH_M_MATRIX, index_col=0)
    # # Remove row B
    M = M.drop("B")

    # Filtrage proposé par Arnaud
    # keep only columns that have at least one cell with a value > 0.1
    M = M.loc[:, M.max(axis=0) > 0.1]

    # My filter
    # M = M.T
    # gisaidMat = M.loc[M.max(axis=1) > 0.02]
    # variants = gisaidMat.columns
    # varStd = gisaidMat[variants].std(axis=1)
    # # this is to ensure that I only keep mutations that are NOT equally characterising
    # # the variants of interest.
    # # for that, I simply keep mutations that have some deviation in occurence accross the variants
    # mutList1 = list(gisaidMat.loc[varStd >= np.percentile(varStd, 20)].index)
    # # add some noise
    # mutList2 = list(
    #     np.random.choice(
    #         gisaidMat.loc[varStd < np.percentile(varStd, 20)].index, size=min(50, len(gisaidMat.loc[varStd < np.percentile(varStd, 20)].index.to_list())), replace=False
    #     )
    # )
    # subGisaidMat = gisaidMat.loc[gisaidMat.index.isin(mutList1 + mutList2), variants]
    # M = subGisaidMat.T

    variants = M.index.values
    # M = pd.read_csv('data/MmatrixFreyjaOldDelsFULL.csv', index_col=0)
    # M = M.T
    muts_data_df = pd.read_csv(file)
    Weights_df = pd.read_csv(file.replace("Xsparse_absolute_", "Wsparse_absolute_"))
    mut_idx_df = pd.read_csv(file.replace("Xsparse_absolute_", "mutations_index_"))
    muts_data = [set(literal_eval(x)) if not pd.isna(x) else set() for x in muts_data_df.muts.values]

    starts_idx = muts_data_df.startIdx_0Based.values
    ends_idx = muts_data_df.endIdx_0Based.values

    Weights = Weights_df.Counts.values
    muts_idx = mut_idx_df.Mutations.values

    # print('Number of mutations in M matrix: ', M.shape[1])
    # print('Number of mutations in bam: ', len(muts_idx))
    muts_in_bam_and_M = set(muts_idx).intersection(set(M.columns))
    muts_to_analyse = set(M.columns)
    muts_to_analyse = {mut: extract_positions(mut) for idx, mut in enumerate(muts_to_analyse)}
    muts_to_analyse = {k: v for k, v in sorted(muts_to_analyse.items(), key=lambda item: item[1])}
    all_positions = list(muts_to_analyse.values())
    # Update start and end index to be relative to mutations, not absulute to the reference
    starts_idx_new = muts_data_df["startIdx_0Based"].apply(lambda x: min(len(muts_to_analyse) - 1, bisect.bisect_left(all_positions, x + 1)))
    starts_idx_new = starts_idx_new.to_numpy()
    ends_idx_new = muts_data_df["endIdx_0Based"].apply(lambda x: bisect.bisect_right(all_positions, x + 1))
    ends_idx_new = ends_idx_new.to_numpy()
    # update mutations_index to take into account the mutations that are not present in bam but present in M matrix
    temp_muts_dict = {mut: [idx, muts_to_analyse[mut]] for idx, mut in enumerate(muts_to_analyse.keys())}
    muts_idx_new = [temp_muts_dict[mut][0] for mut in muts_in_bam_and_M]
    muts_data_new = []
    for mut_set in muts_data:
        res = set()
        for mut in mut_set:
            if muts_idx[mut] in muts_in_bam_and_M:
                res.add(temp_muts_dict[muts_idx[mut]][0])
        muts_data_new.append(res)
    muts_data_new = np.array(muts_data_new)
    M = M[list(muts_to_analyse.keys())].to_numpy().T
    nM, nV = M.shape
    mutations = np.array(list(muts_to_analyse.keys()))

    resFreyja = np.zeros((NbBootstraps, 4 + nV))
    top5_list = []
    print("Number of reads: ", np.sum(Weights))
    for i in range(NbBootstraps):
        print("Bootstrap: ", i + 1)
        weight = get_sample_bootstrap_weight(Weights)  # Do the bootstrap on the weights not on the X matrix to reduce the memory usage
        start = time.time()
        res_Freyja = VariantsProportionFreyjaSparse.VariantsProportionFreyjaSparse(
            starts_idx_new,
            ends_idx_new,
            muts_data_new,
            M,
            alphaInit=alphaInit,
            readsCount=weight,
        )
        res_Freyja()
        res_Freyja.fit(freezeAlpha=freezeAlpha)
        # if np.abs(pi0 - pi000)<0.001:
        result = res_Freyja.solution

        # order result idx by decreasing order
        idxs = np.argsort(result)[::-1]
        # print result
        # for i in idxs:
        #     print(variants[i], res_Freyja.params[i])
        # save result

        # get top 5 name variants with highest proportion of co-occurrence with their proportion on str
        top5 = [variants[i] + ": " + str(result[i]) + "|" for i in idxs[:5]]
        # convert list to string
        top5 = "".join(top5)
        top5_list.append(top5[:-1])
        resFreyja[i, :nV] = result
        resFreyja[i, nV + 2] = res_Freyja.time_used
        resFreyja[i, nV + 3] = res_Freyja.alpha
        print(top5)

    # save result df
    resFreyja_df = pd.DataFrame(
        resFreyja,
        columns=list(variants) + ["nbIter", "averageTimePerIter", "time_used", "alpha"],
    )
    resFreyja_df["top5"] = top5_list
    resFreyja_df["file"] = file.replace("Xsparse_", "").split("/")[-1]
    # make file first column and top5 second column
    cols = resFreyja_df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    resFreyja_df = resFreyja_df[cols]

    resFreyja_df["nbReads"] = len(Weights)
    resFreyja_df["nbMutations"] = len(mutations)
    # convert to int
    resFreyja_df["nbReads"] = resFreyja_df["nbReads"].astype(int)
    resFreyja_df["nbMutations"] = resFreyja_df["nbMutations"].astype(int)
    resFreyja_df["nbIter"] = resFreyja_df["nbIter"].astype(int)
    # save result on csv
    save_path = os.path.join(PATH_RESULT, file.replace("Xsparse_", "").split("/")[-1])
    print("saving :", save_path)
    resFreyja_df.to_csv(save_path, index=False)


# analyse_file(files_to_analyze[0])
max_workers = 8
with ProcessPoolExecutor(max_workers=max_workers) as executor:
    executor.map(analyse_file, files_to_analyze)
