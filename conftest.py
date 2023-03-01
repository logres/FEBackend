import pytest
from utils.ipfs_dealer import IPFSDealer

@pytest.fixture(scope="session")
def ipfs_dealer():
    return IPFSDealer(api_endpoint="http://localhost:5001")