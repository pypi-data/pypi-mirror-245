'''
nodepads.folder(
    name=’some_folder’,	# Required
    *,
    version=’0.0.0’, 	# Optional
    description=’a folder’,	# Optional
    author=’folder author’,	# Optional
)

‘/notepads/<folder name>/’

# Folder Architecture

[
    {
    ‘name’: name,
    ‘version’: version,
    ‘description’: description,
    ‘author’: author,
    ‘files’: [] # files in the folder
},
]

folder = notepads.folder(*, **)
folder.update(*, name, version, description, author **)
folder.files	 				# Returns list of files in the folder

folder.update_file(*, name, version, description, author, **)		
folder.read_file(name: str) 			# Returns a files content
folder.write_file(name: str, content: str) 	# Write to a file
folder.wipe_file(name: str)			# Wipes a files content
folder.delete_file(name: str)			# Delete a file from the folder
'''

class NotepadsFolder(object):
    def __init__(self, name, *, version=None, description=None, author=None):
        self.name: str = name
        self.version: str = version
        self.description: str = description
        self.author: str = author
        self.files: dict = {}
        self.directory: object = None
        self.path = f'/notepads/{self.name}/'

    def __repr__(self):
        return f'Folder["{self.path}"](name={self.name}, version={self.version}, description={self.description}, author={self.author}, len_files={len(self.files)})'

    def __str__(self):
        return self.__repr__()

    def get(self, name):
        try:
            for child in self.files:
                if child == name:
                    return self.files.get(child)

            return 'Unknown File'
        except:
            pass

    def delete(self):
        for folder in self.directory.folders:
            if folder[0] == self.name:
                folder_index: int = self.directory.folders.index(folder)
                del self.directory.folders[folder_index]
                break

        try:
            del self.directory.all[self.name]

        except: pass

    def update(self, *, name=None, version=None, description=None, author=None):
        if name:
            self.name = name
        if version:
            self.version = version
        if description:
            self.description = description
        if author:
            self.author = author

    def update_file(self, name, *, version=None, description=None, author=None):
        try:
            for child in self.files:
                if child == name:
                    self.files[child].update(name=name, version=version, description=description, author=author)
                    return child

        except:
            pass

    def read_file(self, name):
        try:
            for child in self.files:
                if child == name:
                    return self.files[child].read()

            return 'Unknown File'
        except:
            pass

    def write_file(self, name, content):
        try:
            for child in self.files:
                if child == name:
                    self.files[child].write(content)
                    return self.files[child]

            return 'Unknown File'
        except:
            pass

    def wipe_file(self, name):
        try:
            for child in self.files:
                if child == name:
                    self.files[child].write('')
                    return child[1]

            return 'Unknown File'
        except:
            pass

    def delete_file(self, name):
        try:
            for child in self.files:
                if child == name:
                    self.files[child].delete()
                    return self

            return 'Unknown File'
        except:
            pass