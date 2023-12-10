import json
import os
from mlvault.datapack.main import DataPack, DataPackLoader
with open("config.json", "r") as f:
    registry = json.load(f)
    pack = DataPack(registry,os.getcwd())
    pack.export_files()
