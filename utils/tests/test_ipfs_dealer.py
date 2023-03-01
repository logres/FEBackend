import os

def test_upload_file(ipfs_dealer):
    file_path = "./files/test.txt"
    with open(file_path, "w") as f:
        f.write("Hello World!")
    file_hash = ipfs_dealer.upload_file(file_path)
    os.remove(file_path)
    assert ipfs_dealer.download_file(file_hash, "./files/test.txt")
    
    with open("./files/test.txt", "r") as f:
        content = f.read()
    assert content == "Hello World!"

def test_pin_file(ipfs_dealer):
    file_path = "./files/test.txt"
    with open(file_path, "w") as f:
        f.write("Hello World!")
    file_hash = ipfs_dealer.upload_file(file_path)
    os.remove(file_path)
    assert ipfs_dealer.pin_file(file_hash)