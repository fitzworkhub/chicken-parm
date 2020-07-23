"""
Save predictions to csv with form:
Filename |  Label  | Value | Confidence
---------+---------+-------+------------

"""

import config as poc_config
import os
import pandas as pd

from poctoolkit.predictions import predictions_to_csv
from poctoolkit.folder_utils import files_from_directory, check_folder


model_name = "total_tax_model"

demo_dir = os.path.join(poc_config.DEMO_FILE_DIR, model_name)
prediction_dir = os.path.join(demo_dir, "predictions")
prediction_files = files_from_directory(prediction_dir)

csv_dir = os.path.join(demo_dir, "output_csv_files")
check_folder(csv_dir)

csv_filepath = os.path.join(csv_dir, "predictions.csv")
predictions_to_csv(prediction_files, csv_filepath)

# clean up prediction csv (just sort at the moment)
csv = pd.read_csv(csv_filepath)
csv.sort_values(["Filename", "Label", "Confidence"], ascending=False, inplace=True)
csv.to_csv(csv_filepath, index=False)
print(pd.unique(csv.sample(10)['Filename']))
