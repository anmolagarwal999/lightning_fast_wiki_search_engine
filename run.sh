#!/bin/bash

START=37
END=37

read -p 'Have you checked that all details are proper ??? ' uservar

for ((i=START;i<=END;i++)); do
    echo "curr num is " $i
    INPUT_FILE_NAME="part_${i}"
    echo "filename is " "$INPUT_FILE_NAME"
    python3 ../stint_master.py "$INPUT_FILE_NAME" >> ../../mounted_dump/again_run_logs.txt 2>&1
done