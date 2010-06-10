Summary:        JON server
Name:           jon
Version:        2.3.1.GA
Release:        1
License:        LGPL
BuildArch:      noarch
Group:          Applications/System
Source0:        jon-server-%{version}.zip
Source3:        jon.init
Source4:        preconfigure-rhq.sh
Source5:        rhq-server.properties
Source6:        jon-plugin-pack-eap-%{version}.zip
Source7:        jon-plugin-pack-ews-%{version}.zip

Source10:       jon-server-%{version}-patch2.zip

Requires:       shadow-utils
Requires:       java-1.6.0-openjdk
Requires:       unzip
Requires:       urw-fonts
Requires(pre):  postgresql-server
Requires(post): /sbin/chkconfig
Requires(post): /bin/sed
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv:    0
AutoReq:        0

%define runuser %{name}
%define __jar_repack %{nil}

%description
An integrated management platform that simplifies the development, testing, deployment and monitoring of your JBoss Enterprise Middleware. From the JBoss Operations Network (JBoss ON) console you can inventory resources from the operating system to applications. Control and audit your application configurations to standardize deployments. Manage, monitor and tune your applications for improved visibility, performance and availability. One central console provides an integrated view and control of your JBoss middleware infrastructure.

%prep
rm -rf $RPM_BUILD_DIR
unzip -q %{SOURCE0} -d $RPM_BUILD_DIR

unzip -q %{SOURCE6} -d $RPM_BUILD_DIR
unzip -q %{SOURCE7} -d $RPM_BUILD_DIR

unzip -q %{SOURCE10} -d $RPM_BUILD_DIR
unzip -q $RPM_BUILD_DIR/jon-server-%{version}-patch2-overlay.zip -d $RPM_BUILD_DIR

cp -r $RPM_BUILD_DIR/jon-server-%{version}/jbossas/server/default/deploy/rhq.ear/* $RPM_BUILD_DIR/jon-server-%{version}/jbossas/server/default/deploy/rhq.ear.rej
rm -rf $RPM_BUILD_DIR/jon-server-%{version}/jbossas/server/default/deploy/rhq.ear                                                                        

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/%{name}-%{version}
cp -R %{name}-server-%{version}/* $RPM_BUILD_ROOT/opt/%{name}-%{version}

cp -R %{name}-plugin-pack-ews-%{version}/*.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-plugins
cp -R %{name}-plugin-pack-eap-%{version}/*.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-plugins

cp -R %{name}-plugin-pack-eap-%{version}/*.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-plugins

install -d -m 755 $RPM_BUILD_ROOT/usr/share/%{name}
install -m 755 %{SOURCE4} $RPM_BUILD_ROOT/usr/share/%{name}/preconfigure-rhq.sh
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/usr/share/%{name}/rhq-server.properties

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "RHQ_VERSION=%{version}"            > $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "RHQ_HOME=/opt/%{name}-%{version}" >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_initrddir}/%{name}

%clean
rm -Rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r rhq 2>/dev/null || :
/usr/sbin/useradd -c "rhq" -r -s /bin/bash -d /opt/%{name}-%{version} -g rhq rhq 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}
/sbin/chkconfig %{name} on

%files
%defattr(-,rhq,rhq)
/

%changelog
* Wed Jun 09 2009 Marek Goldmann 2.3.1
- Initial packaging
