#!/bin/bash

if [ $(hostname) = "onlixme" ]; then # official host
    PYTHON_BIN="/stuff/./pypy3.9-v7.3.9-linux64/bin/pypy"
    cd "/home/python/web/public/"
    echo "» Recognized official host"
else # selfhost
    PYTHON_BIN="python"
    echo "» Recognized self-host"
fi

echo "» Starting in: $(pwd)"

while true
do
    echo "» BEGIN"
    # source web/bin/activate
    # PREPARE
    pip install pipreqs
    pipreqs --mode gt --print > requirements.txt
    $PYTHON_BIN -m pip install -r ./requirements.txt > logs/pip.txt
    
    echo "» Running..."

    # RUN
    date +"%s" > logs/last_start.txt
    $PYTHON_BIN web.py > logs/web.py.txt
    # ====================================
    echo "» BROKE"
    sleep 3
    echo "» END"
done
