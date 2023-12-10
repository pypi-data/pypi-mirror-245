'''
notepads.file(
    name=’some_file’,	 # Required
    *,
    parent=’some_folder’, # Optional
    version=’0.0.0’, 	# Optional
    description=’a file,	# Optional
    author=file author’,	# Optional
)

‘notepads/<file name>’

if parent:
‘/notepads/<folder name>/<file name>/’

# File Architecture

[
    {
    ‘name’: name,
    ‘version’: version,
    ‘description’: description,
    ‘author’: author,
    ‘parent’: parent
},
]

file = notepads.file(*, **)
file.update(*, name, version, description, author, parent, **)
file.read()		 			# Returns file contents
file.write(content: str) 				# Write to file
file.wipe()					# Makes file content blank
file.move(folder: str)				# Move to a new folder
file.delete()	
'''

class NotepadsFile(object):
    def __init__(self, name, *, version=None, description=None, author=None, parent=None):
        self.name: str = name
        self.version: str = version
        self.description: str = description
        self.author: str = author
        self.parent: str = parent
        self.content: str = ''
        self.directory: object = None
        self.path = '/notepads'
        if self.parent: self.path += f'/{self.parent.name}'
        self.path += f'/{self.name}/'

    def __repr__(self):
        string = f'File["{self.path}"](name={self.name}, version={self.version}, description={self.description}, author={self.author}'
        if self.parent: string += f', parent={self.parent.name})'
        return string

    def __str__(self):
        return self.__repr__()

    def update(self, *, name=None, version=None, description=None, author=None, content=None):
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

    def read(self):
        return self.content

    def write(self, content):
        self.content = content
        return self

    def wipe(self):
        self.content = ''
        return self

    def move(self, folder):
        if folder == self.parent.name:
            return self.parent
        self.directory.all[folder].files[self.name] = self
        if self.parent: del self.directory.all[self.parent].files[self.name]
        self.parent = self.directory.all[folder]
        self.parent.files[self.name] = self
        return self.directory.all[folder]

    def delete(self):
        if self.parent: del self.directory.all[self.parent].files[self.name]
        del self.directory.all[self.name]
        for file in self.directory.files:
            if file[0] == self.name:
                del self.directory.files[file]
                break
        self.parent = None
        return self