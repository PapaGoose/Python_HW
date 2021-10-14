import os
import tempfile


class File:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        if not os.path.exists(path_to_file):
            with open(path_to_file, 'w'):
                pass
        self.container = []
        with open(path_to_file, 'r') as f:
            for x in f:
                self.container.append(x)

    def __str__(self):
        return self.path_to_file

    def read(self):
        with open(self.path_to_file, 'r') as f:
            return f.read()

    def write(self, text):
        with open(self.path_to_file, 'w') as f:
            f.write(text)
            return len(text)

    def __add__(self, obj):
        storage_path = os.path.join(tempfile.gettempdir(), tempfile.NamedTemporaryFile().name)
        with open(self.path_to_file, 'r') as r1, open(obj.path_to_file, 'r') as r2:
            s = r1.read() + r2.read()
        with open(storage_path, 'w') as f:
            f.write(s)
        new_p = File(storage_path)
        return new_p

    def __getitem__(self, item):
        return self.container[item]
