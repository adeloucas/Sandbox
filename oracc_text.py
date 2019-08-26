import json as JSON
from typing import Dict, List, Any

import requests
from bs4 import BeautifulSoup


def grab_translation(project: str, pnum: str):
    translation: List[str] = []
    r = requests.get(f"http://oracc.org/{project}/{pnum}")
    soup = BeautifulSoup(r.text)
    for line in soup.find_all("p", class_="tr"):
        s = BeautifulSoup(str(line))
        # seems like SAA10 at least is in Windows-1252 (gross!)
        # https://www.i18nqa.com/debug/utf8-debug.html
        # TODO: add line detection
        # you just need to s.find(class_='xtr-label').get_text()
        s = bytes(s.get_text(), encoding="cp1252").decode()
        translation.append(s)
    return translation


def grab_all(input_json, type: str, split_lines: bool = False) -> List[str]:
    def recursive_walk(json, type):
        if isinstance(json, dict):
            if split_lines:
                if json.get("node") == "d":
                    if json.get("type") == "line-start":
                        yield f"**{json.get('label')}"
            for k, v in json.items():
                if k == type:
                    yield v
                else:
                    yield from recursive_walk(v, type)
        elif isinstance(json, list):
            for item in json:
                yield from recursive_walk(item, type)

    output: list = [token for token in recursive_walk(input_json, type)]
    if split_lines:
        output = " ".join(output).split("**")
    return output


class FileReader:
    """
    This class reads in a file object and converts it from json into a native
    python object.
    It should be identical in functionality to an API reader.
    """

    def __init__(self, filename: str):
        self.filename = filename
        with open(self.filename) as f:
            self.data: Dict[str, Any] = JSON.loads(f.read())


class APIReader:
    """
    This class reads in a URL json file from the ORACC API and turns it into a
    native python object.
    It should be identical in functionality to the file reader.
    The ORACC API is currently non-functional.
    """

    def __init__(self, url: str):
        self.url = url
        # TODO: request and process url


class ORACC_Text:
    """
    This class represent a text from an ORACC corpus.
    """

    def __init__(self, json: dict):
        self.json: Dict[str, Any] = json
        self.norm: List[str] = []
        self.translit: List[str] = []

    def get_norm(self) -> List[str]:
        # I'm not sure of these if/else statements actually do anything with
        # such small texts.
        if len(self.norm) > 0:
            return self.norm
        else:
            self.norm = grab_all(self.json, type="norm")
            return self.norm

    def pprint_norm(self) -> None:
        for line in grab_all(self.json, "norm", split_lines=True):
            print(line)

    def get_translit(self) -> List[str]:
        if len(self.translit) > 0:
            return self.translit
        else:
            self.translit = grab_all(self.json, type="frag")
            return self.translit

    def pprint_translit(self) -> None:
        for line in grab_all(self.json, "frag", split_lines=True):
            print(line)

    # TODO: add 'sense'
