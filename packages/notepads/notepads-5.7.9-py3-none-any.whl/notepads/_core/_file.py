from .._utils._syntax import NotepadsSyntax

class NotepadsFile(object):
    def __init__(self, name, *, version=None, description=None, author=None, parent=None, **kwargs):
        self.name: str = name
        self.file_type = str(self.name).split('.')[-1]
        self.version: str = version
        self.description: str = description
        self.author: str = author
        self.parent: str = parent
        self.content: str = ''
        self.directory: object = None
        self.path = '/notepads'
        if self.parent: self.path += f'/{self.parent.name}'
        self.path += f'/{self.name}/'

        for key, value in kwargs.items():
            try: setattr(self, key, value)
            except: pass

    def syntax(self):
        return NotepadsSyntax(self.file_type, self.content)

    def __repr__(self):
        string = f'File["{self.path}"](name={self.name}, version={self.version}, description={self.description}, author={self.author}'
        if self.parent: string += f', parent={self.parent.name})'
        return string

    def __str__(self):
        return self.__repr__()

    def update(self, *, name=None, version=None, description=None, author=None, content=None, **kwargs):
        if name:
            self.name = name
        if version:
            self.version = version
        if description:
            self.description = description
        if author:
            self.author = author
        if content:
            self.content = content

        for key, value in kwargs.items():
            try: setattr(self, key, value)
            except: pass

    def read(self):
        return self.syntax()

    def write(self, content):
        self.content = content
        return self

    def wipe(self):
        self.content = ''
        return self

    def move(self, folder=''):
        try:
            if self.parent:
    
                if folder == self.parent.name:
                    return self.parent
            self.directory.all[folder].files[self.name] = self
            if self.parent: 
                del self.parent.files[self.name]
    
            self.parent = self.directory.all[folder]
            self.parent.files[self.name] = self
            return self.directory.all[folder]
        except KeyError:
            if self.parent:
                del self.parent.files[self.name]
                self.parent = None

            self.directory.all[self.name] = self
            self.directory.files.append((self.name, self))
            return self.directory.all[self.name]
            

    def delete(self):
        if self.parent: 
            del self.parent.files[self.name]

        try: del self.directory.all[self.name]
        except: pass
        for file in self.directory.files:
            if file[0] == self.name:
                indx = self.directory.files.index(file)
                del self.directory.files[indx]
                break
        self.parent = None
        return self
