import re as _re
import typing as t

from .request import *

_re_lyric = _re.compile(r" *\[\d+?:")
_re_al_url = _re.compile(r'(?<=<meta property="og:image" content=").+?(?=")')


class ImplSongInfo(Impl[dict]):

    def __init__(self, json_data: dict):
        super().__init__(json_data)
        self.json = json_data

    @property
    def id(self):
        return self.json["id"]

    @property
    def name(self):
        """歌曲"""
        return self.json["name"]

    @property
    def ar(self):
        """歌手"""
        return self.json["ar"]

    @property
    def al(self):
        """专辑"""
        return self.json["al"]

    @property
    def dt(self):
        """时长"""
        return self.json["dt"]


class ImplSearch(Impl[dict]):

    def __init__(self, json_data: dict):
        super().__init__(json_data)
        self.json = json_data

    def get_song_by_id(self, music_id: int):
        for song in self.json["result"]["songs"]:
            if song["id"] == music_id:
                return ImplSongInfo(song)
        return None

    @property
    def songs(self):
        return list(map(ImplSongInfo, self.json["result"]["songs"]))


class ImplMusicInfo(Impl[dict]):

    def __init__(self, json_data: dict):
        super().__init__(json_data)
        self.json = json_data

    @property
    def info(self) -> dict:
        return self.json["data"][0]

    @property
    def url(self) -> str:
        return self.json["data"][0]["url"]

    @property
    def req_m4a(self):
        _requests = NoHtmlRequests()
        _requests.url = self.url
        return _requests


class ImplAlbumArt(Impl[str]):

    def __init__(self, text: str):
        super().__init__(text)
        self.text = text

    @property
    def url(self):
        url = _re_al_url.search(self.text)
        if url:
            return url.group()
        return ""

    @property
    def req_image(self):
        _requests = NoHtmlRequests()
        _requests.url = self.url
        return _requests


class ImplLyric(Impl[dict]):

    def __init__(self, json_data: dict):
        super().__init__(json_data)
        self.json = json_data

    @property
    def uncollected(self) -> bool:
        return self.json.get("uncollected", False)

    @property
    def sgc(self) -> bool:
        return self.json.get("sgc", False)

    @property
    def sfy(self) -> bool:
        return self.json.get("sfy", False)

    @property
    def qfy(self) -> bool:
        return self.json.get("qfy", False)

    @property
    def lyric_user(self) -> dict:
        return self.json.get("lyricUser", {})

    @property
    def trans_user(self) -> dict:
        return self.json.get("transUser", {})

    @property
    def nolyric(self) -> bool:
        return self.json.get("nolyric", False)

    @property
    def lrc(self) -> dict:
        return self.json.get("lrc", {})

    @property
    def tlyric(self) -> dict:
        return self.json.get("tlyric", {})

    @property
    def lyrics(self) -> t.List[t.Tuple[float, str, str]]:
        def _parse_lyricstr(s):
            t, text = s.split("[", 1)[1].split("]", 1)
            t = t.split(":", 1)
            return round(int(t[0])*60 + float(t[1]), 3), text.strip()

        olyric_list = []
        for lyric in self.lrc.get("lyric", "").splitlines():
            if _re_lyric.match(lyric):
                olyric_list.append(_parse_lyricstr(lyric))
            else:
                olyric_list.append((0.0, lyric))
        tlyric_list = []
        for lyric in self.tlyric.get("lyric", "").splitlines():
            if _re_lyric.match(lyric):
                tlyric_list.append(_parse_lyricstr(lyric))
        lyric_list = []
        while olyric_list or tlyric_list:
            if olyric_list and tlyric_list:
                olyric = olyric_list[0]
                tlyric = tlyric_list[0]
                if olyric[0] == tlyric[0]:
                    lyric_list.append((olyric[0], olyric[1], tlyric[1]))
                    del olyric_list[0], tlyric_list[0]
                elif olyric[0] < tlyric[0]:
                    lyric_list.append((olyric[0], olyric[1], ""))
                    del olyric_list[0]
                else:
                    lyric_list.append((tlyric[0], "", tlyric[1]))
                    del tlyric_list[0]
            elif olyric_list:
                olyric = olyric_list.pop(0)
                lyric_list.append((olyric[0], olyric[1], ""))
            else:
                tlyric = tlyric_list.pop(0)
                lyric_list.append((tlyric[0], "", tlyric[1]))
        return lyric_list


class ImplComments(Impl[dict]):

    def __init__(self, json_data: dict):
        super().__init__(json_data)
        self.json = json_data

    @staticmethod
    def _parse_comments(comments_list: list):
        comments = []
        for i in comments_list:
            if not i:
                continue
            comment = {
                **i,
                "userId": i["user"]["userId"],
                "nickname": i["user"]["nickname"],
                "avatarUrl": i["user"]["avatarUrl"],
            }
            comment["beReplied"] = [{
                **be_replied,
                "userId": be_replied["user"]["userId"],
                "nickname": be_replied["user"]["nickname"],
                "avatarUrl": be_replied["user"]["avatarUrl"],
            } for be_replied in i["beReplied"]] if i["beReplied"] else []
            comments.append(comment)
        return comments

    @property
    def top_comments(self):
        return self._parse_comments(self.json.get("topComments", {}))

    @property
    def hot_comments(self):
        return self._parse_comments(self.json.get("hotComments", []))

    @property
    def comments(self):
        return self._parse_comments(self.json.get("comments", {}))

    @property
    def more(self) -> bool:
        return self.json["more"]

    @property
    def more_hot(self) -> bool:
        return self.json["moreHot"]

    @property
    def is_musician(self) -> bool:
        return self.json["isMusician"]

    @property
    def total(self) -> int:
        return self.json["total"]

    @property
    def user_id(self) -> int:
        return self.json["userId"]
