# Docker-Backup
Simple bash script to backup docker volumes using a list of containers




## Usage
### Python Script:
Create `.env` file containing:

```bash
CONTAINER_LIST="CONTAINER_A CONTAINER_B CONTAINER_C"
BACKUP_PATH="<BACKUP_PATH>"
```

#### Running
```bash
chmod +x deenesse
./deenesse [configuration]
```

## Systemd
Create `/etc/docker-backup/production.conf` file containing:

```bash
CONTAINER_LIST="CONTAINER_A CONTAINER_B CONTAINER_C"
BACKUP_PATH="<BACKUP_PATH>"
```

#### Enable Timer
```bash
sudo systemctl enable docker-backup@production.timer
```

### Bash Script
## Install
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

