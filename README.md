# Docker-Backup
Simple bash script to backup docker volumes using a list of containers


## Install
``` bash
curl -O https://raw.githubusercontent.com/RebertiCS/Docker-Backup/refs/heads/main/docker-backup.sh
chmod +x docker-backup.sh
```

## Usage
### Command
``` bash
bash dboard-backup.sh ./container_list.txt /backup/volumes/
```

### Crontab
Runs everyday at 12 PM
``` bash
0 0 * * * /usr/bin/bash /root/dboard-backup.sh /root/container_list.txt /home/rebertics/backups/ag_00/volumes/
```

