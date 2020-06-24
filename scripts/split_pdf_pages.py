"""
In the customer provided dataset, each page of a multipage document contains a
single invoice sample. The app does not currently support pdf splitting during
labeling and needs to be done upload

This script performs the following steps:

1) Get a list of all pdf paths
2) split pdfs into single pages
"""
from poctoolkit import pdf_utils, folder_utils
import click
import click_pathlib


def split_pdfs(pdf_folder, output_folder):
    pdf_filepaths = folder_utils.files_from_directory(pdf_folder, "*.pdf")
    for pdf_filepath in pdf_filepaths:
        pdf_utils.split_pdf_pages(pdf_filepath, output_folder)


@click.command()
@click.argument("pdf_folder", type=click_pathlib.Path(exists=True))
@click.argument("output_folder")
def split_pdf_driver(pdf_folder, output_folder):
    split_pdfs(pdf_folder, output_folder)


if __name__ == "__main__":
    split_pdf_driver()
