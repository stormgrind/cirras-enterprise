%define eap_major_version 5.1
%define ews_user jboss-ews
%define ews_version 1.0.1
%define ews_major_version 1.0
%define eap_name jboss-ep

%define arch i386

%ifarch x86_64
    %define arch x86_64
%endif

Summary:            JBoss Enterprise Application Platform native libraries
Name:               jboss-eap-native
Version:            5.1.0.Beta
Release:            20100808
License:            LGPL
Group:              Applications/System
Source0:            %{eap_name}-native-%{version}-RHEL5-%{arch}.zip
Source1:            mod_cluster.conf
Requires(build):    unzip
Requires(pre):      jboss-ews
Requires(post):     /sbin/chkconfig
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
JBoss Enterprise Application Platform (JBoss EAP) is the market-leading, open source enterprise Java platform for developing and deploying innovative and scalable Java applications. Combining a robust, yet flexible, architecture with an open source software license, JBoss EAP has become the most popular middleware system for developers, independent software vendors (ISVs), and enterprises alike. 

%prep
rm -rf %{name}-%{eap_major_version}
unzip -q %{SOURCE0} -d %{name}-%{eap_major_version}

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/jboss-ews-%{ews_version}/httpd/modules

# modules
cp -R %{name}-%{eap_major_version}/%{eap_name}-%{eap_major_version}/native/lib/httpd/modules/* $RPM_BUILD_ROOT/opt/jboss-ews-%{ews_version}/httpd/modules/

# not sure why there is mod_jk, in EWS is one too!
rm -f $RPM_BUILD_ROOT/opt/jboss-ews-%{ews_version}/httpd/modules/mod_jk.so

install -d -m 755 $RPM_BUILD_ROOT/opt/jboss-ews-%{ews_version}/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/opt/jboss-ews-%{ews_version}/httpd/conf.d/mod_cluster.conf

%post
sed -i s/"^LoadModule proxy_balancer_module"/"#LoadModule proxy_balancer_module"/ /opt/jboss-ews-%{ews_version}/httpd/conf/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{ews_user},%{ews_user})
/

%changelog
* Sun Aug 08 2010 Marek Goldmann 5.1.0.Beta-20100808
- Rebuild

* Tue May 24 2010 Marek Goldmann 5.0.1-1
- Initial release
