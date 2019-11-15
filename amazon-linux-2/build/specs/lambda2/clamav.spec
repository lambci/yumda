#global prerelease  rc1

## Fedora Extras specific customization below...
%if 0%{?fedora} || 0%{?rhel} > 6
%bcond_without  systemd
%bcond_without  tmpfiles
%bcond_with     sysv
%bcond_with     upstart
%else
%if 0%{?rhel} && 0%{?rhel} <= 6
%bcond_with     systemd
%bcond_with     tmpfiles
%bcond_without  sysv
%bcond_without  upstart
%else
%bcond_with     systemd
%bcond_with     tmpfiles
%bcond_without  sysv
%bcond_with     upstart
%endif
%endif
%bcond_with     unrar
%ifnarch ppc64
%bcond_without  llvm
%else
%bcond_with     llvm
%endif

##

%global _hardened_build 1

%ifnarch s390 s390x
%global have_ocaml  1
%else
%global have_ocaml  0
%endif

%{!?_rundir:%global _rundir /var/run}
%{!?_unitdir:%global _unitdir /lib/systemd/system}
%{!?_initrddir:%global _initrddir /etc/rc.d/init.d}

%global updateuser  clamupdate
%global homedir     %_var/lib/clamav
%global freshclamlog    %_var/log/freshclam.log
%global milteruser  clamilt
%global milterlog   %_var/log/clamav-milter.log
%global milterstatedir  %_rundir/clamav-milter
%global pkgdatadir  %_datadir/%name
%global scanuser    clamscan
%global scanstatedir    %_rundir/clamd.scan


Summary:    End-user tools for the Clam Antivirus scanner
Name:       clamav
Version:    0.101.4
Release:    1%{?dist}
License:    %{?with_unrar:proprietary}%{!?with_unrar:GPLv2}
URL:        https://www.clamav.net/
%if %{with unrar}
Source0:    https://www.clamav.net/downloads/production/%name-%version%{?prerelease}.tar.gz
Source999:  https://www.clamav.net/downloads/production/%name-%version%{?prerelease}.tar.gz.sig
%else
# Unfortunately, clamav includes support for RAR v3, derived from GPL
# incompatible unrar from RARlabs. We have to pull this code out.
# tarball was created by
#  make clean-sources NAME=clamav VERSION=<version> TARBALL=clamav-<version>.tar.gz TARBALL_CLEAN=clamav-<version>-norar.tar.xz
Source0:    %name-%version%{?prerelease}-norar.tar.xz
%endif
#for server
Source2:    clamd.sysconfig
Source3:    clamd.logrotate
Source5:    clamd-README
Source7:    clamd.SERVICE.init
# To download the *.cvd, go to https://www.clamav.net and use the links
# there (I renamed the files to add the -version suffix for verifying).
# Check the first line of the file for version or run file *cvd
# Attention file < 5.33-7 have bugs see https://bugzilla.redhat.com/show_bug.cgi?id=1539107
#http://database.clamav.net/main.cvd
Source10:   main-58.cvd
#http://database.clamav.net/daily.cvd
Source11:   daily-25550.cvd
#http://database.clamav.net/bytecode.cvd
Source12:   bytecode-330.cvd
#for devel
Source100:  clamd-gen
#for update
Source200:  freshclam-sleep
Source201:  freshclam.sysconfig
Source202:  clamav-update.crond
Source203:  clamav-update.logrotate
#for milter
Source300:  README.fedora
#for clamav-milter.upstart
Source310:  clamav-milter.upstart
#for milter-sysvinit
Source320:  clamav-milter.sysv
#for clamav-milter.systemd
Source330:  clamav-milter.systemd
#for scanner-upstart
Source410:  clamd.scan.upstart
#for scanner-systemd
Source430:  clamd@scan.service
#for server-sysvinit
Source520:  clamd-wrapper
#for server-systemd
Source530:  clamd@.service

Patch0:     clamav-0.100.0-stats-deprecation.patch
Patch1:     clamav-0.100.1-defaults_locations.patch
Patch24:    clamav-0.99-private.patch
Patch27:    clamav-0.100.0-umask.patch
# https://llvm.org/viewvc/llvm-project/llvm/trunk/lib/ExecutionEngine/JIT/Intercept.cpp?r1=128086&r2=137567
Patch30:    llvm-glibc.patch


BuildRequires:  autoconf automake gettext-devel libtool libtool-ltdl-devel
BuildRequires:  gcc-c++
BuildRequires:  zlib-devel bzip2-devel gmp-devel curl-devel json-c-devel
BuildRequires:  ncurses-devel openssl-devel libxml2-devel
BuildRequires:  pcre2-devel
#BuildRequires:  %%_includedir/tcpd.h
BuildRequires:  bc tcl groff graphviz
%{?have_ocaml:BuildRequires: ocaml}
# nc required for tests
BuildRequires: nc
%if %{with systemd}
%{?systemd_requires}
BuildRequires: systemd-devel
%endif
#for milter
BuildRequires:  sendmail-devel

Requires:   clamav-lib = %version-%release
Requires:   data(clamav)

%description
Clam AntiVirus is an anti-virus toolkit for UNIX. The main purpose of this
software is the integration with mail servers (attachment scanning). The
package provides a flexible and scalable multi-threaded daemon, a command
line scanner, and a tool for automatic updating via Internet. The programs
are based on a shared library distributed with the Clam AntiVirus package,
which you can use with your own software. The virus database is based on
the virus database from OpenAntiVirus, but contains additional signatures
(including signatures for popular polymorphic viruses, too) and is KEPT UP
TO DATE.

%package filesystem
Summary:    Filesystem structure for clamav
# Prevent version mix
Conflicts:  %name < %version-%release
Conflicts:  %name > %version-%release
Requires(pre):  shadow-utils
BuildArch:  noarch

%description filesystem
This package provides the filesystem structure and contains the
user-creation scripts required by clamav.


%package lib
Summary:    Dynamic libraries for the Clam Antivirus scanner
Requires:   data(clamav)
Provides:   bundled(libmspack) = 0.5-0.1.alpha.modified_by_clamav

%description lib
This package contains dynamic libraries shared between applications
using the Clam Antivirus scanner.


%package devel
Summary:    Header files and libraries for the Clam Antivirus scanner
Requires:   clamav-lib        = %version-%release
Requires:   clamav-filesystem = %version-%release
Requires:   openssl-devel

%description devel
This package contains headerfiles and libraries which are needed to
build applications using clamav.


%package data
Summary:    Virus signature data for the Clam Antivirus scanner
Requires:   clamav-filesystem = %version-%release
Provides:   data(clamav) = full
Provides:   clamav-db = %{version}-%{release}
Obsoletes:  clamav-db < %{version}-%{release}
BuildArch:  noarch

%description data
This package contains the virus-database needed by clamav. This
database should be updated regularly; the 'clamav-update' package
ships a corresponding cron-job. Use this package when you want a
working (but perhaps outdated) virus scanner immediately after package
installation.


%package update
Summary:    Auto-updater for the Clam Antivirus scanner data-files
Requires:   clamav-filesystem = %version-%release
Requires:   crontabs
Requires:   /etc/cron.d
Provides:   data(clamav) = empty
Provides:   clamav-data-empty = %{version}-%{release}
Obsoletes:  clamav-data-empty < %{version}-%{release}
Requires(post):     %__chown %__chmod

%description update
This package contains programs which can be used to update the clamav
anti-virus database automatically. It uses the freshclam(1) utility for
this task. To activate it, uncomment the entry in /etc/cron.d/clamav-update.
Use this package when you go updating the virus database regulary and
do not want to download a >120MB sized rpm-package with outdated virus
definitions.


%package -n clamd
Summary: The Clam AntiVirus Daemon
Requires:   data(clamav)
Requires:   clamav-filesystem = %version-%release
Requires:   clamav-lib        = %version-%release
Requires:   coreutils
Requires(pre):  shadow-utils
%if %{with sysv}
Requires:   %_initrddir
Provides:   clamav-server-sysvinit = %version-%release
%endif
Obsoletes:  clamav-server-sysvinit < %version-%release
%if %{with systemd}
%endif
# Remove me after EOL of RHEL6
%if %{with sysv}
Requires:   %_initrddir
Requires(postun):   initscripts
Requires(post):     chkconfig
Requires(preun):    chkconfig initscripts
%else
Obsoletes:  clamav-scanner-sysvinit < %version-%release
%endif
# Remove me after EOL of RHEL6
%if %{with upstart}
Requires:   /etc/init
Requires(post):     /usr/bin/killall
Requires(preun):    /sbin/initctl
Provides:  clamav-scanner-upstart = %version-%release
%endif
Obsoletes:  clamav-scanner-upstart < %version-%release

%if %{with systemd}
Provides: clamav-scanner-systemd = %{version}-%{release}
Provides: clamav-server-systemd = %{version}-%{release}
%endif
Obsoletes: clamav-scanner-systemd < %{version}-%{release}
Obsoletes: clamav-server-systemd < %{version}-%{release}

### Fedora Extras introduced them differently :(
Provides: clamav-server = %{version}-%{release}
Obsoletes: clamav-server < %{version}-%{release}
Provides: clamav-server-sysv = %{version}-%{release}
Obsoletes: clamav-server-sysv < %{version}-%{release}
Provides: clamav-scanner = %{version}-%{release}
Obsoletes: clamav-scanner < %{version}-%{release}
Provides: clamav-scanner-upstart = %{version}-%{release}
Obsoletes: clamav-scanner-upstart < %{version}-%{release}
Provides: clamav-server-sysvinit = %{version}-%{release}
Obsoletes: clamav-server-sysvinit < %{version}-%{release}


%description -n clamd
The Clam AntiVirus Daemon
See the README file how this can be done with a minimum of effort.
This package contains a generic system wide clamd service which is
e.g. used by the clamav-milter package.


%package milter
Summary:    Milter module for the Clam Antivirus scanner
# clamav-milter could work without clamd and without sendmail
#Requires: clamd = %%{version}-%%{release}
#Requires: /usr/sbin/sendmail
Requires:   clamav-filesystem = %version-%release
Requires(post): coreutils
Requires(pre):  shadow-utils

# Remove me after EOL of RHEL6
%if %{with sysv}
Requires:       %_initrddir
Requires(postun):   initscripts
Requires(post):     chkconfig
Requires(preun):    chkconfig initscripts
Provides:   clamav-milter-sysvinit = %version-%release
%endif
Obsoletes:  clamav-milter-sysvinit < %version-%release
# Remove me after EOL of RHEL6
%if %{with upstart}
Requires:   /etc/init
Requires(post):     /usr/bin/killall
Requires(preun):    /sbin/initctl
Provides:  clamav-milter-upstart = %version-%release
%endif
Obsoletes:  clamav-milter-upstart < %version-%release

%if %{with systemd}
Provides: clamav-milter-systemd = %{version}-%{release}
%endif
Obsoletes: clamav-milter-systemd < %{version}-%{release}

%description milter
This package contains files which are needed to run the clamav-milter.

## ------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}%{?prerelease}

%patch0 -p0 -b .stats-deprecation
%patch1 -p1 -b .default_confs
%patch24 -p1 -b .private
%patch27 -p1 -b .umask
%patch30 -p1

install -p -m0644 %SOURCE300 clamav-milter/

mkdir -p libclamunrar{,_iface}
%{!?with_unrar:touch libclamunrar/{Makefile.in,all,install}}

sed -ri \
    -e 's!^#?(LogFile ).*!#\1/var/log/clamd.<SERVICE>!g' \
    -e 's!^#?(LocalSocket ).*!#\1/var/run/clamd.<SERVICE>/clamd.sock!g' \
    -e 's!^(#?PidFile ).*!\1/var/run/clamd.<SERVICE>/clamd.pid!g' \
    -e 's!^#?(User ).*!\1<USER>!g' \
    -e 's!^#?(AllowSupplementaryGroups|LogSyslog).*!\1 yes!g' \
    -e 's! /usr/local/share/clamav,! %homedir,!g' \
    etc/clamd.conf.sample

sed -ri \
    -e 's!^Example!#Example!' \
    -e 's!^#?(UpdateLogFile )!#\1!g;' \
    -e 's!^#?(LogSyslog).*!\1 yes!g' \
    -e 's!(DatabaseOwner *)clamav$!\1%updateuser!g' etc/freshclam.conf.sample


## ------------------------------------------------------------

%build
#CFLAGS="$RPM_OPT_FLAGS -Wall -W -Wmissing-prototypes -Wmissing-declarations -std=gnu99"
#CXXFLAGS="$RPM_OPT_FLAGS -std=gnu++98"
export LDFLAGS='%{?__global_ldflags} -Wl,--as-needed'
# IPv6 check is buggy and does not work when there are no IPv6 interface on build machine
export have_cv_ipv6=yes

rm -rf libltdl autom4te.cache Makefile.in
autoreconf -i
%configure \
    --enable-milter \
    --disable-clamav \
    --disable-static \
    --disable-zlib-vcheck \
    %{!?with_unrar:--disable-unrar} \
    --enable-id-check \
    --enable-dns \
    --with-dbdir=%homedir \
    --with-group=%updateuser \
    --with-user=%updateuser \
    --disable-rpath \
    --disable-silent-rules \
    --enable-clamdtop \
    %{!?with_llvm:--disable-llvm}

# TODO: check periodically that CLAMAVUSER is used for freshclam only


# build with --as-needed and disable rpath
sed -i \
    -e 's! -shared ! -Wl,--as-needed\0!g'                   \
    -e '/sys_lib_dlsearch_path_spec=\"\/lib \/usr\/lib /s!\"\/lib \/usr\/lib !/\"/%_lib /usr/%_lib !g'  \
    libtool

%make_build


## ------------------------------------------------------------

%install
rm -rf _doc*
%make_install

function smartsubst() {
    local tmp
    local regexp=$1
    shift

    tmp=$(mktemp /tmp/%name-subst.XXXXXX)
    for i; do
        sed -e "$regexp" "$i" >$tmp
        cmp -s $tmp "$i" || cat $tmp >"$i"
        rm -f $tmp
    done
}


install -d -m 0755 \
    $RPM_BUILD_ROOT%_sysconfdir/{mail,clamd.d,logrotate.d} \
    $RPM_BUILD_ROOT%_tmpfilesdir \
    $RPM_BUILD_ROOT%_rundir \
    $RPM_BUILD_ROOT%_var/log \
    $RPM_BUILD_ROOT%milterstatedir \
    $RPM_BUILD_ROOT%pkgdatadir/template \
    $RPM_BUILD_ROOT%_initrddir \
    $RPM_BUILD_ROOT%homedir \
    $RPM_BUILD_ROOT%scanstatedir

rm -f   $RPM_BUILD_ROOT%_sysconfdir/clamd.conf.sample \
    $RPM_BUILD_ROOT%_libdir/*.la


touch $RPM_BUILD_ROOT%homedir/{daily,main,bytecode}.cld
touch $RPM_BUILD_ROOT%homedir/mirrors.dat

install -D -m 0644 -p %SOURCE10     $RPM_BUILD_ROOT%homedir/main.cvd
install -D -m 0644 -p %SOURCE11     $RPM_BUILD_ROOT%homedir/daily.cvd
install -D -m 0644 -p %SOURCE12     $RPM_BUILD_ROOT%homedir/bytecode.cvd

## prepare the server-files
install -D -m 0644 -p %SOURCE2      _doc_server/clamd.sysconfig
install -D -m 0644 -p %SOURCE3      _doc_server/clamd.logrotate
%if %{with sysv}
install -D -m 0755 -p %SOURCE7      _doc_server/clamd.init
%endif
install -D -m 0644 -p %SOURCE5      _doc_server/README
install -D -m 0644 -p etc/clamd.conf.sample _doc_server/clamd.conf

%if %{with sysv}
install -m 0644 -p %SOURCE520       $RPM_BUILD_ROOT%pkgdatadir/
%endif
install -m 0755 -p %SOURCE100       $RPM_BUILD_ROOT%pkgdatadir/
cp -pa _doc_server/*            $RPM_BUILD_ROOT%pkgdatadir/template

%if %{with sysv}
smartsubst 's!/usr/share/clamav!%pkgdatadir!g' $RPM_BUILD_ROOT%pkgdatadir/clamd-wrapper
%endif
install -D -p -m 0644 %SOURCE530        $RPM_BUILD_ROOT%_unitdir/clamd@.service


## prepare the update-files
install -D -m 0644 -p %SOURCE203    $RPM_BUILD_ROOT%_sysconfdir/logrotate.d/clamav-update
touch $RPM_BUILD_ROOT%freshclamlog

install -D -p -m 0755 %SOURCE200    $RPM_BUILD_ROOT%pkgdatadir/freshclam-sleep
install -D -p -m 0644 %SOURCE201    $RPM_BUILD_ROOT%_sysconfdir/sysconfig/freshclam
install -D -p -m 0600 %SOURCE202    $RPM_BUILD_ROOT%_sysconfdir/cron.d/clamav-update
mv -f $RPM_BUILD_ROOT%_sysconfdir/freshclam.conf{.sample,}
# Can contain HTTPProxyPassword (bugz#1733112)
chmod 600 $RPM_BUILD_ROOT%_sysconfdir/freshclam.conf

smartsubst 's!webmaster,clamav!webmaster,%updateuser!g;
        s!/usr/share/clamav!%pkgdatadir!g;
        s!/usr/bin!%_bindir!g;
            s!/usr/sbin!%_sbindir!g;' \
   $RPM_BUILD_ROOT%_sysconfdir/cron.d/clamav-update \
   $RPM_BUILD_ROOT%pkgdatadir/freshclam-sleep


### The scanner stuff
sed -e 's!<SERVICE>!scan!g;s!<USER>!%scanuser!g' \
    etc/clamd.conf.sample > $RPM_BUILD_ROOT%_sysconfdir/clamd.d/scan.conf

%if %{with sysv}
sed -e 's!<SERVICE>!scan!g;' $RPM_BUILD_ROOT%pkgdatadir/template/clamd.init \
    > $RPM_BUILD_ROOT%_initrddir/clamd.scan
%endif

install -D -p -m 0644 %SOURCE410 $RPM_BUILD_ROOT%_sysconfdir/init/clamd.scan.conf
install -D -p -m 0644 %SOURCE430 $RPM_BUILD_ROOT%_unitdir/clamd@scan.service

cat << EOF > $RPM_BUILD_ROOT%_tmpfilesdir/clamd.scan.conf
d %scanstatedir 0710 %scanuser virusgroup
EOF

touch $RPM_BUILD_ROOT%scanstatedir/clamd.{sock,pid}


### The milter stuff
sed -r \
    -e 's!^#?(User).*!\1 %milteruser!g' \
    -e 's!^#?(AllowSupplementaryGroups|LogSyslog) .*!\1 yes!g' \
    -e 's! /tmp/clamav-milter.socket! %milterstatedir/clamav-milter.socket!g' \
    -e 's! /var/run/clamav-milter.pid! %milterstatedir/clamav-milter.pid!g' \
    -e 's! /var/run/clamd/clamd.socket! %scanstatedir/clamd.sock!g' \
    -e 's! /tmp/clamav-milter.log! %milterlog!g' \
    etc/clamav-milter.conf.sample > $RPM_BUILD_ROOT%_sysconfdir/mail/clamav-milter.conf

install -D -p -m 0644 %SOURCE310 $RPM_BUILD_ROOT%_sysconfdir/init/clamav-milter.conf
%if %{with sysv}
install -D -p -m 0755 %SOURCE320 $RPM_BUILD_ROOT%_initrddir/clamav-milter
%endif
install -D -p -m 0644 %SOURCE330 $RPM_BUILD_ROOT%_unitdir/clamav-milter.service

cat << EOF > $RPM_BUILD_ROOT%_tmpfilesdir/clamav-milter.conf
d %milterstatedir 0710 %milteruser %milteruser
EOF

rm -f $RPM_BUILD_ROOT%_sysconfdir/clamav-milter.conf.sample
touch $RPM_BUILD_ROOT{%milterstatedir/clamav-milter.{socket,pid},%milterlog}

%{!?with_upstart:  rm -rf $RPM_BUILD_ROOT%_sysconfdir/init}
%{!?with_systemd:  rm -rf $RPM_BUILD_ROOT%_unitdir}
%{!?with_sysv:     rm -f  $RPM_BUILD_ROOT%_initrddir/*}
%{!?with_sysv:     rm -rf $RPM_BUILD_ROOT%_rundir/*/*.pid}
%{!?with_tmpfiles: rm -rf $RPM_BUILD_ROOT%_tmpfilesdir}

%if %{with systemd}
# TODO: Evaluate using upstream's unit files
rm $RPM_BUILD_ROOT%_unitdir/clamav-{daemon,freshclam}.*
%endif

%if %{with sysv}
# keep clamd-wrapper in every case because it might be needed by other
# packages
ln -s %pkgdatadir/clamd-wrapper     $RPM_BUILD_ROOT%_initrddir/clamd-wrapper
%endif

## ------------------------------------------------------------

%check
make check

## ------------------------------------------------------------

%pre filesystem
getent group %{updateuser} >/dev/null || groupadd -r %{updateuser}
getent passwd %{updateuser} >/dev/null || \
    useradd -r -g %{updateuser} -d %{homedir} -s /sbin/nologin \
    -c "Clamav database update user" %{updateuser}
getent group virusgroup >/dev/null || groupadd -r virusgroup
usermod %{updateuser} -a -G virusgroup
exit 0


%pre -n clamd
getent group %{scanuser} >/dev/null || groupadd -r %{scanuser}
getent passwd %{scanuser} >/dev/null || \
    useradd -r -g %{scanuser} -d / -s /sbin/nologin \
    -c "Clamav scanner user" %{scanuser}
usermod %{scanuser} -a -G virusgroup
exit 0

%post -n clamd
%if %{with sysv}
/sbin/chkconfig --add clamd.scan
%endif
%if %{with upstart}
/usr/bin/killall -u %scanuser clamd 2>/dev/null || :
%endif
%if %{with systemd}
%systemd_post clamd@.service
%systemd_post clamd@scan.service
%{?with_tmpfiles:/bin/systemd-tmpfiles --create %_tmpfilesdir/clamd.scan.conf || :}
%endif

%preun -n clamd
%if %{with sysv}
test "$1" != 0 || %_initrddir/clamd.scan stop &>/dev/null || :
test "$1" != 0 || /sbin/chkconfig --del clamd.scan
%endif
%if %{with upstart}
test "$1" != "0" || /sbin/initctl -q stop clamd.scan || :
%endif
%if %{with systemd}
%systemd_preun clamd@.service
%systemd_preun clamd@scan.service
%endif

%postun -n clamd
%if %{with sysv}
test "$1"  = 0 || %_initrddir/clamd.scan condrestart >/dev/null || :
%endif
%if %{with systemd}
%systemd_postun_with_restart clamd@.service
%systemd_postun_with_restart clamd@scan.service
%endif


%post update
test -e %freshclamlog || {
    touch %freshclamlog
    %__chmod 0664 %freshclamlog
    %__chown root:%updateuser %freshclamlog
    ! test -x /sbin/restorecon || /sbin/restorecon %freshclamlog
}


%triggerin milter -- clamav-scanner
# Add the milteruser to the scanuser group; this is required when
# milter and clamd communicate through local sockets
/usr/sbin/groupmems -g %scanuser -a %milteruser &>/dev/null || :

%pre milter
getent group %{milteruser} >/dev/null || groupadd -r %{milteruser}
getent passwd %{milteruser} >/dev/null || \
    useradd -r -g %{milteruser} -d %{milterstatedir} -s /sbin/nologin \
    -c "Clamav Milter user" %{milteruser}
usermod %{milteruser} -a -G virusgroup
exit 0

%post milter
test -e %milterlog || {
    touch %milterlog
    chmod 0620             %milterlog
    chown root:%milteruser %milterlog
    ! test -x /sbin/restorecon || /sbin/restorecon %milterlog
}
%if %{with sysv}
/sbin/chkconfig --add clamav-milter
%endif
%if %{with upstart}
/usr/bin/killall -u %milteruser clamav-milter 2>/dev/null || :
%endif
%if %{with systemd}
%systemd_post clamav-milter.service
%{?with_tmpfiles:/bin/systemd-tmpfiles --create %_tmpfilesdir/clamav-milter.conf || :}
%endif

%preun milter
%if %{with sysv}
test "$1" != 0 || %_initrddir/clamav-milter stop &>/dev/null || :
test "$1" != 0 || /sbin/chkconfig --del clamav-milter
%endif
%if %{with upstart}
test "$1" != "0" || /sbin/initctl -q stop clamav-milter || :
%endif
%if %{with systemd}
%systemd_preun clamav-milter.service
%endif

%postun milter
%if %{with sysv}
test "$1"  = 0 || %_initrddir/clamav-milter condrestart >/dev/null || :
%endif
%if %{with systemd}
%systemd_postun_with_restart clamav-milter.service
%endif

%ldconfig_scriptlets   lib


%files
%license COPYING
%doc NEWS.md README.md docs/html
%_bindir/clambc
%_bindir/clamconf
%_bindir/clamdscan
%_bindir/clamdtop
%_bindir/clamscan
%_bindir/clamsubmit
%_bindir/sigtool
%_mandir/man[15]/*
%exclude %_mandir/*/freshclam*
%exclude %_mandir/man5/clamd.conf.5*

## -----------------------

%files lib
%_libdir/libclamav.so.9*
%_libdir/libclammspack.so.0*

## -----------------------

%files devel
%_includedir/*
%_libdir/*.so
%pkgdatadir/template
%pkgdatadir/clamd-gen
%_libdir/pkgconfig/*
%_bindir/clamav-config

## -----------------------

%files filesystem
%attr(-,%updateuser,%updateuser) %dir %homedir
%attr(-,root,root)           %dir %pkgdatadir
%dir %_sysconfdir/clamd.d

## -----------------------

%files data
%defattr(-,%updateuser,%updateuser,-)
# use %%config to keep files which were updated by 'freshclam'
# already. Without this tag, they would be overridden with older
# versions whenever a new -data package is installed.
%config %verify(not size md5 mtime) %homedir/*.cvd


%files update
%_bindir/freshclam
%_mandir/*/freshclam*
%pkgdatadir/freshclam-sleep
%config(noreplace) %verify(not mtime)    %_sysconfdir/freshclam.conf
%config(noreplace) %verify(not mtime)    %_sysconfdir/logrotate.d/*
%config(noreplace) %_sysconfdir/cron.d/clamav-update
%config(noreplace) %_sysconfdir/sysconfig/freshclam

%ghost %attr(0664,root,%updateuser) %verify(not size md5 mtime) %freshclamlog
%ghost %attr(0664,%updateuser,%updateuser) %homedir/*.cld
%ghost %attr(0664,%updateuser,%updateuser) %homedir/mirrors.dat


## -----------------------

%files -n clamd
%doc _doc_server/*
%_mandir/man5/clamd.conf.5*
%_mandir/man8/clamd.8*
%_sbindir/clamd
%if %{with sysv}
%_initrddir/clamd-wrapper
%pkgdatadir/clamd-wrapper
%endif
%if %{with systemd}
%_unitdir/clamd@.service
%endif

%config(noreplace) %_sysconfdir/clamd.d/scan.conf
%ghost %scanstatedir/clamd.sock
%if %{with tmpfiles}
  %_tmpfilesdir/clamd.scan.conf
  %ghost %dir %attr(0710,%scanuser,virusgroup) %scanstatedir
%else
  %dir %attr(0710,%scanuser,virusgroup) %scanstatedir
%endif
%if %{with sysv}
  %attr(0755,root,root) %config %_initrddir/clamd.scan
  %ghost %scanstatedir/clamd.pid
%endif
%if %{with upstart}
  %config(noreplace) %_sysconfdir/init/clamd.scan*
%endif
%if %{with systemd}
  %_unitdir/clamd@scan.service
%endif

## -----------------------

%files milter
%doc clamav-milter/README.fedora
%_sbindir/*milter*
%_mandir/man8/clamav-milter*
%dir %_sysconfdir/mail
%config(noreplace) %_sysconfdir/mail/clamav-milter.conf
%ghost %attr(0620,root,%milteruser) %verify(not size md5 mtime) %milterlog
%ghost %milterstatedir/clamav-milter.socket

%if %{with tmpfiles}
  %_tmpfilesdir/clamav-milter.conf
  %ghost %dir %attr(0710,%milteruser,%milteruser) %milterstatedir
%else
  %dir %attr(0710,%milteruser,%milteruser) %milterstatedir
%endif
%if %{with sysv}
  %config %_initrddir/clamav-milter
  %ghost %milterstatedir/clamav-milter.pid
%endif
%if %{with upstart}
  %config(noreplace) %_sysconfdir/init/clamav-milter*
%endif
%if %{with systemd}
  %_unitdir/clamav-milter.service
%endif


%changelog
* Thu Aug 22 2019 Orion Poplawski <orion@nwra.com> - 0.101.4-1
- Update to 0.101.4

* Wed Aug 7 2019 Orion Poplawski <orion@nwra.com> - 0.101.3-1
- Update to 0.101.3
- Fix permissions on freshclam.conf (bugz#1733112)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.101.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 Sérgio Basto <sergio@serjux.com> - 0.101.2-2
- One year later we may remove pakages workaround of clamav-milter-systemd,
  clamav-scanner-systemd and clamav-server-systemd, before I forget it was one
  workaround to allow migration of service without stop it and disable it
  (#1583599).

* Thu Mar 28 2019 Sérgio Basto <sergio@serjux.com> - 0.101.2-1
- Update to 0.101.2

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.101.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Sérgio Basto <sergio@serjux.com> - 0.101.1-1
- Update to 0.101.1

* Thu Jan 3 2019 Orion Poplawski <orion@nwra.com> - 0.101.0-3
- Actually apply patch

* Thu Jan 3 2019 Orion Poplawski <orion@nwra.com> - 0.101.0-2
- Explicitly list sonames to catch soname bumps
- Backport header fix (bug #1663011)

* Thu Dec 13 2018 Orion Poplawski <orion@nwra.com> - 0.101.0-1
- Update to 0.101.0
- Add %%license
- pdf docs replaced with html

* Thu Oct 04 2018 Sérgio Basto <sergio@serjux.com> - 0.100.2-2
- Revert unwanted committed parts of commit "clean whitespace"

* Thu Oct 04 2018 Sérgio Basto <sergio@serjux.com> - 0.100.2-1
- Update to 0.100.2
- Fix logrotate example (#1610735)
- Improve clamd@.service (enter in commit "clean whitespace" by mistake sorry)

* Mon Jul 30 2018 Sérgio Basto <sergio@serjux.com> - 0.100.1-4
- Change the default location of configuration files in clamconf, binaries and
  man pages, replacing with our default packaging (#859339).

* Sun Jul 29 2018 Sérgio Basto <sergio@serjux.com> - 0.100.1-3
- Modify group of /var/run/clamd.scan to virusgroup
- Add some SELinux notes from (#787434)
- Drop pointless clamav-0.99.1-setsebool.patch
- Drop conditionalized build of noarch

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.100.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Sérgio Basto <sergio@serjux.com> - 0.100.1-1
- Update to 0.100.1

* Mon Jul 02 2018 Sérgio Basto <sergio@serjux.com> - 0.100.0-3
- Remove sub-package clamav-data-empty
- Also remove conflicts between clamav-data and clamav-data-empty

* Sun Jun 03 2018 Sérgio Basto <sergio@serjux.com> - 0.100.0-2
- Try to mitigate bug #1583599
- Move comments one line (to read before starting the scriptlet)
- clamav-milter could work without clamd and without sendmail (#1583599)
- Get rid of provides/requires with updateuser, virusgroup, scanuser and
  milteruser and just simply require clamav-filesystem

* Mon May 28 2018 Robert Scheck <robert@fedoraproject.org> - 0.100.0-1
- Upgrade to 0.100.0 (#1565381)

* Wed Mar 21 2018 Sérgio Basto <sergio@serjux.com> - 0.99.4-3
- Fix data-empty sub-package (ghost the correct files)
- Add Obsoletes systemd sub-packages

* Mon Mar 12 2018 Sérgio Basto <sergio@serjux.com> - 0.99.4-2
- Revert fix for llvm, build using -std=gnu++98 (#1307378)
- Revert CFLAG assignment in commmit a4a6d252 (made in 2006)
- BR systemd-devel to fix detection in configure.
- Disable llvm in ppc64 (#1534071)
- "Disable llvm will use the internal bytecode interpreter rather than the llvm
  jit", so drop bytecode build condition and use condional on enable or disable
  llvm.

* Fri Mar 02 2018 Orion Poplawski <orion@nwra.com> - 0.99.4-1
- Update to 0.99.4
- Security fixes CVE-2012-6706 CVE-2017-6419 CVE-2017-11423 CVE-2018-1000085
  CVE-2018-0202

* Tue Feb 13 2018 Sérgio Basto <sergio@serjux.com> - 0.99.3-7
- Remove sub-packages sysvinit, upstart and systemd to be more compatible with
  el6 .
- Remove provides/obsoletes for very old sub-packges clamav-milter-core,
  clamav-milter-sendmail and clamav-milter-core
- Call server and scanner sub-packages as clamd (el6 compatible and as uppstream
  call it)
- clamav-data provides clamav-db (el6 compatible)
- Explicitly enable-id-check and enable-dns in configure (as in el6).
- Add missing build-time requirement pcre2-devel (it misses in el6 at least)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.99.3-6
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Sérgio Basto <sergio@serjux.com> - 0.99.3-4
- Last Epel 7 macro already have systemctl daemon-reload, reverting 0.99.3-3 release
- Remove BR _includedir/tcpd.h due:
  https://fedoraproject.org/wiki/Changes/Deprecate_TCP_wrappers

* Wed Jan 31 2018 Sérgio Basto <sergio@serjux.com> - 0.99.3-3
- Use systemctl daemon-reload because we change services and epel7 seems not
  reload services and break conditional restart.

* Wed Jan 31 2018 Sérgio Basto <sergio@serjux.com>
- Fix and organize systemd scriptlets, clamd@.service missed systemd_preun macro
  and had a wrong systemd_postun_with_restart
- Remove triggerin macros that aren't need it anymore
- Fix scriplet
- Organize startup scriptlets
- Exclude one file listed twice

* Fri Jan 26 2018 Orion Poplawski <orion@nwra.com> - 0.99.3-1
- Update to 0.99.3
- Security fixes CVE-2017-12374 CVE-2017-12375 CVE-2017-12376 CVE-2017-12377
  CVE-2017-12378 CVE-2017-12379 CVE-2017-12380 (bug #1539030)
- Drop clamav-notify-servers and it's dependency on ncat (bug #1530678)

* Wed Jan 17 2018 Sérgio Basto <sergio@serjux.com> - 0.99.2-18
- Fix type of clamd@ service
- Fix packages name of Obsoletes directives
- Also fix type of clamav-milter.service

* Thu Jan 11 2018 Sérgio Basto <sergio@serjux.com> - 0.99.2-17
- Security fixes CVE-2017-6420 (#1483910), CVE-2017-6418 (#1483908)

* Tue Jan 09 2018 Sérgio Basto <sergio@serjux.com> - 0.99.2-16
- Make sure that Obsoletes sysv and upstart for Epel upgrade and update

* Mon Jan 08 2018 Sérgio Basto <sergio@serjux.com> - 0.99.2-15
- Fix rundir path (#1126595)
- Update main.cvd, daily.cvd and bytecode.cvd
- Fixes for rhbz 1464269 and rhbz 1126625
- Move Sources and BuildRequires to the beginning
- Build systemd for F22+ and el7+
- Build sysv and upstart for el6 else build only sysv
- Only enable tmpfiles with systemd enabled
- Move descritions to near the package macro and remove his build
  conditionals, this also fix the generation of src.rpm
- Remove hack from 2010 (git show e1a9be60)
- Use autoreconf without --force

* Thu Jan 04 2018 Sérgio Basto <sergio@serjux.com> - 0.99.2-14
- Use 4 spaces instead tabs
- Fix rhbz #1530678
- Fix rhbz #1518016
- Simplify conditional builds reference: /usr/lib/rpm/macros
- use make_build and make install macros

* Sun Nov 26 2017 Robert Scheck <robert@fedoraproject.org> - 0.99.2-13
- Backported upstream patch to unbreak e2guardian vs. temp files

* Fri Sep 15 2017 Sérgio Basto <sergio@serjux.com> - 0.99.2-12
- Try fix rhbz #1473642

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Sérgio Basto <sergio@serjux.com> - 0.99.2-9
- Add patch for openssl-1.1

* Mon Mar 27 2017 Orion Poplawski <orion@cora.nwra.com> - 0.99.2-8
- Create virusgroup group and add the various clam* users to it

* Sun Mar 26 2017 Orion Poplawski <orion@cora.nwra.com> - 0.99.2-7
- Fix clamav-milter startup under selinux (bug #1434176)
- Move /etc/clam.d to clamav-filesystem (bug #1275630)
- Make clamav-milter own /etc/mail (bug #1175473)

* Sun Mar 26 2017 Orion Poplawski <orion@cora.nwra.com> - 0.99.2-6
- Start clamav-milter after clamd@scan (bug #1356507))

* Sun Mar 26 2017 Orion Poplawski <orion@cora.nwra.com> - 0.99.2-5
- Allow freshclam to run automatically on install (bug #1408649)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 07 2016 Richard W.M. Jones <rjones@redhat.com> - 0.99.2-3
- Rebuild for OCaml 4.04.0.

* Tue Oct 18 2016 Orion Poplawski <orion@cora.nwra.com> - 0.99.2-2
- Also send logrotate script stdout to /dev/null (bug #1376815)

* Mon Jun 13 2016 Orion Poplawski <orion@cora.nwra.com> - 0.99.2-1
- Update to 0.99.2
- Drop cliopts patch fixed upstream, use upstream's "--forground" option name
- Fix main.cvd (fedora #1325482, epel #1325717)
- Own bytecode.cld (#1176252) and mirrors.dat, ship bytecode.cvd
- Update daily.cvd
- Fixup Requires(pre) usage (#1319151)

* Tue Mar 29 2016 Robert Scheck <robert@fedoraproject.org> - 0.99.1-1
- Upgrade to 0.99.1 and updated main.cvd and daily.cvd (#1314115)
- Complain about antivirus_use_jit rather clamd_use_jit (#1295473)

* Tue Mar 29 2016 Robert Scheck <robert@fedoraproject.org> - 0.99-4
- Link using %%{?__global_ldflags} for hardened builds (#1321173)
- Build using -std=gnu++98 (#1307378, thanks to Yaakov Selkowitz)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 06 2015 Robert Scheck <robert@fedoraproject.org> - 0.99-2
- Require openssl-devel for clamav-devel
- Change clamav-milter unit for upstream changes (#1287795)

* Wed Dec 02 2015 Robert Scheck <robert@fedoraproject.org> - 0.99-1
- Upgrade to 0.99 and updated daily.cvd (#1287327)

* Tue Jun 30 2015 Robert Scheck <robert@fedoraproject.org> - 0.98.7-3
- Move /etc/tmpfiles.d/ to /usr/lib/tmpfiles.d/ (#1126595)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Robert Scheck <robert@fedoraproject.org> - 0.98.7-1
- Upgrade to 0.98.7 and updated daily.cvd (#1217014)

* Tue Mar 10 2015 Adam Jackson <ajax@redhat.com> 0.98.6-2
- Drop sysvinit subpackages in F23+

* Thu Jan 29 2015 Robert Scheck <robert@fedoraproject.org> - 0.98.6-1
- Upgrade to 0.98.6 and updated daily.cvd (#1187050)

* Wed Nov 19 2014 Robert Scheck <robert@fedoraproject.org> - 0.98.5-2
- Corrected summary of clamav-server-systemd package (#1165672)

* Wed Nov 19 2014 Robert Scheck <robert@fedoraproject.org> - 0.98.5-1
- Upgrade to 0.98.5 and updated daily.cvd (#1138101)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 21 2014 Robert Scheck <robert@fedoraproject.org> - 0.98.4-1
- Upgrade to 0.98.4 and updated daily.cvd (#1111811)
- Add build requirement to libxml2 for DMG, OpenIOC and XAR

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Robert Scheck <robert@fedoraproject.org> - 0.98.3-1
- Upgrade to 0.98.3 and updated daily.cvd (#1095614)
- Avoid automatic path detection breakage regarding curl
- Added build requirement to openssl-devel for hasing code
- Added clamsubmit to main package

* Wed Jan 15 2014 Robert Scheck <robert@fedoraproject.org> - 0.98.1-1
- Upgrade to 0.98.1 and updated daily.cvd (#1053400)

* Wed Oct 09 2013 Dan Horák <dan[at]danny.cz> - 0.98-2
- Use fanotify from glibc instead of the limited hand-crafted version

* Sun Oct 06 2013 Robert Scheck <robert@fedoraproject.org> - 0.98-1
- Upgrade to 0.98 and updated main.cvd and daily.cvd (#1010168)

* Wed Aug 07 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.97.8-4
- Add a missing requirement on crontabs to spec file
- Fix RHBZ#988605

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 2 2013 Nick Bebout <nb@fedoraproject.org> - 0.97.8-1
- Update to 0.97.8

* Wed Apr 10 2013 Jon Ciesla <limburgher@gmail.com> - 0.97.7-2
- Migrate from fedora-usermgmt to guideline scriptlets.

* Sat Mar 23 2013 Nick Bebout <nb@fedoraproject.org> - 0.97.7-1
- Update to 0.97.7

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97.6-1901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Sep 22 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.6-1900
- updated to 0.97.6
- use %%systemd macros

* Tue Aug 14 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.5-1900
- disabled upstart support

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97.5-1801
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.5-1800
- updated to 0.97.5
- CVE-2012-1457: allows to bypass malware detection via a TAR archive
  entry with a length field that exceeds the total TAR file size
- CVE-2012-1458: allows to bypass malware detection via a crafted
  reset interval in the LZXC header of a CHM file
- CVE-2012-1459: allows to bypass malware detection via a TAR archive
  entry with a length field corresponding to that entire entry, plus
  part of the header of the next entry
- ship local copy of virus database; it was removed by accident from
  0.97.5 tarball
- removed sysv compat stuff

* Fri Apr 13 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.4-1801
- build with -fPIE

* Fri Mar 16 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.4-1800
- updated to 0.97.4

* Sun Feb  5 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.3-1703
- fixed SELinux restorecon invocation
- added trigger to fix SELinux contexts of logfiles created by old
  packages
- fixed build with recent gcc/glibc toolchain

* Sat Jan 21 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.3-1703
- rewrote clamav-notify-servers to be init system neutral
- set PrivateTmp systemd option (#782488)

* Sun Jan  8 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.3-1702
- set correct SELinux context for logfiles generated in %%post (#754555)
- create systemd tmpfiles in %%post
- created -server-systemd subpackage providing a clamd@.service template
- made script in -scanner-systemd an instance of clamd@.service

* Tue Oct 18 2011 Nick Bebout <nb@fedoraproject.org> - 0.97.3-1700
- updated to 0.97.3
- CVE-2011-3627 clamav: Recursion level crash fixed in v0.97.3

* Thu Aug  4 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.2-1700
- moved sysv wrapper script into -sysv subpackage
- start systemd services after network.target and nss-lookup.target

* Tue Jul 26 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.2-1600
- updated to 0.97.2
- CVE-2011-2721 Off-by-one error by scanning message hashes (#725694)
- fixed systemd scripts and their installation

* Thu Jun  9 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97.1-1600
- updated to 0.97.1
- fixed Requires(preun) vs. Requires(postun) inconsistency

* Sat Apr 23 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97-1601
- fixed tmpfiles.d syntax (#696812)

* Sun Feb 20 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.97-1600
- updated to 0.97
- rediffed some patches

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96.5-1503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan  8 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.5-1502
- fixed signal specifier in clamd-wrapper (#668131, James Ralston)

* Fri Dec 24 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.5-1501
- added systemd init scripts which obsolete to old sysvinit ones
- added tmpfiles.d/ descriptions

* Sat Dec  4 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.5-1500
- updated to 0.96.5
- CVE-2010-4260 Multiple errors within the processing of PDF files can
  be exploited to e.g. cause a crash.
- CVE-2010-4261 An off-by-one error within the "icon_cb()" function
  can be exploited to cause a memory corruption.

* Sun Oct 31 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.4-1500
- updated to 0.96.4
- execute 'make check' (#640347) but ignore errors for now because
  four checks are failing on f13

* Wed Sep 29 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.3-1501
- lowered stop priority of sysv initscripts (#629435)

* Wed Sep 22 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.3-1500
- updated to 0.96.3
- fixes CVE-2010-0405 in shipped bzlib.c copy

* Sun Aug 15 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.2-1500
- updated to 0.96.2
- rediffed patches
- removed the -jit-disable patch which is replaced upstream by a more
  detailed configuration option.

* Wed Aug 11 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de>
- removed old %%trigger which renamed the 'clamav' user- and groupnames
  to 'clamupdate'
- use 'groupmems', not 'usermod' to add a user to a group because
  'usermod' does not work when user does not exist in local /etc/passwd

* Tue Jul 13 2010 Dan Horák <dan[at]danny.cz> - 0.96.1-1401
- ocaml not available (at least) on s390(x)

* Tue Jun  1 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96.1-1400
- updated to 0.96.1
- rediffed patches

* Sat May 29 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 0.96.1403
- CVE-2010-1639 Clam AntiVirus: Heap-based overflow, when processing malicious PDF file(s)

* Wed Apr 21 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96-1402
- updated to final 0.96
- applied upstream patch which allows to disable JIT compiler (#573191)
- build JIT compiler again
- disabled JIT compiler by default
- removed explicit 'pkgconfig' requirements in -devel (#533956)

* Sat Mar 20 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96-0.1401.rc1
- do not build the bytecode JIT compiler for now until it can be disabled
  at runtime (#573191)

* Thu Mar 11 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.96-1400.rc1
- updated to 0.96rc1
- added some BRs

* Sun Dec  6 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.3-1301
- updated -upstart to upstart 0.6.3

* Sat Nov 21 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de>
- adjusted chkconfig positions for clamav-milter (#530101)
- use %%apply instead of %%patch

* Thu Oct 29 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.3-1300
- updated to 0.95.3

* Sun Sep 13 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de>
- conditionalized build of noarch subpackages to ease packaging under RHEL5

* Sun Aug  9 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.2-5
- modified freshclam configuration to log by syslog by default
- disabled LocalSocket option in sample configuration
- fixed clamav-milter sysv initscript to use bash interpreter and to
  be disabled by default

* Sat Aug  8 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.2-4
- renamed 'clamav' user/group to 'clamupdate'
- add the '%%milteruser' user to the '%%scanuser' group when the -scanner
  subpackage is installed

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.2-1
- updated to 0.95.2

* Sun Apr 19 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.1-3
- fixed '--without upstart' operation

* Wed Apr 15 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95.1-2
- added '%%bcond_without upstart' conditional to ease skipping of
  -upstart subpackage creation e.g. on EL5 systems
- fixed Provides/Obsoletes: typo in -milter-sysvinit subpackage which
  broke update path

* Fri Apr 10 2009 Robert Scheck <robert@fedoraproject.org> - 0.95.1-1
- Upgrade to 0.95.1 (#495039)

* Wed Mar 25 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95-1
- updated to final 0.95
- added ncurses-devel (-> clamdtop) BR
- enforced IPv6 support

* Sun Mar  8 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.95-0.1.rc1
- updated to 0.95rc1
- added -upstart subpackages
- renamed -sysv to -sysvinit to make -upstart win the default dep resolving
- reworked complete milter stuff
- added -scanner subpackage which contains a preconfigured daemon
  (e.g. for use by -milter)
- moved %%changelog entries from 2006 and before into ChangeLog-rpm.old

* Wed Feb 25 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.94.2-3
- made some subpackages noarch
- fixed typo in SysV initscript which removes 'touch' file (#473513)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.94.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 02 2008 Robert Scheck <robert@fedoraproject.org> - 0.94.2-1
- Upgrade to 0.94.2 (#474002)

* Wed Nov 05 2008 Robert Scheck <robert@fedoraproject.org> - 0.94.1-1
- Upgrade to 0.94.1

* Sun Oct 26 2008 Robert Scheck <robert@fedoraproject.org> - 0.94-1
- Upgrade to 0.94 (SECURITY), fixes #461461:
- CVE-2008-1389 Invalid memory access in the CHM unpacker
- CVE-2008-3912 Out-of-memory NULL pointer dereference in mbox/msg
- CVE-2008-3913 Memory leak in code path in freshclam's manager.c
- CVE-2008-3914 Multiple file descriptor leaks on the code paths

* Sun Jul 13 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.93.3-1
- updated to 0.93.3; another fix for CVE-2008-2713 (out-of-bounds read
  on petite files)
- put pid instead of pgrp into pidfile of clamav-milter (bz #452359)
- rediffed patches

* Tue Jun 17 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.93.1-1
- updated to 0.93.1
- rediffed -path patch
- CVE-2008-2713 Invalid Memory Access Denial Of Service Vulnerability

* Mon Apr 14 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.93-1
- updated to final 0.93
- removed daily.inc + main.inc directories; they are now replaced by
  *.cld containers
- trimmed down MAILTO list of cronjob to 'root' again; every well
  configured system has an alias for this recipient

* Wed Mar 12 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.93-0.1.rc1
- moved -milter scriptlets into -milter-core subpackage
- added a requirement on the milteruser to the -milter-sendmail
  subpackage (reported by Bruce Jerrick)

* Tue Mar  4 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.93-0.0.rc1
- updated to 0.93rc1
- fixed rpath issues

* Mon Feb 11 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.92.1-1
- updated to 0.92.1

* Tue Jan  1 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.92-6
- redisabled unrar stuff completely by using clean sources
- splitted -milter subpackage into pieces to allow use without sendmail
  (#239037)

* Tue Jan  1 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.92-5
- use a better way to disable RPATH-generation (needed for '--with
  unrar' builds)

* Mon Dec 31 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.92-4
- added a README.fedora to the milter package (#240610)
- ship original sources again; unrar is now licensed correctly (no more
  stolen code put under GPL). Nevertheless, this license is not GPL
  compatible, and to allow libclamav to be used by GPL applications,
  unrar is disabled by a ./configure switch.
- use pkg-config in clamav-config to emulate --cflags and --libs
  operations (fixes partly multilib issues)
- registered some more auto-updated files and marked them as %%ghost

* Fri Dec 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.92-3
- updated to 0.92 (SECURITY):
- CVE-2007-6335 MEW PE File Integer Overflow Vulnerability

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.91.2-3
- remove RAR decompression code from source tarball because of
  legal problems (resolves 334371)
- correct license tag

* Mon Sep 24 2007 Jesse Keating <jkeating@redhat.com> - 0.91.2-2
- Bump release for upgrade path.

* Sat Aug 25 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.91.2-1
- updated to 0.91.2 (SECURITY):
- CVE-2007-4510 DOS in RTF parser
- DOS in html normalizer
- arbitrary command execution by special crafted recipients in
  clamav-milter's black-hole mode
- fixed an open(2) issue

* Tue Jul 17 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.91.1-0
- updated to 0.91.1

* Thu Jul 12 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.91-1
- updated to 0.91

* Thu May 31 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90.3-1
- updated to 0.90.3
- BR tcpd.h instead of tcp_wrappers(-devel) to make it build both
  in FC6- and F7+

* Fri Apr 13 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90.2-1
- [SECURITY] updated to 0.90.2; fixes CVE-2007-1745, CVE-2007-1997

* Fri Mar  2 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90.1-2
- BR 'tcp_wrappers-devel' instead of plain 'tcp_wrappers'

* Fri Mar  2 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90.1-1
- updated to 0.90.1
- updated %%doc list

* Sun Feb 18 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90-1
- updated to final 0.90
- removed -visibility patch since fixed upstream

* Sun Feb  4 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90-0.3.rc3
- build with -Wl,-as-needed and cleaned up pkgconfig file
- removed old hack which forced installation of freshclam.conf; related
  check was removed upstream
- removed static library
- removed %%changelog entries from before 2004

* Sat Feb  3 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.90-0.2.rc3
- updated to 0.90rc3
- splitted mandatory parts from the data-file into a separate -filesystem
  subpackage
- added a -data-empty subpackage to allow a setup where database is
  updated per cron-job and user does not want to download the large
  -data package with outdated virus definitations (#214949)
- %%ghost'ed the files downloaded by freshclam
