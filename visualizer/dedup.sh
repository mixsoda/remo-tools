#!/bin/bash
mv $1 $1.old
uniq $1.old | grep -v "^, $" > $1