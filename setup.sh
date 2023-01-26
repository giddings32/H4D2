#!/bin/bash
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi
chmod +x h4d2
sudo mv ../H4D2 /opt/H4D2
sudo cp -s /opt/H4D2/h4d2 /usr/bin/h4d2

