########################################
# Derived definitions
########################################
%define __check_files %{nil}
%define name pm_logconv
%define cluster cs
%define version 2.3
%define release 1
%define prefix /usr
%define instdir pm_logconv
%define ORGARCH %{name}-%{version}
# rpmbuild --with ...
%bcond_with upstart
%bcond_with systemd
#
#
Summary: Pacemaker and Corosync log converter
Name: %{name}-%{cluster}
Version: %{version}
Release: %{release}%{?dist}
Group: Applications
Source: %{name}-%{version}.tar.gz
License: GPL
Vendor: NIPPON TELEGRAPH AND TELEPHONE CORPORATION
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildRequires: make
BuildArch: noarch
Requires: python >= 2.4, python < 3.0
Requires: pacemaker >= 1.1.12
Requires: corosync >= 2.3.3

########################################
%description
Log message converter for Pacemaker and Corosync.

########################################
%prep
########################################
rm -rf $RPM_BUILD_ROOT

########################################
%setup -q
########################################

########################################
%build
########################################

########################################
%configure \
%{?with_upstart:--enable-upstart} \
%{?with_systemd:--enable-systemd}
########################################

########################################
%pre
########################################

########################################
%install
########################################
make DESTDIR=$RPM_BUILD_ROOT install

########################################
%clean
########################################
if
	[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ]
then
	rm -rf $RPM_BUILD_ROOT
fi
rm -rf $RPM_BUILD_DIR/%{ORGARCH}

########################################
%post
########################################
true
########################################
%preun
########################################
%if %{with systemd}
%systemd_preun pm_logconv.service
%endif
%if %{with upstart}
/sbin/initctl stop pm_logconv_init > /dev/null 2>&1 || :
%endif
########################################
%postun
########################################
true

########################################
%files
########################################
%defattr(-,root,root)
%dir /etc
%config /etc/pm_logconv.conf.sample
%config /etc/logrotate.d/pm_logconv
%dir %{prefix}/share/pacemaker/%{instdir}
%{prefix}/share/pacemaker/%{instdir}/pm_logconv.py
%{prefix}/share/pacemaker/%{instdir}/pm_logconv_rules.conf
%{?with_upstart:%attr (644, root, root) %{_sysconfdir}/init/pm_logconv_init.conf}
%{?with_systemd:%attr (644, root, root) %{_unitdir}/pm_logconv.service}

%changelog
* Mon Aug 25 2014 Yusuke Iida <yusk.iida@gmail.com> - 2.0
- support version
-    Pacemaker : 1.1.12 or more
-    Corosync  : 2.3.3 or more
