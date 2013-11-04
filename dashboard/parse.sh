#!/bin/bash

CSVDIR=/home/soup
UPDATER=/root/updater.sh
OUTFILE=output.sql
HOST=starrs.example.com
USER=starrs_admin
DB=starrs

for f in $(ls $CSVDIR); do bash $UPDATER $CSVDIR/$f; done > $OUTFILE
psql -h $HOST -U $USER $DB -f $OUTFILE > /dev/null

