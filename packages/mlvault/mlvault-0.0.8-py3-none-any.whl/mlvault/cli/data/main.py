import json
import os
from huggingface_hub import snapshot_download
from mlvault.cli.data.extract import run_extract
from mlvault.datapack.main import export_data_from_dataset
from .down import download_dataset
from .pack import run_pack
from mlvault.datapack import DataPack, DataPackLoader
from mlvault.config import get_r_token, get_w_token

def upload_dataset(args:list[str]):
    try:
        i_file_path, = args
        file_path = i_file_path if i_file_path.startswith("/") else os.path.join(os.getcwd(), i_file_path)
        if not file_path.endswith(".yml"):
            print("File must be a .yml file")
            exit(1)
        if not os.path.exists(file_path):
            print("File does not exist")
            exit(1)
        else:
            DataPack.from_yml(file_path).push_to_hub(get_w_token())
    except ValueError:
        print("Please provide a file name")
        exit(1)


def snapshot(repo_id:str):
    snapshot_download(repo_id, token=get_r_token(), local_dir=os.getcwd())

def main(input_args:list[str]):
    action, *args = input_args
    if action == "up":
        upload_dataset(args)
    elif action == "down":
        download_dataset(args)
    elif action == "snapshot":
        snapshot(args[0])
    elif action == "pack":
        run_pack(args)
    elif action == "extract":
        run_extract(args)
