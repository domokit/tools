#!/usr/bin/env python

import subprocess
import time

instance_name = "mojo-builder-1"
address = "130.211.144.95"
machine_type = "n1-highcpu-16"
zone = "us-central1-f"

def gcompute(command):
    return subprocess.check_call(["gcloud", "compute"] + command)

gcompute(["instances", "create",
          instance_name,
          "--address", address,
          "--boot-disk-type", "pd-standard",
          "--disk", "name=mojo-builder-ssd",
          "--image", "debian-7-backports",
          "--machine-type", machine_type,
          "--project", "google.com:webkit",
          "--zone", zone,
          "--quiet"])

try:
    # Give the instance a bit of time to spin up or the ssh will fail.
    while subprocess.call(["gcloud", "compute", "ssh",
                           instance_name,
                           "--command", "true",
                           "--quiet",
                           "--zone", zone]) != 0:
        print "waiting for instance to allow ssh..."
        time.sleep(5)


    gcompute(["copy-files",
              "prepare_image.py",
              instance_name + ":~/prepare_image.py",
              "--zone", zone])

    gcompute(["ssh",
              instance_name,
              "--command", "~/prepare_image.py",
              "--quiet",
              "--zone", zone])

except:
    gcompute(["instances", "delete",
              instance_name,
              "--zone", zone,
              "--quiet"])
