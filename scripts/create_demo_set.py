"""
This script gets a list of files that are a part of the 20% test set and
unlabeled values from a given teach task(dataset?)

Filename -> Row index mapping from cyclone export
test/training inds from cyclone export

return filenames where row index belongs to [test_inds, unlabeled_inds]
where unlabeled_inds = row_inds - test_inds - training_inds
"""
from indico.queries.export import CreateExport, DownloadExport
from indico.queries import JobStatus, RetrieveStorageObject

import config as indico_config
import pandas as pd
import os
import ast
import shutil


def get_indices(csv_filepath):
    csv = pd.read_csv(csv_filepath)
    inds = ast.literal_eval(csv['row_indices'][0])
    return inds


DATASET_ID = 6911
LABELSET_ID = 18140

"""
CreateExport is borken as of 07/13/2020, would have been WAY easier lol

export_obj = PROD_CLIENT.call(
    CreateExport(dataset_id=DATASET_ID, labelset_ids=[LABELSET_ID],  file_info=True)
     )

export_df = PROD_CLIENT.call(
    DownloadExport(export=export_obj)
     )

export_df.to_csv(output_path, index=False)
"""


testing_filename = "testing_inds.csv"
training_filename = "training_inds.csv"
mapping_filename = "row_index_filename_map.csv"

# filename _-> row index mapping
# beware!!!!! all these index files are coming directly from db with no data
# checks
mapping_filepath = os.path.join(indico_config.SNAPSHOT_DIR, mapping_filename)
filename_index_map = pd.read_csv(mapping_filepath)
row_inds = set(filename_index_map['index'])

# Row indices of test and train set
training_filepath = os.path.join(indico_config.SNAPSHOT_DIR, training_filename)
testing_filepath = os.path.join(indico_config.SNAPSHOT_DIR, testing_filename)

test_inds = get_indices(testing_filepath)
train_inds = get_indices(training_filepath)

# calculate unlabeled_inds
demo_inds = row_inds.difference(train_inds)
print(demo_inds)


demo_filenames = filename_index_map.set_index('index').loc[demo_inds, 'name']
print(demo_filenames)

# move files to demo_folder
pdf_dir = os.path.join("split_pages_max_page_3")
text_dir = os.path.join("text_files")
pdf_extraction_dir = os.path.join("pdf_extractions")

input_data_dirs = [pdf_dir, text_dir, pdf_extraction_dir]
extensions = ['.pdf', '.txt', '.json']
save_dir = os.path.join(indico_config.DEMO_FILE_DIR, "all_valid_model")
for input_data_dir, extension in zip(input_data_dirs, extensions):
    for filename in demo_filenames:
        filename_ext = os.path.splitext(filename)[0] + extension

        input_folder = os.path.join(indico_config.DATA_DIR, input_data_dir)    
        input_filename = os.path.join(input_folder, filename_ext)

        output_folder = os.path.join(save_dir, input_data_dir)
        output_filepath = os.path.join(output_folder, filename_ext)

        shutil.copy(input_filename, output_filepath)
