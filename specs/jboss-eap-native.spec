%define eap_major_version 5.0
%define eap_user jboss-eap
%define arch i386

%ifarch x86_64
    %define arch x86_64
%endif

Summary:            JBoss Enterprise Application Platform native libraries
Name:               jboss-eap-native
Version:            5.0.1
Release:            1
License:            LGPL
Group:              Applications/System
Source0:            %{name}-%{version}-RHEL5-%{arch}.zip

Requires(build):    unzip
Requires(pre):      jboss-eap
Requires(post):     /sbin/chkconfig
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
JBoss Enterprise Application Platform (JBoss EAP) is the market-leading, open source enterprise Java platform for developing and deploying innovative and scalable Java applications. Combining a robust, yet flexible, architecture with an open source software license, JBoss EAP has become the most popular middleware system for developers, independent software vendors (ISVs), and enterprises alike. 

%prep
rm -rf %{name}-%{eap_major_version}
unzip -q %{SOURCE0} -d %{name}-%{eap_major_version}

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/jboss-eap-%{version}
cp -R %{name}-%{eap_major_version}/jboss-eap-%{eap_major_version}/* $RPM_BUILD_ROOT/opt/jboss-eap-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{eap_user},%{eap_user})
/

%changelog
* Tue May 24 2010 Marek Goldmann 5.0.1-1
- Initial release
