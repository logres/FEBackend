from .ipfs_dealer import get_ipfs_dealer
import json

def generate_metadata(attr_dict: dict):
    # 生成metadata
    meta_data_dict = "A"

    ipfs_dealer = get_ipfs_dealer()