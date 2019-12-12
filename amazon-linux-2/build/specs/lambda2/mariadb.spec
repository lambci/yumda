# TokuDB engine is now part of MariaDB, but it is available only for x86_64;
# variable tokudb allows to build with TokuDB storage engine
%bcond_with tokudb

Name: mariadb
Version: 5.5.64
Release: 1%{?dist}
Epoch: 1

Summary: A community developed branch of MySQL
Group: Applications/Databases
URL: http://mariadb.org
# Exceptions allow client libraries to be linked with most open source SW,
# not only GPL code.  See README.mysql-license
# Some innobase code from Percona and Google is under BSD license
# Some code related to test-suite is under LGPLv2
License: GPLv2 with exceptions and LGPLv2 and BSD

# The evr of mysql we want to obsolete
%global obsoleted_mysql_evr 5.5-0

# Regression tests take a long time, you can skip 'em with this
%global runselftest 0

Source0: http://mirror.hosting90.cz/%{name}/%{name}-%{version}/source/%{name}-%{version}.tar.gz
Source3: my.cnf
Source5: my_config.h
Source6: README.mysql-docs
Source7: README.mysql-license
Source8: libmysql.version
Source9: mysql-embedded-check.c
Source10: mariadb.tmpfiles.d
Source11: mariadb.service
Source12: mariadb-prepare-db-dir
Source13: mariadb-wait-ready
Source14: rh-skipped-tests-base.list
Source16: README.mysql-cnf
# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh

# Comments for these patches are in the patch files.
Patch1: mariadb-errno.patch
Patch2: mariadb-strmov.patch
Patch3: mariadb-install-test.patch
Patch7: mariadb-s390-tsc.patch
Patch8: mariadb-logrotate.patch
Patch9: mariadb-cipherreplace.patch
Patch10: mariadb-file-contents.patch
Patch11: mariadb-string-overflow.patch
Patch14: mariadb-basedir.patch
Patch17: mariadb-covscan-signexpr.patch
Patch18: mariadb-covscan-stroverflow.patch
Patch20: mariadb-mysql_secure_installation.patch

BuildRequires: perl, readline-devel, openssl-devel
BuildRequires: cmake, ncurses-devel, zlib-devel, libaio-devel
BuildRequires: systemtap-sdt-devel
BuildRequires: pam-devel
# make test requires time and ps
BuildRequires: time procps
# perl modules needed to run regression tests
BuildRequires: perl(Socket), perl(Time::HiRes)
BuildRequires: perl(Data::Dumper), perl(Test::More), perl(Env)
# version 5.5.56+ requires checkpolicy and policycoreutils-python
BuildRequires: checkpolicy policycoreutils-python

Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: grep, fileutils, bash

# MariaDB replaces mysql packages
Provides: mysql = %{epoch}:%{version}-%{release}
Provides: mysql%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: mysql < %{obsoleted_mysql_evr}

# By default, patch(1) creates backup files when chunks apply with offsets.
# Turn that off to ensure such files don't get included in RPMs (cf bz#884755).
%global _default_patch_flags --no-backup-if-mismatch

Prefix: %{_prefix}

%description
MariaDB is a community developed branch of MySQL.
MariaDB is a multi-user, multi-threaded SQL database server.
It is a client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the standard MariaDB/MySQL client programs and generic MySQL files.

%package libs

Summary: The shared libraries required for MariaDB/MySQL clients
Group: Applications/Databases
Requires: /sbin/ldconfig
Provides: mysql-libs = %{epoch}:%{version}-%{release}
Provides: mysql-libs%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: mysql-libs < %{obsoleted_mysql_evr}
Prefix: %{_prefix}

%description libs
The mariadb-libs package provides the essential shared libraries for any
MariaDB/MySQL client program or interface. You will need to install this
package to use any other MariaDB package or any clients that need to connect
to a MariaDB/MySQL server. MariaDB is a community developed branch of MySQL.

%package server

Summary: The MariaDB server and related files
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: sh-utils
# Make sure it's there when scriptlets run, too
Requires(post): /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
# mysqlhotcopy needs DBI/DBD support
Requires: perl-DBI, perl-DBD-MySQL
Provides: mysql-compat-server = %{epoch}:%{version}-%{release}
Provides: mysql-compat-server%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: mysql-server < %{obsoleted_mysql_evr}
Prefix: %{_prefix}

%description server
MariaDB is a multi-user, multi-threaded SQL database server. It is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MariaDB server and some accompanying files and directories.
MariaDB is a community developed branch of MySQL.

%package embedded

Summary: MariaDB as an embeddable library
Group: Applications/Databases
Requires: /sbin/ldconfig
Obsoletes: mysql-embedded < %{obsoleted_mysql_evr}
Prefix: %{_prefix}

%description embedded
MariaDB is a multi-user, multi-threaded SQL database server. This
package contains a version of the MariaDB server that can be embedded
into a client application instead of running as a separate process.
MariaDB is a community developed branch of MySQL.


%prep
%setup -q -n mariadb-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch14 -p1
%patch17 -p1
%patch18 -p1
%patch20 -p1

# workaround for upstream bug #56342
rm -f mysql-test/t/ssl_8k_key-master.opt

# generate a list of tests that fail, but are not disabled by upstream
cat %{SOURCE14} > mysql-test/rh-skipped-tests.list



%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
	if [ x"`id -u`" = x0 ]; then
		echo "The mariadb's regression tests may fail if run as root."
		echo "If you really need to build the RPM as root, use"
		echo "--define='runselftest 0' to skip the regression tests."
		exit 1
	fi
%endif

CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
# force PIC mode so that we can build libmysqld.so
CFLAGS="$CFLAGS -fPIC"
# gcc seems to have some bugs on sparc as of 4.4.1, back off optimization
# submitted as bz #529298
%ifarch sparc sparcv9 sparc64
CFLAGS=`echo $CFLAGS| sed -e "s|-O2|-O1|g" `
%endif
# significant performance gains can be achieved by compiling with -O3 optimization
# rhbz#1051069
%ifarch %{power64}
CFLAGS=`echo $CFLAGS| sed -e "s|-O2|-O3|g" `
%endif
CXXFLAGS="$CFLAGS"
export CFLAGS CXXFLAGS
# building with PIE
LDFLAGS="$LDFLAGS -fPIE -pie -Wl,-z,relro,-z,now"
export LDFLAGS

# The INSTALL_xxx macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{_datadir} and so forth here.

cmake . -DBUILD_CONFIG=mysql_release \
	-DFEATURE_SET="community" \
	-DINSTALL_LAYOUT=RPM \
	-DRPM="%{?rhel:rhel%{rhel}}%{!?rhel:fedora}" \
	-DCMAKE_INSTALL_PREFIX="%{_prefix}" \
	-DINSTALL_DOCDIR=share/doc/%{name}-%{version} \
	-DINSTALL_DOCREADMEDIR=share/doc/%{name}-%{version} \
	-DINSTALL_INCLUDEDIR=include/mysql \
	-DINSTALL_INFODIR=share/info \
	-DINSTALL_LIBDIR="%{_lib}/mysql" \
	-DINSTALL_MANDIR=share/man \
	-DINSTALL_MYSQLSHAREDIR=share/mysql \
	-DINSTALL_MYSQLTESTDIR=share/mysql-test \
	-DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
	-DINSTALL_SBINDIR=libexec \
	-DINSTALL_SCRIPTDIR=bin \
	-DINSTALL_SQLBENCHDIR=share \
	-DINSTALL_SUPPORTFILESDIR=share/mysql \
	-DINSTALL_SYSCONFDIR=etc \
	-DINSTALL_SYSCONF2DIR=etc/my.cnf.d \
	-DMYSQL_DATADIR="%{_localstatedir}/lib/mysql" \
	-DMYSQL_UNIX_ADDR="%{_localstatedir}/lib/mysql/mysql.sock" \
	-DENABLED_LOCAL_INFILE=ON \
	-DENABLE_DTRACE=no \
	-DWITH_EMBEDDED_SERVER=ON \
	-DWITH_READLINE=no \
	-DWITH_SSL=system \
	-DWITH_ZLIB=system \
	-DWITH_JEMALLOC=no \
%{!?with_tokudb:	-DWITHOUT_TOKUDB=ON}\
	-DTMPDIR=%{_localstatedir}/tmp \
	-DWITH_MYSQLD_LDFLAGS="-Wl,-z,relro,-z,now"

#For CMake "List Advanced Help" about possible arguments and their values
#cmake -LAH

make %{?_smp_mflags} VERBOSE=1

# debuginfo extraction scripts fail to find source files in their real
# location -- satisfy them by copying these files into location, which
# is expected by scripts
for e in innobase xtradb ; do
  for f in pars0grm.c pars0grm.y pars0lex.l lexyy.c ; do
    cp -p "storage/$e/pars/$f" "storage/$e/$f"
  done
done


%install
make DESTDIR=$RPM_BUILD_ROOT install

# List the installed tree for RPM package maintenance purposes.
find $RPM_BUILD_ROOT -print | sed "s|^$RPM_BUILD_ROOT||" | sort > ROOTFILES

# multilib header hacks
# we only apply this to known Red Hat multilib arches, per bug #181335
unamei=$(uname -i)
%ifarch %{arm}
unamei=arm
%endif
%ifarch %{power64}
unamei=ppc64
%endif
%ifarch %{arm} aarch64 %{ix86} x86_64 ppc %{power64} %{sparc} s390 s390x
mv $RPM_BUILD_ROOT%{_includedir}/mysql/my_config.h $RPM_BUILD_ROOT%{_includedir}/mysql/my_config_${unamei}.h
mv $RPM_BUILD_ROOT%{_includedir}/mysql/private/config.h $RPM_BUILD_ROOT%{_includedir}/mysql/private/my_config_${unamei}.h
install -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_includedir}/mysql/
install -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_includedir}/mysql/private/config.h
%endif

# cmake generates some completely wacko references to -lprobes_mysql when
# building with dtrace support.  Haven't found where to shut that off,
# so resort to this blunt instrument.  While at it, let's not reference
# libmysqlclient_r anymore either.
sed -e 's/-lprobes_mysql//' -e 's/-lmysqlclient_r/-lmysqlclient/' \
	${RPM_BUILD_ROOT}%{_bindir}/mysql_config >mysql_config.tmp
cp -p -f mysql_config.tmp ${RPM_BUILD_ROOT}%{_bindir}/mysql_config
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/mysql_config

# install INFO_SRC, INFO_BIN into libdir (upstream thinks these are doc files,
# but that's pretty wacko --- see also mariadb-file-contents.patch)
install -p -m 644 Docs/INFO_SRC ${RPM_BUILD_ROOT}%{_libdir}/mysql/
install -p -m 644 Docs/INFO_BIN ${RPM_BUILD_ROOT}%{_libdir}/mysql/
rm -rf ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/MariaDB-server-%{version}/

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/mariadb
chmod 0750 $RPM_BUILD_ROOT%{_localstatedir}/log/mariadb
touch $RPM_BUILD_ROOT%{_localstatedir}/log/mariadb/mariadb.log

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/mariadb
install -m 0755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/mysql

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/my.cnf

# install systemd unit files and scripts for handling server startup
install -p -m 755 %{SOURCE12} ${RPM_BUILD_ROOT}%{_libexecdir}/
install -p -m 755 %{SOURCE13} ${RPM_BUILD_ROOT}%{_libexecdir}/

mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
install -p -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_tmpfilesdir}/%{name}.conf

# Fix funny permissions that cmake build scripts apply to config files
#chmod 644 ${RPM_BUILD_ROOT}%{_datadir}/mysql/config.*.ini

# Fix scripts for multilib safety
mv ${RPM_BUILD_ROOT}%{_bindir}/mysql_config ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysql_config
touch ${RPM_BUILD_ROOT}%{_bindir}/mysql_config

mv ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysqlbug
touch ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug

# Remove libmysqld.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.a

# libmysqlclient_r is no more.  Upstream tries to replace it with symlinks
# but that really doesn't work (wrong soname in particular).  We'll keep
# just the devel libmysqlclient_r.so link, so that rebuilding without any
# source change is enough to get rid of dependency on libmysqlclient_r.
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so*
ln -s libmysqlclient.so ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so

# mysql-test includes one executable that doesn't belong under /usr/share,
# so move it and provide a symlink
mv ${RPM_BUILD_ROOT}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process ${RPM_BUILD_ROOT}%{_bindir}
ln -s ../../../../../bin/my_safe_process ${RPM_BUILD_ROOT}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process

# should move this to /etc/ ?
rm -f ${RPM_BUILD_ROOT}%{_bindir}/mysql_embedded
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/*.a
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/binary-configure
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/magic
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/ndb-config-2-node.ini
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql.server
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysqld_multi.server
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-stress-test.pl.1*
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-test-run.pl.1*
rm -f ${RPM_BUILD_ROOT}%{_bindir}/mytop

# put logrotate script where it needs to be
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mv ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql-log-rotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mariadb
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mariadb

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/mysql" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

# copy additional docs into build tree so %%doc will find them
cp -p %{SOURCE6} README.mysql-docs
cp -p %{SOURCE7} README.mysql-license
cp -p %{SOURCE16} README.mysql-cnf
install -p -m 0644 README.mysql-cnf ${RPM_BUILD_ROOT}%{_datadir}/mysql/README.mysql-cnf

# install the list of skipped tests to be available for user runs
install -p -m 0644 mysql-test/rh-skipped-tests.list ${RPM_BUILD_ROOT}%{_datadir}/mysql-test

# remove unneeded RHEL-4 SELinux stuff
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/mysql/SELinux/

# remove SysV init script
rm -f ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d/mysql

# remove duplicate logrotate script
rm -f ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/mysql

# remove doc files that we rather pack using %%doc
rm -f ${RPM_BUILD_ROOT}%{_datadir}/doc/COPYING
rm -f ${RPM_BUILD_ROOT}%{_datadir}/doc/INFO_BIN
rm -f ${RPM_BUILD_ROOT}%{_datadir}/doc/INFO_SRC
rm -f ${RPM_BUILD_ROOT}%{_datadir}/doc/INSTALL-BINARY
rm -f ${RPM_BUILD_ROOT}%{_datadir}/doc/README

# we don't care about scripts for solaris
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/solaris/postinstall-solaris

sed -i '1 s|^#!/usr/bin/perl|#!%{_bindir}/perl|' %{buildroot}%{_bindir}/*

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/alternatives

%post server
/usr/sbin/update-alternatives --altdir %{_sysconfdir}/alternatives --install %{_bindir}/mysqlbug \
	mysqlbug %{_libdir}/mysql/mysqlbug %{__isa_bits}

%postun server
if [ $1 -eq 0 ] ; then
	/usr/sbin/update-alternatives --altdir %{_sysconfdir}/alternatives --remove mysqlbug %{_libdir}/mysql/mysqlbug
fi


%files
%license COPYING README.mysql-license storage/innobase/COPYING.Percona storage/innobase/COPYING.Google
%{_bindir}/msql2mysql
%{_bindir}/mysql
%{_bindir}/mysql_find_rows
%{_bindir}/mysql_waitpid
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{?with_tokudb:%{_bindir}/tokuftdump}
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/my_print_defaults
%{_bindir}/aria_chk
%{_bindir}/aria_dump_log
%{_bindir}/aria_ftdump
%{_bindir}/aria_pack
%{_bindir}/aria_read_log
%config(noreplace) %{_sysconfdir}/my.cnf.d/client.cnf

%files libs
%license COPYING README.mysql-license storage/innobase/COPYING.Percona storage/innobase/COPYING.Google
# although the default my.cnf contains only server settings, we put it in the
# libs package because it can be used for client settings too.
%config(noreplace) %{_sysconfdir}/my.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%dir %{_sysconfdir}/my.cnf.d
%dir %{_libdir}/mysql
%{_libdir}/mysql/libmysqlclient.so.*
%{_libdir}/mysql/plugin/dialog.so
%{_libdir}/mysql/plugin/mysql_clear_password.so
%{_sysconfdir}/ld.so.conf.d/*
%dir %{_datadir}/mysql
%{_datadir}/mysql/english
%lang(cs) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(nl) %{_datadir}/mysql/dutch
%lang(et) %{_datadir}/mysql/estonian
%lang(fr) %{_datadir}/mysql/french
%lang(de) %{_datadir}/mysql/german
%lang(el) %{_datadir}/mysql/greek
%lang(hu) %{_datadir}/mysql/hungarian
%lang(it) %{_datadir}/mysql/italian
%lang(ja) %{_datadir}/mysql/japanese
%lang(ko) %{_datadir}/mysql/korean
%lang(no) %{_datadir}/mysql/norwegian
%lang(no) %{_datadir}/mysql/norwegian-ny
%lang(pl) %{_datadir}/mysql/polish
%lang(pt) %{_datadir}/mysql/portuguese
%lang(ro) %{_datadir}/mysql/romanian
%lang(ru) %{_datadir}/mysql/russian
%lang(sr) %{_datadir}/mysql/serbian
%lang(sk) %{_datadir}/mysql/slovak
%lang(es) %{_datadir}/mysql/spanish
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian
%{_datadir}/mysql/charsets

%files server
%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_install_db
%{_bindir}/mysql_plugin
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_upgrade
%{_bindir}/mysql_zap
%ghost %{_bindir}/mysqlbug
%{_bindir}/mysqldumpslow
%{_bindir}/mysqld_multi
%{_bindir}/mysqld_safe
%{_bindir}/mysqld_safe_helper
%{_bindir}/mysqlhotcopy
%{_bindir}/mysqltest
%{_bindir}/innochecksum
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip
%config(noreplace) %{_sysconfdir}/my.cnf.d/server.cnf
%{?with_tokudb:%config(noreplace) %{_sysconfdir}/my.cnf.d/tokudb.cnf}
%{_libexecdir}/mysqld
%{_libdir}/mysql/INFO_SRC
%{_libdir}/mysql/INFO_BIN
%{_libdir}/mysql/mysqlbug
%exclude %{_libdir}/mysql/plugin/dialog.so
%exclude %{_libdir}/mysql/plugin/mysql_clear_password.so
%{_libdir}/mysql/plugin
%{_datadir}/mysql/errmsg-utf8.txt
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/mysql_performance_tables.sql
%{_libexecdir}/mariadb-prepare-db-dir
%{_libexecdir}/mariadb-wait-ready
%{_tmpfilesdir}/%{name}.conf
%attr(0755,mysql,mysql) %dir %{_localstatedir}/run/mariadb
%attr(0755,mysql,mysql) %dir %{_localstatedir}/lib/mysql
%attr(0750,mysql,mysql) %dir %{_localstatedir}/log/mariadb
%attr(0640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) %{_localstatedir}/log/mariadb/mariadb.log
%config(noreplace) %{_sysconfdir}/logrotate.d/mariadb
%dir %{_sysconfdir}/alternatives

%files embedded
%license COPYING README.mysql-license storage/innobase/COPYING.Percona storage/innobase/COPYING.Google
%{_libdir}/mysql/libmysqld.so.*

%exclude %{_includedir}
%exclude %{_libdir}/mysql/libmysqlclient.so
%exclude %{_libdir}/mysql/libmysqlclient_r.so
%exclude %{_libdir}/mysql/mysql_config
%exclude %{_libdir}/mysql/libmysqld.so
%exclude %{_bindir}/mysql_config
%exclude %{_bindir}/mysql_client_test_embedded
%exclude %{_bindir}/mysqltest_embedded
%exclude %{_bindir}/mysql_client_test
%exclude %{_bindir}/my_safe_process
%exclude %{_datadir}/aclocal
%exclude %{_datadir}/mysql/my-*.cnf
%exclude %{_datadir}/mysql/README.mysql-cnf
%exclude %{_datadir}/sql-bench
%exclude %{_datadir}/mysql-test
%exclude %{_mandir}


%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu May 02 2019 Michal Schorm <mschorm@redhat.com> - 1:5.5.64-1
- Rebase to 5.5.64
- Resolves: #1490398
- CVE's fixed: #1610986
  CVE-2018-3058 CVE-2018-3063 CVE-2018-3066 CVE-2018-3081
- CVE's fixed: #1664043
  CVE-2018-3282 CVE-2019-2503
- CVE's fixed: #1701686
  CVE-2019-2529

* Thu May 10 2018 Michal Schorm <mschorm@redhat.com> - 1:5.5.60-1
- Rebase to 5.5.60
- CVE's fixed: #1558256, #1558260, #1559060
  CVE-2017-3636 CVE-2017-3641 CVE-2017-3653 CVE-2017-10379
  CVE-2017-10384 CVE-2017-10378 CVE-2017-10268 CVE-2018-2562
  CVE-2018-2622 CVE-2018-2640 CVE-2018-2665 CVE-2018-2668
  CVE-2018-2755 CVE-2018-2819 CVE-2018-2817 CVE-2018-2761
  CVE-2018-2781 CVE-2018-2771 CVE-2018-2813
- Resolves: #1535217, #1491833, #1511982, #1145455, #1461692

* Thu Jun 08 2017 Honza Horak <hhorak@redhat.com> - 1:5.5.56-2
- Do not fix context and change owner if run by root in mariadb-prepare-db-dir
  Related: #1458940
- Check properly that datadir includes only expected files
  Related: #1356897

* Mon Jun 05 2017 Honza Horak <hhorak@redhat.com> - 1:5.5.56-1
- Rebase to 5.5.56
  That release also fixes the following security issues:
  CVE-2016-5617/CVE-2016-6664 CVE-2017-3312 CVE-2017-3238 CVE-2017-3243
  CVE-2017-3244 CVE-2017-3258 CVE-2017-3313 CVE-2017-3317 CVE-2017-3318
  CVE-2017-3291 CVE-2017-3302 CVE-2016-5483/CVE-2017-3600 CVE-2017-3308
  CVE-2017-3309 CVE-2017-3453 CVE-2017-3456 CVE-2017-3464
  Resolves: #1458933
  New deps required by upstream: checkpolicy and policycoreutils-python
  License text removed by upstream: COPYING.LESSER
  Do not ignore test-suite failure
  Downstream script mariadb-prepare-db-dir fixed for CVE-2017-3265
  Resolves: #1458940

* Tue Mar 21 2017 Michal Schorm <mschorm@redhat.com> - 5.5.52-2
- Extension of mariadb-prepare-db-dir script
- Resolves: #1356897

- Rebase to 5.5.52, that also include fix for CVE-2016-6662
  Resolves: #1377974

* Wed Sep 21 2016 Honza Horak <hhorak@redhat.com> - 5.5.52-1
- Rebase to 5.5.52, that also include fix for CVE-2016-6662
  Resolves: #1377974

* Wed Aug 24 2016 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.50-2
- Rebuild
  Related: #1359629

* Mon Jul 25 2016 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.50-1
- Rebase to 5.5.50
  Resolves: #1359629

* Thu Jul 07 2016 Honza Horak <hhorak@redhat.com> - 1:5.5.47-5
- Use full relro instead of just pie
  Resolves: #1335863

* Mon May 09 2016 Honza Horak <hhorak@redhat.com> - 1:5.5.47-4
- dialog.so and mysql_clear_password.so should be in mariadb-libs package
  Resolves: #1138843

* Tue Apr 26 2016 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.47-3
- Fixed mysql_secure_installation
  Resolves: #1186040

* Thu Feb 18 2016 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.47-2
- Add warning to /usr/lib/tmpfiles.d/mariadb.conf
  Resolves: #1241623

* Wed Feb  3 2016 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.47-1
- Rebase to 5.5.47
  Also fixes: CVE-2015-4792 CVE-2015-4802 CVE-2015-4815 CVE-2015-4816
  CVE-2015-4819 CVE-2015-4826 CVE-2015-4830 CVE-2015-4836 CVE-2015-4858
  CVE-2015-4861 CVE-2015-4870 CVE-2015-4879 CVE-2015-4913 CVE-2015-7744
  CVE-2016-0505 CVE-2016-0546 CVE-2016-0596 CVE-2016-0597 CVE-2016-0598
  CVE-2016-0600 CVE-2016-0606 CVE-2016-0608 CVE-2016-0609 CVE-2016-0616
  CVE-2016-2047
  Resolves: #1300621

* Thu Jan 21 2016 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.44-3
- MDEV-8827 Duplicate key with auto increment
  fix innodb auto-increment handling three bugs:
    1. innobase_next_autoinc treated the case of current<offset incorrectly
    2. ha_innobase::get_auto_increment didn't recalculate current when increment changed
    3. ha_innobase::get_auto_increment didn't pass offset down to innobase_next_autoinc
  Resolves: #1300621

* Mon Sep 21 2015 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.44-2
- Rebuild
  Related: #1247022

* Tue Jul 28 2015 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.44-1
- Rebase to 5.5.44
  Resolves: #1247022

* Wed Jul  8 2015 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.41-3
- rebuild for correct systemtap markers on aarch64
  Resolves: #1238468

* Thu Jan 29 2015 Honza Horak <hhorak@redhat.com> - 1:5.5.41-2
- Include new certificate for tests
  Resolves: #1186110

* Tue Jan 27 2015 Matej Muzila <mmuzila@redhat.com> - 1:5.5.41-1
- Rebase to 5.5.41
  Also fixes: CVE-2014-6568 CVE-2015-0374 CVE-2015-0381 CVE-2015-0382
  CVE-2015-0391 CVE-2015-0411 CVE-2015-0432
  Resolves: #1186110

* Tue Dec 30 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.40-2
- Fix header to let dependencies to build fine
  Resolves: #1166603

* Thu Nov 06 2014 Matej Muzila <mmuzila@redhat.com> - 1:5.5.40-1
- Rebase to 5.5.40
  Also fixes: CVE-2014-4274 CVE-2014-4287 CVE-2014-6463 CVE-2014-6464
  CVE-2014-6469 CVE-2014-6484 CVE-2014-6505 CVE-2014-6507 CVE-2014-6520
  CVE-2014-6530 CVE-2014-6551 CVE-2014-6555 CVE-2014-6559 CVE-2014-6564
  Resolves: #1160549

* Thu Aug 21 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.37-3
- Fix my_config.h to include correct header
  Related: #1123497

* Tue Aug 19 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.37-2
- Build with -O3 on all power64 arches
  Disable some failing tests temporarily on ppc64le
  Resolves: #1123497

* Mon May 26 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.37-1
- Rebase to 5.5.37
  https://kb.askmonty.org/en/mariadb-5537-changelog/
  Also fixes: CVE-2014-2440 CVE-2014-0384 CVE-2014-2432 CVE-2014-2431
  CVE-2014-2430 CVE-2014-2436 CVE-2014-2438 CVE-2014-2419
  Resolves: #1101062

* Thu Mar 06 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.35-3
- Fix a typo in last commit
  Related: #1069586

* Wed Feb 26 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.35-2
- Remove unnecessary pid guessing and include README for included cnf files
  Resolves: #1069586

* Thu Jan 30 2014 Honza Horak <hhorak@redhat.com> 5.5.35-1
- Rebase to 5.5.35
  https://kb.askmonty.org/en/mariadb-5535-changelog/
  Also fixes: CVE-2014-0001, CVE-2014-0412, CVE-2014-0437, CVE-2013-5908,
  CVE-2014-0420, CVE-2014-0393, CVE-2013-5891, CVE-2014-0386, CVE-2014-0401,
  CVE-2014-0402
  Resolves: #1054041

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:5.5.34-6
- Mass rebuild 2014-01-24

* Tue Jan 14 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.34-5
- Adopt compatible system versioning
  Resolves: #1045013

* Mon Jan 13 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-4
- Fix alternatives calls for mysql_config
  Related: #1050920

* Fri Jan 10 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-3
- Clean all non-needed doc files properly
  Related: #1044532
- Disable main.gis-precise test also for AArch64
  Disable perfschema.func_file_io and perfschema.func_mutex for AArch64
  (like it is done for 32-bit ARM)
  Resolves: #1050988
- Build with -O3 on ppc64 (disabling innodb_prefix_index_restart_server)
  Related: #1051069
- Move mysql_config to -devel sub-package and remove Require: mariadb
  Resolves: #1050920

* Tue Jan  7 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-1
- Rebase to 5.5.34
- Obsolete mysql packages
  Resolves: #1043971
- Don't test EDH-RSA-DES-CBC-SHA cipher, it seems to be removed from openssl
  which now makes mariadb/mysql FTBFS because openssl_1 test fails
  Resolves: #1048881
- Check if socket file is not being used by another process at a time
  of starting the service
  Resolves: #1045435

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:5.5.33a-4
- Mass rebuild 2013-12-27

* Mon Nov  4 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-3
- Check if correct process is running in mysql-wait-ready script
  Resolves: #1026313

* Mon Nov  4 2013 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.33a-2
- Add pam-devel to BuildRequires for auth_pam.so to be built
  Resolves: #1019945

* Wed Oct 23 2013 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.33a-1
- Rebase to 5.5.33a
- Disable main.mysql_client_test_nonblock on i686
  Resolves: #1020032

* Wed Oct  9 2013 Jakub Dorňák <jdornak@redhat.com> - 1:5.5.32-11
- Remove outfile_loaddata from rh-skipped-tests-base.list
  Resolves: #950489

* Wed Sep  4 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-10
- Multilib issues solved by alternatives
  Resolves: #986959

* Thu Aug 29 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-9
- Move log file into /var/log/mariadb/mariadb.log
- Rename logrotate script to mariadb
- Resolves: #999589

* Mon Aug 19 2013 Honza Horak <hhorak@redhat.com> 5.5.32-8
- Fix comments in mariadb.service file

* Wed Jul 31 2013 Honza Horak <hhorak@redhat.com> 5.5.32-7
- Do not use login shell for mysql user

* Tue Jul 30 2013 Honza Horak <hhorak@redhat.com> 5.5.32-6
- Remove unneeded systemd-sysv requires
- Provide mysql-compat-server symbol
- Create mariadb.service symlink
- Fix multilib header location for arm
- Enhance documentation in the unit file
- Use scriptstub instead of links to avoid multilib conflicts
- Revert docs in unversioned dir
- Remove mysql provides from server-side and obsoleting mysql
- Revert explicit enabling mysqld in the beggining of the transaction

* Sun Jul 28 2013 Dennis Gilmore <dennis@ausil.us> - 5.5.32-5
- remove "Requires(pretrans): systemd" since its not possible
- when installing mariadb and systemd at the same time. as in a new install

* Sat Jul 27 2013 Kevin Fenzi <kevin@scrye.com> 5.5.32-4
- Set rpm doc macro to install docs in unversioned dir

* Fri Jul 26 2013 Dennis Gilmore <dennis@ausil.us> 5.5.32-3
- add Requires(pre) on systemd for the server package

* Tue Jul 23 2013 Dennis Gilmore <dennis@ausil.us> 5.5.32-2
- replace systemd-units requires with systemd
- remove solaris files

* Fri Jul 19 2013 Honza Horak <hhorak@redhat.com> 5.5.32-1
- Rebase to 5.5.32
  https://kb.askmonty.org/en/mariadb-5532-changelog/
- Clean-up un-necessary systemd snippets

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:5.5.31-7
- Perl 5.18 rebuild

* Mon Jul  1 2013 Honza Horak <hhorak@redhat.com> 5.5.31-6
- Test suite params enhanced to decrease server condition influence
- Fix misleading error message when uninstalling built-in plugins
  Related: #966873

* Thu Jun 27 2013 Honza Horak <hhorak@redhat.com> 5.5.31-5
- Apply fixes found by Coverity static analysis tool

* Wed Jun 19 2013 Honza Horak <hhorak@redhat.com> 5.5.31-4
- Do not use pretrans scriptlet, which doesn't work in anaconda
  Resolves: #975348

* Fri Jun 14 2013 Honza Horak <hhorak@redhat.com> 5.5.31-3
- Explicitly enable mysqld if it was enabled in the beggining
  of the transaction.

* Thu Jun 13 2013 Honza Horak <hhorak@redhat.com> 5.5.31-2
- Apply man page fix from Jan Stanek

* Fri May 24 2013 Honza Horak <hhorak@redhat.com> 5.5.31-1
- Rebase to 5.5.31
  https://kb.askmonty.org/en/mariadb-5531-changelog/
- Preserve time-stamps in case of installed files
- Use /var/tmp instead of /tmp, since the later is using tmpfs,
  which can cause problems
  Resolves: #962087
- Fix test suite requirements

* Sun May  5 2013 Honza Horak <hhorak@redhat.com> 5.5.30-2
- Remove mytop utility, which is packaged separately
- Resolve multilib conflicts in mysql/private/config.h

* Fri Mar 22 2013 Honza Horak <hhorak@redhat.com> 5.5.30-1
- Rebase to 5.5.30
  https://kb.askmonty.org/en/mariadb-5530-changelog/

* Fri Mar 22 2013 Honza Horak <hhorak@redhat.com> 1:5.5.29-11
- Obsolete MySQL since it is now renamed to community-mysql
- Remove real- virtual names

* Thu Mar 21 2013 Honza Horak <hhorak@redhat.com> 1:5.5.29-10
- Adding epoch to have higher priority than other mysql implementations
  when comes to provider comparison

* Wed Mar 13 2013 Honza Horak <hhorak@redhat.com> 5.5.29-9
- Let mariadb-embedded-devel conflict with MySQL-embedded-devel
- Adjust mariadb-sortbuffer.patch to correspond with upstream patch

* Mon Mar  4 2013 Honza Horak <hhorak@redhat.com> 5.5.29-8
- Mask expected warnings about setrlimit in test suite

* Thu Feb 28 2013 Honza Horak <hhorak@redhat.com> 5.5.29-7
- Use configured prefix value instead of guessing basedir
  in mysql_config
Resolves: #916189
- Export dynamic columns and non-blocking API functions documented
  by upstream

* Wed Feb 27 2013 Honza Horak <hhorak@redhat.com> 5.5.29-6
- Fix sort_buffer_length option type

* Wed Feb 13 2013 Honza Horak <hhorak@redhat.com> 5.5.29-5
- Suppress warnings in tests and skip tests also on ppc64p7

* Tue Feb 12 2013 Honza Horak <hhorak@redhat.com> 5.5.29-4
- Suppress warning in tests on ppc
- Enable fixed index_merge_myisam test case

* Thu Feb 07 2013 Honza Horak <hhorak@redhat.com> 5.5.29-3
- Packages need to provide also %%_isa version of mysql package
- Provide own symbols with real- prefix to distinguish from mysql
  unambiguously
- Fix format for buffer size in error messages (MDEV-4156)
- Disable some tests that fail on ppc and s390
- Conflict only with real-mysql, otherwise mariadb conflicts with ourself

* Tue Feb 05 2013 Honza Horak <hhorak@redhat.com> 5.5.29-2
- Let mariadb-libs to own /etc/my.cnf.d

* Thu Jan 31 2013 Honza Horak <hhorak@redhat.com> 5.5.29-1
- Rebase to 5.5.29
  https://kb.askmonty.org/en/mariadb-5529-changelog/
- Fix inaccurate default for socket location in mysqld-wait-ready
  Resolves: #890535

* Thu Jan 31 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-8
- Enable obsoleting mysql

* Wed Jan 30 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-7
- Adding necessary hacks for perl dependency checking, rpm is still
  not wise enough
- Namespace sanity re-added for symbol default_charset_info

* Mon Jan 28 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-6
- Removed %%{_isa} from provides/obsoletes, which doesn't allow
  proper obsoleting
- Do not obsolete mysql at the time of testing

* Thu Jan 10 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-5
- Added licenses LGPLv2 and BSD
- Removed wrong usage of %%{epoch}
- Test-suite is run in %%check
- Removed perl dependency checking adjustment, rpm seems to be smart enough
- Other minor spec file fixes

* Tue Dec 18 2012 Honza Horak <hhorak@redhat.com> 5.5.28a-4
- Packaging of MariaDB based on MySQL package

