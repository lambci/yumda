
%define _trivial .0
%define _buildid .3

Name:		libjpeg-turbo
Version:	1.2.90
Release:	6%{?dist}%{?_trivial}%{?_buildid}
Summary:	A MMX/SSE2 accelerated library for manipulating JPEG image files

Group:		System Environment/Libraries
License:	IJG
URL:		http://sourceforge.net/projects/libjpeg-turbo
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf, automake, libtool
BuildRequires:	nasm

# moved this from -utils, in an attempt to get it to better override
# libjpeg in rawhide -- Rex
Obsoletes:	libjpeg < 6b-47
# add provides (even if it not needed) to workaround bad packages, like
# java-1.6.0-openjdk (#rh607554) -- atkac
Provides:	libjpeg = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:	libjpeg%{_isa} = 6b-47%{?dist}
%endif

Patch0:		libjpeg-turbo12-noinst.patch
Patch1:		libjpeg-turbo12-CVE-2013-6630.patch
Patch2:		libjpeg-turbo12-CVE-2013-6629.patch
Patch3:		libjpeg-turbo12-pkgconfig.patch
Patch4:		libjpeg-turbo12-CVE-2018-11212.patch
Patch5:		libjpeg-turbo12-CVE-2016-3616_CVE-2018-11213_CVE-2018-11214.patch
Patch6:		libjpeg-turbo12-CVE-2018-11813.patch
Patch7:		libjpeg-turbo12-CVE-2018-14498.patch

Prefix: %{_prefix}

%description
The libjpeg-turbo package contains a library of functions for manipulating
JPEG images.

%package utils
Summary:	Utilities for manipulating JPEG images
Group:		Applications/Multimedia
Requires:	libjpeg-turbo%{?_isa} = %{version}-%{release}
Prefix: %{_prefix}

%description utils
The libjpeg-turbo-utils package contains simple client programs for
accessing the libjpeg functions. It contains cjpeg, djpeg, jpegtran,
rdjpgcom and wrjpgcom. Cjpeg compresses an image file into JPEG format.
Djpeg decompresses a JPEG file into a regular image file. Jpegtran
can perform various useful transformations on JPEG files. Rdjpgcom
displays any text comments included in a JPEG file. Wrjpgcom inserts
text comments into a JPEG file.

%package -n turbojpeg
Summary:	TurboJPEG library
Group:		System Environment/Libraries
Prefix: %{_prefix}

%description -n turbojpeg
The turbojpeg package contains the TurboJPEG shared library.

%prep
%setup -q

%patch0 -p1 -b .noinst
%patch1 -p1 -b .CVE-2013-6630
%patch2 -p1 -b .CVE-2013-6629
%patch3 -p1 -b .pkgconfig
%patch4 -p1 -b .CVE-2018-11212
%patch5 -p1 -b .CVE-2016-3616_CVE-2018-11213_CVE-2018-11214
%patch6 -p1 -b .CVE-2018-11813
%patch7 -p1 -b .CVE-2018-14498

%build
autoreconf -fiv

%configure --disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Fix perms
chmod -x README-turbo.txt

%files
%defattr(-,root,root,-)
%license README README-turbo.txt
%{_libdir}/libjpeg.so.62*

%files utils
%defattr(-,root,root,-)
%{_bindir}/cjpeg
%{_bindir}/djpeg
%{_bindir}/jpegtran
%{_bindir}/rdjpgcom
%{_bindir}/wrjpgcom

%files -n turbojpeg
%{_libdir}/libturbojpeg.so.0*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Oct 17 2019 Emmanuel Lepage <emmlep@amazon.com> - 1.2.90-6.amzn2.0.3
- Remove a duplicated patch.

* Fri Apr 19 2019 Jeremiah Mahler <jmmahler@amazon.com> - 1.2.90-5.amzn2.0.3
- Fix CVE-2018-11212
* Wed Mar 20 2019 Nikola Forró <nforro@redhat.com> - 1.2.90-8
- Fix CVE-2018-14498 (#1687475)

* Thu Dec 06 2018 Nikola Forró <nforro@redhat.com> - 1.2.90-7
- Fix CVE-2018-11212 (#1586062)
- Fix CVE-2016-3616 (#1318509), CVE-2018-11213 (#1589091)
  and CVE-2018-11214 (#1589110)
- Fix CVE-2018-11813 (#1591203)

* Thu May 24 2018 Nikola Forró <nforro@redhat.com> - 1.2.90-6
- Add pkgconfig scripts (#1581687)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.2.90-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2.90-4
- Mass rebuild 2013-12-27

* Tue Nov 26 2013 Petr Hracek <phracek@redhat.com> - 1.2.90-3
- Resolves: #1031739 app patches CVE-2013-6629 and CVE-2013-6630

* Tue Mar 26 2013 Adam Tkac <atkac redhat com> - 1.2.90-2
- rebuild for ARM64 support

* Fri Feb 08 2013 Adam Tkac <atkac redhat com> 1.2.90-1
- update to 1.2.90

* Mon Feb 04 2013 Adam Tkac <atkac redhat com> 1.2.90-0.1.20130204svn922
- update to 1.2.80 snapshot (#854695)
- run `make test` during build

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> 1.2.1-6
- build with jpeg6 API/ABI (jpeg8-ABI feature was dropped)

* Tue Dec 04 2012 Adam Tkac <atkac redhat com> 1.2.1-5
- change license to IJG (#877517)

* Wed Oct 24 2012 Adam Tkac <atkac redhat com> 1.2.1-4
- build with jpeg8 API/ABI (#854695)

* Thu Oct 18 2012 Adam Tkac <atkac redhat com> 1.2.1-3
- minor provides tuning (#863231)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Adam Tkac <atkac redhat com> 1.2.1-1
- update to 1.2.1

* Thu Mar 08 2012 Adam Tkac <atkac redhat com> 1.2.0-1
- update to 1.2.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Orion Poplawski <orion cora nwra com> 1.1.1-3
- Make turobojpeg-devel depend on turbojpeg

* Fri Oct 7 2011 Orion Poplawski <orion cora nwra com> 1.1.1-2
- Ship the turbojpeg library (#744258)

* Mon Jul 11 2011 Adam Tkac <atkac redhat com> 1.1.1-1
- update to 1.1.1
  - ljt11-rh688712.patch merged

* Tue Mar 22 2011 Adam Tkac <atkac redhat com> 1.1.0-2
- handle broken JPEGs better (#688712)

* Tue Mar 01 2011 Adam Tkac <atkac redhat com> 1.1.0-1
- update to 1.1.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Adam Tkac <atkac redhat com> 1.0.90-1
- update to 1.0.90
- libjpeg-turbo10-rh639672.patch merged

* Fri Oct 29 2010 Adam Tkac <atkac redhat com> 1.0.1-3
- add support for arithmetic coded files into decoder (#639672)

* Wed Sep 29 2010 jkeating - 1.0.1-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Adam Tkac <atkac redhat com> 1.0.1-1
- update to 1.0.1
  - libjpeg-turbo10-rh617469.patch merged
- add -static subpkg (#632859)

* Wed Aug 04 2010 Adam Tkac <atkac redhat com> 1.0.0-3
- fix huffman decoder to handle broken JPEGs well (#617469)

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.0-2
- add libjpeg-devel%%{_isa} provides to -devel subpkg to satisfy imlib-devel
  deps

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.0-1
- update to 1.0.0
- patches merged
  - libjpeg-turbo-programs.patch
  - libjpeg-turbo-nosimd.patch
- add libjpeg provides to the main package to workaround problems with broken
  java-1.6.0-openjdk package

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 0.0.93-13
- remove libjpeg provides from -utils subpkg

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> 0.0.93-12
- move Obsoletes: libjpeg to main pkg

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> 0.0.93-11
- -utils: Requires: %%name ...

* Wed Jun 30 2010 Adam Tkac <atkac redhat com> 0.0.93-10
- add Provides = libjpeg to -utils subpackage

* Mon Jun 28 2010 Adam Tkac <atkac redhat com> 0.0.93-9
- merge review related fixes (#600243)

* Wed Jun 16 2010 Adam Tkac <atkac redhat com> 0.0.93-8
- merge review related fixes (#600243)

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 0.0.93-7
- obsolete -static libjpeg subpackage (#600243)

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 0.0.93-6
- improve package description a little (#600243)
- include example.c as %%doc in the -devel subpackage

* Fri Jun 11 2010 Adam Tkac <atkac redhat com> 0.0.93-5
- don't use "fc12" disttag in obsoletes/provides (#600243)

* Thu Jun 10 2010 Adam Tkac <atkac redhat com> 0.0.93-4
- fix compilation on platforms without MMX/SSE (#600243)

* Thu Jun 10 2010 Adam Tkac <atkac redhat com> 0.0.93-3
- package review related fixes (#600243)

* Wed Jun 09 2010 Adam Tkac <atkac redhat com> 0.0.93-2
- package review related fixes (#600243)

* Fri Jun 04 2010 Adam Tkac <atkac redhat com> 0.0.93-1
- initial package
