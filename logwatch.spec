%include	/usr/lib/rpm/macros.perl
Summary:	Analyzes system logs
Summary(pl.UTF-8):	Logwatch - analizator logów systemowych
Name:		logwatch
Version:	7.4.3
Release:	3
License:	MIT
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/logwatch/%{name}-%{version}.tar.gz
# Source0-md5:	22bd22841caa45f12c605abc3e0c2b09
# https://po2.uni-stuttgart.de/~rusjako/logwatch/default.html
Source1:	https://po2.uni-stuttgart.de/~rusjako/logwatch/%{name}-syslog-ng.tar.gz
# Source1-md5:	2f834407b85080e8e6556d6182d245aa
Source2:	%{name}.sysconfig
Source3:	%{name}-cron.sh
Source4:	%{name}.cron
Source5:	%{name}.tmpwatch
Patch0:		%{name}-log_conf.patch
Patch1:		%{name}-archives.patch
Patch2:		%{name}-exim.patch
Patch3:		%{name}-journald-source.patch
Patch4:		%{name}-journal.patch
Patch5:		%{name}-postfix.patch
Patch6:		%{name}-secure-userhelper.patch
Patch7:		%{name}-sshd.patch
Patch8:		%{name}-sshd-2.patch
Patch9:		%{name}-vsftpd.patch
Patch10:	%{name}-dovecot.patch
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
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_logwatchconf}/{conf,scripts},/etc/{cron.d,sysconfig,tmpwatch}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},%{_logwatchdir}/{lib,default.conf},/var/cache/logwatch}

cp -p conf/logwatch.conf $RPM_BUILD_ROOT%{_logwatchconf}/conf
cp -p conf/logwatch.conf $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
cp -p conf/ignore.conf $RPM_BUILD_ROOT%{_logwatchconf}/conf
cp -p conf/ignore.conf $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
touch $RPM_BUILD_ROOT%{_logwatchconf}/conf/override.conf
# Where to put it The Right Way(TM)?
cp -p lib/Logwatch.pm $RPM_BUILD_ROOT%{_logwatchdir}/lib

cp -a conf/html $RPM_BUILD_ROOT%{_logwatchconf}/conf
cp -a conf/html $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
cp -a conf/services $RPM_BUILD_ROOT%{_logwatchconf}/conf
cp -a conf/services $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
cp -a conf/logfiles $RPM_BUILD_ROOT%{_logwatchconf}/conf
cp -a conf/logfiles $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
cp -a scripts $RPM_BUILD_ROOT%{_logwatchdir}
cp -p logwatch-syslog-ng/syslog-ng.conf $RPM_BUILD_ROOT%{_logwatchconf}/conf/services
cp -p logwatch-syslog-ng/syslog-ng $RPM_BUILD_ROOT%{_logwatchdir}/scripts/services

mv $RPM_BUILD_ROOT%{_logwatchdir}/scripts/logwatch.pl $RPM_BUILD_ROOT%{_sbindir}/logwatch

ln -sf %{_sbindir}/logwatch $RPM_BUILD_ROOT%{_logwatchdir}/scripts/logwatch.pl

install -p %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}/logwatch-cron
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/cron.d/logwatch
cp -p %{SOURCE5} $RPM_BUILD_ROOT/etc/tmpwatch/%{name}.conf
cp -p logwatch.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -p logwatch.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
cp -p override.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
cp -p ignore.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5

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
%doc README HOWTO-*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/tmpwatch/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/logwatch
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_logwatchconf}/conf/ignore.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_logwatchconf}/conf/logwatch.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_logwatchconf}/conf/override.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_logwatchconf}/conf/html/*.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_logwatchconf}/conf/logfiles/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_logwatchconf}/conf/services/*.conf
%attr(750,root,root) %dir %{_logwatchconf}
%attr(750,root,root) %dir %{_logwatchconf}/conf
%attr(750,root,root) %dir %{_logwatchconf}/conf/html
%attr(750,root,root) %dir %{_logwatchconf}/conf/logfiles
%attr(750,root,root) %dir %{_logwatchconf}/conf/services
%attr(750,root,root) %dir %{_logwatchconf}/scripts
%{_logwatchdir}
%attr(755,root,root) %{_sbindir}/logwatch
%attr(755,root,root) %{_sbindir}/logwatch-cron
%attr(750,root,root) %dir /var/cache/logwatch
%{_mandir}/man[58]/*
