Summary:	Library for reading and writing sound files
Name:		libsndfile
Version:	1.0.25
Release: 10%{?dist}.0.2
License:	LGPLv2+ and GPLv2+ and BSD
Group:		System Environment/Libraries
URL:		http://www.mega-nerd.com/libsndfile/
Source0:	http://www.mega-nerd.com/libsndfile/files/libsndfile-%{version}.tar.gz
Patch0:		%{name}-1.0.25-system-gsm.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	alsa-lib-devel
BuildRequires:	flac-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	sqlite-devel
BuildRequires:	gsm-devel
BuildRequires:	libtool


%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface. It can
currently read/write 8, 16, 24 and 32-bit PCM files as well as 32 and
64-bit floating point WAV files and a number of compressed formats. It
compiles and runs on *nix, MacOS, and Win32.


%package devel
Summary:	Development files for libsndfile
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release} pkgconfig


%description devel
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface.
This package contains files needed to develop with libsndfile.


%package utils
Summary:	Command Line Utilities for libsndfile
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Obsoletes:	libsndfile < 1.0.20-4


%description utils
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface.
This package contains command line utilities for libsndfile.


%prep
%setup -q
%patch0 -p1
rm -r src/GSM610 ; autoreconf -I M4 -fiv # for system-gsm patch
#also for aarch64 support which requires autotools 2.69+


%build
%configure \
	--disable-dependency-tracking \
	--enable-sqlite \
	--enable-alsa \
	--enable-largefile \
	--disable-static

# Get rid of rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __docs
make install DESTDIR=$RPM_BUILD_ROOT
cp -pR $RPM_BUILD_ROOT%{_docdir}/libsndfile1-dev/html __docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/libsndfile1-dev

# fix multilib issues
%if %{__isa_bits} == 64
%define wordsize 64
%else
%define wordsize 32
%endif

mv %{buildroot}%{_includedir}/sndfile.h \
   %{buildroot}%{_includedir}/sndfile-%{wordsize}.h

cat > %{buildroot}%{_includedir}/sndfile.h <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "sndfile-32.h"
#elif __WORDSIZE == 64
# include "sndfile-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif
EOF

%if 0%{?rhel} != 0
rm -f %{buildroot}%{_bindir}/sndfile-jackplay
%endif


%check
LD_LIBRARY_PATH=$PWD/src/.libs make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS README NEWS
%{_libdir}/%{name}.so.*

%files utils
%defattr(-,root,root,-)
%{_bindir}/sndfile-cmp
%{_bindir}/sndfile-concat
%{_bindir}/sndfile-convert
%{_bindir}/sndfile-deinterleave
%{_bindir}/sndfile-info
%{_bindir}/sndfile-interleave
%{_bindir}/sndfile-metadata-get
%{_bindir}/sndfile-metadata-set
%{_bindir}/sndfile-play
%{_bindir}/sndfile-regtest
%{_bindir}/sndfile-salvage
%{_mandir}/man1/sndfile-cmp.1*
%{_mandir}/man1/sndfile-concat.1*
%{_mandir}/man1/sndfile-convert.1*
%{_mandir}/man1/sndfile-deinterleave.1*
%{_mandir}/man1/sndfile-info.1*
%{_mandir}/man1/sndfile-interleave.1*
%{_mandir}/man1/sndfile-metadata-get.1*
%{_mandir}/man1/sndfile-metadata-set.1*
%{_mandir}/man1/sndfile-play.1*

%files devel
%defattr(-,root,root,-)
%doc __docs/*
%doc ChangeLog
%exclude %{_libdir}/%{name}.la
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_includedir}/sndfile-%{wordsize}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/sndfile.pc


%changelog
* Sat Aug  2 2014 Peter Robinson <pbrobinson@redhat.com> 1.0.25-10
- Generic 32/64 bit platform detection - fix ppc64le build (#1126140)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.0.25-9
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.25-8
- Mass rebuild 2013-12-27

* Mon Jun 03 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.0.25-7
- fix support for aarch64, another part (#969831)

* Wed Mar 27 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.0.25-6
- fix support for aarch64 (#925887)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 12 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.0.25-2
- Patch to use system libgsm instead of a bundled copy.
- Make main package dep in -devel ISA qualified.
- Drop -octave Provides (not actually built with octave > 3.0).
- Don't build throwaway static lib.
- Run test suite during build.

* Thu Jul 14 2011 Michal Hlavinka <mhlavink@redhat.com> - 1.0.25-1
- Update to 1.0.25
- fixes integer overflow by processing certain PAF audio files (#721240)

* Sun Mar 27 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.24-1
- Update to 1.0.24

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 16 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.23-1
- Update to 10.0.23

* Tue Oct 05 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.22-1
- Update to 10.0.22

* Tue May 11 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.21-1
- Update to 10.0.21
- Do not include the static library in the package (RHBZ#556074)
- Remove BR on jack since sndfile-jackplay is not provided anymore

* Mon Feb  1 2010 Stepan Kasal <skasal@redhat.com> - 1.0.20-5
- Do not build against Jack on RHEL
- Fix the Source0: URL
- Fix the licence tag

* Sat Nov 14 2009 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.20-4
- Split utils into a subpackage

* Sat Nov 14 2009 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.20-3
- Add FLAC/Ogg/Vorbis support (BR: libvorbis-devel)
- Make build verbose
- Remove rpath
- Fix ChangeLog encoding
- Move the big Changelog to the devel package

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 06 2009 Lennart Poettering <lpoetter@redhat.com> - 1.0.20-1
- Updated to 1.0.20

* Tue Mar 03 2009 Robert Scheck <robert@fedoraproject.org> - 1.0.17-8
- Rebuilt against libtool 2.2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 25 2008 Andreas Thienemann <andreas@bawue.net> - 1.0.17-6
- Removed spurious #endif in the libsndfile.h wrapper. Thx to Edward
  Sheldrake for finding it. Fixes #468508.
- Fix build for autoconf-2.63

* Thu Oct 23 2008 Andreas Thienemann <andreas@bawue.net> - 1.0.17-5
- Fixed multilib conflict. #342401
- Made flac support actually work correctly.

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.17-4
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.17-3
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Andreas Thienemann <andreas@bawue.net> - 1.0.17-2
- Adding FLAC support to libsndfile courtesy of gentoo, #237575
- Fixing CVE-2007-4974. Thanks to the gentoo people for the patch, #296221

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 1.0.17-1
- Updated to 1.0.17

* Sun Apr 30 2006 Andreas Thienemann <andreas@bawue.net> - 1.0.16-1
- Updated to 1.0.16

* Thu Mar 30 2006 Andreas Thienemann <andreas@bawue.net> - 1.0.15-1
- Updated to 1.0.15

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.0.14-1.fc5
- Updated to 1.0.14
- Dropped patch0

* Thu May 12 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.11-3
- rebuilt

* Sat Mar  5 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.11-2
- Fix format string bug (#149863).
- Drop explicit Epoch 0.

* Sat Dec  4 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.0.11-0.fdr.1
- Update to 1.0.11.

* Wed Oct 13 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.0.10-0.fdr.1
- Update to 1.0.10, update URLs, include ALSA support.
- Disable dependency tracking to speed up the build.
- Add missing ldconfig invocations.
- Make -devel require pkgconfig.
- Include developer docs in -devel.
- Provide -octave in main package, own more related dirs.
- Bring specfile up to date with current spec templates.

* Sat Apr 12 2003 Dams <anvil[AT]livna.org>
- Initial build.
