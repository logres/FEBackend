import requests
import json
from my_settings import ipfs_setting


# 单例模式返回IPFSDealer
def get_ipfs_dealer():
    if not hasattr(get_ipfs_dealer, "instance"):
        get_ipfs_dealer.instance = IPFSDealer(ipfs_setting['api_endpoint'])
    return get_ipfs_dealer.instance

class IPFSDealer:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint

    # Upload a file to IPFS network， return the hash of the file
    def upload_file(self, file_path: str) -> str:
        try:
            url = self.api_endpoint + "/api/v0/add"
            with open(file_path, 'rb') as f:
                response = requests.post(url, files={'file': f})
            return json.loads(response.text)["Hash"]
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None

    # Download a file from IPFS network, return True if success
    def download_file(self, file_hash, file_name) -> bool:
        try:
            url = self.api_endpoint + "/api/v0/cat"
            response = requests.post(url, params={'arg': file_hash})
            with open(file_name, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            print(f"Error downloading file: {e}")
            return False

    # Pin a file to IPFS network, return True if success
    def pin_file(self, file_hash):
        try:
            url = self.api_endpoint + "/api/v0/pin/add"
            response = requests.post(url, params={'arg': file_hash})
            return True
        except Exception as e:
            print(f"Error pinning file: {e}")
            return False
    
    # Unpin a file from IPFS network, return True if success
    def unpin_file(self, file_hash):
        try:
            url = self.api_endpoint + "/api/v0/pin/rm"
            response = requests.post(url, params={'arg': file_hash})
            return True
        except Exception as e:
            print(f"Error unpinning file: {e}")
            return False