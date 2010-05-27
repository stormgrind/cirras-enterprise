%define eap_major_version 5.0

Summary:        JBoss Enterprise Application Platform cloud profiles
Name:           jboss-eap-cloud-profiles
Version:        5.0.1
Release:        1
License:        LGPL
BuildArch:      noarch
Group:          Applications/System
Source0:        jboss-eap-%{version}.zip
Source1:        %{name}-mod_cluster-listener.patch
Source2:        %{name}-mod_cluster-service.patch
Source3:        %{name}-jvm-route.patch
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
install -d -m 755 $RPM_BUILD_ROOT/opt/jbos-eap-%{version}/jboss-as/server/cluster-ec2
install -d -m 755 $RPM_BUILD_ROOT/opt/jbos-eap-%{version}/jboss-as/server/cluster
install -d -m 755 $RPM_BUILD_ROOT/opt/jbos-eap-%{version}/jboss-as/server/group

# copy profiles
cp -R jboss-eap-%{eap_major_version}/jboss-as/server/default/* $RPM_BUILD_ROOT/opt/jbos-eap-%{version}/jboss-as/server/group/
cp -R jboss-eap-%{eap_major_version}/jboss-as/server/production/* $RPM_BUILD_ROOT/opt/jbos-eap-%{version}/jboss-as/server/cluster/
cp -R jboss-eap-%{eap_major_version}/jboss-as/server/production/* $RPM_BUILD_ROOT/opt/jbos-eap-%{version}/jboss-as/server/cluster-ec2/

# install mod_cluster
cp -R jboss-eap-%{eap_major_version}/mod_cluster/mod-cluster.sar $RPM_BUILD_ROOT/opt/jbos-eap-%{version}/jboss-as/server/group/deploy/
cp -R jboss-eap-%{eap_major_version}/mod_cluster/mod-cluster.sar $RPM_BUILD_ROOT/opt/jbos-eap-%{version}/jboss-as/server/cluster/deploy/
cp -R jboss-eap-%{eap_major_version}/mod_cluster/mod-cluster.sar $RPM_BUILD_ROOT/opt/jbos-eap-%{version}/jboss-as/server/cluster-ec2/deploy/

cd $RPM_BUILD_ROOT/opt/jbos-eap-%{version}
patch -p1 < %{SOURCE3}
patch -p1 < %{SOURCE1}
patch -p1 < %{SOURCE2}

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,jboss-eap,jboss-eap)
/

%changelog
* Thu Dec 03 2009 Marek Goldmann 5.0.1-1
- Initial release
