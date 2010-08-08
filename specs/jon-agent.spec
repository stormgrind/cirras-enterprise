%define agent_name rhq-enterprise-agent
%define agent_version 3.0.0.GA

Summary:        JON Agent
Name:           jon-agent
Version:        2.4.0.GA
Release:        1
License:        LGPL
BuildArch:      noarch
Source0:        jon-server-%{version}.zip
Source1:        jon-agent.init
Source2:        jon-agent-install.sh
Group:          Applications/System
Requires:       java-1.6.0-openjdk
Requires(post): /sbin/chkconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Probably this is not a good idea, but this is the only way to create a noarch package
# This package contains several libraries, I only found glibc requires, add other here too 
AutoReqProv:    no
Requires:       glibc

%define runuser %{name}
%define __jar_repack %{nil}

%description
An integrated management platform that simplifies the development, testing, deployment and monitoring of your JBoss Enterprise Middleware. From the JBoss Operations Network (JBoss ON) console you can inventory resources from the operating system to applications. Control and audit your application configurations to standardize deployments. Manage, monitor and tune your applications for improved visibility, performance and availability. One central console provides an integrated view and control of your JBoss middleware infrastructure.

%prep
rm -rf $RPM_BUILD_DIR
unzip -q %{SOURCE0} jon-server-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-agent/rhq-enterprise-agent-%{agent_version}.jar -d $RPM_BUILD_DIR
cd $RPM_BUILD_DIR/jon-server-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-agent/ && jar xf rhq-enterprise-agent-%{agent_version}.jar
unzip -q $RPM_BUILD_DIR/jon-server-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-agent/rhq-enterprise-agent-%{agent_version}.zip

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/%{name}-%{version}

cp -R $RPM_BUILD_DIR/jon-server-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-agent/rhq-agent/* $RPM_BUILD_ROOT/opt/%{name}-%{version}

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "RHQ_AGENT_VERSION=%{version}"              > $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "RHQ_AGENT_HOME=/opt/%{name}-%{version}"   >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT/usr/share/%{name}
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/%{name}/jon-agent-install.sh

%clean
rm -Rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r %{name} 2>/dev/null || :
/usr/sbin/useradd -c "%{name}" -r -s /bin/bash -d /opt/%{name}-%{version} -g %{name} %{name} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}
/sbin/chkconfig %{name} on

%files
%defattr(-,root,root)
/

%changelog
* Wed Sep 04 2010 Marek Goldmann 2.4.0.GA
- Upgrade to 2.4.0.GA

* Wed Jun 09 2009 Marek Goldmann 2.3.1
- Initial packaging
