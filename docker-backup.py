#!/usr/bin/python3
"""Docker volume backup"""
import os
import re
import sys
import subprocess

from datetime import datetime

import boto3
from dotenv import load_dotenv


BAD_PATH = [
    "/var/run/docker.sock",
    "/etc/localtime",
    "/etc/timezone",
]


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

    s3_enabled = "true" in os.getenv("S3_ENABLED", "false")
    s3_client = None

    if s3_enabled:
        s3_client = config_s3()

    for container in container_list:
        bkp_list = create_backup(container)

        if s3_client and len(bkp_list) > 0:
            upload_s3(s3_client, bkp_list)


    exit(0)


def config_s3():
    try:
        s3_key = os.getenv("S3_KEY")
        s3_secret_key = os.getenv("S3_SECRET_KEY")
        s3_endpoint = os.getenv("S3_ENDPOINT")
        s3_region = os.getenv("S3_REGION")
    except KeyError:
        print("Missing S3_KEY,S3_SECRET_KEY,S3_REGION or S3_ENDPOINT enviromental variable")
        return None

    try:
        client = boto3.client(
            service_name='s3',
            region_name=s3_region,
            aws_access_key_id=s3_key,
            aws_secret_access_key=s3_secret_key,
            endpoint_url=s3_endpoint
        )
    except:
        return None

    return client


def upload_s3(client, backup_list=[]) -> bool:

    bucket = None
    s3_path = None

    try:
        bucket = os.getenv("S3_BUCKET")
        s3_path = os.getenv("S3_PATH")
    except KeyError:
        print("Missing S3_BUCKET or S3_PATH enviromental variabel")
        return False

    for file in backup_list:
        backup_name = re.split("/", file)[-1]
        backup_path = f"{s3_path}/{re.split('/', file)[-2]}"

        print(f"desc=uploading to s3 file={backup_name} path={backup_path}")

        try:
            client.upload_file(file, bucket, f"{backup_path}/{backup_name}",
                               ExtraArgs={'ContentType': 'application/x-tar'})
        except:
            return False

    return True


def create_backup(container):

    backup_dir = None

    try:
        backup_dir = os.getenv("BACKUP_PATH")
    except KeyError:
        print("Missing BACKUP_PATH enviromental variabel, using /tmp/docker-backup")
        backup_dir = "/tmp/docker-backup"

    date_str = datetime.now().strftime('%Y-%m-%d_%H%M%S')

    volume_list = get_volumes(container)

    # Make backup dir
    subprocess.run(["mkdir", "-p", f"{backup_dir}/{container}"],
                   capture_output=True,
                   text=True)

    subprocess.run(["docker", "stop", f"{container}"],
                   capture_output=True,
                   text=True)

    backup_list = []

    for volume_path in volume_list:
        try:
            volume_name = re.split("/", volume_path)[-1]
        except:
            print(f"desc='empty vol, skiping' path={volume_path}")
            continue

        if volume_name == "_data":
            volume_name = re.split("/", volume_path)[-2]

        print(f"desc='Creating backup' name={volume_name} path={volume_path} dest='{backup_dir}/{container}/{volume_name}-{date_str}.tar.xz'")

        command = [
            "tar",
            "-Jcf",
            f"{backup_dir}/{container}/{volume_name}-{date_str}.tar.xz",
            "-C",
            f"{volume_path}",
            "."
        ]

        backup_list.append(
            f"{backup_dir}/{container}/{volume_name}-{date_str}.tar.xz"
        )

        # Run backup
        subprocess.run(command,
                       capture_output=True,
                       text=True)

    # Start container
    subprocess.run(["docker", "start", f"{container}"],
                   capture_output=True,
                   text=True)

    return backup_list


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

    volume_clr = []

    for vol in volume_list:
        if vol not in BAD_PATH:
            volume_clr.append(vol)

    return volume_clr


if __name__ == "__main__":
    main()
