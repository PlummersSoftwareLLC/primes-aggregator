import abc
import re
import typing
from abc import ABC
from typing import Optional, List

import bcrypt


class Hasher(ABC):
    @abc.abstractmethod
    def is_my_hashtype(self, hash: bytes) -> bool:
        ...

    @abc.abstractmethod
    def is_up_to_date(self, hash: bytes) -> bool:
        ...

    @abc.abstractmethod
    def hash(self, password: str) -> bytes:
        ...

    @abc.abstractmethod
    def verify(self, hash: bytes, password: str) -> bool:
        ...


class PlaintextHasher(Hasher):
    def __init__(self, prefix: bytes = b'{', encoding: str = "utf-8"):
        self.prefix = prefix
        self.encoding = encoding

    def is_my_hashtype(self, hash: bytes) -> bool:
        return hash.startswith(self.prefix)

    def is_up_to_date(self, hash: bytes) -> bool:
        return True

    def hash(self, password: str) -> bytes:
        return self.prefix + password.encode(self.encoding)

    def verify(self, hash: bytes, password: str) -> bool:
        return self.hash(password) == hash


class BcryptHasher(Hasher):
    bcrypt_re: typing.ClassVar[re.Pattern] = re.compile(br"^[$](?P<version>2[abxy]?)[$](?P<strength>(?P<cost>(0[4-9]|[12][0-9]|3[01])))[$](?P<password>((?P<salt>[./0-9a-zA-Z]{22})(?P<hash>[./0-9a-zA-Z]{31})))$")

    def __init__(self, cost: int = 12):
        self.cost = cost

    def is_my_hashtype(self, hash: bytes) -> bool:
        match = BcryptHasher.bcrypt_re.match(hash)
        return True if match else False

    def is_up_to_date(self, hash: bytes) -> bool:
        match = BcryptHasher.bcrypt_re.match(hash)

        return match.group('cost') == str(self.cost) and match.group('version') == "2b"

    def hash(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def verify(self, hash: bytes, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hash)


preferred_hasher: Hasher = BcryptHasher()
other_hashers: List[Hasher] = [PlaintextHasher()]


def get_hasher(hash: bytes) -> Optional[Hasher]:
    if preferred_hasher.is_my_hashtype(hash):
        return preferred_hasher

    for hasher in other_hashers:
        if hasher.is_my_hashtype(hash):
            return hasher

    return None


def needs_rehash(hash: bytes, hasher: Optional[Hasher] = None) -> bool:
    if hasher is None:
        hasher = get_hasher(hash)

    if hasher is not preferred_hasher:
        return True

    if not hasher.is_up_to_date(hash):
        return True

    return False


def hash_password(password: str) -> bytes:
    return preferred_hasher.hash(password)


def verify_password(hash: bytes, password: str) -> typing.Union[bool, bytes]:
    hasher = get_hasher(hash)
    if hasher is None:
        return False

    if not hasher.verify(hash, password):
        return False

    if needs_rehash(hash, hasher):
        return hasher.hash(password)

    return True
