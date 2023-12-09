import json
import os
from huggingface_hub import snapshot_download
from mlvault.datapack import DataPack, DataPackLoader
from mlvault.config import get_r_token, get_w_token
import re
from mlvault.datapack.main import DataTray

from mlvault.util import is_image
from PIL import Image

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

def download_dataset(args:list[str]):
    repo_id = args[0]
    DataPackLoader.load_datapack_from_hf(repo_id, get_r_token(), os.getcwd()).export_files(".",get_r_token())

def snapshot(repo_id:str):
    snapshot_download(repo_id, token=get_r_token(), local_dir=os.getcwd())

def pack(base_dir:str, token_filter:list[str], repo_name:str):
    cucrrent = os.getcwd()
    image_info_dict = {}
    class_dir_images_dict = {}
    base_dir = base_dir if base_dir.startswith("/") else os.path.join(cucrrent, base_dir)
    images = filter(lambda name: is_image(name),  os.listdir(os.path.join(base_dir)))
    for image_name in images:
        image_info_dict[image_name] = {}
        name, _ = os.path.splitext(image_name)
        caption_file_name = name + ".txt"
        caption_file_path = os.path.join(base_dir, caption_file_name)
        image_info_dict[image_name]["path"] = os.path.join(base_dir, image_name)
        image_info_dict[image_name]["captions"] = []
        is_file_exist = os.path.exists(caption_file_path)
        if is_file_exist:
            with open(caption_file_path, "r") as f:
                image_info_dict[image_name]["captions"] = list(map(lambda token: token.strip() ,f.readline().replace("_", " ").replace('1girl', 'girl').replace('1boy', 'boy').split(", ")))

    current_list = os.listdir(cucrrent)
    class_dirs = filter(lambda name: re.match('\[.*\].*',name) , current_list )
    for class_dir in class_dirs:
        class_name = re.sub('\[.*\]', '', class_dir).replace("_", " ").strip()
        class_dir_images_dict[class_name] = []
        class_images = list(filter(lambda name: is_image(name), os.listdir(os.path.join(cucrrent, class_dir))))
        class_dir_images_dict[class_name] = class_images
        for image_name in class_images:
            if image_name not in image_info_dict:
                print("Image {} not found in base directory".format(image_name))
            else :
                image_record = image_info_dict[image_name]
                def remove_and_reinsert():
                    image_record['captions'].remove(class_name)
                if class_name in image_record['captions']:
                    remove_and_reinsert()
                image_record['captions'].insert(0, class_name)
    data_tray = DataTray()
    for image_name in image_info_dict:
        image_record = image_info_dict[image_name]
        image = Image.open(image_record['path'])
        filter_len = len(token_filter)
        if filter_len:
            filter_matched = 0
            for toekn_filter in token_filter:
                if toekn_filter in image_record['captions']:
                    filter_matched += 1
            if filter_matched != filter_len:
                continue
        captions = ", ".join(image_record['captions'])
        data_tray.add("generated/generated", image_name, image, captions, ".txt")
    dataset = data_tray.to_dataset()
    data_tray.push_to_hub(repo_name, get_w_token())
    print(f"going upload {len(dataset)} images to {repo_name}")
    print("make config file with these option")
    print("datasets:")
    print("  generated:")
    print("    subsets:")
    print("      generated:")
    print("        caption_extension: .txt")

def find_args(args:list[str], arg:str):
    try:
        index = args.index(arg)
        return args[index + 1]
    except ValueError:
        return None

def print_help():
    print("Usage: mlvcli pack <options>")
    print("Options:")
    print("  --d <base directory>")
    print("  --f <class filter> : quotes are required, comma separated")
    print("  --r <repo name>")


def main(input_args:list[str]):
    action, *args = input_args
    if action == "up":
        upload_dataset(args)
    elif action == "down":
        download_dataset(args)
    elif action == "snapshot":
        snapshot(args[0])
    elif action == "pack":
        base_dir = find_args(args, "--d")
        tokens_raw = find_args(args, "--f")
        repo_name = find_args(args, "--r")
        token_filter = list(map(lambda token: token.strip(), tokens_raw.split(","))) if tokens_raw else []
        
        if not repo_name:
            print("Please provide a repo name")
            print_help()
            exit(1)
        elif not base_dir:
            print("Please provide a base directory")
            print_help()
            exit(1)
        elif not os.path.exists(base_dir):
            print("Base directory does not exist")
            print_help()
            exit(1)
        else:
            pack(base_dir, token_filter, repo_name)
    elif action == "extract":
        json_path = args[0]
        file = open(json_path, "r")
        json_content :dict = json.load(file)
        dp = DataPackLoader.load_dynamic_datapack(json_content, os.getcwd())
        dp.export_files(os.getcwd(), get_r_token())
