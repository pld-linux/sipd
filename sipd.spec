Summary:	SIP proxy, redirect and registrar server
Summary(pl):	Serwer SIP rejestruj±cy, przekierowuj±cy i robi±cy proxy
Name:		sipd
Version:	1.18
Release:	0.4
License:	commercial
Group:		Networking/Daemons
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.cs.columbia.edu/IRT/cinema/
BuildRequires:	autoconf
BuildRequires:	db3-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
#BuildRequires:	xerces-c-devel
#BuildRequires:	automake
#BuildRequires:	libtool
#BuildRequires:	libwrap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sipd is a SIP redirect, forking proxy and registration server that
provides name mapping, user location and scripting services. It can
use external routines to do the actual work of resolving aliases
(including group names), mapping names and locating users. It also
allows users to register their current location with the server. Users
can be registered at multiple locations. Each user can register a
script in any scripting language or executable format understood by
the server that will be executed when receiving a call. The scripting
interface conforms to the SIP cgi-bin interface (RFC 3050).

%prep
%setup -q

%build
#rm -f missing
#%{__libtoolize}
#%{__aclocal}
#%{__autoconf}
#%{__automake}
cp %{_includedir}/mysql/mysql.h libcine
%configure2_13 \
	--with-db="%{_prefix}" \
	--with-ldap="%{_prefix}" \
	--with-mysql="%{_prefix}"
#	--with-xerces=

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir},%{_sysconfdir}/{sipd,sysconfig,rc.d/init.d}}
install -d $RPM_BUILD_ROOT/var/lib/sipd/logs

install sipd/sipd $RPM_BUILD_ROOT%{_sbindir}
install sipd/sipd.conf $RPM_BUILD_ROOT%{_sysconfdir}/sipd
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/sipd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/sipd
install sipd/gateways.sample $RPM_BUILD_ROOT%{_sysconfdir}/sipd
install tools/canonicalize/dialplan.sample $RPM_BUILD_ROOT%{_sysconfdir}/sipd

install tools/addsipuser/addsipuser $RPM_BUILD_ROOT%{_bindir}
install tools/base64/base64-{decode,encode} $RPM_BUILD_ROOT%{_bindir}
install tools/canonicalize/canonicalize $RPM_BUILD_ROOT%{_bindir}
install tools/canonicalize/libcanon.so $RPM_BUILD_ROOT%{_libdir}
install tools/ishere/ishere $RPM_BUILD_ROOT%{_bindir}
install tools/md5string/md5string $RPM_BUILD_ROOT%{_bindir}
install tools/random32/random32 $RPM_BUILD_ROOT%{_bindir}
install tools/sippasswd/sippasswd $RPM_BUILD_ROOT%{_bindir}
install tools/tracker/tracker $RPM_BUILD_ROOT%{_bindir}

ln -s  %{_sysconfdir}/sipd/gateways.sample $RPM_BUILD_ROOT/var/lib/sipd/gateways.sample

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add sipd
if [ -f /var/lock/subsys/sipd ]; then
	etc/rc.d/init.d/sipd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/sipd start\" to start sip Daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/sipd ]; then
		/etc/rc.d/init.d/sipd stop 1>&2
fi
	/sbin/chkconfig --del sipd
fi

%files
%defattr(644,root,root,755)
%doc README doc/*.{txt,html,gif,css} sipd/{BUGS,README.*,TODO} scripts
%doc tools/{addsipuser/*.html,canonicalize/*.{html,txt},ishere/*.html,tracker/*.html}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*
%dir %{_sysconfdir}/sipd
%config(noreplace) %{_sysconfdir}/sipd/sipd.conf
%config(noreplace) %{_sysconfdir}/sipd/gateways.sample
%config(noreplace) %{_sysconfdir}/sipd/dialplan.sample
%config(noreplace) %{_sysconfdir}/sysconfig/sipd
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/sipd
%dir /var/lib/sipd
%dir /var/lib/sipd/logs
/var/lib/sipd/gateways.sample
