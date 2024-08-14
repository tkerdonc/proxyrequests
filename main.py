#!/usr/bin/env python3

import os
import sys
import subprocess
from src import head, page, tail

head = head.Head()
head.render()

for folder in sys.argv[1:]:
    p = page.Page(folder)
    p.render()

tail = tail.Tail()
tail.render()