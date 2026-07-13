#!/usr/bin/python3
"""Docker volume backup"""
import os
import re
import sys
import subprocess

from time import process_time
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
    except AttributeError:
        print(f"File {sys.argv[1]} doenst exist, check systemd configuration.")
        raise
    except Exception as err:
        print(f"Unhandled error, exiting:\n - Error:\n {err}")
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
    start_time = process_time()

    volume_list = get_volumes(container)

    # Make backup dir
    print(f"Creating backup directory for {container}.")
    subprocess.run(["mkdir", "-p", f"{backup_dir}/{container}"],
                   capture_output=True,
                   text=True)

    subprocess.run(["docker", "stop", f"{container}"],
                   capture_output=True,
                   text=True)

    for volume_path in volume_list:
        try:
            volume_name = re.split("/", volume_path)[-2]
        except:
            print("Found empty volume path, skipping...")
            continue

        print(f"Creating backup:\n - Name: {volume_name}\n - Path: {volume_path}\n - Dest: {backup_dir}/{container}/{volume_name}-{date_str}.tar.xz")

        command = [
            "tar",
            "-Jcf",
            f"{backup_dir}/{container}/{volume_name}-{date_str}.tar.xz",
            "-C",
            f"{volume_path}",
            "."
        ]

        # Run backup
        subprocess.run(command,
                       capture_output=True,
                       text=True)

    # Start container
    subprocess.run(["docker", "start", f"{container}"],
                   capture_output=True,
                   text=True)

    total_time = round((process_time() - start_time) * 1000, 2)
    print(f" - Runtime: {total_time}s")



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
