Summary:     Analyzes system logs 
Name:        logwatch
Version:     1.1
Release:     2
Copyright:   GPL
Group:       Utilities/System
Source:      ftp://ftp.kaybee.org/pub/linux/%{name}-%{version}.tar.gz
Requires:    perl
Buildroot:   /tmp/%{name}-%{version}-root
Buildarch:   noarch
Summary(pl): Logwatch - analizator logów systemowych

%description
LogWatch is a customizable, pluggable log-monitoring system.  It will go
through your logs for a given period of time and make a report in the areas
that you wish with the detail that you wish.  Easy to use - works right out
of the package on almost all systems.

%description -l pl
Pakiet zawiera logwatch - program przeznaczony do automatycznego analizowania
logów systemowych i przesy³aniu ich po wstêpnjej obróbce poczt± elektroniczn± 
do administratora systemu. Logwatch jest ³atwy w u¿yciu i moze pracowaæ na 
wiêkszo¶ci systemów.

%prep
%setup -q

%build

%install
install -d $RPM_BUILD_ROOT/etc/log.d/scripts/{services,shared,logfiles/{messages,xferlog}}
install -d $RPM_BUILD_ROOT/etc/log.d/conf/{services,logfiles}
install -d $RPM_BUILD_ROOT/usr/{sbin,man/man8}
install -d $RPM_BUILD_ROOT/etc/cron.daily

install scripts/logwatch.pl $RPM_BUILD_ROOT/etc/log.d/scripts/logwatch.pl
install scripts/logfiles/xferlog/* $RPM_BUILD_ROOT/etc/log.d/scripts/logfiles/xferlog
install scripts/services/* $RPM_BUILD_ROOT/etc/log.d/scripts/services
install scripts/shared/* $RPM_BUILD_ROOT/etc/log.d/scripts/shared

install conf/logwatch.conf $RPM_BUILD_ROOT/etc/log.d/conf/logwatch.conf
install conf/logfiles/* $RPM_BUILD_ROOT/etc/log.d/conf/logfiles
install conf/services/* $RPM_BUILD_ROOT/etc/log.d/conf/services

install logwatch.8 $RPM_BUILD_ROOT/usr/man/man8

bzip2 -9 $RPM_BUILD_ROOT/usr/man/man8/*

rm -f $RPM_BUILD_ROOT/etc/log.d/logwatch 
rm -f $RPM_BUILD_ROOT/etc/log.d/logwatch.conf 
rm -f $RPM_BUILD_ROOT/etc/cron.daily/00-logwatch 
rm -f $RPM_BUILD_ROOT/usr/sbin/logwatch

ln -sf /etc/log.d/scripts/logwatch.pl $RPM_BUILD_ROOT/etc/log.d/logwatch 
ln -sf /etc/log.d/conf/logwatch.conf $RPM_BUILD_ROOT/etc/log.d/logwatch.conf 
ln -sf /etc/log.d/scripts/logwatch.pl $RPM_BUILD_ROOT/etc/cron.daily/00-logwatch 
ln -sf /etc/log.d/scripts/logwatch.pl $RPM_BUILD_ROOT/usr/sbin/logwatch 

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo
echo "You should take a look at /etc/log.d/logwatch.conf..."
echo "Especially the Detail entry..."
echo

%files
%defattr(644,root,root,755)
%doc README

%attr(700,root,root) %dir /etc/log.d
%attr(700,root,root) %dir /etc/log.d/conf
%attr(700,root,root) %dir /etc/log.d/scripts
%attr(700,root,root) %dir /etc/log.d/conf/logfiles
%attr(700,root,root) %dir /etc/log.d/conf/services
%attr(700,root,root) %dir /etc/log.d/scripts/logfiles
%attr(700,root,root) %dir /etc/log.d/scripts/services
%attr(700,root,root) %dir /etc/log.d/scripts/shared
%attr(700,root,root) %dir /etc/log.d/scripts/logfiles/messages
%attr(700,root,root) %dir /etc/log.d/scripts/logfiles/xferlog

%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/log.d/conf/logwatch.conf
%attr(600,root,root) %config /etc/log.d/conf/services/*
%attr(600,root,root) %config /etc/log.d/conf/logfiles/*
%attr(700,root,root) /etc/log.d/scripts/logwatch.pl
%attr(700,root,root) /usr/sbin/logwatch
%attr(700,root,root) %config /etc/log.d/scripts/shared/*
%attr(700,root,root) %config /etc/log.d/scripts/services/*
%attr(700,root,root) %config /etc/log.d/scripts/logfiles/xferlog/*
%attr(700,root,root) /etc/log.d/logwatch
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/log.d/logwatch.conf
%attr(700,root,root) /etc/cron.daily/00-logwatch
%attr(644,root, man) /usr/man/man8/*
