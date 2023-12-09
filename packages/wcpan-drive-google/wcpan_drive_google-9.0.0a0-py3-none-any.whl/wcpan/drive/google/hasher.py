from typing import override
import hashlib

from wcpan.drive.core.types import Hasher


async def create_hasher():
    return Md5Hasher()


class Md5Hasher(Hasher):
    def __init__(self):
        self._hasher = hashlib.md5()

    @override
    async def update(self, data: bytes):
        self._hasher.update(data)

    @override
    async def hexdigest(self):
        return self._hasher.hexdigest()

    @override
    async def digest(self):
        return self._hasher.digest()

    @override
    async def copy(self):
        return Md5Hasher()
