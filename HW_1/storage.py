import argparse
import os
import tempfile
import json


parser = argparse.ArgumentParser()
parser.add_argument("--key")
parser.add_argument("--value")
args = parser.parse_args()


def write(key, value):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    # Проверка на наличе файла
    if not os.path.isfile(storage_path):
        # Создание файла
        with open(storage_path, 'w') as f:
            f.write(json.dumps({key: [value]}))
    else:
        # Обновление файла
        with open(storage_path, 'r') as f:
            json_obj = json.load(f)
        if key in json_obj.keys():
            json_obj[key].append(value)
        else:
            json_obj[key] = [value]
        with open(storage_path, 'w') as f:
            json.dump(json_obj, f)


def read(key):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    if not os.path.isfile(storage_path):
        print(None)
    else:
        with open(storage_path, 'r') as f:
            dct = json.loads(f.read())
            # Результат вывод
            try:
                print(', '.join(dct[key]))
            except:
                print(None)


if args.value is not None:
    write(args.key, args.value)
else:
    read(args.key)
