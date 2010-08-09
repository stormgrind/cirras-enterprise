Summary:            PostgreSQL support for JBoss EAP
Name:               jboss-eap-local-ds-helper
Version:            5.1.0.Beta
Release:            20100727
License:            LGPL
Group:              Applications/System
BuildArch:          noarch
Source0:            %{name}.init

Requires:           postgresql-server

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
JBoss Enterprise Application Platform (JBoss EAP) is the market-leading, open source enterprise Java platform for developing and deploying innovative and scalable Java applications. Combining a robust, yet flexible, architecture with an open source software license, JBoss EAP has become the most popular middleware system for developers, independent software vendors (ISVs), and enterprises alike. 

%install
install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE0} $RPM_BUILD_ROOT%{_initrddir}/%{name}

%post
/sbin/chkconfig --add %{name}

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/

%changelog
* Wed Jul 28 2010 Marek Goldmann 5.1.0.Beta-20100727
- Initial release
