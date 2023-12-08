from test_base_package.utils.read_util import ReadFileData

dataRow = {}


def get_conf():
    read = ReadFileData()
    data = read.load_yaml("conf.yml")
    return data


dataRow = get_conf()
