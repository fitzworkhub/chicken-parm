"""
The answer sheet provided by the client does not have labels for all documents
provided.  This script will output the differences between the answer key and
documents by comparing the number of pages in a document to the number of rows
for that document in the answer key

The logic for this script will be based on the document naming convention:
<filename>_page_n.pdf
"""

from poctoolkit.folder_utils import files_from_directory
import os
import re
from collections import defaultdict
import pandas as pd


FILENAME_COL = "Filename"
DATA_COL = "Data Counts"
ANSWER_KEY_COL = "Answer Key Counts"
COMPARE_COL = "Comparison"


def convert_to_df(d, column_name):
    df = pd.DataFrame.from_dict(d, orient="index", columns=[column_name])
    df.index.name = FILENAME_COL
    df.reset_index(inplace=True)
    return df


# get all filepaths
data_dir = "/home/fitz/Documents/POC/chicken-parm/data"
split_text_folder = os.path.join(data_dir, "split_pages")
answer_key_folder = os.path.join(data_dir, "answer_keys")

full_filepaths = files_from_directory(split_text_folder, "*.pdf")

# track number of pages for each document
file_count_pdfs = defaultdict(int)
for filepath in full_filepaths:
    filename = os.path.basename(filepath)
    key = re.sub(r"_page_\d+", "", filename)
    key = re.sub(r"\.pdf+", "", key)
    file_count_pdfs[key] += 1
data_counts_df = convert_to_df(file_count_pdfs, DATA_COL)

# Track number of rows per document in answer key
answer_key_filename = "All Samples Answer Key.csv"
answer_key_path = os.path.join(answer_key_folder, answer_key_filename)

df = pd.read_csv(answer_key_path)
answer_key_counts = df["Invoice Name"].value_counts().astype(int).to_dict()
answer_key_counts_df = convert_to_df(answer_key_counts, ANSWER_KEY_COL)

# merge counts
comparison_df = data_counts_df.merge(
    answer_key_counts_df, on=FILENAME_COL, how="outer"
).sort_values("Filename")

# compare counts
diff_mask = comparison_df[ANSWER_KEY_COL] != comparison_df[DATA_COL]
diffs_df = comparison_df[diff_mask]

diffs_df.to_csv("answer_key_diffs.csv")
