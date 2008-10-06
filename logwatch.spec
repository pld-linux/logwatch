%include	/usr/lib/rpm/macros.perl
Summary:	Analyzes system logs
Summary(pl.UTF-8):	Logwatch - analizator logów systemowych
Name:		logwatch
Version:	7.3.6
Release:	3
License:	MIT
Group:		Applications/System
# Path for stable versions:
Source0:	ftp://ftp.logwatch.org/pub/linux/%{name}-%{version}.tar.gz
# Source0-md5:	937d982006b2a76a83edfcfd2e5a9d7d
# Path for pre-versions:
#Source0:	ftp://ftp.kaybee.org/pub/beta/linux/%{name}-pre%{version}.tar.gz
Source1:	%{name}.cron
Source2:	%{name}.sysconfig
Source3:	%{name}.tmpwatch
# https://po2.uni-stuttgart.de/~rusjako/logwatch/default.html
Source4:	https://po2.uni-stuttgart.de/~rusjako/logwatch/%{name}-syslog-ng.tar.gz
# Source4-md5:	491e353044e93d8c31484cff8f252a68
Patch0:		%{name}-log_conf.patch
Patch1:		%{name}-archives.patch
URL:		http://www.logwatch.org/
BuildRequires:	rpm-perlprov
Requires:	crondaemon
Requires:	gawk
Requires:	perl-modules
Requires:	smtpdaemon
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_logwatchdir	%{_datadir}/%{name}
%define		_logwatchconf	%{_sysconfdir}/%{name}

%description
LogWatch is a customizable, pluggable log-monitoring system. It will
go through your logs for a given period of time and make a report in
the areas that you wish with the detail that you wish. Easy to use -
works right out of the package on almost all systems.

%description -l pl.UTF-8
Pakiet zawiera logwatch - program przeznaczony do automatycznego
analizowania logów systemowych i przesyłaniu ich po wstępnej obróbce
pocztą elektroniczną do administratora systemu. Logwatch jest łatwy w
użyciu i może pracować na większości systemów.

%prep
%setup -q -a4
%patch0 -p1
%patch1 -p1

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_logwatchconf}/{conf,scripts},/etc/{cron.daily,sysconfig,tmpwatch}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_logwatchdir}/{lib,default.conf},/var/cache/logwatch}

install conf/logwatch.conf $RPM_BUILD_ROOT%{_logwatchconf}/conf
install conf/logwatch.conf $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
# Where to put it The Right Way(TM)?
install lib/Logwatch.pm $RPM_BUILD_ROOT%{_logwatchdir}/lib

cp -a conf/html $RPM_BUILD_ROOT%{_logwatchconf}/conf
cp -a conf/html $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
cp -a conf/services $RPM_BUILD_ROOT%{_logwatchconf}/conf
cp -a conf/services $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
cp -a conf/logfiles $RPM_BUILD_ROOT%{_logwatchconf}/conf
cp -a conf/logfiles $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
cp -a scripts $RPM_BUILD_ROOT%{_logwatchdir}
install syslog-ng.conf $RPM_BUILD_ROOT%{_logwatchconf}/conf/services
install syslog-ng $RPM_BUILD_ROOT%{_logwatchdir}/scripts/services

mv $RPM_BUILD_ROOT%{_logwatchdir}/scripts/logwatch.pl $RPM_BUILD_ROOT%{_sbindir}/logwatch

ln -sf %{_sbindir}/logwatch $RPM_BUILD_ROOT%{_logwatchdir}/scripts/logwatch.pl

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/0%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/tmpwatch/%{name}.conf

install logwatch.8 $RPM_BUILD_ROOT%{_mandir}/man8

# Cleanup junk:
rm $RPM_BUILD_ROOT%{_logwatchdir}/default.conf/services/pureftpd.conf.orig
rm $RPM_BUILD_ROOT%{_logwatchconf}/conf/services/pureftpd.conf.orig

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# needed for smooth upgrade from < 4.3.2 package
if [ -d /etc/log.d/conf ]; then
	mv -f /etc/log.d/conf/logwatch.conf* /etc/log.d/ || :
	mv -f /etc/log.d/conf/services /etc/log.d/ || :
	mv -f /etc/log.d/conf/logfiles /etc/log.d/ || :
# needed for smooth upgrade from < 7.0 package:
elif [ -d /etc/log.d ]; then
	echo "Moving configuration from /etc/log.d to /etc/logwatch/conf..."
	if [ ! -d /etc/logwatch/conf ]; then
		mkdir -p /etc/logwatch/conf
	fi
	mv -f /etc/log.d/logwatch.conf* /etc/logwatch/conf/ || :
	mv -f /etc/log.d/services /etc/logwatch/conf/ || :
	mv -f /etc/log.d/logfiles /etc/logwatch/conf/ || :
fi

%files
%defattr(644,root,root,755)
%doc README HOWTO-* project/{CHANGES,TODO}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/tmpwatch/%{name}.conf
%attr(755,root,root) /etc/cron.daily/0%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_logwatchconf}/conf/logwatch.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_logwatchconf}/conf/html/*.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_logwatchconf}/conf/logfiles/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_logwatchconf}/conf/services/*.conf
%attr(750,root,root) %dir %{_logwatchconf}
%attr(750,root,root) %dir %{_logwatchconf}/conf
%attr(750,root,root) %dir %{_logwatchconf}/conf/html
%attr(750,root,root) %dir %{_logwatchconf}/conf/logfiles
%attr(750,root,root) %dir %{_logwatchconf}/conf/services
%attr(750,root,root) %dir %{_logwatchconf}/scripts
%attr(755,root,root) %{_logwatchdir}
%attr(755,root,root) %{_sbindir}/logwatch
%attr(750,root,root) %dir /var/cache/logwatch
%{_mandir}/man8/*
