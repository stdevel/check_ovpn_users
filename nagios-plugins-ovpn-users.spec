Name:           nagios-plugins-ovpn-users
Version:        0.5.0
Release:        1%{?dist}
Summary:        A Nagios / Icinga plugin for checking the amount of connected OpenVPN users

Group:          Applications/System
License:        GPL
URL:            https://github.com/stdevel/check_ovpn_users
Source0:        nagios-plugins-ovpn-users-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:
Requires:       Python(logging)

%description
This package contains a Nagios / Icinga plugin for checking the amount of connected OpenVPN users.

Check out the GitHub page for further information: https://github.com/stdevel/check_ovpn_users

%prep
%setup -q

%build
#change /usr/lib64 to /usr/lib if we're on i686
%ifarch i686
sed -i -e "s/usr\/lib64/usr\/lib/" check_ovpn_users.cfg
%endif

%install
install -m 0755 -d %{buildroot}%{_libdir}/nagios/plugins/
install -m 0755 check_ovpn_users.py %{buildroot}%{_libdir}/nagios/plugins/check_ovpn_users
%if 0%{?el7}
        install -m 0755 -d %{buildroot}%{_sysconfdir}/nrpe.d/
        install -m 0755 check_ovpn_users.cfg  %{buildroot}%{_sysconfdir}/nrpe.d/check_ovpn_users.cfg
%else
        install -m 0755 -d %{buildroot}%{_sysconfdir}/nagios/plugins.d/
        install -m 0755 check_ovpn_users.cfg  %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_ovpn_users.cfg
%endif



%clean
rm -rf $RPM_BUILD_ROOT

%files
%if 0%{?el7}
        %config %{_sysconfdir}/nrpe.d/check_ovpn_users.cfg
%else
        %config %{_sysconfdir}/nagios/plugins.d/check_ovpn_users.cfg
%endif
%{_libdir}/nagios/plugins/check_ovpn_users


%changelog
* Fri Jan 5 2018 Christian Stankowic <info@cstan.io> - 0.5.0-1
- First release
