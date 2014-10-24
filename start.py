#!/usr/bin/env python

import random
import subprocess
import sys

job_name = "mojo-builder-%s" % str(random.randint(1, 100000))
print "job_name: %s" % job_name

retval = subprocess.call(["sudo",
    "-n", "docker",
    "run",
    "--name=%s" % job_name, "mojo-image",
    "-v", "/var/lib/jenkins/jobs/mojo_continuous_builder/workspace:" +
          "/workspace:ro",
    "/mojo/build.py"])
subprocess.check_call(["sudo", "-n", "docker", "rm", job_name])

sys.exit(retval)
