#!/bin/sh

if hash python3 2>/dev/null
then
      echo "Python3 installed."
else
      echo "Python3 is not installed. Refer to Linux guide!"
      exit 1
fi

echo "Running Quote with autorestart."
while : ; do python3 quote.py; sleep 5s; done
echo "Done"

exit 0
