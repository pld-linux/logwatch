# TODO:
# - prepare cron-job to generate not only e-mail, but html (like calamaris) too
# - choice in cron-jol: html, html-embed or clean text
%include	/usr/lib/rpm/macros.perl
Summary:	Analyzes system logs
Summary(pl):	Logwatch - analizator log�w systemowych
Name:		logwatch
Version:	6.0
Release:	0.pre.1.3
License:	MIT
Group:		Applications/System
#Source0:	ftp://ftp.logwatch.org/pub/linux/%{name}-%{version}.tar.gz
#Path for pre-versions:
Source0:	ftp://ftp.kaybee.org/pub/beta/linux/%{name}-pre%{version}.tar.gz
# Source0-md5:	591d6e4480db79d5a2f9f397bbf565eb
Source1:	%{name}-saslauthd
Source2:	%{name}-saslauthd.conf
Source3:	http://www.stellarcore.net/downloads/mailscanner
# Source3-md5:	d79724b0f5373b135770f3a8be23d58f
Patch0:		%{name}-config.patch
Patch1:		%{name}-log_conf.patch
Patch2:		%{name}-postfix.patch
Patch3:		%{name}-http.patch
Patch4:		%{name}-zz-disk_space.patch
Patch5:		%{name}-pam_unix.patch
Patch6:		%{name}-sshd.patch
Patch7:		%{name}-pop3.patch
Patch8:		%{name}-amavisd-new-log_format.patch
Patch9:		%{name}-postfix_verbosity.patch
Patch10:	%{name}-postfix-revDNS.patch
Patch11:	%{name}-pam_unix.conf.patch
Patch12:	%{name}-secure.patch
Patch13:	%{name}-secure.conf.patch
Patch14:	%{name}-pop3.conf.patch
Patch15:	%{name}-proftpd-messages.patch
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
analizowania log�w systemowych i przesy�aniu ich po wst�pnej obr�bce
poczt� elektroniczn� do administratora systemu. Logwatch jest �atwy w
u�yciu i mo�e pracowa� na wi�kszo�ci system�w.

%prep
%setup -q -n %{name}-pre%{version}
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p1
%patch10 -p1
%patch11 -p0
%patch12 -p0
%patch13 -p0
%patch14 -p0
%patch15 -p0

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

# saslauthd:
install %{SOURCE1} $RPM_BUILD_ROOT%{_logwatchdir}/scripts/services/saslauthd
install %{SOURCE2} $RPM_BUILD_ROOT%{_logwatchconf}/services/saslauthd.conf

# mailscanner:
install %{SOURCE3} $RPM_BUILD_ROOT%{_logwatchdir}/scripts/services/

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
%attr(750,root,root) %dir %{_logwatchconf}
%attr(750,root,root) %dir %{_logwatchconf}/logfiles
%attr(750,root,root) %dir %{_logwatchconf}/services
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/logwatch.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/services/*.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/logfiles/*.conf

%attr(755,root,root) %{_logwatchdir}

%attr(755,root,root) %{_sbindir}/logwatch
%attr(755,root,root) /etc/cron.daily/00-logwatch
%{_mandir}/man8/*
