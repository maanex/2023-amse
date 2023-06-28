#!/bin/bash

python ./data/pull-data.py

print "Pulling data complete"

pytest ./data/test/test1.py

print "Test complete"
