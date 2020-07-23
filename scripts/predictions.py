import os
import json
from tqdm import tqdm
import config as indico_config

from poctoolkit.predictions import predict
from poctoolkit.folder_utils import files_from_directory, check_folder

# all valid values model
SELECTED_MODEL_ID = 31093
MODEL_FOLDER = "total_tax_model"


def extraction_driver(pdf_text_dir, demo_dir, batch_size=10):

    batch_size = 10

    prediction_dir = "predictions"
    prediction_path = os.path.join(demo_dir, prediction_dir)
    check_folder(prediction_path)
    
    samples = []
    prediction_dicts = []
    # get all pdf_extraction_files
    pdf_text_paths = files_from_directory(pdf_text_dir)

    for pdf_text_path in pdf_text_paths:
        with open(pdf_text_path) as f:
            text = f.read()
        samples.append(text)

    for batch_start in tqdm(range(0, len(samples), batch_size)):
        batch_end = batch_start + batch_size
        batch_samples = samples[batch_start:batch_end]
        prediction_dicts.extend(predict(batch_samples, SELECTED_MODEL_ID))

    for prediction, filepath in zip(prediction_dicts, pdf_text_paths):
        filename = os.path.basename(filepath)
        filename_json = os.path.splitext(filename)[0] + ".json"
        output_path = os.path.join(prediction_path, filename_json)
        with open(output_path, "w") as f:
            json.dump(prediction, f)


if __name__ == "__main__":

    demo_dir = os.path.join(
        indico_config.DATA_DIR, indico_config.DEMO_FILE_DIR, MODEL_FOLDER
    )

    pdf_text_dir = os.path.join(demo_dir, "text_files")

    extraction_driver(pdf_text_dir, demo_dir)
