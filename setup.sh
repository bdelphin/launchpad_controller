#!/bin/sh

# Launchpad Controller - Setup script
# github.com/bdelphin/launchpad_controller

python_version=$(python --version | awk '{print $2}' | cut -c1)
if [ "$python_version" -ge "3" ]
then
    echo "Python 3 detected."

    # dependencies install
    python -m pip install -r requirements.txt
else
    python_version=$(python3 --version | awk '{print $2}' | cut -c1)
    if [ "$python_version" -ge "3" ]
    then
        echo "Python 3 detected."

        # dependencies install
        python3 -m pip install -r requirements.txt
    else
        echo "Python 3 not found, aborting."
        echo "Please install Python 3 first."
        exit 0
    fi
fi

# copy files
echo "root access needed, you'll be prompted to enter your password."
sudo cp LaunchpadController.desktop /usr/share/applications/
sudo mkdir /usr/LPcontroller
sudo cp 