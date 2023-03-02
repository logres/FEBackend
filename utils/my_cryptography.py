import ecdsa
import hashlib
import sha3
# 设计思路

# 1. 私钥 256bit随机数  | base58 -> 压缩私钥
# 2. 公钥 私钥 -> ecdsa SECP256k1 -> 公钥
# 3. 地址 公钥 -> keccak256 -> 地址

# 字符串与bytes管理 注意，不使用0x前缀

def hash160(data: bytes) -> bytes:
    # 先计算SHA256 再计算RIPEMD160
    return hashlib.new('ripemd160', hashlib.sha256(data).digest()).digest()

def hash256(data: bytes) -> bytes:
    # 计算两遍SHA256
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def message_hash(message: str) -> bytes:
    # 计算keccak256
    return sha3.keccak_256(message.encode('utf-8')).digest()

class PublicKey:

    def __init__(self, public_key: str) -> None:
        # public_key b'04'+64字节
        self._public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1) # 特殊对象

    @property
    def public_key(self) -> str:
        return '04' + self._public_key.to_string().hex()
    
    @property
    def no_prefix_public_key(self) -> str:
        return self._public_key.to_string().hex()
    
    @property
    def x(self) -> str:
        return self._public_key.pubkey.point.x().to_bytes(32, 'big').hex()
    
    @property
    def y(self) -> str:
        return self._public_key.pubkey.point.y().to_bytes(32, 'big').hex()
    
    @property
    def compressed_public_key(self) -> str:
        return '02' + self.x if int(self.y, 16) % 2 == 0 else '03' + self.x

    @property
    def public_key_hash(self) -> str:
        # keccak256 哈希
        return sha3.keccak_256(bytes.fromhex(self.no_prefix_public_key)).hexdigest()

    def verify(self, message: bytes, signature: bytes) -> bool:
        return self._public_key.verify(signature, message)

    def to_address(self) -> "Address":
        # 生成地址 取右20字节
        return Address(self.public_key_hash[-40:])

class Address:

    def __init__(self, address: str) -> None:
        # address 1+20+4
        self._address :str = address

    @property
    def address(self) -> str:
        return self._address
    
    def check_public_address(self, public_key: PublicKey) -> bool:
        # 检查地址是否正确
        return self.address == public_key.to_address().address


class PrivateKey:

    def __init__(self, private_key: str) -> None:
        # private_key 256位
        self._private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)

    @property
    def private_key(self) -> str:
        return self._private_key.to_string().hex()
    
    def sign(self, message: bytes) -> bytes:
        return self._private_key.sign(message)
    
    def public_key(self) -> PublicKey:
        # 生成公钥
        public_key = self._private_key.get_verifying_key()
        return PublicKey(public_key.to_string().hex())


def generate_key_pair() -> tuple[PrivateKey, PublicKey]:
    # 生成公钥和私钥
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    return PrivateKey(private_key.to_string().hex()), PublicKey(public_key.to_string().hex())


pk = '07129eb5e54477817c4db5a98523d0a19562a9c405b68c0e1854de416e7fbff1'
private_key = PrivateKey(pk)

address = private_key.public_key().to_address()

print(address.address)