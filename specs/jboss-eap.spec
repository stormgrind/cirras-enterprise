%define eap_major_version 5.1
%define eap_profile default
%define eap_user jboss

Summary:            JBoss Enterprise Application Platform
Name:               jboss-eap
Version:            5.1.0.Beta
Release:            20100808
License:            LGPL
Group:              Applications/System
BuildArch:          noarch
Source0:            %{name}-%{version}.zip
Source1:            %{name}.init
Requires(build):    unzip
Requires:           shadow-utils
Requires:           coreutils curl
Requires:           java-1.6.0-openjdk
Requires:           initscripts
Requires(post):     /sbin/chkconfig
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define runuser %{name}
%define __jar_repack %{nil}

%description
JBoss Enterprise Application Platform (JBoss EAP) is the market-leading, open source enterprise Java platform for developing and deploying innovative and scalable Java applications. Combining a robust, yet flexible, architecture with an open source software license, JBoss EAP has become the most popular middleware system for developers, independent software vendors (ISVs), and enterprises alike. 

%prep
rm -rf %{name}-%{eap_major_version}
unzip -q %{SOURCE0}

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/%{name}-%{version}
install -d -m 755 $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/tmp

cp -R %{name}-%{eap_major_version}/* $RPM_BUILD_ROOT/opt/%{name}-%{version}

# it caused adding bad requires for package
rm -rf $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/bin/jboss_init_solaris.sh

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "JBOSS_VERSION=%{version}"                         > $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "JBOSS_HOME=/opt/%{name}-\$JBOSS_VERSION/jboss-as" >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "JBOSS_CONFIG=%{eap_profile}"                      >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "JBOSS_TMP=\$JBOSS_HOME/tmp"                       >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}

chmod 600 $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -Rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r %{eap_user} 2>/dev/null || :
/usr/sbin/useradd -c "JBoss" -r -s /bin/bash -m -g %{eap_user} %{eap_user} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}
/sbin/chkconfig %{name} off
ln -s /etc/sysconfig/%{name} /home/jboss/.jboss

%files
%defattr(-,%{eap_user},%{eap_user})
/

%changelog
* Sun Aug 08 2010 Marek Goldmann 5.1.0.Beta-20100808
- Rebuild

* Tue Jul 27 2010 Marek Goldmann 5.1.0.Beta-20100727
- Upgrade to JBoss EAP 5.1.0.Beta

* Tue Jul 15 2010 Marek Goldmann 5.0.1-20100715
- Initial release
