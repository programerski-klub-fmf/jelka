#!/bin/bash
set -xeuo pipefail
if [ x$1 = xstart ]
then
	mkdir -p $2
	mount -t tmpfs -o nr_blocks=1,mode=0755 tmp $2
	for i in /bin /dev/null /etc /lib /usr /lib64
	do
		[ -d $i ] && mkdir -p $2/$i || { mkdir -p $2/`rev <<<$i | cut -d/ -f2- | rev` && touch $2/$i; }
		[ -e $i ] && mount --bind -onosuid,ro $i $2/$i
	done
	mkdir -p $2/jelka
	mount --bind -onosuid,ro .. $2/jelka
	mkdir -p $2/dev/shm
else
	mount | grep $2 | cut -d\  -f3 | xargs -I '{}' umount '{}'
fi
