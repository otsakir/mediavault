

class Breadcrumb:
    label = ''
    url = None

    def __init__(self, label: str, url: str|None):
        self.label = label
        self.url = url
