#!/bin/bash

#
# Base World Unix install script!
#     Written by Mrmagicpie!
#

# Check if the user is root before we continue!
if [ $EUID -ne 0 ]; then

   echo
   echo "|------------------------------------|"
   echo "|You are not root! Please use sudo or|"
   echo "|     root to run this script!       |"
   echo "|                                    |"
   echo "|        Exiting World Setup!        |"
   echo "|------------------------------------|"
   echo

   exit 1
fi;

# Define functions bc they're cool!

# Timeout to be called when read times out
timeout()
{

  echo
  echo "|------------------------------------|"
  echo "|  You have timed out! Please rerun  |"
  echo "|           this script!             |"
  echo "|------------------------------------|"
  echo

  sleep 3
  exit 1
}

# Function for if apt gets an error
apt_error()
{

  echo
  echo "|------------------------------------|"
  echo "| An unknown APT error has occurred! |"
  echo "|------------------------------------|"
  echo

  sleep 3
  exit 1
}

# Function to install things with apt
install()
{
  echo
  echo "Working... "

  # Update the system, sending to le void bc people don't need that
  sudo apt-get update >> /dev/null || apt_error
  # Installing dependencies, again, sending to le void
  sudo apt-get install default-jdk python3 python3-venv >> /dev/null || apt_error

  # Create a python venv
  python3 -m venv env
  sleep 1

  echo
  echo "|------------------------------------|"
  echo "| Installation complete! Please run: |"
  echo -e "|$PURPLE     source ./env/bin/activate      $NOCOLOUR|"
  echo "|                and                 |"
  echo -e "|$PURPLE python3 -m pip install -r requirements.txt $NOCOLOUR|"
  echo "|------------------------------------|"
  echo

  sleep 1

  echo
  echo "|------------------------------------|"
  echo -e "| I \033[0;31mstrongly$NOCOLOUR encourage you to \033[0;31mnever$NOCOLOUR  |"
  echo -e "| run things as root unless you \033[0;31mhave$NOCOLOUR |"
  echo "|    to! Please, make a new user!    |"
  echo "|------------------------------------|"
  echo

  sleep 3
  exit 0
}

# Define colour variables, and the bot apt requirements
PURPLE="\033[0;35m"
NOCOLOUR="\033[0m"
REQUIREMENTS="""
|
$PURPLE  Java$NOCOLOUR
  |$PURPLE Python3$NOCOLOUR
  |$PURPLE Python3-VENV
   $NOCOLOUR    |
"""

# TODO: Setup os options.

echo
echo "|------------------------------------|"
echo "| Would you like to install these?   |"  # Yes ik there's a spacing issue here, bash bad
echo -e $REQUIREMENTS
echo "|------------------------------------|"
echo

# Read command line input and save into "installing", has a timeout of 25 seconds
read -t 25 -p "Please answer with y/n: " installing || timeout

# Check if the user has inputted a valid answer!
case $installing in

  y|Y)
    install
    ;;

  n|N)
    echo
    echo "|------------------------------------|"
    echo "|              Exiting!              |"
    echo "|------------------------------------|"
    echo

    sleep 3
    exit 0
    ;;

  *)
    echo
    echo "|------------------------------------|"
    echo "|          Invalid option!           |"
    echo "|------------------------------------|"
    echo

    sleep 3
    exit 1
    ;;

# Esac is a funky word
esac


#
#  Copyright (c) 2021 Mrmagicpie & Contributors
#            All rights reserved!
#
#        https://GitHub.com/Mrmagicpie
#

#      Please no remove copyright Shuana :D
