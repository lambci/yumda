%define _trivial .0
%define _buildid .1


Name:           lz4
Version:        1.7.5
Release:        2%{?dist}%{?_trivial}%{?_buildid}
Summary:        Extremely fast compression algorithm

License:        GPLv2+ and BSD
URL:            https://lz4.github.io/lz4/
Source0:        https://github.com/Cyan4973/lz4/archive/v%{version}/%{name}-%{version}.tar.gz

Patch1000:      lz4-githubbug332.patch

%description
LZ4 is an extremely fast loss-less compression algorithm, providing compression
speed at 400 MB/s per core, scalable with multi-core CPU. It also features
an extremely fast decoder, with speed in multiple GB/s per core, typically
reaching RAM speed limits on multi-core systems.

%package        devel
Summary:        Development files for lz4
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains the header(.h) and library(.so) files required to build
applications using liblz4 library.

%package        static
Summary:        Static library for lz4

%description    static
LZ4 is an extremely fast loss-less compression algorithm. This package
contains static libraries for static linking of applications.

%prep
%autosetup -p1
echo '#!/bin/sh' > ./configure
chmod +x ./configure

%build
%configure
%make_build

%install
%configure
%make_install LIBDIR=%{_libdir} PREFIX=%{_prefix} INSTALL="install -p"

%post
/sbin/ldconfig

## Repair problems caused by "lz4 -t" of nonroot or non-a=rw files
find /dev/null ! -uid 0     -exec chown -v 0    {} \;
find /dev/null ! -gid 0     -exec chown -v  :0  {} \;
find /dev/null ! -perm a=rw -exec chmod -v a=rw {} \;

%postun -p /sbin/ldconfig

%files
%license programs/COPYING lib/LICENSE
%doc NEWS
%{_bindir}/lz4
%{_bindir}/lz4c
%{_bindir}/lz4cat
%{_bindir}/unlz4
%{_mandir}/man1/lz4.1*
%{_mandir}/man1/lz4c.1*
%{_mandir}/man1/lz4cat.1*
%{_mandir}/man1/unlz4.1*
%{_libdir}/liblz4.so.*

%files devel
%doc lib/LICENSE
%{_includedir}/lz4*.h
%{_libdir}/liblz4.so
%{_libdir}/pkgconfig/liblz4.pc

%files static
%doc lib/LICENSE
%{_libdir}/liblz4.a

%changelog
* Tue Oct 23 2018 Chad Miller <millchad@amazon.com> - 1.7.5-2.1
- Apply upstream tpatch that prevents "-t" from clobbering /dev/null perms
- Repair /dev/null perms if already broken by older version

* Wed Sep 27 2017 Jakub Martisko <jamartis@rehat.com> - 1.7.5-1 - 2
- Initial RHEL release

* Thu Jan 05 2017 pjp <pjp@fedoraproject.org> - 1.7.5-1 - 1
- Update to 1.7.5

* Sat Nov 19 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.7.3-1
- Update to 1.7.3 (RHBZ #1395458)

* Mon Jul 06 2015 pjp <pjp@fedoraproject.org> - r131-1
- New: Dos/DJGPP target #114.
- Added: Example using lz4frame library #118.
- Changed: liblz4.a no longer compiled with -fPIC by default.

* Thu Jun 18 2015 pjp <pjp@fedoraproject.org> - r130-1
- Fixed: incompatibility sparse mode vs console.
- Fixed: LZ4IO exits too early when frame crc not present.
- Fixed: incompatibility sparse mode vs append mode.
- Performance fix: big compression speed boost for clang(+30%).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - r129-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 pjp <pjp@fedoraproject.org> - r129-1
- New LZ4_compress_fast() API.
- New LZ4 CLI improved performance with multiple files.
- Other bug fix and documentation updates.

* Mon Apr 06 2015 pjp <pjp@fedoraproject.org> - r128-2
- Update files section to install unlz4 & its manual

* Wed Apr 01 2015 pjp <pjp@fedoraproject.org> - r128-1
- lz4cli sparse file support
- Restored lz4hc compression ratio
- lz4 cli supports long commands
- Introduced lz4-static sub package BZ#1208203

* Thu Jan 08 2015 pjp <pjp@fedoraproject.org> - r127-2
- Bump dist to override an earlier build.

* Wed Jan 07 2015 pjp <pjp@fedoraproject.org> - r127-1
- Fixed a bug in LZ4 HC streaming mode
- New lz4frame API integrated into liblz4
- Fixed a GCC 4.9 bug on highest performance settings

* Thu Nov 13 2014 pjp <pjp@fedoraproject.org> - r124-1
- New LZ4 HC Streaming mode

* Tue Sep 30 2014 pjp <pjp@fedoraproject.org> - r123-1
- Added experimental lz4frame API.
- Fix s390x support.

* Sat Aug 30 2014 pjp <pjp@fedoraproject.org> - r122-1
- new release
- Fixed AIX & AIX64 support (SamG)
- Fixed mips 64-bits support (lew van)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - r121-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - r121-2
- fix destdir

* Fri Aug 08 2014 pjp <pjp@fedoraproject.org> - r121-1
- new release
- Added a pkg-config file.
- Fixed a LZ4 streaming crash bug.

* Thu Jul 03 2014 pjp <pjp@fedoraproject.org> - r119-1
- new release
- Fixed a high Address allocation issue in 32-bits mode.

* Sat Jun 28 2014 pjp <pjp@fedoraproject.org> - r118-1
- new release
- install libraries under appropriate _libdir directories.

* Sat Jun 14 2014 pjp <pjp@fedoraproject.org> - r117-3
- Move shared library object to -devel package.

* Sat Jun 07 2014 pjp <pjp@fedoraproject.org> - r117-2
- Skip static library from installation.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - r117-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jun 06 2014 pjp <pjp@fedoraproject.org> - r117-1
- new release
- added lz4c & lz4cat manual pages.

* Sun Apr 13 2014 pjp <pjp@fedoraproject.org> - r116-1
- new release 116
- added lz4cat utility for posix systems

* Sat Mar 15 2014 pjp <pjp@fedoraproject.org> - r114-1
- new release r114
- added RPM_OPT_FLAGS to CFLAGS
- introduced a devel package to build liblz4

* Thu Jan 02 2014 pjp <pjp@fedoraproject.org> - r110-1
- new release r110

* Sun Nov 10 2013 pjp <pjp@fedoraproject.org> - r108-1
- new release r108

* Wed Oct 23 2013 pjp <pjp@fedoraproject.org> - r107-1
- new release r107

* Mon Oct 07 2013 pjp <pjp@fedoraproject.org> - r106-3
- fixed install section to replace /usr/ with a macro.
  -> https://bugzilla.redhat.com/show_bug.cgi?id=1015263#c5

* Sat Oct 05 2013 pjp <pjp@fedoraproject.org> - r106-2
- fixed install section above as suggested in the review.
  -> https://bugzilla.redhat.com/show_bug.cgi?id=1015263#c1

* Sun Sep 22 2013 pjp <pjp@fedoraproject.org> - r106-1
- Initial RPM release of lz4-r106
