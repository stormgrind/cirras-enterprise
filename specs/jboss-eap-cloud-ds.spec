%define eap_name jboss-eap
%define eap_profile cluster-ec2
%define mysql_connector_version 5.1.13

Summary:            Amazon RDS support for JBoss EAP
Name:               jboss-eap-cloud-ds
Version:            5.1.0.Beta
Release:            20100727
License:            LGPL
Group:              Applications/System
BuildArch:          noarch
Source0:            http://mirror.services.wisc.edu/mysql/Downloads/Connector-J/mysql-connector-java-%{mysql_connector_version}.tar.gz
Source1:            cloud-ds.xml

Requires:           jboss-eap-cloud-profiles

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define runuser %{name}
%define __jar_repack %{nil}

%description
JBoss Enterprise Application Platform (JBoss EAP) is the market-leading, open source enterprise Java platform for developing and deploying innovative and scalable Java applications. Combining a robust, yet flexible, architecture with an open source software license, JBoss EAP has become the most popular middleware system for developers, independent software vendors (ISVs), and enterprises alike.

%prep
%setup -n mysql-connector-java-%{mysql_connector_version}

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/%{eap_name}-%{version}/jboss-as/server/%{eap_profile}/lib/
install -d -m 755 $RPM_BUILD_ROOT/opt/%{eap_name}-%{version}/jboss-as/server/%{eap_profile}/deploy/

cp mysql-connector-java-%{mysql_connector_version}-bin.jar $RPM_BUILD_ROOT/opt/%{eap_name}-%{version}/jboss-as/server/%{eap_profile}/lib/

install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/opt/%{eap_name}-%{version}/jboss-as/server/%{eap_profile}/deploy/

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,jboss,jboss)
/

%changelog
* Wed Jul 28 2010 Marek Goldmann 5.1.0.Beta-20100727
- Initial release
