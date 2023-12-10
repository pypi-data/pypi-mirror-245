from __future__ import annotations

import base64
import json
import random
from typing import Generic, TypeVar

import httpx
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class Encryptor:
    """数据加密"""
    def __init__(self):
        self.character = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.iv = "0102030405060708"
        self.public_key = "010001"
        self.modulus = (
            "00e0b509f6259df8642dbc35662901477df22677ec152b"
            "5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417"
            "629ec4ee341f56135fccf695280104e0312ecbda92557c93"
            "870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b"
            "424d813cfe4875d3e82047b97ddef52741d546b8e289dc69"
            "35b3ece0462db0a22b8e7"
        )
        self.nonce = "0CoJUm6Qyw8W8jud"

    def create_random_str(self):
        """产生16位随机字符, 对应函数a"""
        generate_string = random.sample(self.character, 16)
        return "".join(generate_string)

    def aes_encrypt(self, text, key):
        """AES加密, 对应函数b"""
        # 数据填充
        text = pad(data_to_pad=text.encode(), block_size=AES.block_size)
        key = key.encode()
        iv = self.iv.encode()
        aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        encrypt_text = aes.encrypt(plaintext=text)
        # 字节串转为字符串
        return base64.b64encode(encrypt_text).decode()

    @staticmethod
    def rsa_encrypt(i, e, n):
        """RSA加密, 对应函数c"""
        num = pow(int(i[::-1].encode().hex(), 16), int(e, 16), int(n, 16))
        return format(num, "x")

    def encrypt(self, data):
        """对应函数d"""
        i = self.create_random_str()
        enc_text = self.aes_encrypt(data, self.nonce)
        enc_text = self.aes_encrypt(enc_text, i)
        enc_sec_key = self.rsa_encrypt(i, self.public_key, self.modulus)
        from_data = {"params": enc_text, "encSecKey": enc_sec_key}
        return from_data


class Requests:
    """请求"""

    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "referer": "https://music.163.com/",
    }
    encoding = "UTF-8"
    method = "get"
    url = ""
    data = None

    _response: httpx.Response | None = None
    json = None
    responsed = False
    ok = False
    exc: Exception | None = None
    finished = False

    def request(self):
        try:
            self._response = httpx.request(self.method, url=self.url, headers=self.headers, data=self.data)
            self.response.encoding = self.encoding
            self.responsed = True
            self.ok = self.response.status_code == 200
            if self.json is not None:
                self.json = json.loads(self.response.text)
        except Exception as exc:
            self.exc = exc
        else:
            self.finished = True
        return self

    @property
    def response(self):
        if not self._response:
            raise Exception("Request not responsed")
        return self._response

    @property
    def content(self):
        return self.response.content

    @property
    def text(self):
        return self.response.text

    @property
    def impl(self):
        return None


class NoHtmlRequests(Requests):
    """非页面请求"""
    def request(self):
        super().request()
        if self.success and b"<html>" in self.content[:100]:
            self.success = False


T = TypeVar("T")


class Impl(Generic[T]):
    """接口"""
    def __init__(self, api: T):
        self.api = api

    def __str__(self):
        return "%s(%r)" % (self.__class__.__name__, self.api)

    __repr__ = __str__


encryptor = Encryptor()
