from datasets import load_dataset, DatasetDict, IterableDatasetDict, Dataset

from mlvault.config import get_r_token
def is_image(filename:str):
    img_extensions = ["jpg", "jpeg", "png", "webp"]
    extension = filename.split(".")[-1]
    return extension in img_extensions

def find_args(args:list[str], arg:str):
    try:
        index = args.index(arg)
        return args[index + 1]
    except ValueError:
        return None

def load_dataset_for_dpack(repo_id:str):
    ds = load_dataset(repo_id, split="train", token=get_r_token())
    if isinstance(ds, Dataset):
        return ds
    else :
        raise Exception("Invalid dataset")

