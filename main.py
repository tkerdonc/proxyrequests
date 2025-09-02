#!/usr/bin/env python3

import os
import sys
import subprocess
from src import head, page, tail

root = sys.argv[1]
folders = [
            os.path.join(root, item)
            for item in os.listdir(root)
            if os.path.isdir(os.path.join(root, item))
]

head = head.Head(root)
head.render()

for folder in sorted(folders):
    p = page.Page(folder)
    p.render()

tail = tail.Tail()
tail.render()
