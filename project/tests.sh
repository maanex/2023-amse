#!/bin/bash

python ./data/pull-data.py

echo "Pulling data complete"

pytest ./data/test/test1.py

echo "Test complete"
