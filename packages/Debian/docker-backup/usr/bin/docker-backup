#!/usr/bin/python3
"""Docker volume backup"""
import os
import re
import sys
import subprocess
from datetime import datetime

from dotenv import load_dotenv

def main():
    """Docker backup start"""
    if len(sys.argv) > 1:
        load_dotenv(sys.argv[1])
    else:
        load_dotenv()

    try:
        container_list = os.getenv("CONTAINER_LIST").split(" ")
    except KeyError:
        print("Missing CONTAINER_LIST enviromental variable")
        raise

    for container in container_list:
        create_backup(container)


    return 0

def create_backup(container):

    backup_dir = None

    try:
        backup_dir = os.getenv("BACKUP_PATH")
    except KeyError:
        print("Missing BACKUP_PATH enviromental variabel")
        raise

    date_str = datetime.now().strftime('%Y-%m-%d_%H%M%S')

    volume_list = get_volumes(container)

    # Stop container
    subprocess.run(["docker", "stop", f"{container}"])

    # Make backup dir
    subprocess.run(["mkdir", "-p", f"{backup_dir}/{container}"])

    for volume_path in volume_list:
        volume_name = re.split("/", volume_path)[-2]

        command = [
            "tar",
            "-Jcf",
            f"{backup_dir}/{container}/{volume_name}-{date_str}.tar.xz",
            "-C",
            f"{volume_path}",
            "."
        ]

        # Run backup
        subprocess.run(command)

    # Start container
    subprocess.run(["docker", "start", f"{container}"])


def get_volumes(container):
    cmd_list = [
        "docker",
        "inspect",
        "-f",
        "'{{ range .Mounts }}{{ .Source }} {{ end }}'",
        f"{container}"
    ]

    volume_list = (
        subprocess
        .run(
            cmd_list,
            capture_output=True,
            text=True)
        .stdout
        .replace(" '\n", "")
        .replace("'", "")
        .split(" ")
    )

    return volume_list





if __name__ == "__main__":
    main()
