import yaml


def yaml_reader_list(filepath):
    with open(filepath, "r") as file_descriptor:
        try:
            data = list(yaml.safe_load_all(file_descriptor))
            return data
        except yaml.YAMLError as exc:
            print("ERROR:", exc)


def yaml_writer_list(filepath, data):
    with open(filepath, "w") as file_descriptor:
        yaml.dump_all(data, file_descriptor, explicit_start=True, sort_keys=False)


def yaml_reader(filepath):
    with open(filepath, "r") as file_descriptor:
        try:
            data = yaml.safe_load(file_descriptor)
            return data
        except yaml.YAMLError as exc:
            print("ERROR:", exc)


def yaml_writer(filepath, data):
    yaml.Dumper.ignore_aliases = lambda *args : True
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor, width=float("inf"), explicit_start=False, sort_keys=False)
