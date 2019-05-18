
# NOTE: packages that can use jasper:
# ImageMagick
# netpbm

Summary: Implementation of the JPEG-2000 standard, Part 1
Name:    jasper
Group:   System Environment/Libraries
Version: 1.900.1
Release: 33%{?dist}

License: JasPer
URL:     http://www.ece.uvic.ca/~frodo/jasper/
Source0: http://www.ece.uvic.ca/~frodo/jasper/software/jasper-%{version}.zip

Patch1: jasper-1.701.0-GL.patch
# autoconf/automake bits of patch1
Patch2: jasper-1.701.0-GL-ac.patch
# CVE-2007-2721 (bug #240397)
# borrowed from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=413041;msg=88
Patch3: patch-libjasper-stepsizes-overflow.diff
# borrowed from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=469786 
Patch4: jpc_dec.c.patch
# OpenBSD hardening patches addressing couple of possible integer overflows
# during the memory allocations
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3520
Patch5: jasper-1.900.1-CVE-2008-3520.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3522
Patch6: jasper-1.900.1-CVE-2008-3522.patch
# add pkg-config support
Patch7: jasper-pkgconfig.patch

Patch8: jasper-1.900.1-CVE-2011-4516-CVE-2011-4517-CERT-VU-887409.patch

Patch9: jasper-CVE-2014-9029.patch
Patch10: jasper-CVE-2014-8137.patch
Patch11: jasper-CVE-2014-8138.patch
Patch12: jasper-CVE-2014-8157.patch
Patch13: jasper-CVE-2014-8158.patch

# Issues found by static analysis of code
Patch110: jasper-1.900.1-Coverity-BAD_SIZEOF.patch
Patch111: jasper-1.900.1-Coverity-CHECKED_RETURN.patch
Patch112: jasper-1.900.1-Coverity-FORWARD_NULL.patch
Patch113: jasper-1.900.1-Coverity-NULL_RETURNS.patch
Patch114: jasper-1.900.1-Coverity-RESOURCE_LEAK.patch
Patch115: jasper-1.900.1-Coverity-UNREACHABLE.patch
Patch116: jasper-1.900.1-Coverity-UNUSED_VALUE.patch

Patch14: jasper-CVE-2015-5203-CVE-2016-9262.patch
Patch15: jasper-CVE-2015-5221.patch
Patch16: jasper-CVE-2016-1577.patch
Patch17: jasper-CVE-2016-1867.patch
Patch18: jasper-CVE-2016-2089.patch
Patch19: jasper-CVE-2016-2116.patch
Patch20: jasper-CVE-2016-8654.patch
Patch21: jasper-CVE-2016-8690-CVE-2016-8884-CVE-2016-8885.patch
Patch22: jasper-CVE-2016-8691-CVE-2016-8692.patch
Patch23: jasper-CVE-2016-8693.patch
Patch24: jasper-CVE-2016-9390.patch
Patch25: jasper-CVE-2016-9392-CVE-2016-9393-CVE-2016-9394.patch
Patch26: jasper-CVE-2016-9560.patch
Patch27: jasper-CVE-2016-10251.patch
Patch28: jasper-CVE-2016-9583.patch
Patch29: jasper-CVE-2016-9591.patch
Patch30: jasper-CVE-2016-9600.patch
Patch31: jasper-CVE-2016-10248.patch
Patch32: jasper-CVE-2016-10249.patch
Patch33: jasper-CVE-2016-8883.patch
Patch34: jasper-CVE-2016-9387.patch
Patch35: jasper-CVE-2016-9388.patch
Patch36: jasper-CVE-2016-9389.patch
Patch37: jasper-CVE-2016-9391.patch
Patch38: jasper-CVE-implicit-declaration-fix.patch

Patch39: jasper-1.900.1-define-SIZE-MAX.patch	
Patch40: jasper-1.900.1-CVE-2016-9396.patch
Patch41: jasper-1.900.1-CVE-2017-1000050.patch

# autoreconf
BuildRequires: autoconf automake libtool
BuildRequires: freeglut-devel 
BuildRequires: libGLU-devel
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
This package contains an implementation of the image compression
standard JPEG-2000, Part 1. It consists of tools for conversion to and
from the JP2 and JPC formats.

%package devel
Summary: Header files, libraries and developer documentation
Group:   Development/Libraries
Provides: libjasper-devel = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: libjpeg-devel
Requires: pkgconfig
%description devel
%{summary}.

%package libs 
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries
Conflicts: jasper < 1.900.1-4
%description libs 
%{summary}.

%package utils 
Summary: Nonessential utilities for %{name}
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description utils 
%{summary}, including jiv and tmrdemo.



%prep
%setup -q -n %{name}-%{version}

%patch1 -p1 -b .GL
%patch2 -p1 -b .GL-ac
%patch3 -p1 -b .CVE-2007-2721
%patch4 -p1 -b .jpc_dec_assertion
%patch5 -p1 -b .CVE-2008-3520
%patch6 -p1 -b .CVE-2008-3522
%patch7 -p1 -b .pkgconfig
%patch8 -p1 -b .CVE-2011-4516-4517
%patch9 -p1 -b .CVE-2014-9029
%patch10 -p1 -b .CVE-2014-8137
%patch11 -p1 -b .CVE-2014-8138
%patch12 -p1 -b .CVE-2014-8157
%patch13 -p1 -b .CVE-2014-8158

%patch110 -p1 -b .BAD_SIZEOF
%patch111 -p1 -b .CHECKED_RETURN
%patch112 -p1 -b .FORWARD_NULL
%patch113 -p1 -b .NULL_RETURNS
%patch114 -p1 -b .RESOURCE_LEAK
%patch115 -p1 -b .UNREACHABLE
%patch116 -p1 -b .UNUSED_VALUE

%patch14 -p1 -b .CVE-2015-5203
%patch15 -p1 -b .CVE-2015-5221
%patch16 -p1 -b .CVE-2016-1577
%patch17 -p1 -b .CVE-2016-1867
%patch18 -p1 -b .CVE-2016-2089
%patch19 -p1 -b .CVE-2016-2116
%patch20 -p1 -b .CVE-2016-8654
%patch21 -p1 -b .CVE-2016-8690
%patch22 -p1 -b .CVE-2016-8691
%patch23 -p1 -b .CVE-2016-8693
%patch24 -p1 -b .CVE-2016-9390
%patch25 -p1 -b .CVE-2016-9392
%patch26 -p1 -b .CVE-2016-9560
%patch27 -p1 -b .CVE-2016-10251
%patch28 -p1 -b .CVE-2016-9583
%patch29 -p1 -b .CVE-2016-9591
%patch30 -p1 -b .CVE-2016-9600
%patch31 -p1 -b .CVE-2016-10248
%patch32 -p1 -b .CVE-2016-10249
%patch33 -p1 -b .CVE-2016-8883
%patch34 -p1 -b .CVE-2016-9387
%patch35 -p1 -b .CVE-2016-9388
%patch36 -p1 -b .CVE-2016-9389
%patch37 -p1 -b .CVE-2016-9391
%patch38 -p1 -b .CVE-implicit-declaration-fix
%patch39 -p1 -b .define-SIZE-MAX
%patch40 -p1 -b .CVE-2016-9396
%patch41 -p1 -b .CVE-2017-1000050

autoreconf --verbose --force --install


%build

# jas_icc.c:744:2: warning: assuming signed overflow does not occur
# when assuming that (X + c) < X is always false [-Wstrict-overflow]
#
# comment from Red Hat Security Response Team:
# gcc inlines jas_iccattrtab_resize into jas_iccattrtab_add. Additionally, it
# essentially removes the "assert(maxents >= tab->numattrs);" assertion in
# jas_iccattrtab_resize, because it assumes that "maxents >= tab->numattrs" will
# always be true due to jas_iccattrtab_resize(attrtab, attrtab->numattrs + 32),
# especially the + 32. This assumption can only be true if it completely ignores
# the problem of signed integer overflows. I don't think it's a smart idea to
# accept that.
# -fno-strict-overflow forces gcc into keeping the assertion there.
CFLAGS="%{optflags} -fno-strict-overflow" \
%configure \
  --enable-shared \
  --disable-static 

make %{?_smp_mflags}


%install

make install DESTDIR=$RPM_BUILD_ROOT

# Unpackaged files
rm -f doc/README
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
make check



%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%{_bindir}/imgcmp
%{_bindir}/imginfo
%{_bindir}/jasper
%{_mandir}/man1/img*
%{_mandir}/man1/jasper.1*

%files devel
%doc doc/*
%{_includedir}/jasper/
%{_libdir}/libjasper.so
%{_libdir}/pkgconfig/jasper.pc

%files libs
%doc COPYRIGHT LICENSE NEWS README
%{_libdir}/libjasper.so.1*

%files utils
%{_bindir}/jiv
%{_bindir}/tmrdemo
%{_mandir}/man1/jiv.1*


%changelog
* Thu Jun 21 2018 Josef Ridky <jridky@redhat.com> - 1.900.1-33
- remove implicit declaration of jas_eprintf (#1585830)

* Thu Jun 21 2018 Josef Ridky <jridky@redhat.com> - 1.900.1-32
- Fix CVE-2016-9396 (#1583721)
- Fix CVE-2017-1000050 (#1585830)

* Wed May 31 2017 Josef Ridky <jridky@redhat.com> - 1.900.1-31
- Fix missing declaration of SIZE_MAX constant in jas_math.h (#1455489)

* Tue Apr 25 2017 Josef Ridky <jridky@redhat.com> - 1.900.1-30
- Multiple security fixes (fixed by thoger):
  CVE-2015-5203 CVE-2015-5221 CVE-2016-1577 CVE-2016-1867 CVE-2016-2089
  CVE-2016-2116 CVE-2016-8654 CVE-2016-8690 CVE-2016-8691 CVE-2016-8692
  CVE-2016-8693 CVE-2016-8883 CVE-2016-8884 CVE-2016-8885 CVE-2016-9262
  CVE-2016-9387 CVE-2016-9388 CVE-2016-9389 CVE-2016-9390 CVE-2016-9391
  CVE-2016-9392 CVE-2016-9393 CVE-2016-9394 CVE-2016-9560 CVE-2016-9583
  CVE-2016-9591 CVE-2016-9600 CVE-2016-10248 CVE-2016-10249 CVE-2016-10251
- Fix implicit declaration warning caused by security fixes above

* Mon Jan 19 2015 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-29
- CVE-2014-8157 - dec->numtiles off-by-one check in jpc_dec_process_sot() (#1183674)
- CVE-2014-8158 - unrestricted stack memory use in jpc_qmfb.c (#1183682)

* Fri Dec 12 2014 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-28
- CVE-2014-8137 - double-free in in jas_iccattrval_destroy (#1173569)
- CVE-2014-8138 - heap overflow in jp2_decode (#1173569)

* Sat Dec 06 2014 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-27
- CVE-2014-9029 - incorrect component number check in COC, RGN and QCC
                  marker segment decoders (#1171211)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.900.1-26
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.900.1-25
- Mass rebuild 2013-12-27

* Mon Mar 25 2013 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-24
- added --force option to autoreconf (#925604)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.900.1-22
- rebuild due to "jpeg8-ABI" feature drop

* Thu Dec 06 2012 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-21
- build with -fno-strict-overflow

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-18
- CVE-2011-4516, CVE-2011-4517 jasper: heap buffer overflow flaws
  lead to arbitrary code execution (CERT VU#887409) (#765660)
- Fixed problems found by static analysis of code (#761440)
- spec file modernized

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-16
- rebuild

* Sun Feb 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-15
- FTBFS jasper-1.900.1-14.fc12: ImplicitDSOLinking (#564794)

* Thu Oct 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-14
- add pkgconfig support

* Mon Oct 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-13
- CVE-2008-3520 jasper: multiple integer overflows in jas_alloc calls (#461476)
- CVE-2008-3522 jasper: possible buffer overflow in 
  jas_stream_printf() (#461478)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-11
- FTBFS jasper-1.900.1-10.fc11 (#511743)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Rex Dieter <rdieter@fedoraproject.org> 1.900.1-9
- patch for "jpc_dec_tiledecode: Assertion `dec->numcomps == 3' failed)
  (#481284, #481291)

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.900.1-8
- respin (gcc43)

* Mon Oct 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-7
- -libs: %%post/%%postun -p /sbin/ldconfig

* Mon Sep 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-6
- -libs: -Requires: %%name
- -devel: +Provides: libjasper-devel
- drop (unused) geojasper bits

* Wed Aug 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-4
- -libs subpkg to be multilib friendlier
- -utils subpkg for non-essential binaries jiv, tmrdemo (#244153)

* Fri Aug 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-3
- License: JasPer

* Wed May 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-2
- CVE-2007-2721 (#240397)

* Thu Mar 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-1
- jasper-1.900.1

* Fri Dec 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.900.0-3
- omit deprecated memleak patch

* Fri Dec 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.900.0-2
- jasper-1.900.0 (#218947)

* Mon Sep 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-15
- memory leak (#207006)

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-13
- fc6 respin

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-12
- fixup build issues introduced by geojasper integration

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-10
- support/use geojasper (optional, default no)
- fc5: gcc/glibc respin

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Tue Jan 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-9
- workaround "freeglut-devel should Requires: libGL-devel, libGLU-devel"
  (#179464)

* Tue Jan 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-8
- revert jasper to jaspertool rename (#176773)
- actually use/apply GL patch

* Tue Oct 18 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-7
- GL patch to remove libGL dependancy (using only freeglut)

* Tue Oct 18 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-6
- token %%check section
- --enable-shared 

* Mon Oct 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-5
- use %%{?dist}
- BR: libGL-devel 

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Oct 23 2004 Rex Dieter <rexdieter at sf.net> 0:1.701.0-0.fdr.3
- Capitalize summary
- remove 0-length ChangeLog

* Fri Jun 04 2004 Rex Dieter <rexdieter at sf.net> 0:1.701.0-0.fdr.2
- nuke .la file
- BR: glut-devel -> freeglut-devel

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:1.701.0-0.fdr.1
- 1.701.0

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:1.700.5-0.fdr.2
- avoid conflicts with fc'2 tomcat by renaming /usr/bin/jasper -> jaspertool

* Mon Mar 08 2004 Rex Dieter <rexdieter at sf.net> 0:1.700.5-0.fdr.1
- use Epochs.
- -devel: Requires: %%name = %%epoch:%%version

* Thu Jan 22 2004 Rex Dieter <rexdieter at sf.net> 1.700.5-0.fdr.0
- first try

