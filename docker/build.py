#!/usr/bin/env python

import os
import subprocess

def system(command):
    return subprocess.check_call(command)

os.chdir("/mojo")

system(["cp", "-r", "/workspace", "src"])
system(["gclient", "sync"])
os.chdir("/mojo/src")
system(["./mojo/tools/mojob.sh", "--debug", "gn"])
system(["./mojo/tools/mojob.sh", "--debug", "build"])
system(["./mojo/tools/mojob.sh", "--debug", "test"])
