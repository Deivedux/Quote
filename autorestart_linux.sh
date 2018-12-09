#!/bin/sh

if hash python3 2>/dev/null; then
      echo "Python 3.5+ installed."
      echo "Running Quote with Auto-Restart!"
      while : ; do python3 quote.py; sleep 5s; done
      echo "Done"
      exit 0
else
      echo "Python 3.5+ is not installed. Refer to Linux guide!"
      exit 1
fi