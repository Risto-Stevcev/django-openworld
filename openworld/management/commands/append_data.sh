#!/usr/bin/env bash
if [ $# != 2 ]; then
    echo "Usage: $0 [json input file] [output file]"
else
    echo '{"data":' >> $2
    cat $1 >> $2
    echo '}' >> $2
fi
