#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test foreground and background colors"""

import time

from ansi_escape_room import attr, bg, fg


def test_1(do_sleep=False):
    for color in range(0, 256):
        print("%s This text is colored %s" % (fg(color), attr("reset")))
        print("%s This background is colored %s" % (bg(color), attr("reset")))
        do_sleep and time.sleep(0.1)

    assert True


if __name__ == "__main__":
    do_sleep = True
    test_1(do_sleep)
