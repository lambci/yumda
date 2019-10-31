%define __soversion_major 4
%define __soversion %{__soversion_major}.8

Summary: The Berkeley DB database library (version 4) for C
Name: libdb4
Version: 4.8.30
Release: 13%{?dist}
URL: http://www.oracle.com/database/berkeley-db/
License: Sleepycat and BSD
Group: System Environment/Libraries

Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: http://download.oracle.com/berkeley-db/db.1.85.tar.gz
# db-1.85 upstream patches
Patch10: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.1
Patch11: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.2
Patch12: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.3
Patch13: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.4
# other patches
Patch20: db-1.85-errno.patch
Patch21: db-4.6.21-1.85-compat.patch
Patch22: db-4.5.20-jni-include-dir.patch
Patch23: db-4.8.30-quotas-segfault.patch
Patch24: db-4.8.30-format-security.patch

Conflicts: filesystem < 3
Obsoletes: db4 < 5.0.0
Provides: db4 = %{version}
BuildRequires: perl perl-Carp libtool ed util-linux-ng
BuildRequires: tcl-devel%{?_isa} >= 8.5.2-3
BuildRequires: chrpath
BuildRequires: java-devel >= 1:1.6.0

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
Summary: Command line tools for managing Berkeley DB (version 4) databases
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: db4-utils < 5.0.0
Provides: db4-utils = %{version}
Prefix: %{_prefix}

%description utils
This package contains command-line tools for managing Berkeley DB (version
4) databases.

%package cxx
Summary: The Berkeley DB database library (version 4) for C++
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: db4-cxx < 5.0.0
Provides: db4-cxx = %{version}
Prefix: %{_prefix}

%description cxx
This package contains the C++ version of the Berkeley DB library (v4).

%prep
%setup -q -n db-%{version} -a 1

pushd db.1.85/PORT/linux
%patch10 -p0 -b .1.1
popd
pushd db.1.85
%patch11 -p0 -b .1.2
%patch12 -p0 -b .1.3
%patch13 -p0 -b .1.4
%patch20 -p1 -b .errno
popd

%patch21 -p1 -b .185compat
%patch22 -p1 -b .4.5.20.jni
%patch23 -p1 -b .quotas-segfault
%patch24 -p1 -b .format-security

cd dist
./s_config

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"

# Build the old db-185 libraries.
make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

test -d dist/dist-tls || mkdir dist/dist-tls
# Static link db_dump185 with old db-185 libraries.
/bin/sh libtool --tag=CC --mode=compile %{__cc} $RPM_OPT_FLAGS -Idb.1.85/PORT/%{_os}/include -D_REENTRANT -c db_dump185/db_dump185.c -o dist/dist-tls/db_dump185.lo
/bin/sh libtool --tag=LD --mode=link %{__cc} -o dist/dist-tls/db_dump185 dist/dist-tls/db_dump185.lo db.1.85/PORT/%{_os}/libdb.a

# Update gnu-config files for AArch64
chmod 644 dist/config.{guess,sub}
cp /usr/lib/rpm/redhat/config.{guess,sub} dist/

pushd dist/dist-tls
ln -sf ../configure .
%configure -C \
	--enable-compat185 --enable-dump185 \
	--enable-shared --disable-static \
	--disable-tcl \
	--enable-cxx \
	--disable-java \
	--disable-test \
	--disable-rpath

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
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

# Disable built-in binaries stripping (#729002)
%makeinstall STRIP=/bin/true -C dist/dist-tls

# XXX Nuke non-versioned archives and symlinks
rm -f ${RPM_BUILD_ROOT}%{_libdir}/{libdb.a,libdb_cxx.a}

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so*

# Eliminate installed doco
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/docs

# unify documentation and examples, remove stuff we don't need
rm -rf docs/csharp
rm -rf examples/csharp
rm -rf docs/installation

# XXX Avoid Permission denied. strip when building as non-root.
chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*

# remove unneeded .la files (#225675)
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

# rename utils so that they won't conflict with libdb (#749293)
pushd ${RPM_BUILD_ROOT}%{_bindir}
for i in `ls | sed s/db_//`; do
  mv db_$i db%{__soversion_major}_$i;
done
popd

# put unversioned libraries to separate directory to not to conflict
# with libdb-devel (#839508)
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{name}
pushd ${RPM_BUILD_ROOT}%{_libdir}/%{name}
for i in libdb libdb_cxx; do
  rm -f ${RPM_BUILD_ROOT}%{_libdir}/$i.so
  ln -s ../$i-%{__soversion}.so $i.so
done
popd

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
%{_bindir}/db*_sql
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify

%files cxx
%defattr(-,root,root,-)
%{_libdir}/libdb_cxx-%{__soversion}.so
%{_libdir}/libdb_cxx-%{__soversion_major}.so

%exclude %{_includedir}
%exclude %{_libdir}/%{name}/libdb.so
%exclude %{_libdir}/%{name}/libdb_cxx.so

%changelog
* Wed Oct 30 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Dec 03 2013 Jan Stanek <jstanek@redhat.com> - 4.8.30-13
- Adjusted for -Werror=format-security gcc flag.

* Fri Nov 08 2013 Honza Horak <hhorak@redhat.com> - 4.8.30-12
- Updated the config files for aarch64 architecture (#1028112)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.30-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Jan Stanek <jstanek@redhat.com> - 4.8.30-10
- Fixed missing debuginfos for utils subpackage (#729002)

* Wed Apr 24 2013 Jan Stanek <jstanek@redhat.com> - 4.8.30-9
- Added sanity patch fixing crashes when no more disc space left (#740631)

* Tue Apr 02 2013 Jan Stanek <jstanek@redhat.com> - 4.8.30-8
- Removed dependency on gcc-java

* Tue Mar 26 2013 Jan Stanek <jstanek@redhat.com> - 4.8.30-7
- Fix file conflict with libdb-java (#800359)
- Add missing perl-Carp to BuildRequires

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 4.8.30-4
- Add db4 provides to allow transisition for name change
- Spec cleanup

* Sat Jul 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 4.8.30-3
- Specify tag for libtool

* Thu Jul 12 2012 Jindrich Novy <jnovy@redhat.com> 4.8.30-2
- fix dependencies in cxx-devel and fix file conflict with
  libdb-devel (#839508)

* Sun Apr 22 2012 Jindrich Novy <jnovy@redhat.com> 4.8.30-1
- introduction of libdb4
