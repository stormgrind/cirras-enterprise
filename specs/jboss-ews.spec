%define ews_major_version 1.0
%define arch i386

%ifarch x86_64
    %define arch x86_64
%endif

Summary:            JBoss Enterprise Web Server
Name:               jboss-ews
Version:            1.0.1
Release:            20100808
License:            LGPL
Group:              Applications/System
Source0:            %{name}-%{version}-RHEL5-%{arch}.zip
Source1:            %{name}-httpd.init
Source2:            %{name}.sysconfig

Source10:           JBPAPP-4188.zip
Source11:           JBPAPP-3906.zip

Requires(build):    unzip
Requires:           shadow-utils
Requires:           coreutils
Requires:           openssl
Requires:           distcache apr-util apr mailcap
Requires:           java-1.6.0-openjdk
Requires:           initscripts
Requires(post):     /sbin/chkconfig
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
JBoss Enterprise Web Server combines market leading open source technologies with enterprise capabilities to provide a single solution for large scale websites and lightweight web applications.

By integrating Apache Tomcat, Apache Web Server and all of the common connectors used in between under a single subscription, JBoss Enterprise Web Server provides IT with a simple and complete solution for lightweight Java applications. Enterprise Web Server is backed by longterm support lifecycles and operational features to ensure application infrastructure remains up to date and secure. Delivered by the experts in open source middleware, JBoss Enterprise Web Server is the ideal solution for building and managing simple Java applications. 

%prep
%setup -n %{name}-%{ews_major_version}

cd $RPM_BUILD_DIR

# Patches BEGIN ----------------------------
rm -rf JBPAPP-4188
unzip -q %{SOURCE10}

rm -rf JBPAPP-3906
unzip -q %{SOURCE11}
# Patches END ------------------------------

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/%{name}-%{version}
cp -R . $RPM_BUILD_ROOT/opt/%{name}-%{version}

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}-httpd

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-httpd

cd $RPM_BUILD_DIR

# Patches BEGIN ----------------------------
cd JBPAPP-4188
cp jasper.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/tomcat6/lib/
cd ..

cd JBPAPP-3906
unzip -q jboss-ews-1.0.1-2010-CVE-patch-bundle-1-RHEL5-%{arch}.zip
cp -r jboss-ews-1.0/httpd/ $RPM_BUILD_ROOT/opt/jboss-ews-%{version}/httpd/
cd ..
# Patches END ------------------------------

echo "JBOSS_EWS_VERSION=%{version}"                                     >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "JBOSS_EWS_HOME=/opt/%{name}-\$JBOSS_EWS_VERSION"                  >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}

echo "HTTPD=\$JBOSS_EWS_HOME/httpd/sbin/httpd"                  >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}-httpd
echo "CONFFILE=\$JBOSS_EWS_HOME/httpd/conf/httpd.conf"          >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}-httpd
echo "APACHECTL=\$JBOSS_EWS_HOME/httpd/sbin/apachectl"          >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}-httpd
echo "OPTIONS=\"-f \$JBOSS_EWS_HOME/httpd/conf/httpd.conf\""    >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}-httpd

install -d -m 755 $RPM_BUILD_ROOT/var/run/%{name}

rm -rf $RPM_BUILD_ROOT/opt/%{name}-%{version}/httpd/run 
ln -s /var/run/%{name} $RPM_BUILD_ROOT/opt/%{name}-%{version}/httpd/run

%pre
/usr/sbin/groupadd -r %{name} 2>/dev/null || :
/usr/sbin/useradd -c "JBoss EWS" -r -s /bin/bash -d /opt/%{name}-%{version} -g %{name} %{name} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}-httpd
/sbin/chkconfig %{name}-httpd off

umask 077

if [ ! -f /etc/pki/tls/private/localhost.key ] ; then
openssl genrsa -rand /proc/apm:/proc/cpuinfo:/proc/dma:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/pci:/proc/rtc:/proc/uptime 1024 > /etc/pki/tls/private/localhost.key 2> /dev/null
fi

FQDN=`hostname`
if [ "x${FQDN}" = "x" ]; then
   FQDN=localhost.localdomain
fi

if [ ! -f /etc/pki/tls/certs/localhost.crt ] ; then
cat << EOF | openssl req -new -key /etc/pki/tls/private/localhost.key \
         -x509 -days 365 -set_serial $RANDOM \
         -out /etc/pki/tls/certs/localhost.crt 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
root@${FQDN}
EOF
fi

ews_home=/opt/%{name}-%{version}
ews_httpd_home=$ews_home/httpd

sed -i -e "s:User apache:User %{name}:" -e "s:Group apache:Group %{name}:" -e "s: modules/: $ews_httpd_home/modules/:g" -e "s:/var/www:$ews_httpd_home/www:g" -e "s:ServerRoot \"/etc/httpd\":ServerRoot \"$ews_httpd_home/\":" $ews_httpd_home/conf/httpd.conf
cat > .tmppostinstallfile << EOF
# the options for httpd command
OPTIONS="-f $ews_httpd_home/conf/httpd.conf -E $ews_httpd_home/logs/httpd.log"
# the library path
export LD_LIBRARY_PATH=$ews_httpd_home/lib
EOF
sed -i -e "s:HTTPD='./httpd':HTTPD='$ews_httpd_home/sbin/httpd':g" -e "/HTTPD=/r .tmppostinstallfile" $ews_httpd_home/sbin/apachectl
rm -f .tmppostinstallfile

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{name},%{name})
/

%changelog
* Tue May 24 2010 Marek Goldmann 1.0.1-20100808
- Patch for JBPAPP-4188

* Tue May 24 2010 Marek Goldmann 1.0.1-1
- Initial release
