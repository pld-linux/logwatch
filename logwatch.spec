%include	/usr/lib/rpm/macros.perl
Summary:	Analyzes system logs
Summary(pl):	Logwatch - analizator logów systemowych
Name:		logwatch
Version:	5.1
Release:	0.pre.8
License:	MIT
Group:		Applications/System
#Source0:	ftp://ftp.logwatch.org/pub/linux/%{name}-%{version}.tar.gz
Source0:	ftp://ftp.kaybee.org/pub/beta/linux/%{name}-pre%{version}.tar.gz
# Source0-md5:	7939ffc153261984d028bb3e56882412
Source1:	http://piorun.ds.pg.gda.pl/~blues/patches/clam-update-1.0.tar.gz
# Source1-md5:	d92959cfa650ccce908721cbbe4fd6ef
Patch0:		%{name}-config.patch
Patch1:		%{name}-log_conf.patch
Patch2:		%{name}-sshd.patch
Patch3:		%{name}-sendmail.patch
Patch4:		%{name}-secure.patch
Patch5:		%{name}-samba.patch
URL:		http://www.logwatch.org/
BuildRequires:	rpm-perlprov
Requires:	perl-modules
Requires:	smtpdaemon
Requires:	crondaemon
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q -a1 -n %{name}-pre%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/log.d/,/etc/cron.daily} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_datadir}/logwatch/lib}

install conf/logwatch.conf $RPM_BUILD_ROOT%{_sysconfdir}/log.d
# Where to put it The Right Way(TM)?
install lib/Logwatch.pm $RPM_BUILD_ROOT%{_datadir}/logwatch/lib

cp -a conf/services $RPM_BUILD_ROOT%{_sysconfdir}/log.d
cp -a conf/logfiles $RPM_BUILD_ROOT%{_sysconfdir}/log.d
cp -a scripts $RPM_BUILD_ROOT%{_datadir}/logwatch

mv $RPM_BUILD_ROOT%{_datadir}/logwatch/scripts/logwatch.pl $RPM_BUILD_ROOT%{_sbindir}/logwatch

ln -sf %{_sbindir}/logwatch $RPM_BUILD_ROOT%{_datadir}/logwatch/scripts/logwatch.pl
ln -sf %{_sbindir}/logwatch $RPM_BUILD_ROOT%{_sysconfdir}/log.d/logwatch
ln -sf %{_sbindir}/logwatch $RPM_BUILD_ROOT/etc/cron.daily/00-logwatch

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

%post
echo "You should take a look at /etc/log.d/logwatch.conf..."
echo "Especially the Detail entry..."

%files
%defattr(644,root,root,755)
%doc README HOWTO-Make-Filter project/{CHANGES,TODO}
%attr(700,root,root) %dir %{_sysconfdir}/log.d
%attr(700,root,root) %dir %{_datadir}/logwatch/
%attr(700,root,root) %dir %{_datadir}/logwatch/scripts

%attr(700,root,root) %dir %{_sysconfdir}/log.d/logfiles
%attr(700,root,root) %dir %{_sysconfdir}/log.d/services

%attr(700,root,root) %dir %{_datadir}/logwatch/scripts/services
%attr(700,root,root) %dir %{_datadir}/logwatch/scripts/shared
%attr(700,root,root) %dir %{_datadir}/logwatch/scripts/logfiles
%attr(700,root,root) %dir %{_datadir}/logwatch/scripts/logfiles/autorpm
%attr(700,root,root) %dir %{_datadir}/logwatch/scripts/logfiles/cron
%attr(700,root,root) %dir %{_datadir}/logwatch/scripts/logfiles/samba
%attr(700,root,root) %dir %{_datadir}/logwatch/scripts/logfiles/up2date
%attr(700,root,root) %dir %{_datadir}/logwatch/scripts/logfiles/xferlog
%attr(700,root,root) %dir %{_datadir}/logwatch/lib

%attr(700,root,root) %{_datadir}/logwatch/scripts/shared/*
%attr(700,root,root) %{_datadir}/logwatch/scripts/services/*
%attr(700,root,root) %{_datadir}/logwatch/scripts/logfiles/*/*
%attr(700,root,root) %{_datadir}/logwatch/scripts/logwatch.pl

%attr(600,root,root) %{_datadir}/logwatch/lib/*.pm

%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/log.d/logwatch.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/log.d/services/*.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/log.d/logfiles/*.conf

%attr(700,root,root) %{_sbindir}/logwatch
%attr(700,root,root) /etc/cron.daily/00-logwatch
%{_mandir}/man8/*
