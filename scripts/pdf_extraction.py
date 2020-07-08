"""
Generate pdf extractions
"""
import os
import json
import click
import click_pathlib
from tqdm import tqdm

from config import PROD_CLIENT, detailed_pdf_extraction_config

from indico.queries.documents import DocumentExtraction
from indico.queries import JobStatus, RetrieveStorageObject

from poctoolkit.folder_utils import files_from_directory


@click.group()
def main():
    pass


def save_extraction(extraction, src_doc, dst_folder):
    """
    Save json extraction to dst_folder with the name of the src_doc file

    Arguments:
        config {dict} -- pdf extraction dictionary
        src_doc {str} -- path to Brochure pdf file
        dst_folder {str} -- path to save json output

    Returns:
        str -- output file path

    """
    filename = os.path.basename(src_doc)
    filename_no_ext = os.path.splitext(filename)[0]
    output_filename = filename_no_ext + ".json"
    output_filepath = os.path.join(dst_folder, output_filename)

    with open(output_filepath, "w") as f:
        json.dump(extraction, f)

    return output_filepath


def pdf_extraction_call(pdf_filepath, client, config):
    """
    Given a filepath, run Indico document extraction and save json output to
    dst_folder

    Arguments:
        pdf_filepath {str} -- path to Brochure pdf file
        client {IndicoClient} -- IndicoClient object containing auth details
        config {dict} -- Indico Document extraction options

    Returns:
        dict -- pdf extraction of pdf_filepath

    """

    jobs = client.call(
        DocumentExtraction(files=[pdf_filepath], json_config=json.dumps(config))
    )

    for i, j in enumerate(jobs):
        try:
            job = client.call(JobStatus(id=j.id, wait=True))
            doc_extract = client.call(RetrieveStorageObject(job.result))
        except Exception as e:
            print(e)
            print(job.result)
            return None
    return doc_extract


@main.command("extract")
@click.argument("src_dir", type=click_pathlib.Path(exists=True))
@click.argument("dst_folder")
def pdf_extraction_driver(src_dir, dst_folder):
    """
    Given a filepath, run Indico document extraction and save json output to
    dst_folder witht the same name as the src_doc

    Arguments:
        src {str} -- path to Brochure pdf file or files
        dst_folder {str} -- path to folder to save json output

    Returns:
        str -- output file path

    """
    # if src is directory, iterate through all pdf files
    if os.path.isdir(src_dir):
        pdf_paths = files_from_directory(src_dir)
        for pdf_path in tqdm(pdf_paths):
            pdf_extraction = pdf_extraction_call(
                pdf_path, PROD_CLIENT, detailed_pdf_extraction_config
            )
            if pdf_extraction:
                _ = save_extraction(pdf_extraction, pdf_path, dst_folder)
            else:
                continue
    # otherwise pass single file
    else:
        pdf_extraction = pdf_extraction_call(
            src_dir, PROD_CLIENT, detailed_pdf_extraction_config
        )
        _ = save_extraction(pdf_extraction, pdf_path, dst_folder)


@main.command("extraction_to_text")
@click.argument("src_dir", type=click_pathlib.Path(exists=True))
@click.argument("dst_folder")
def extraction_to_text(src_dir, dst_folder):
    """
    Write single page pdf extraction text to txt file
    """
    pdf_extraction_paths = files_from_directory(src_dir)
    for pdf_extraction_path in pdf_extraction_paths:
        with open(pdf_extraction_path) as f:
            pdf_extraction = json.load(f)

        filename = os.path.basename(pdf_extraction_path)
        filename_not_ext = os.path.splitext(filename)[0]
        output_filepath = os.path.join(dst_folder, filename_not_ext + ".txt")
        text = pdf_extraction["pages"][0]["text"]

        with open(output_filepath, "w") as f:
            f.write(text)


if __name__ == "__main__":
    main()
