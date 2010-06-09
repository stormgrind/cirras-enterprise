#!/bin/sh

[ -f /etc/sysconfig/boxgrinder ] && . /etc/sysconfig/boxgrinder

JON_AGENT_HOME=/opt/jon-agent

[ -f /etc/sysconfig/jon-agent ] && . /etc/sysconfig/jon-agent

[ "x$JON_SERVER_IP" = "x" ] && exit 0

JON_AGENT_JAR_LOCATION=http://$JON_SERVER_IP:7080/agentupdate/download

rm -rf $JON_AGENT_HOME
mkdir -p $JON_AGENT_HOME

sleep=0
downloaded=0
while [ "$downloaded" = "0" ]; do
    sleep 5
    sleep=`expr $sleep + 5`

    http_code=`curl -o /dev/null -s -m 5 -w '%{http_code}' $JON_AGENT_JAR_LOCATION`

    if [ $http_code -eq "200" ]
    then
        wget $JON_AGENT_JAR_LOCATION -O $JON_AGENT_HOME/jon-agent.jar
        downloaded=1        
    fi
done

cd $JON_AGENT_HOME

java -jar jon-agent.jar --install

sed -i s/#AGENT_NAME#/$APPLIANCE_NAME-$HOSTNAME/g $JON_AGENT_HOME/jon-agent/conf/agent-configuration.xml
