%define rhq_name jon-cli
%define cli_version 3.0.0.GA

Summary:        JON Helper
Name:           jon-helper
Version:        2.4.0.GA
Release:        1
License:        LGPL
BuildArch:      noarch
Source0:        rhq-cli-install.sh
Source1:        import-servers.js
Source2:        import-servers.sh
Source3:        ftp://ftp.mozilla.org/pub/mozilla.org/js/rhino1_7R2.zip
Source4:        http://scripting.dev.java.net/files/documents/4957/37592/jsr223-engines.tar.gz
Group:          Applications/System
Requires:       java-1.6.0-openjdk unzip wget cronie initscripts
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Helps with importing and configuring RHQ in CirrAS environment.

%prep
rm -rf rhino1_7R2
unzip -q %{SOURCE3}

rm -rf jsr223-engines
mkdir jsr223-engines
tar -C jsr223-engines -xf %{SOURCE4}

%install
install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "RHQ_CLI_VERSION=%{cli_version}"    > $RPM_BUILD_ROOT/etc/sysconfig/%{rhq_name}
echo "RHQ_CLI_HOME=/opt/%{rhq_name}-%{version}"    >> $RPM_BUILD_ROOT/etc/sysconfig/%{rhq_name}
echo "RHQ_CLI_USERNAME=rhqadmin"        >> $RPM_BUILD_ROOT/etc/sysconfig/%{rhq_name}
echo "RHQ_CLI_PASSWORD=rhqadmin"        >> $RPM_BUILD_ROOT/etc/sysconfig/%{rhq_name}
echo "RHQ_SERVER_PORT=7080"             >> $RPM_BUILD_ROOT/etc/sysconfig/%{rhq_name}

install -d -m 755 $RPM_BUILD_ROOT/usr/share/%{name}
install -d -m 755 $RPM_BUILD_ROOT/var/log/%{name}
install -m 744 %{SOURCE0} $RPM_BUILD_ROOT/usr/share/%{name}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/%{name}
install -m 744 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/%{name}

install -d -m 755 $RPM_BUILD_ROOT/usr/lib/jvm/jre-1.6.0/lib/ext/
cp rhino1_7R2/js.jar $RPM_BUILD_ROOT/usr/lib/jvm/jre-1.6.0/lib/ext/
cp jsr223-engines/javascript/build/js-engine.jar $RPM_BUILD_ROOT/usr/lib/jvm/jre-1.6.0/lib/ext/

%clean
rm -Rf $RPM_BUILD_ROOT

%post
echo "sh /usr/share/%{name}/rhq-cli-install.sh &" >> /etc/rc.local
echo '* * * * * /usr/share/%{name}/import-servers.sh >> /var/log/%{name}/import.log' | crontab -

%files
%defattr(-,root,root)
/

%changelog
* Fri May 05 2010 Marek Goldmann 3.0.0.B05
- Upgrade to upstream 3.0.0.B05 release

* Thu Feb 23 2010 Marek Goldmann 1.0.0.Beta2
- Version upgrade

* Thu Jan 28 2010 Marek Goldmann 1.0.0.Beta1
- Initial packaging
