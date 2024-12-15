#!/bin/bash
echo "calling insta scripts via shell file."

echo "activating virtual environment"
source <path to your files>/env/Scripts/activate # windows
source <path to your files>/env/bin/activate # mac or linux

# replace with your desired script or add more than one. 
# BEWARE of IG locking you out if overused. YMMV
python <path to your files>/insta_delete/insta_like.py 

echo "killing all firefox processes"
pgrep firefox | xargs kill