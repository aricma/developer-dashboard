class SkipMissingDict(dict):
    def __missing__(self, _):
        return ""


class KeepMissingDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'
