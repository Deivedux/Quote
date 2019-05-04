#!/bin/sh
echo ""
echo "Welcome to Quote launcher."

choice=3
    echo "1. Launch Without Auto Restart"
    echo "2. Launch With Auto Restart"
    echo "3. Download"
    echo "4. Update"
    echo -e "• You have been given pre-ready publicly accessible program's code that already strictly follows Discord's API Terms of Service (https://discordapp.com/developers/docs/legal)./n • You are free to modify the code to your own likings, but failure to accept the license agreement(https://github.com/Deivedux/Quote/blob/master/LICENSE) will result in a blacklist from the official bot, a ban from it's official Discord server, and a possible flag on your GitHib account.\n • If you are planning on injecting malicious code into your copy of the program, you are risking a ban on your bot account, and a possible Discord account termination under Discord Staff discretion.If you will be found not banned yet, then the above punishments will apply.\nBy self hosting, you agree to these terms."

while [ "$choice" = "4" ]; do
read choice

if [ "$choice" = "1" ] ; then
    echo ""
    echo "Checking requirements.."
    sleep 5s
    curl https://raw.githubusercontent.com/Kwothsei/QuoteRequirements/master/reqs.sh | sh
    echo ""
    echo "Done!"
    echo "Starting the bot.."
    sleep 5s
    python3 quote.py
else
    if [ "$choice" = "2" ] ; then
        curl https://raw.githubusercontent.com/Kwothsei/QuoteRequirements/master/reqs.sh | sh
        echo "Starting the bot with auto restart.."
        sh autorestart_linux.sh
        exit 1
    else
        if ["$choice" = "3" ] ; then
            echo "Downloading Quote.."
            sleep 5s
            git clone https://github.com/Deivedux/Quote.git ./Quote
            echo ""
            echo "Done!"
        else
            if [ "$choice" = "4" ] ; then
                echo "Updating Quote.."
                if [ -d "./Quote" ] ; then
                    if [ -d "./Quote-Old" ] ; then
                        rm ./Quote-Old/* -f
                        mv -v ./Quote/configs -t ./Quote-Old -f
                        rm -rf ./Quote
                        git clone https://github.com/Deivedux/Quote.git ./Quote
                        rm -rf ./Quote/configs -f
                        mv -v ./Quote-Old/configs -t ./Quote -f
                        echo ""
                        echo "Successfully updated!"
                    else
                        sudo mkdir ./Quote-Old
                        mv -v ./Quote/configs -t ./Quote-Old -f
                        rm -rf ./Quote
                        git clone https://github.com/Deivedux/Quote.git ./Quote
                        rm -rf ./Quote/configs -f
                        mv -v ./Quote-Old/configs -t ./Quote -f
                        echo ""
                        echo "Successfully updated!"
                    fi
                else
                    sudo mkdir ./Quote
                    git clone https://github.com/Deivedux/Quote.git ./Quote
                    echo ""
                    echo "Successfully updated!"
                fi
            fi
        fi
    fi
fi
done
exit 0

