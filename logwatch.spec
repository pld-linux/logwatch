%include	/usr/lib/rpm/macros.perl
Summary:	Analyzes system logs
Summary(pl):	Logwatch - analizator logów systemowych
Name:		logwatch
Version:	4.3.2
Release:	6
License:	MIT
Group:		Applications/System
Source0:	ftp://ftp.logwatch.org/pub/linux/%{name}-%{version}.tar.gz
# Source0-md5:	fdd2edb48c17f52ace9e2b00a3ac17f9
Source1:	http://www.jimohalloran.com/archives/files/patches030325.tar.gz
# Source1-md5:	20f356691c4bf48280f1a623b8b7d8a5
Patch0:		%{name}-more_features.patch
Patch1:		%{name}-dirs.patch
Patch2:		%{name}-init.patch
Patch3:		%{name}-sendmail_warning.patch
Patch4:		%{name}-pam_unix2.patch
Patch5:		%{name}-modprobe.patch
Patch6:		http://piorun.ds.pg.gda.pl/~blues/patches/%{name}-sendmail_detail.patch
URL:		http://www.logwatch.org/
BuildRequires:	rpm-perlprov
Requires:	perl-modules
Requires:	smtpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Buildarch:	noarch

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
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

cat in.qpopper.patch030319 | patch -p3
cat sendmail.conf.patch030319 | patch -p3
cat sendmail.patch030325 | patch -p3

%build
mv amavis.conf conf/services
mv amavis scripts/services
for i in scripts/{shared/{onlycontains,remove},services/zz-fortune}; do
	mv -f $i $i.
	sed -e s/bash/sh/ $i. > $i
	rm -f $i.
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/log.d/ \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_datadir}/logwatch} \
	$RPM_BUILD_ROOT/etc/cron.daily

install conf/logwatch.conf $RPM_BUILD_ROOT%{_sysconfdir}/log.d

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

%attr(700,root,root) %{_datadir}/logwatch/scripts/shared/*
%attr(700,root,root) %{_datadir}/logwatch/scripts/services/*
%attr(700,root,root) %{_datadir}/logwatch/scripts/logfiles/*/*
%attr(700,root,root) %{_datadir}/logwatch/scripts/logwatch.pl

%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/log.d/logwatch.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/log.d/services/*.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/log.d/logfiles/*.conf

%attr(700,root,root) %{_sbindir}/logwatch
%attr(700,root,root) /etc/cron.daily/00-logwatch
%{_mandir}/man8/*
