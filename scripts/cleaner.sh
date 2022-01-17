#!/usr/bin/bash

awk -F, '$1 !~ /WARNING/' $1 > $2