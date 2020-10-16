BLUE="\033[1;34m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
GREEN="\033[1;32m"
DEFAULT="\033[0m"

echo -e "${BLUE}"
rm nohup.out
mv .env .env0
mv requirements.txt requirements0.txt
git reset --hard HEAD
git pull https://github.com/shuanaongithub/World
mv .env0 .env

if [[ $(diff requirements.txt requirements0.txt) ]]; then
    echo -e "${GREEN}"
    echo Installing new packages...
    echo -e "${DEFAULT}"
    python3 -m pip install -r requirements.txt
fi

rm requirement0.txt

echo -e "${GREEN}"
echo Starting bot...

echo -e "${YELLOW}"
echo ----------------
echo NOTE: If the bot is not online, there probably was
echo an error while starting it.
echo
echo Press CTRL-C and run cat nohup.out to see the errors, if there were
echo some.
echo ----------------

echo -e "${RED}"
echo To shut down the bot, press CTRL-C.

echo -e "${DEFAULT}"
nohup python3 bot.py
