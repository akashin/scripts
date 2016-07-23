#!/bin/bash

echo "Syncing taskwarrior on" $(date)
/usr/local/bin/task sync
echo "Sync completed"
