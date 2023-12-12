# -*- coding: utf-8 -*-
# Author : Ethan
# Time : 2023/12/11 16:13
import time

import pytest

@pytest.mark.timeassert(1)
def test_01():
    time.sleep(2)


@pytest.mark.timeassert(2)
def test_01():
    time.sleep(2)


@pytest.mark.timeassert(3)
def test_01():
    time.sleep(2)