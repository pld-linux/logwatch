%include	/usr/lib/rpm/macros.perl
Summary:	Analyzes system logs
Summary(pl):	Logwatch - analizator logów systemowych
Name:		logwatch
Version:	6.0.1
Release:	20050422.2
License:	MIT
Group:		Applications/System
Source0:	http://mieszkancy.ds.pg.gda.pl/~blues/SOURCES/%{name}-20050422.tar.bz2
# Source0-md5:	b74d162259d1fe2870d17b977576ef8a
# Path for stable versions:
#Source0:	ftp://ftp.logwatch.org/pub/linux/%{name}-%{version}.tar.gz
# Path for pre-versions:
#Source0:	ftp://ftp.kaybee.org/pub/beta/linux/%{name}-pre%{version}.tar.gz
Source1:	%{name}.cron
Source2:	%{name}.sysconfig
Source3:	http://www.blues.gda.pl/%{name}-zz-network-0.12.tar.gz
# Source3-md5:	1938dd3a5f037a439adb35961d849a1f
Patch0:		%{name}-config.patch
Patch1:		%{name}-log_conf.patch
Patch2:		%{name}-secure.patch
Patch3:		%{name}-http.patch
Patch4:		%{name}-postfix.patch
Patch5:		%{name}-sendmail.patch
URL:		http://www.logwatch.org/
BuildRequires:	rpm-perlprov
Requires:	crondaemon
Requires:	gawk
Requires:	perl-modules
Requires:	smtpdaemon
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_logwatchdir	%{_datadir}/logwatch
%define		_logwatchconf	%{_sysconfdir}/log.d

%description
LogWatch is a customizable, pluggable log-monitoring system. It will
go through your logs for a given period of time and make a report in
the areas that you wish with the detail that you wish. Easy to use -
works right out of the package on almost all systems.

%description -l pl
Pakiet zawiera logwatch - program przeznaczony do automatycznego
analizowania logów systemowych i przesy³aniu ich po wstêpnej obróbce
poczt± elektroniczn± do administratora systemu. Logwatch jest ³atwy w
u¿yciu i mo¿e pracowaæ na wiêkszo¶ci systemów.

%prep
%setup -q -n %{name} -a3
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0

find -name '*~' | xargs rm || exit 0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_logwatchconf},/etc/{cron.daily,sysconfig}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_logwatchdir}/lib}

install conf/logwatch.conf $RPM_BUILD_ROOT%{_logwatchconf}
# Where to put it The Right Way(TM)?
install lib/Logwatch.pm $RPM_BUILD_ROOT%{_logwatchdir}/lib

cp -a conf/services $RPM_BUILD_ROOT%{_logwatchconf}
cp -a conf/logfiles $RPM_BUILD_ROOT%{_logwatchconf}
cp -a scripts $RPM_BUILD_ROOT%{_logwatchdir}

mv $RPM_BUILD_ROOT%{_logwatchdir}/scripts/logwatch.pl $RPM_BUILD_ROOT%{_sbindir}/logwatch

ln -sf %{_sbindir}/logwatch $RPM_BUILD_ROOT%{_logwatchdir}/scripts/logwatch.pl
ln -sf %{_sbindir}/logwatch $RPM_BUILD_ROOT%{_logwatchconf}/logwatch

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/00-%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install logwatch.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# needed for smooth upgrade from < 4.3.2 package
if [ -d /etc/log.d/conf ]; then
	mv -f /etc/log.d/conf/logwatch.conf* /etc/log.d/
	mv -f /etc/log.d/conf/services /etc/log.d/
	mv -f /etc/log.d/conf/logfiles /etc/log.d/
fi

%files
%defattr(644,root,root,755)
%doc README HOWTO-Make-Filter project/{CHANGES,TODO}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}
%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) /etc/cron.daily/00-%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/logwatch.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/services/*.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/logfiles/*.conf
%attr(750,root,root) %dir %{_logwatchconf}
%attr(750,root,root) %dir %{_logwatchconf}/logfiles
%attr(750,root,root) %dir %{_logwatchconf}/services
%attr(755,root,root) %{_logwatchdir}
%attr(755,root,root) %{_sbindir}/logwatch
%{_mandir}/man8/*
