#!/bin/bash

apt-get -y install openjdk-7-jre
apt-get -y install python-pip
pip install --upgrade google-api-python-client
pip install pyyaml
pip install requests
pip install psutil
pip install git+https://github.com/twoolie/NBT@version-1.4.1#egg=NBT

MINECRAFT_URL=$(curl http://metadata/computeMetadata/v1beta1/instance/attributes/minecraft-url)
mkdir minecraft
cd minecraft
wget $MINECRAFT_URL -O minecraft_server.jar

curl http://metadata/computeMetadata/v1beta1/instance/attributes/log4j2 -o log4j2.xml

cd ..
mkdir coal
cd coal

PROJECT_ID=$(curl http://metadata/computeMetadata/v1beta1/instance/attributes/project_id)
$PROJECT_MC_URL="https://$PROJECT_ID.appspot.com/mc"
curl http://metadata/computeMetadata/v1beta1/instance/attributes/project-id -o project_id

curl http://metadata/computeMetadata/v1beta1/instance/attributes/timezones -o timezones.py

curl http://metadata/computeMetadata/v1beta1/instance/attributes/agent-script -o mc_coal_agent.py
chmod a+x mc_coal_agent.py

$MC_PROP_URL="$PROJECT_MC_URL/server.properties"
wget $MC_PROP_URL -O server.properties

$CONTROLLER_URL="$PROJECT_MC_URL/mc_coal_controller.py"
wget $CONTROLLER_URL -O mc_coal_controller.py
chmod a+x mc_coal_controller.py
./mc_coal_controller.py &
