from typing import Literal

from .impl import *
from .request import *

MusicLevel = Literal["standard", "higher", "lossless"]


class ReqSearch(Requests):
    """搜索"""

    method = "post"
    url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
    data = {
        "hlpretag": '<span class="s-fc7">',
        "hlposttag": "</span>",
        "s": "",
        "type": "1",
        "offset": "0",
        "total": "true",
        "limit": "",
        "csrf_token": "",
    }
    json = {}

    def __init__(self, text: str, limit=30):
        self.data = encryptor.encrypt(str({
            **self.data,
            "s": text,
            "limit": str(limit),
        }))
        super().__init__()

    @property
    def impl(self):
        return ImplSearch(self.json)


class ReqMusicInfo(Requests):
    """歌曲信息"""

    method = "post"
    url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
    data = {
        "ids": "",
        "level": "",
        "encodeType": "aac",
        "csrf_token": "",
    }
    json = {}

    def __init__(self, music_id: int, level: MusicLevel = "standard"):
        self.data = encryptor.encrypt(str({
            **self.data,
            "ids": str([music_id]),
            "level": level,
        }))
        super().__init__()

    @property
    def impl(self):
        return ImplMusicInfo(self.json)


class ReqAlbumArt(NoHtmlRequests):
    """专辑封面"""

    method = "get"
    url = "https://music.163.com/m/song?id={}"

    def __init__(self, music_id: int):
        self.url = self.url.format(music_id)
        super().__init__()

    @property
    def impl(self):
        return ImplAlbumArt(self.text)


class ReqLyric(Requests):
    """歌词"""
    method = "post"
    url = "https://music.163.com/weapi/song/lyric?csrf_token="
    data = {
        "id": 0,
        "lv": -1,
        "tv": -1,
        "csrf_token": "",
    }
    json = {}

    def __init__(self, music_id: int):
        self.data = encryptor.encrypt(str({
            **self.data,
            "id": music_id,
        }))
        super().__init__()

    @property
    def impl(self):
        return ImplLyric(self.json)


class ReqComments(NoHtmlRequests):
    """评论"""

    method = "get"
    url = "http://music.163.com/api/v1/resource/comments/R_SO_4_{}?limit={}&offset={}"
    json = {}

    def __init__(self, music_id: int, page_index: int, limit=100):
        self.url = self.url.format(music_id, limit, limit * page_index)
        super().__init__()

    @property
    def impl(self):
        return ImplComments(self.json)


class ReqMp3(NoHtmlRequests):
    """下载歌曲"""

    method = "get"
    url = "http://music.163.com/song/media/outer/url?id={}.mp3"

    def __init__(self, music_id: int):
        self.url = self.url.format(music_id)
        super().__init__()


def search(text: str, limit=30):
    return ReqSearch(text, limit).request()


def music_info(music_id: int, level: MusicLevel = "standard"):
    return ReqMusicInfo(music_id, level).request()


def album_art(music_id: int):
    return ReqAlbumArt(music_id).request()


def lyric(music_id: int):
    return ReqLyric(music_id).request()


def comments(music_id: int, page_index: int, limit=100):
    return ReqComments(music_id, page_index, limit).request()


def mp3(music_id: int):
    return ReqMp3(music_id).request()
