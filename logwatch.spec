Summary:    	Analyzes system logs 
Summary(pl): 	Logwatch - analizator logów systemowych
Name:        	logwatch
Version:     	3.1
Release:     	1
License:   	MIT
Group:       	Applications/System
Source:      	ftp://ftp.logwatch.org/pub/linux/%{name}-%{version}.tar.gz
URL:		http://www.logwatch.org/
Requires:    	perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Buildarch:   	noarch

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
for i in scripts/{shared/{onlycontains,remove},services/zz-fortune}; do
	mv -f $i $i.
	sed -e s/bash/sh/ $i. > $i
	rm -f $i.
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/log.d/ \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/etc/cron.daily 

cp -a scripts $RPM_BUILD_ROOT/etc/log.d/
cp -a conf $RPM_BUILD_ROOT/etc/log.d/

install logwatch.8 $RPM_BUILD_ROOT%{_mandir}/man8

ln -sf /etc/log.d/scripts/logwatch.pl $RPM_BUILD_ROOT/etc/log.d/logwatch 
ln -sf /etc/log.d/conf/logwatch.conf $RPM_BUILD_ROOT/etc/log.d/logwatch.conf 
ln -sf /etc/log.d/scripts/logwatch.pl $RPM_BUILD_ROOT/etc/cron.daily/00-logwatch 
ln -sf /etc/log.d/scripts/logwatch.pl $RPM_BUILD_ROOT%{_sbindir}/logwatch 


%post
echo
echo "You should take a look at /etc/log.d/logwatch.conf..."
echo "Especially the Detail entry..."
echo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc  README

%attr(700,root,root) %dir /etc/log.d
%attr(700,root,root) %dir /etc/log.d/conf
%attr(700,root,root) %dir /etc/log.d/scripts

%attr(700,root,root) %dir /etc/log.d/conf/logfiles
%attr(700,root,root) %dir /etc/log.d/conf/services

%attr(700,root,root) %dir /etc/log.d/scripts/logfiles
%attr(700,root,root) %dir /etc/log.d/scripts/services
%attr(700,root,root) %dir /etc/log.d/scripts/shared

%attr(700,root,root) %dir /etc/log.d/scripts/logfiles/*

%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/log.d/conf/logwatch.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/log.d/logwatch.conf

%attr(600,root,root) %config %verify(not size mtime md5) /etc/log.d/conf/services/*
%attr(600,root,root) %config %verify(not size mtime md5) /etc/log.d/conf/logfiles/*

%attr(700,root,root) /etc/log.d/scripts/logwatch.pl
%attr(700,root,root) %{_sbindir}/logwatch

%attr(700,root,root) /etc/log.d/scripts/shared/*
%attr(700,root,root) /etc/log.d/scripts/services/*
%attr(700,root,root) /etc/log.d/scripts/logfiles/*/*

%attr(700,root,root) /etc/log.d/logwatch

%attr(700,root,root) /etc/cron.daily/00-logwatch
%{_mandir}/man8/*
