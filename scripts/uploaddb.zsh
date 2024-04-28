#!/bin/zsh
DATABASE=$1
# some things here maybe
gsutil -h /Users/Max_1/.cloudkeys/bmi520nbastatssql-bf37b9f3e131.json cp $DATABASE gs://bmi520nbastats2023_24/${DATABASE%%.*}

