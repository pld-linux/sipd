Summary:	SIP proxy, redirect and registrar server
Summary(pl):	Serwer SIP rejestruj±cy, przekierowuj±cy i robi±cy proxy
Name:		sipd
Version:	1.17
Release:	1
License:	commercial
Group:		Networking/Daemons
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
NoSource:	0
Patch0:		%{name}-shared_mysqllib.patch
Patch1:		%{name}-system_apps.patch
Patch2:		%{name}-fork.patch
URL:		http://www.cs.columbia.edu/IRT/cinema/
#BuildRequires:	autoconf
BuildRequires:	db3-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	tcl-devel
#BuildRequires:	xerces-c-devel
#BuildRequires:	automake
#BuildRequires:	libtool
#BuildRequires:	libwrap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webdir		/home/services/httpd/cgi-bin/sipd

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

%description -l pl
sipd jest serwerem SIP przekierowuj±cym, buforuj±cym i rejestruj±cym,
udostêpniaj±cym mapowanie nazw i us³ugi zwi±zane z lokalizowaniem
u¿ytkownika i skryptami. Mo¿e u¿ywaæ zewnêtrznych funkcji do
wykonywania w³a¶ciwego rozwi±zywania aliasów (w³±cznie z nazwami
grup), mapowania nazw i lokalizowania u¿ytkowników. sipd pozwala
tak¿e u¿ytkownikom na rejestrowanie na serwerze swojej aktualnej
lokalizacji. U¿ytkownicy mog± byæ zarejestrowani w wielu
lokalizacjach. Ka¿dy u¿ytkownik mo¿e zarejestrowaæ skrypt w dowolnym
jêzyku skryptowym lub formacie wykonywalnym rozumianym przez serwer;
skrypt ten bêdzie wykonywany po odebraniu po³±czenia. Interfejs
skryptowy jest zgodny z interfejsem SIP cgi-bin (RFC 3050).

%package cgi
Summary:	SIP proxy, redirect and registrar server
Summary(pl):	Serwer SIP rejestruj±cy, przekierowuj±cy i robi±cy proxy
Group:		Networking/Daemons
Requires:	%{name}-tools = %{version}
Requires:	cgi.tcl

%description cgi
cgi files for sipd.

%description cgi -l pl
Pliki cgi dla sipd.

%package tools
Summary:	SIP proxy, redirect and registrar server
Summary(pl):	Serwer SIP rejestruj±cy, przekierowuj±cy i robi±cy proxy
Group:		Networking/Daemons
Requires:	bind-utils

%description tools
tools for sipd.

%description tools -l pl
Narzêdzia dla sipd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# Change tclsh location in all web-files:
cd web
for i in *.cgi *.tcl; do
	sed -e "s/\/usr\/local\/bin/\/usr\/bin/" $i > $i.tmp
	mv -f $i.tmp $i
done
cd ..

#rm -f missing
#%%{__libtoolize}
#%%{__aclocal}
#%%{__autoconf}
#%%{__automake}
#cp %{_includedir}/mysql/mysql.h libcine
%configure2_13 \
	--with-db="%{_prefix}" \
	--with-ldap="%{_prefix}" \
	--with-mysql="%{_prefix}" \
	--with-tcl="/usr/lib/" \
	--with-tclincludes="/usr/include/"
#	--with-xerces=

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir},%{_sysconfdir}/{sipd,sysconfig,rc.d/init.d}}
install -d $RPM_BUILD_ROOT{/var/lib/sipd/logs,%{_webdir}}

install sipd/sipd $RPM_BUILD_ROOT%{_sbindir}
install sipd/sipd.conf $RPM_BUILD_ROOT%{_sysconfdir}/sipd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/sipd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/sipd
install sipd/gateways.sample $RPM_BUILD_ROOT%{_sysconfdir}/sipd
install tools/canonicalize/dialplan.sample $RPM_BUILD_ROOT%{_sysconfdir}/sipd

install tools/addsipuser/addsipuser $RPM_BUILD_ROOT%{_bindir}
install tools/base64/base64-{decode,encode} $RPM_BUILD_ROOT%{_bindir}
install tools/canonicalize/canonicalize $RPM_BUILD_ROOT%{_bindir}
# exists in 1.18
#install tools/canonicalize/libcanon.so $RPM_BUILD_ROOT%{_libdir}
install tools/fbsql/libfbsql.so $RPM_BUILD_ROOT%{_libdir}
install tools/ishere/ishere $RPM_BUILD_ROOT%{_bindir}
install tools/md5string/md5string $RPM_BUILD_ROOT%{_bindir}
install tools/random32/random32 $RPM_BUILD_ROOT%{_bindir}
install tools/sippasswd/sippasswd $RPM_BUILD_ROOT%{_bindir}
install tools/tracker/tracker $RPM_BUILD_ROOT%{_bindir}

rm -rf web/cgi1.4.3/
install web/* $RPM_BUILD_ROOT%{_webdir}

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
%doc README doc/*.{html,gif,css} sipd/{BUGS,README.*,TODO} scripts
%doc tools/{addsipuser/*.html,canonicalize/*.html,ishere/*.html,tracker/*.html}
%attr(755,root,root) %{_bindir}/base64-*
%attr(755,root,root) %{_bindir}/canonicalize
%attr(755,root,root) %{_bindir}/ishere
%attr(755,root,root) %{_bindir}/tracker
%attr(755,root,root) %{_sbindir}/*
# exists in 1.18
#%attr(755,root,root) %{_libdir}/libcanon.so
%dir %{_sysconfdir}/sipd
%config(noreplace) %{_sysconfdir}/sipd/sipd.conf
%config(noreplace) %{_sysconfdir}/sipd/gateways.sample
%config(noreplace) %{_sysconfdir}/sipd/dialplan.sample
%config(noreplace) /etc/sysconfig/sipd
%attr(754,root,root) /etc/rc.d/init.d/sipd
%dir /var/lib/sipd
%dir /var/lib/sipd/logs
/var/lib/sipd/gateways.sample

%files cgi
%defattr(644,root,root,755)
%config(noreplace) %{_webdir}/*.conf
%attr(755,root,root) %{_webdir}/*.cgi
%{_webdir}/*.html
%{_webdir}/*.tcl
%{_webdir}/*.gif
%{_webdir}/*.jpg
%{_webdir}/*.js
# this should be removed... later...
%{_webdir}/wordlist

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/addsipuser
%attr(755,root,root) %{_bindir}/md5string
%attr(755,root,root) %{_bindir}/random32
%attr(755,root,root) %{_bindir}/sippasswd
%attr(755,root,root) %{_libdir}/libfbsql.so
