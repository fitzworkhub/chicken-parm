from indico import IndicoConfig, IndicoClient
import os


# edit this with the path to your api token
API_TOKEN_PATH = '/home/fitz/Documents/POC/chicken-parm/indico_api_token.txt'
INDICO_PROD_URL = 'app.indico.io'

indico_prod_config = IndicoConfig(
        host=INDICO_PROD_URL,
        api_token_path=API_TOKEN_PATH,
)

PROD_CLIENT = IndicoClient(config=indico_prod_config)

detailed_pdf_extraction_config = {
    "preset_config": 'detailed'
}

# DataFolders
DATA_DIR = "/home/fitz/Documents/POC/chicken-parm/data"
SNAPSHOT_DIR = os.path.join(DATA_DIR, "snapshots")
DEMO_FILE_DIR = os.path.join(DATA_DIR, "demo_files")
