#!/usr/bin/env python

import os
import subprocess

def system(command):
    return subprocess.check_call(command)

os.chdir("/mojo")

system(["gclient", "sync"])
os.chdir("/mojo/src")
system(["gn", "gen", "out/Debug"])
system(["ninja", "-C", "out/Debug", "mojo"])
system(["./mojo/tools/mojob.sh", "test", "--debug"])
