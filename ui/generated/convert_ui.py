#!/usr/bin/env python3

import os, subprocess

for root, sub_dirs, files in os.walk(u'.'):
    for f in files:
        if f.endswith(".ui"):
            ui_path = os.path.join(root, f)
            py_path = os.path.join(root, f[:-3] + ".py")
            if os.path.isfile(py_path):
                os.remove(py_path)
            subprocess.run(["pyuic5", ui_path, "-o", py_path])