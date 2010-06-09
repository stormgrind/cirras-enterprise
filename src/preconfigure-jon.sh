#!/bin/sh

echo "Preconfiguring JON server..."

[ -f /etc/sysconfig/boxgrinder ]   && . /etc/sysconfig/boxgrinder
[ -f /etc/sysconfig/jon ]          && . /etc/sysconfig/jon

DATABASE_NAME=jon
DATABASE_USER=jon
DATABASE_NAME=jon
DATABASE_PASSWORD=`head -c10 /dev/urandom | md5sum | head -c30`

IP_ADDRESS=`ip addr list eth0 | grep "inet " | cut -d' ' -f6 | cut -d/ -f1`

status_code=`curl -o /dev/null -s -m 5 -w '%{http_code}' http://169.254.169.254/latest/meta-data/local-ipv4`

if [ $status_code -eq "200" ]
then
    LOCAL_IP=`curl -s http://169.254.169.254/latest/meta-data/local-ipv4`
    PUBLIC_IP=`curl -s http://169.254.169.254/latest/meta-data/public-ipv4`
else
    LOCAL_IP=$IP_ADDRESS
    # this is intentional
    PUBLIC_IP=$IP_ADDRESS
fi

echo "Local IP address: $LOCAL_IP"
echo "Public IP address: $PUBLIC_IP"

# this will avoid false positive return from below commands
cd /

USER_CREATED=`/bin/su postgres -c "/bin/echo '\du' | /usr/bin/psql -tA" | awk -F\| '{ print $1 }' | grep $DATABASE_USER | wc -l`
DATABASE_CREATED=`/bin/su postgres -c "/usr/bin/psql -tAl" | awk -F\| '{ print $1 }' | grep $DATABASE_NAME | wc -l`

if [ $USER_CREATED -eq "0" ]
then
    echo "Database user $DATABASE_USER not created, creating..."
    /bin/su postgres -c "/usr/bin/createuser -SDR $DATABASE_USER"
    echo "ALTER USER $DATABASE_USER WITH PASSWORD '$DATABASE_PASSWORD';" | /bin/su postgres -c /usr/bin/psql
    echo "User created."
else
    echo "Database user $DATABASE_USER already exists, skipping."
fi

if [ $DATABASE_CREATED -eq "0" ]
then
    echo "Database $DATABASE_NAME not created, creating..."
    /bin/su postgres -c "/usr/bin/createdb -O $DATABASE_USER $DATABASE_NAME"
    echo "Database created."
else
    echo "Database $DATABASE_NAME already exists, skipping."
fi

echo "Reconfiguring jon-server.properties file..."
sed s/#LOCAL_IP#/$LOCAL_IP/g /usr/share/jon/jon-server.properties | sed s/#PUBLIC_IP#/$PUBLIC_IP/g | sed s/#DATABASE_USER#/$DATABASE_USER/g | sed s/#DATABASE_PASSWORD#/$DATABASE_PASSWORD/g | sed s/#DATABASE_NAME#/$DATABASE_NAME/g > $JON_HOME/bin/jon-server.properties
echo "File reconfigured."

echo "Changing permissions in $JON_HOME directory..."
chown jon:jon $JON_HOME -R
echo "Permissions changed."

echo "JON server is preconfigured now."