# Docker-Backup
Simple bash script to backup docker volumes using a list of containers

## Backup Tree:
Date time formats are in ISO (8096) format: (yyyy-mm-dd_hhmmss)
```
`-- random_backup_folder
    |-- postgresql-1
    |   |-- database-2026-06-13_211757.tar.xz
    |   |-- database-2026-06-15_000119.tar.xz
    |   `-- database-2026-06-16_000117.tar.xz
    |-- dashboard-db
    |   |-- database-2026-06-13_211702.tar.xz
    |   |-- database-2026-06-15_000004.tar.xz
    |   `-- database-2026-06-16_000006.tar.xz
    `-- something
        |-- something_something-data-2026-06-15_000154.tar.xz
        |-- something_something-data-2026-06-16_000153.tar.xz
        |-- something_something-ssl-2026-06-15_000154.tar.xz
        `-- something_something-ssl-2026-06-16_000153.tar.xz
```
## Install
---
### Debian:

``` bash
wget <LATEST_GITLAB_RELEASE>.deb
sudo dkpg -i <LATEST_GITLAB_RELEASE>.deb
# or
sudo apt install -f ./<LATEST_GITLAB_RELEASE>.deb
```

## Usage

### Python Script:
Create `prod.conf` file containing:

```bash
CONTAINER_LIST="CONTAINER_A CONTAINER_B CONTAINER_C"
BACKUP_PATH="<BACKUP_PATH>"
```

#### Running
```bash
chmod +x deenesse
./deenesse [configuration]
```

#### Systemd
Create `/etc/docker-backup/production.conf` file containing:

```bash
CONTAINER_LIST="CONTAINER_A CONTAINER_B CONTAINER_C"
BACKUP_PATH="<BACKUP_PATH>"
```

#### Enable Timer
```bash
sudo systemctl enable docker-backup@production.timer
```

## Bash Script
### Install
``` bash
curl -O https://raw.githubusercontent.com/RebertiCS/Docker-Backup/refs/heads/main/docker-backup.sh
chmod +x docker-backup.sh
```

#### Command
``` bash
bash dboard-backup.sh ./container_list.txt /backup/volumes/
```

#### Crontab
Runs everyday at 12 PM
``` bash
0 0 * * * /usr/bin/bash /root/dboard-backup.sh /root/container_list.txt /home/rebertics/backups/ag_00/volumes/
```

