from django.shortcuts import render

# Create your views here.
import shutil
from ninja import Router, Schema
from ninja.files import UploadedFile
from ninja import File
from utils.ipfs_dealer import get_ipfs_dealer
import json

router = Router()

class CreateNFTRequest(Schema):
    name: str
    description: str
    attributes: str

@router.post("/create_nft/")
def create_nft(request, nft_detail: CreateNFTRequest ,file: UploadedFile = File(...)):
    ipfs_dealer = get_ipfs_dealer()
    # 将文件存储到media文件夹
    with open(f"media/{file.name}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    img_ipfs_hash = ipfs_dealer.upload_file(f"media/{file.name}")
    nft_metadata ={
        "name": nft_detail.name,
        "description": nft_detail.description,
        "image": img_ipfs_hash,
    }
    nft_metadata_string = json.dumps(nft_metadata)
    # 存储metadata到media
    with open(f"media/{nft_detail.name}.json", "w") as buffer:
        buffer.write(nft_metadata_string)
    nft_metadata_ipfs_hash = ipfs_dealer.upload_file(f"media/{nft_detail.name}.json")
    # 清楚临时文件
    shutil.rmtree("media")
    return {"message": "success", "ipfs_hash": nft_metadata_ipfs_hash}
