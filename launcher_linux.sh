#!/bin/bash

echo "Welcome to Quote launcher for Linux!"
echo ""


choices=4
echo "1-- Launch The Bot"
echo "2-- Launch With Auto-Restart"
echo "3-- Update to latest version"
echo "4-- Update to stable version"

while [ $choice -eq 4]; do
read choice
if [ $choice -eq 1] ; then
  run_bot
else
      if [ $choice -eq 2] ; then
        echo "Starting the bot with auto-restart.."
        echo "-to be added"
      else
            if [ $choice -eq 3] ; then
              echo "Updating to latest version.."
            else
                  if [ $choice -eq 4] ; then
                    echo "Updating to stable version.."
                  fi
            fi
      fi
fi

run_bot() {
  echo "Checking requirements.."
  if hash python3 2>/dev/null; then
    if python -m pip install --user -r curl -L https://raw.githubusercontent.com/aki-jp/QuoteRequirements/master/requirements.txt | txt; then
      echo "Starting Quote.."
      python quote.py
    else
      echo "Failed to install requirements!"
      exit 254
    fi
  elif hash python 2>/dev/null; then
          case "$(python --version 2>&1)" in
                  *" 3."*)
                          echo ""
                          ;;
                  *)
                          echo "Wrong Python version! You need Python 3.5+ to run Quote!"
                          exit
                          ;;
          esac
  fi
}

done
exit 0
