#!/usr/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Root privileges are needed!"
  exit 2
fi

if (( $# != 2 )); then
    >&2 echo "docker-backup <CONTAINER_LIST_FILE> <BACKUP_DEST>"
    exit 2
fi

if [ -e $1 ]; then echo "Container lists exists"; else echo "Container list file doenst exist" && exit 2; fi

TARGET_DIR=$2
CONTAINER_LIST=($(cat $1))

for container in "${CONTAINER_LIST[@]}"; do
    VOLUME_LIST=($(docker inspect -f '{{ range .Mounts }}{{ .Source }} {{ end }}' $container))

    mkdir -p "$TARGET_DIR/$container"
    echo "================================="
    echo "Backup: $container"

    docker stop $container
    for VOLUME in "${VOLUME_LIST[@]}"; do
	    echo "Path: $VOLUME"
	    tar czf "$TARGET_DIR/$container/$container-$(date +%Y-%m-%d).tar.bz2" $VOLUME
	done
    docker start $container
done
