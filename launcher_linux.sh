#!/bin/bash

echo "Welcome to Quote launcher for Linux!"
echo ""

choice=4
              echo "1-- Launch The Bot"
              echo "2-- Launch With Auto-Restart"
              echo "3-- Update to latest version"
              echo "4-- Update to stable version"

while [ "$choice" = "4" ]; do
read choice
if [ "$choice" = "1" ] ; then
  run_bot
else
        if [ "$choice" = "2" ] ; then
            echo "Starting the bot with auto-restart.."
            echo "-to be added"
        else
                if [ "$choice" = "3" ] ; then
                    echo "Updating to latest version.."
                else
                        if [ "$choice" = "4" ] ; then
                            echo "Updating to stable version.."
                            if [ -d "/home/Quote" ]; then
                                if [ -d "/home/Quote-Old" ]; then
                                    rm /home/Quote-Old/* -f
                                    mv -Ri /home/Quote/configs /home/Quote-Old
                                    rm -rf /home/Quote -f
                                    git clone https://github.com/Deivedux/Quote.git
                                    mv -Ri /home/Quote-Old/configs /home/Quote
                                else
                                    sudo mkdir /home/Quote-Old
                                    mv -Ri /home/Quote/configs /home/Quote-Old
                                    git clone https://github.com/Deivedux/Quote.git 
                                    mv -Ri /home/Quote-Old/configs /home/Quote
                                fi
                            else
                                git clone https://github.com/Deivedux/Quote.git
                            fi
            fi
        fi
    fi
fi

run_bot() {
  echo "Checking requirements.."
  if hash python3 2>/dev/null; then
    if python -m pip install --user -r https://raw.githubusercontent.com/aki-jp/QuoteRequirements/master/requirements.txt; then
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
