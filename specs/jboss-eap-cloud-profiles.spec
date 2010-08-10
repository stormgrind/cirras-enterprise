%define eap_major_version 5.1
%define eap_user jboss

Summary:        JBoss Enterprise Application Platform Cloud profiles
Name:           jboss-eap-cloud-profiles
Version:        5.1.0.Beta
Release:        20100808
License:        LGPL
BuildArch:      noarch
Group:          Applications/System
Source0:        jboss-eap-%{version}.zip
Source1:        %{name}-mod_cluster-listener.patch
Source2:        %{name}-mod_cluster-service.patch
Source3:        %{name}-jvm-route.patch
Source4:        %{name}-s3_ping.patch
Source5:        %{name}-jmx-access.patch
Requires:       jboss-eap = %{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
JBoss Enterprise Application Platform cloud profiles

%define __jar_repack %{nil}

%prep
rm -rf jboss-eap-%{eap_major_version}
unzip -q %{SOURCE0}

%install
rm -Rf $RPM_BUILD_ROOT

# create directories
install -d -m 755 $RPM_BUILD_ROOT/opt/jboss-eap-%{version}/jboss-as/server/cluster-ec2
install -d -m 755 $RPM_BUILD_ROOT/opt/jboss-eap-%{version}/jboss-as/server/cluster
install -d -m 755 $RPM_BUILD_ROOT/opt/jboss-eap-%{version}/jboss-as/server/group

# copy profiles
cp -R jboss-eap-%{eap_major_version}/jboss-as/server/default/* $RPM_BUILD_ROOT/opt/jboss-eap-%{version}/jboss-as/server/group/
cp -R jboss-eap-%{eap_major_version}/jboss-as/server/production/* $RPM_BUILD_ROOT/opt/jboss-eap-%{version}/jboss-as/server/cluster/
cp -R jboss-eap-%{eap_major_version}/jboss-as/server/production/* $RPM_BUILD_ROOT/opt/jboss-eap-%{version}/jboss-as/server/cluster-ec2/

# install mod_cluster
cp -R jboss-eap-%{eap_major_version}/mod_cluster/mod-cluster.sar $RPM_BUILD_ROOT/opt/jboss-eap-%{version}/jboss-as/server/group/deploy/
cp -R jboss-eap-%{eap_major_version}/mod_cluster/mod-cluster.sar $RPM_BUILD_ROOT/opt/jboss-eap-%{version}/jboss-as/server/cluster/deploy/
cp -R jboss-eap-%{eap_major_version}/mod_cluster/mod-cluster.sar $RPM_BUILD_ROOT/opt/jboss-eap-%{version}/jboss-as/server/cluster-ec2/deploy/

cd $RPM_BUILD_ROOT/opt/jboss-eap-%{version}
patch -p1 < %{SOURCE3}
patch -p1 < %{SOURCE1}
patch -p1 < %{SOURCE2}
patch -p1 < %{SOURCE4}
patch -p1 < %{SOURCE5}

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "JBOSS_EAP_CLOUD_ENABLED=true" > $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,%{eap_user},%{eap_user})
/

%changelog
* Tue Jul 27 2010 Marek Goldmann 5.1.0.Beta-20100727
- Upgrade to JBoss EAP 5.1.0.Beta

* Thu Dec 03 2009 Marek Goldmann 5.0.1-20100715
- Initial release
