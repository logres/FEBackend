from ninja import Router, Schema
from .models import Web3User
from utils.my_cryptography import PublicKey, Address, message_hash
router = Router()

# Create your views here.

class GetUserNonceResponse(Schema):
    nonce: int

@router.get("/nonce/{str:address}")
def get_user(request, address):
    # get user by address from database
    web3user = Web3User.objects.get(address=address)
    nonce = web3user.nonce
    return GetUserNonceResponse(nonce=nonce)

class RegisterUserRequest(Schema):
    username: str
    address: str

@router.post("/register/")
def register_user(request, user: RegisterUserRequest):
    # save user to database
    web3user = Web3User(username=user.username, address=user.address, nonce=0, avatar="https://avatars.githubusercontent.com/u/10000000?v=4")
    web3user.save()
    return {"message": "success"}

class LoginUserRequest(Schema):
    address: str
    public_key: str
    signature: str

class LoginUserResponse(Schema):
    username : str
    address: str
    avatar : str

@router.post("/login/")
def login_user(request, user: LoginUserRequest):
    web3user = Web3User.objects.get(address=address)
    nonce = web3user.nonce
    signature = user.signature
    address = user.address
    public_key = user.public_key
    # Verify address and PublicKey
    address = Address(address)
    public_key = PublicKey(public_key)
    if not address.check_public_address(public_key):
        return {"message": "address and public key not match"}
    # Verify signature and PublicKey
    message = address.address + str(nonce)
    hash_of_message = message_hash(message)
    if not public_key.verify(hash_of_message, signature):
        return {"message": "signature not match"}
    # update nonce and set session
    web3user.nonce += 1
    web3user.save()
    return LoginUserResponse(username=web3user.username, avatar=web3user.avatar, address = web3user.address)
