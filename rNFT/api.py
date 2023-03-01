import shutil
from ninja import Router
from ninja.files import UploadedFile
from ninja import File
from utils.ipfs_dealer import get_ipfs_dealer

router = Router()

# A API receive file and push it to IPFS
@router.post("/upload")
def upload_file(file: UploadedFile = File(...)):
    # Save file to local
    with open(file.name, "wb") as f:
        shutil.copyfileobj(file.file, f)
    # Upload file to IPFS
    ipfs_dealer = get_ipfs_dealer()
    ipfs_hash = ipfs_dealer.upload_file(file.name)
    return {"ipfs_hash": ipfs_hash}

