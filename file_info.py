import os
import argparse
import logging
from collections import namedtuple

FSObject = namedtuple("FSObject", "name ext is_dir parent")


def info_dir(path):
    fs_objects = []
    parent = os.path.basename(os.path.dirname(path))
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                fs_objects.append(
                    FSObject(name=entry.name, ext="", is_dir=True, parent=parent)
                )
                fs_objects.extend(info_dir(entry.path))
            else:
                name, ext = os.path.splitext(entry.name)
                fs_objects.append(
                    FSObject(name=name, ext=ext, is_dir=False, parent=parent)
                )
        logging.info(f"Добавлен объект {fs_objects[-1]}")
    except Exception as exc:
        logging.error(f"Ошибка при обработке директории {path}: {exc}")
    return fs_objects


def save_to_file(fs_objects, file_name):
    with open(file_name, "w") as f:
        for obj in fs_objects:
            f.write(f"{obj.name}, {obj.ext}, {obj.is_dir}, {obj.parent}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Просмотр содержимого директории и вывод информации о файлах."
    )
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=".",
        help="Путь к директории для просмотра. По умолчанию текущая директория.",
    )
    args = parser.parse_args()

    fs_objects = info_dir(args.path)
    for obj in fs_objects:
        print(obj)

    # save_to_file(fs_objects, 'file_info.txt')
    # logging.info('Данные сохранены в файл file_info.txt')


if __name__ == "__main__":
    log_file = "file_info.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    common_log = logging.getLogger(__name__)
    main()
