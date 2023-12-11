import json
import os
import shutil


# ------------------------------------ 增 ------------------------------------


def create_document(path: str, create_parent_if_not_exist: bool = True) -> bool:
    """
    创建指定目录
    :param path: 指定目录的路径
    :param create_parent_if_not_exist: 如果父目录不存在是否创建
    :return: 操作后，是否存在指定目录，且指定目录是文件夹
    """
    if exists(path):
        return is_document(path)
    if create_parent_if_not_exist:
        os.makedirs(path)
    else:
        os.mkdir(path)
    return exists(path) and is_document(path)


def create_file(file_path: str, create_parent_if_not_exist: bool = True) -> bool:
    if exists(file_path):
        return is_file(file_path)
    if create_parent_if_not_exist:
        parent_path = os.path.dirname(file_path)
        create_document(parent_path, create_parent_if_not_exist)
    with open(file_path, 'w') as f:
        f.write('')


# ------------------------------------ 删 ------------------------------------


def remove(path: str) -> bool:
    """
    删除指定文件或文件夹
    :param path: 指定文件或文件夹的路径
    :return: 是否删除成功
    """
    if is_file(path):
        os.remove(path)
    elif is_document(path):
        shutil.rmtree(path)
    return not exists(path)


def remove_all(document_path: str) -> bool:
    """
    删除指定目录下的所有文件和文件夹

    :param document_path: 指定目录
    :return: 指定目录存在，且所有文件和文件夹都被删除，返回True，否则返回False
    """
    if not exists(document_path):
        return False
    all_removed = True
    if exists(document_path):
        for file in os.listdir(document_path):
            all_removed = all_removed and remove(os.path.join(document_path, file))
    return all_removed


# ------------------------------------ 改 ------------------------------------


def append(path: str, message: str) -> int:
    with open(path, 'a') as f:
        result = f.write(message)
    return result


def clear(path: str):
    write(path, '')


def write(path: str, message: str) -> int:
    if path is None or message is None:
        return 0
    with open(path, 'w') as f:
        result = f.write(message)
    return result


# ------------------------------------ 查 ------------------------------------


def exists(path: str) -> bool:
    return os.path.exists(path)


def is_document(path: str) -> bool:
    return os.path.isdir(path)


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def read(path: str, limit: int = None) -> str:
    with open(path, 'r') as f:
        if limit is None:
            result = f.read()
        else:
            result = f.read(limit)
    return result


def read_json(path: str) -> None | str:
    if not exists(path):
        return None
    with open(path, 'r') as f:
        details = json.loads(f.read())
    return details