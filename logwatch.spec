%include	/usr/lib/rpm/macros.perl
Summary:	Analyzes system logs
Summary(pl):	Logwatch - analizator logów systemowych
Name:		logwatch
Version:	5.1
Release:	0.pre.16
License:	MIT
Group:		Applications/System
#Source0:	ftp://ftp.logwatch.org/pub/linux/%{name}-%{version}.tar.gz
Source0:	ftp://ftp.kaybee.org/pub/beta/linux/%{name}-pre%{version}.tar.gz
# Source0-md5:	7939ffc153261984d028bb3e56882412
Source1:	shaperd
Source2:	shaperd.conf
Source3:	oidentd
Source4:	%{name}-oidentd.conf
Patch0:		%{name}-config.patch
Patch1:		%{name}-log_conf.patch
Patch2:		%{name}-sshd.patch
Patch3:		%{name}-sendmail.patch
Patch4:		%{name}-secure.patch
Patch5:		%{name}-samba.patch
Patch6:		%{name}-postfix.patch
Patch7:		%{name}-http.patch
Patch8:		%{name}-pam_unix.patch
Patch9:		%{name}-modprobe.patch
Patch10:	%{name}-pureftpd.patch
Patch11:	%{name}-cron.patch
Patch12:	%{name}-named.patch
Patch13:	%{name}-courier.patch
Patch14:	%{name}-proftpd-messages.patch
URL:		http://www.logwatch.org/
BuildRequires:	rpm-perlprov
Requires:	perl-modules
Requires:	smtpdaemon
Requires:	crondaemon
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
analizowania logów systemowych i przesy³aniu ich po wstêpnjej obróbce
poczt± elektroniczn± do administratora systemu. Logwatch jest ³atwy w
u¿yciu i moze pracowaæ na wiêkszo¶ci systemów.

%prep
%setup -q -n %{name}-pre%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p0
%patch10 -p0
%patch11 -p0
%patch12 -p0
%patch13 -p0
%patch14 -p0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_logwatchconf},/etc/cron.daily} \
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
ln -sf %{_sbindir}/logwatch $RPM_BUILD_ROOT/etc/cron.daily/00-logwatch

install logwatch.8 $RPM_BUILD_ROOT%{_mandir}/man8

install %{SOURCE1} $RPM_BUILD_ROOT%{_logwatchdir}/scripts/services/
install %{SOURCE3} $RPM_BUILD_ROOT%{_logwatchdir}/scripts/services/
install %{SOURCE2} $RPM_BUILD_ROOT%{_logwatchconf}/services/
install %{SOURCE4} $RPM_BUILD_ROOT%{_logwatchconf}/services/oidentd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# needed for smooth upgrade from < 4.3.2 package
if [ -d /etc/log.d/conf ]; then
	mv -f /etc/log.d/conf/logwatch.conf* /etc/log.d/
	mv -f /etc/log.d/conf/services /etc/log.d/
	mv -f /etc/log.d/conf/logfiles /etc/log.d/
fi

%post
echo "You should take a look at /etc/log.d/logwatch.conf..."
echo "Especially the Detail entry..."

%files
%defattr(644,root,root,755)
%doc README HOWTO-Make-Filter project/{CHANGES,TODO}
%attr(700,root,root) %dir %{_logwatchconf}
%attr(700,root,root) %dir %{_logwatchdir}
%attr(700,root,root) %dir %{_logwatchdir}/scripts

%attr(700,root,root) %dir %{_logwatchconf}/logfiles
%attr(700,root,root) %dir %{_logwatchconf}/services

%attr(700,root,root) %dir %{_logwatchdir}/scripts/services
%attr(700,root,root) %dir %{_logwatchdir}/scripts/shared
%attr(700,root,root) %dir %{_logwatchdir}/scripts/logfiles
%attr(700,root,root) %dir %{_logwatchdir}/scripts/logfiles/autorpm
%attr(700,root,root) %dir %{_logwatchdir}/scripts/logfiles/cron
%attr(700,root,root) %dir %{_logwatchdir}/scripts/logfiles/samba
%attr(700,root,root) %dir %{_logwatchdir}/scripts/logfiles/up2date
%attr(700,root,root) %dir %{_logwatchdir}/scripts/logfiles/xferlog
%attr(700,root,root) %dir %{_logwatchdir}/lib

%attr(700,root,root) %{_logwatchdir}/scripts/shared/*
%attr(700,root,root) %{_logwatchdir}/scripts/services/*
%attr(700,root,root) %{_logwatchdir}/scripts/logfiles/*/*
%attr(700,root,root) %{_logwatchdir}/scripts/logwatch.pl

%attr(600,root,root) %{_logwatchdir}/lib/*.pm

%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/logwatch.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/services/*.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/logfiles/*.conf

%attr(700,root,root) %{_sbindir}/logwatch
%attr(700,root,root) /etc/cron.daily/00-logwatch
%{_mandir}/man8/*
