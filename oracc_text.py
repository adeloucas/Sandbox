import json as JSON

def recursive_walk(json, key):
    if isinstance(json, dict):
        # need to check for 'node': 'd' and 'type': 'line-start' in here and yield those
        # I don't think we split here... we should check if we need line breaks and pass off
        # to another function.
        for k, v in json.items():
            if k == key:
                yield v
            else:
                yield from recursive_walk(v, key)
    elif isinstance(json, list):
        for item in json:
            yield from recursive_walk(item, key)


class FileReader():
    '''
    This class reads in a file object and converts it from json into a native python object.
    It should be identical in functionality to an API reader.
    '''
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as f:
            self.data = JSON.loads(f.read())


class APIReader():
    '''
    This class reads in a URL json file from the ORACC API and turns it into a native python object.
    It should be identical in functionality to the file reader.
    The ORACC API is currently non-functional.
    '''
    def __init__(self, url):
        self.url = url
        # request and process url


class ORACC_Text():
    '''
    This class represent a text from an ORACC corpus.
    '''
    def __init__(self, json):
        self.json = json

    def get_norm(self):
        if self.norm:
            return self.norm
        else:
            self.norm = [word for word in recursive_walk(self.json, 'norm')]
            return self.norm
