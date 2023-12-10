"""Test Url Counter."""
import json
import os
from pathlib import Path

import pytest
from rich import print_json
from yirgachefe import logger

from url_counter.main import url_counter

TEST_DIR = Path(__file__).parent.joinpath("./samples")


@pytest.fixture(params=os.listdir(TEST_DIR))
def target_file(request):
    with open(TEST_DIR.joinpath(request.param), "r") as f:
        logger.debug(f'Try test with ({request.param})')
        yield f


class TestUrlCounter:
    def test_url_counter_sample1(self, target_file):
        url_count: dict = url_counter(target_file)
        print_json(json.dumps(url_count))
        for count in url_count:
            assert url_count.get(count, 0) > 0
