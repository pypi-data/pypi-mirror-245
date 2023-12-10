"""Simple Url Counter Main"""
import json
import re
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path

import click
from rich import print_json
from yirgachefe import config, logger


def url_counter(file) -> dict:
    ignores = config.ignores.split(',')
    url_count = defaultdict(int)
    regex_dict = {"json": r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s("
                          r")<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,"
                          r"<>?«»“”‘’]))",
                  "log": r"\b(?:GET|POST|PUT|DELETE)\s+([^\s]+)\b"}
    regex = re.compile(regex_dict[file.name.split('.')[-1]])

    for line in file:
        if any(ignore in line for ignore in ignores if ignore != ''):
            continue

        match = regex.search(line)
        if match:
            url = match.group(0)
            url_count[url] += 1

    return url_count


def make_result_file(targets: list, counter: list):
    result_file_name = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    result = {'targets': targets, 'result': counter}
    with open(result_file_name, "w") as file:
        json.dump(result, file, indent=4)


@click.command()
@click.argument("files", nargs=-1, type=click.File('r'))
@click.option('-d', '--folder', type=click.Path(exists=False), default="", help="Target Json Folder.")
@click.option('-f', '--makefile', is_flag=True, show_default=True, default=False, help="Make Result File.")
@click.option('-r', '--recursive', is_flag=True,
              show_default=True, default=False, help="Includes Sub folders recursively.")
def main(files, folder, makefile, recursive):
    counter = Counter()
    file_list = None
    targets = []

    if files:
        logger.info('Run with files')
        file_list = files
    elif folder:
        directory_path = Path(folder)
        if recursive:
            logger.info(f'Run in path({folder}) recursively.')
            files_ = directory_path.glob('**/*')
        else:
            logger.info(f'Run in path({folder}).')
            files_ = directory_path.glob('*')

        file_list = (
            open(file, "r") for file in files_ if file.suffix in [".json", ".log"] and file.name[:7] != "result_"
        )

    if file_list:
        for file in file_list:
            targets.append(file.name)
            count = url_counter(file)
            counter.update(Counter(count))

    result = [f"{item[0]}: {item[1]}" for item in counter.most_common()]
    if makefile:
        make_result_file(targets, result)

    print_json(json.dumps(result))
