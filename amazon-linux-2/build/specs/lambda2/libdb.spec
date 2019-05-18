%define __soversion_major 5
%define __soversion %{__soversion_major}.3

%define _trivial .0
%define _buildid .1
Summary: The Berkeley DB database library for C
Name: libdb
Version: 5.3.21
Release: 24%{?dist}.0.3
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: http://download.oracle.com/berkeley-db/db.1.85.tar.gz
# libdb man pages generated from the 5.3.21 documentation
Source2: libdb-5.3.21-manpages.tar.gz
Patch0: libdb-multiarch.patch
# db-1.85 upstream patches
Patch10: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.1
Patch11: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.2
Patch12: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.3
Patch13: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.4
# other patches
Patch20: db-1.85-errno.patch
Patch22: db-4.6.21-1.85-compat.patch
Patch24: db-4.5.20-jni-include-dir.patch
# License clarification patch
# http://devel.trisquel.info/gitweb/?p=package-helpers.git;a=blob;f=helpers/DATA/db4.8/007-mt19937db.c_license.patch;h=1036db4d337ce4c60984380b89afcaa63b2ef88f;hb=df48d40d3544088338759e8bea2e7f832a564d48
Patch25: 007-mt19937db.c_license.patch
# sqlite3 overflow fix backport
Patch26: signed-overflow.patch
# CDB race (rhbz #1099509)
Patch27: libdb-cbd-race.patch
# Limit concurrency to max 1024 CPUs
Patch28: libdb-limit-cpu.patch
Patch29: libdb-5.3.21-mutex_leak.patch
# Upstream acknowledged and agreed to use it
Patch30: libdb-5.3.21-region-size-check.patch
# Patch sent upstream
Patch31: checkpoint-opd-deadlock.patch

Patch32: libdb-db_hotbackup-manpages.patch

# Amazon patches
Patch10001: libdb-5.3.21-gcc7x.patch

URL: http://www.oracle.com/database/berkeley-db/
License: BSD and LGPLv2 and Sleepycat
Group: System Environment/Libraries
BuildRequires: perl libtool
BuildRequires: tcl-devel >= 8.5.2-3
BuildRequires: chrpath
Conflicts: filesystem < 3
Obsoletes: db4 < 5

Prefix: %{_prefix}

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package utils
Summary: Command line tools for managing Berkeley DB databases
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: db4-utils < 5
Prefix: %{_prefix}

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. DB supports C, C++, Java and Perl APIs.

%package cxx
Summary: The Berkeley DB database library for C++
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: db4-cxx < 5
Prefix: %{_prefix}

%description cxx
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package tcl
Summary: Development files for using the Berkeley DB with tcl
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: db4-tcl < 5
Prefix: %{_prefix}

%description tcl
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Tcl.

%package sql
Summary: Development files for using the Berkeley DB with sql
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: db4-sql < 5
Prefix: %{_prefix}

%description sql
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in SQL.

%prep
%setup -q -n db-%{version} -a 1
tar -xf %{SOURCE2}

%patch0 -p1
pushd db.1.85/PORT/linux
%patch10 -p0
popd
pushd db.1.85
%patch11 -p0
%patch12 -p0
%patch13 -p0
%patch20 -p1
popd

%patch22 -p1
%patch24 -p1
%patch25 -p1

%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1

%patch10001 -p1

cd dist
./s_config

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
CFLAGS="$CFLAGS -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_FTS3=3 -DSQLITE_ENABLE_RTREE=1 -DSQLITE_SECURE_DELETE=1 -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -I../../../lang/sql/sqlite/ext/fts3/"
export CFLAGS

# Build the old db-185 libraries.
make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

test -d dist/dist-tls || mkdir dist/dist-tls
# Static link db_dump185 with old db-185 libraries.
/bin/sh libtool --tag=CC --mode=compile	%{__cc} $RPM_OPT_FLAGS -Idb.1.85/PORT/%{_os}/include -D_REENTRANT -c util/db_dump185.c -o dist/dist-tls/db_dump185.lo
/bin/sh libtool --tag=LD --mode=link %{__cc} -o dist/dist-tls/db_dump185 %{__global_ldflags} dist/dist-tls/db_dump185.lo db.1.85/PORT/%{_os}/libdb.a

# update gnu-config files for aarch64
cp /usr/lib/rpm/redhat/config.guess dist
cp /usr/lib/rpm/redhat/config.sub   dist
cp /usr/lib/rpm/redhat/config.guess lang/sql/sqlite
cp /usr/lib/rpm/redhat/config.sub   lang/sql/sqlite
cp /usr/lib/rpm/redhat/config.guess lang/sql/jdbc
cp /usr/lib/rpm/redhat/config.sub   lang/sql/jdbc
cp /usr/lib/rpm/redhat/config.guess lang/sql/odbc
cp /usr/lib/rpm/redhat/config.sub   lang/sql/odbc

pushd dist/dist-tls
ln -sf ../configure .
%configure -C \
	--enable-compat185 --enable-dump185 \
	--enable-shared \
	--enable-tcl --with-tcl=%{_libdir} \
	--enable-cxx --enable-sql \
	--disable-java \
	--enable-test \
	--disable-rpath \
  --disable-static \
	--with-tcl=/usr/lib64/tcl8.5

# Remove libtool predep_objects and postdep_objects wonkiness so that
# building without -nostdlib doesn't include them twice.  Because we
# already link with g++, weird stuff happens if you don't let the
# compiler handle this.
perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
perl -pi -e 's/-shared -nostdlib/-shared/' libtool

make %{?_smp_mflags}
popd

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

# Force off stripping of installed binaries
%makeinstall STRIP=/bin/true -C dist/dist-tls

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so*

# Eliminate installed doco
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/docs

# XXX Avoid Permission denied. strip when building as non-root.
chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*

# remove RPATHs
chrpath -d ${RPM_BUILD_ROOT}%{_libdir}/*.so ${RPM_BUILD_ROOT}%{_bindir}/*

%files
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libdb-%{__soversion}.so
%{_libdir}/libdb-%{__soversion_major}.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_replicate
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify
%{_bindir}/db*_tuner

%files cxx
%defattr(-,root,root,-)
%{_libdir}/libdb_cxx-%{__soversion}.so
%{_libdir}/libdb_cxx-%{__soversion_major}.so

%files tcl
%defattr(-,root,root,-)
%{_libdir}/libdb_tcl-%{__soversion}.so
%{_libdir}/libdb_tcl-%{__soversion_major}.so

%files sql
%defattr(-,root,root,-)
%{_libdir}/libdb_sql-%{__soversion}.so
%{_libdir}/libdb_sql-%{__soversion_major}.so

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/libdb.so
%exclude %{_libdir}/libdb_cxx.so
%exclude %{_libdir}/libdb_tcl.so
%exclude %{_libdir}/libdb_sql.so
%exclude %{_bindir}/dbsql

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Jan 11 2018 Matej Mužila <mmuzila@redhat.com> - 5.3.21-24
- Link db_dump185 with %{__global_ldflags}. Resolves: rhbz#1460077

* Tue Dec 19 2017 Matej Mužila <mmuzila@redhat.com> - 5.3.21-23
- Mention in man page that care should be taken when running db_hotbackup
  with -c option. Resolves: rhbz#1460077

* Tue Oct 31 2017 Petr Kubat <pkubat@redhat.com> 5.3.21-22
- Fix deadlocks when reading/writing off-page duplicate tree (#1349779)

* Thu Sep 07 2017 Petr Kubat <pkubat@redhat.com> 5.3.21-21
- Fail properly when encountering removed or 0-byte regions (#1471011)

* Mon Mar 20 2017 Petr Kubat <pkubat@redhat.com> 5.3.21-20
- Add man pages for libdb-utils (#1395665)

* Wed Dec 14 2016 Petr Kubat <pkubat@redhat.com> - 5.3.21-20
- Fix mutexes not being released properly (#1277887)

* Thu Sep 03 2015 Jan Stanek <jstanek@redhat.com> - 5.3.21-19
- Add patch to workaround issues on large systems (>1024 CPU)
  Resolves: #1245410

* Thu Jul 24 2014 Honza Horak <hhorak@redhat.com> - 5.3.21-18
- Concurrent access due to a race in CDB
  Resolves: #1099509

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 5.3.21-17
- Mass rebuild 2014-01-24

* Thu Jan 16 2014 Jan Stanek <jstanek@redhat.com> - 5.3.21-16
- Added Obsoletes in order to override unsupported db4 versions

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 5.3.21-15
- Mass rebuild 2013-12-27

* Tue Nov 05 2013 Jan Stanek <jstanek@redhat.com> - 5.3.21-14
- Backported fix for possible signed overflow (#1026878)

* Tue Nov 05 2013 Jan Stanek <jstanek@redhat.com> - 5.3.21-13
- Updated config files for the aarch64 (#1023795)

* Wed Oct 23 2013 Jan Stanek <jstanek@redhat.com> - 5.3.21-12
- Added Sleepycat to the license list

* Thu May 16 2013 Jan Stanek <jstanek@redhat.com> - 5.3.21-11
- Fix missing debuginfo issue for utils subpackage

* Thu May  9 2013 Tom Callaway <spot@fedoraproject.org> - 5.3.21-10
- add license clarification fix

* Wed Apr 03 2013 Jan Stanek <jstanek@redhat.com> 5.3.21-9
- Added sqlite compability CFLAGS (#788496)

* Wed Mar 27 2013 Jan Stanek <jstanek@redhat.com> 5.3.21-8
- Cleaning the specfile - removed gcc-java dependecy other way

* Wed Mar 27 2013 Jan Stanek <jstanek@redhat.com> 5.3.21-7
- Removed dependency on obsolete gcc-java package (#927742)

* Thu Mar  7 2013 Jindrich Novy <jnovy@redhat.com> 5.3.21-6
- add LGPLv2+ and remove Sleepycat in license tag (#886838)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Tom Callaway <spot@fedoraproject.org> - 5.3.21-4
- fix license tag

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 5.3.21-2
- Specify tag for libtool (fixes FTBFS # 838334 )

* Thu Jul  5 2012 Jindrich Novy <jnovy@redhat.com> 5.3.21-1
- update to 5.3.21
http://download.oracle.com/otndocs/products/berkeleydb/html/changelog_5_3.html

* Tue Jul  3 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-5
- move C++ header files to cxx-devel

* Tue Jul  3 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-4
- fix -devel packages dependencies yet more (#832225)

* Sun May  6 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-3
- package -devel packages correctly

* Sat Apr 21 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-2
- fix multiarch conflict in libdb-devel (#812901)
- remove unneeded dos2unix BR

* Thu Mar 15 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-1
- update to 5.3.15
  http://download.oracle.com/otndocs/products/berkeleydb/html/changelog_5_3.html

* Fri Feb 17 2012 Deepak Bhole <dbhole@redhat.com> 5.2.36-5
- Resolves rhbz#794472
- Patch from Omair Majid <omajid@redhat.com> to remove explicit Java 6 req.

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 5.2.36-4
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 5.2.36-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Jindrich Novy <jnovy@redhat.com> 5.2.36-1
- update to 5.2.36,
  http://download.oracle.com/otndocs/products/berkeleydb/html/changelog_5_2.html#id3647664

* Wed Jun 15 2011 Jindrich Novy <jnovy@redhat.com> 5.2.28-2
- move development documentation to devel-doc subpackage (#705386)

* Tue Jun 14 2011 Jindrich Novy <jnovy@redhat.com> 5.2.28-1
- update to 5.2.28

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Jindrich Novy <jnovy@redhat.com> 5.1.25-1
- update to 5.1.25

* Wed Sep 29 2010 jkeating - 5.1.19-2
- Rebuilt for gcc bug 634757

* Fri Sep 10 2010 Jindrich Novy <jnovy@redhat.com> 5.1.19-1
- update to 5.1.19
- rename -devel-static to -static subpackage (#617800)
- build java on all arches

* Wed Jul  7 2010 Jindrich Novy <jnovy@redhat.com> 5.0.26-1
- update to 5.0.26
- drop BR: ed

* Thu Jun 17 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-2
- add Requires: libdb-cxx to libdb-devel

* Wed Apr 21 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-1
- initial build

* Thu Apr 15 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-0.2
- remove C# documentation
- disable/remove rpath
- fix description
- tighten dependencies
- run ldconfig for cxx and sql subpackages

* Fri Apr  9 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-0.1
- enable sql
- package 5.0.21
