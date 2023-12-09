import os
from os.path import join as join_path
from os.path import isfile
from datasets import Dataset
from PIL import Image
import numpy as np
from huggingface_hub import upload_file
import toml
import yaml
from datasets.load import load_dataset
from huggingface_hub.file_download import hf_hub_download
from tqdm import tqdm
from datasets.dataset_dict import IterableDatasetDict
from typing import Any
from mlvault.api import download_file_from_hf
from mlvault.config import get_r_token

def to_optional_dict(d:Any, keys:list[str]):
    output = {}
    for key in keys:
        val = d.__dict__[key] if hasattr(d, key) else None
        if(val):
            output[key] = val
    return output

def get_ext(file_name: str):
    return os.path.splitext(file_name)[1].lower()

def list_dir_in_ext(path: str, ext: str):
    files = os.listdir(path)
    filtered = filter(lambda file: file.endswith(ext), files)
    return list(filtered)

imgs = ['.png', '.jpg', '.jpeg', '.bmp', '.webp']

def list_dir_in_img(path:str):
    files = os.listdir(path)
    filtered = filter(lambda file: get_ext(file) in imgs, files)
    return list(filtered)   

def check_has_filters(captions:str, filters:list[str], exclude_filters:list[str]=[]):
    caption_list = list(map(lambda token: token.strip(), captions.split(",")))
    filter_cnt = 0
    for e_filter in exclude_filters:
        if e_filter in caption_list:
            return False
    for filter in filters:
        if filter in caption_list:
            filter_cnt += 1
    if filter_cnt == len(filters):
        return True
    else:
        return False

def export_data_from_dataset(dataset:IterableDatasetDict, target_dir:str, filters:list[str]=[], exclude_filters:list[str]=[]):
    filtered = dataset.filter(lambda data: check_has_filters(data['caption'], filters, exclude_filters))
    data_len = len(filtered)
    print(f"exporting {data_len} files")
    for i in tqdm(range(data_len)):
        data = filtered[i]
        os.makedirs(target_dir, exist_ok=True)
        file_name = data['file_name']
        base_name = os.path.splitext(file_name)[0]
        extension = data['caption_extension']
        caption = data['caption']
        image = data['image']
        to_save_img_path = f"{target_dir}/{file_name}"
        to_save_caption_path = f"{target_dir}/{base_name}{extension}"
        caption = (data['caption'] or "").strip()
        if caption:
            open(to_save_caption_path, 'w').write(caption)
        nparr = np.array(image)
        Image.fromarray(nparr).save(to_save_img_path)
    print("datasets exported!")

class DataTray:
    imgs: list = []
    caption: list[str] = []
    div: list[str] = []
    file_name: list[str] = []
    caption_extension:list[str] = []

    def add(self, div: str, img_file_name: str, image: Image.Image, caption: str, caption_extension:str):
        self.div.append(div)
        self.file_name.append(img_file_name)
        self.imgs.append(image)
        self.caption.append(caption)
        self.caption_extension.append(caption_extension)

    def to_dataset(self):
        ds = Dataset.from_dict(
            {
                "div": self.div,
                "image": self.imgs,
                "caption": self.caption,
                "file_name": self.file_name,
                "caption_extension": self.caption_extension
            }
        )
        return ds
    
    def push_to_hub(self, repo_id:str, w_token:str):
        self.to_dataset().push_to_hub(repo_id, token=w_token, private=True)

class SubsetConfig:

    def __init__(self, name:str, config_input:dict) -> None:
        self.name = name
        if "path" in config_input:
            self.path = config_input["path"]
        if "class_tokens" in config_input:
            self.class_tokens = config_input["class_tokens"]
        if "is_reg" in config_input:
            self.is_reg = config_input["is_reg"]
        if "caption_extension" in config_input:
            self.caption_extension = config_input["caption_extension"]
        if "keep_tokens" in config_input:
            self.keep_tokens = config_input["keep_tokens"]
        if "num_repeats" in config_input:
            self.num_repeats = config_input["num_repeats"]
        if "shuffle_caption" in config_input:
            self.shuffle_caption = config_input["shuffle_caption"]
        pass
    
    def to_toml_dict(self, dataset_dir:str):
        toml_dict = to_optional_dict(self, ["caption_extension", "keep_tokens", "num_repeats", "shuffle_caption", "class_tokens", "is_reg"])
        toml_dict["image_dir"] = join_path(dataset_dir, self.name)
        return toml_dict


class DatasetConfig:
    subsets: dict[str, SubsetConfig] = {}

    def __init__(self, name:str, config_input:dict) -> None:
        self.name = name
        if "resolution" in config_input:
            self.resolution = config_input["resolution"]
        if "caption_extension" in config_input:
            self.caption_extension = config_input["caption_extension"]
        if "keep_tokens" in config_input:
            self.keep_tokens = config_input["keep_tokens"]
        if "num_repeats" in config_input:
            self.num_repeats = config_input["num_repeats"]
        if "shuffle_caption" in config_input:
            self.shuffle_caption = config_input["shuffle_caption"]
        if "class_tokens" in config_input:
            self.class_tokens = config_input["class_tokens"]
        for dataset_key in config_input['subsets']:
            config = { **config_input, **config_input['subsets'][dataset_key]}
            self.subsets[dataset_key] = SubsetConfig(dataset_key, config)
        pass

    def to_dict(self):
        dict_subsets = {}
        for subset_key in self.subsets:
            dict_subsets[subset_key] = self.subsets[subset_key].__dict__
        return {
            "caption_extension": self.caption_extension,
            "name": self.name,
            "subsets": dict_subsets
        }
    def to_toml_dict(self, dataset_dir:str):
        toml_dict = to_optional_dict(self, ["resolution"])
        toml_dict["subsets"] = []
        for subset_key in self.subsets:
            toml_dict["subsets"].append(self.subsets[subset_key].to_toml_dict(join_path(dataset_dir, self.name)))
        return toml_dict


class InputConfig:
    datasets: dict[str, DatasetConfig] = {}

    def __init__(self, config_input:dict) -> None:
        self.repo_id = config_input["repo_id"]
        if "resolution" in config_input:
            self.resolution = config_input["resolution"]
        if "caption_extension" in config_input:
            self.caption_extension = config_input["caption_extension"]
        if "keep_tokens" in config_input:
            self.keep_tokens = config_input["keep_tokens"]
        if "num_repeats" in config_input:
            self.num_repeats = config_input["num_repeats"]
        if "shuffle_caption" in config_input:
            self.shuffle_caption = config_input["shuffle_caption"]
        for dataset_key in config_input['datasets']:
            config = { **config_input, **config_input['datasets'][dataset_key]}
            self.datasets[dataset_key] = DatasetConfig(dataset_key, config)
        pass

    def to_dict(self):
        dict_datasets = {}
        for dataset_key in self.datasets:
            dict_datasets[dataset_key] = self.datasets[dataset_key].to_dict()
        return {
            "repo_id": self.repo_id,
            "datasets": dict_datasets
        }
    
    def to_toml_dict(self, datasets_dir:str):
        toml_dict = {"general":{"enable_bucket":True}, "datasets":[]}
        for dataset_key in self.datasets:
            toml_dict["datasets"].append(self.datasets[dataset_key].to_toml_dict(datasets_dir))
        return toml_dict


class OutputConfig:

    def __init__(self, config_input:dict) -> None:
        self.model_name = config_input["model_name"]
        self.save_every_n_epochs = config_input["save_every_n_epochs"]
        self.save_model_as = config_input["save_model_as"]
        pass 

class TrainConfig:
    def __init__(self, config_input:dict) -> None:
        self.learning_rate = config_input["learning_rate"]
        self.train_batch_size = config_input["train_batch_size"]
        self.network_dim = config_input["network_dim"]
        self.network_alpha = config_input["network_alpha"]
        self.max_train_epochs = config_input["max_train_epochs"]
        self.base_model = config_input["base_model"]
        self.optimizer = config_input["optimizer"]
        self.continue_from = config_input.get("continue_from", None)
        pass

class SampleConfig:
    def __init__(self, config_input) -> None:
        self.sample_every_n_epochs = config_input["sample_every_n_epochs"]
        self.prompts = config_input["prompts"]
        self.sampler = config_input["sampler"]
        pass

class DataPack:
    @staticmethod
    def from_yml(config_file_path:str):
        config =  yaml.load(open(config_file_path, 'r'), Loader=yaml.FullLoader)
        os.path.dirname(config_file_path)
        return DataPack(config, os.path.dirname(config_file_path))

    def __init__(self, config:dict, work_dir:str):
        self.work_dir = work_dir
        self.input = InputConfig(config["input"])
        self.output = OutputConfig(config["output"])
        self.train = TrainConfig(config["train"])
        self.sample = SampleConfig(config["sample"])
    
    def to_dict(self):
        return {
            "input": self.input.to_dict()
        }
    
    def to_data_tray(self):
        data_tray = DataTray()
        for dataset_key in self.input.datasets:
            for subset_key in self.input.datasets[dataset_key].subsets:
                subset = self.input.datasets[dataset_key].subsets[subset_key]
                extension = subset.caption_extension
                src_dir = subset.path
                img_names = list_dir_in_img(src_dir)
                caption = []
                for img_name in img_names:
                    name, _ = os.path.splitext(img_name)
                    tag_name = f"{name}{extension}"
                    caption = ""
                    img_path = f"{src_dir}/{img_name}"
                    img = Image.open(img_path)
                    if tag_name and  isfile(f"{src_dir}/{tag_name}"):
                        caption = open(f"{src_dir}/{tag_name}", "r").read()
                    data_tray.add(
                        div=f"{dataset_key}/{subset_key}", image=img, caption=caption, img_file_name=img_name, caption_extension=extension
                    )
        return data_tray
    
    def push_to_hub(self, w_token:str):
        self.to_data_tray().push_to_hub(self.input.repo_id, w_token)
        upload_file(
            repo_id=self.input.repo_id,
            path_or_fileobj=self.work_dir,
            path_in_repo="config.yml",
            token=w_token,
            repo_type="dataset",
        )
    
    def export_files(self, base_dir:str, r_token:str):
        print("start exporting files!")
        hf_hub_download(repo_id=self.input.repo_id, filename="config.yml", repo_type="dataset", local_dir=base_dir, token=r_token)
        dataset_dir = f"{base_dir}/datasets"
        self.export_datasets(dataset_dir, r_token)
        self.write_sample_prompt(base_dir)
        self.write_toml(base_dir)
        self.export_base_models(base_dir)
    
    def export_base_models(self, base_dir:str):
        if self.train.continue_from:
            user_name, repo_name, model_name = self.train.continue_from.split(":")
            repo_id = f"{user_name}/{repo_name}"
            download_file_from_hf(repo_id=repo_id, file_name=model_name, local_dir=join_path(base_dir, "continue_from"), r_token=get_r_token())
            print("base model downloaded!")
        pass

    def write_sample_prompt(self, base_dir:str):
        sample_prompt:list[str] = self.sample.prompts
        sample_prompt_path = f"{base_dir}/sample.txt"
        open(sample_prompt_path, "w").write("\n".join(sample_prompt))
        print("sample prompt written!")

    def write_toml(self, base_dir:str):
        toml_dict = self.input.to_toml_dict(join_path(base_dir, "datasets"))
        toml_path = f"{base_dir}/config.toml"
        toml.dump(toml_dict, open(toml_path, "w"))
        self.toml_path = toml_path
        print("toml written!")
    
    def export_datasets(self, dataset_dir:str, r_token:str):
        repo_id = self.input.repo_id
        dataset: IterableDatasetDict = load_dataset(repo_id, split="train", token=r_token) # type: ignore
        num_rows:int = len(dataset)
        for i in tqdm(range(num_rows)):
            data = dataset[i]
            div = data['div']
            subset_dir = f"{dataset_dir}/{div}"
            os.makedirs(subset_dir, exist_ok=True)
            file_name = data['file_name']
            base_name = os.path.splitext(file_name)[0]
            extension = data['caption_extension']
            caption = data['caption']
            image = data['image']
            to_save_img_path = f"{subset_dir}/{file_name}"
            to_save_caption_path = f"{subset_dir}/{base_name}{extension}"
            caption = (data['caption'] or "").strip()
            if caption:
                open(to_save_caption_path, 'w').write(caption)
            nparr = np.array(image)
            Image.fromarray(nparr).save(to_save_img_path)
        print("datasets exported!")

class DynamicDataPack(DataPack):
    def __init__(self, config_input:dict, work_dir:str) -> None:
        config_input["input"] = {**config_input['extends'], **{"datasets":{"dynamic":{"subsets":{"dynamic":{"caption_extension": ".txt"}}}}}}
        super().__init__(config_input, work_dir)
        self.extends = config_input["extends"]
        self.filters = list(filter(lambda v: v, list(map(lambda token: token.strip(), config_input['extends'].get("filters", "").split(",")))) )
        print(self.filters)
        pass

    def export_files(self, base_dir:str, r_token:str):
        print("start exporting files!")
        dataset_dir = f"{base_dir}/datasets"
        self.export_datasets(f"{dataset_dir}/dynamic/dynamic", r_token)
        self.write_sample_prompt(base_dir)
        self.write_toml(base_dir)
        self.export_base_models(base_dir)

    def check_has_filters(self, captions:str):
        caption_list = list(map(lambda token: token.strip(), captions.split(",")))
        filter_cnt = 0
        print(filter_cnt)
        print(len(self.filters))
        for filter in self.filters:
            if filter in caption_list:
                filter_cnt += 1
        if filter_cnt == len(self.filters):
            return True
        else:
            return False

    def export_datasets(self, target_dir:str, r_token:str,):
        repo_id = self.input.repo_id
        dataset: IterableDatasetDict = load_dataset(repo_id, split="train", token=r_token) # type: ignore
        export_data_from_dataset(dataset, target_dir, self.filters)

class DataPackLoader:
    @staticmethod
    def load_datapack_from_hf(repo_id:str, r_token:str, base_dir:str) -> DataPack:
        hf_hub_download(repo_id=repo_id, filename="config.yml", repo_type="dataset", local_dir=base_dir, token=r_token)
        config_file_path = f"{base_dir}/config.yml"
        return DataPack.from_yml(config_file_path)

    @staticmethod
    def load_dynamic_datapack(config: dict, base_dir:str):
        return DynamicDataPack(config, base_dir)
        
class DataExporter(DynamicDataPack):
    def __init__(self, repo_id:str) -> None:
        pass
