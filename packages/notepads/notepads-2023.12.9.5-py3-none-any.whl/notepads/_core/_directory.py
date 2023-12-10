class NotepadsDirectory(object):
    def __init__(self):
        self.folders: list = []
        self.files: list = []
        self.all: dict = {}
        self.path = '/notepads/'

    def get(self, name):
        return self.all.get(name)

    def delete(self, name):
        if name in self.folders:
            self.folders.remove(name)

        elif name in self.files:
            self.files.remove(name)

        if name in self.all:
            del self.all[name]

        return self
    
    def __repr__(self):
        return f'Directory["{self.path}"](folders=(length, {len(self.folders)}), files=(length, {len(self.files)}))'

    def __str__(self):
        return self.__repr__()

    def __int__(self):
        return len(self.all)

    def __len__(self):
        return self.__int__()

    def __contains__(self, name):
        return name in self.all

    def __getitem__(self, name):
        return self.all[name]

    def __setitem__(self, name, value):
        self.all[name] = value

    def __delitem__(self, name):
        del self.all[name]

    def __iter__(self):
        return iter(self.all)
