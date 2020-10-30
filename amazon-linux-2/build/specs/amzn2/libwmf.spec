%global _trivial .0
%global _buildid .1
Summary: Windows MetaFile Library
Name: libwmf
Version: 0.2.8.4
Release: 44%{?dist}%{?_trivial}%{?_buildid}
Group: System Environment/Libraries
#libwmf is under the LGPLv2+, however...
#1. The tarball contains an old version of the urw-fonts under GPL+.
#   Those fonts are not installed
#2. The header of the command-line wmf2plot utility places it under the GPLv2+.
#   wmf2plot is neither built or install
License: LGPLv2+ and GPLv2+ and GPL+
Source: http://downloads.sourceforge.net/wvware/%{name}-%{version}.tar.gz
URL: http://wvware.sourceforge.net/libwmf.html
#Upstream is uncontactable for some time now, which is a real pity esp.
#wrt CVE-2006-3376/CVE-2009-1364
#Don't install out of date documentation
Patch0:  libwmf-0.2.8.3-nodocs.patch
#Allow use of system install fonts intead of libwmf bundled ones
Patch1:  libwmf-0.2.8.3-relocatablefonts.patch
#Set a fallback font of Times for text if a .wmf file don't set any
Patch2:  libwmf-0.2.8.4-fallbackfont.patch
#Strip unnecessary extra library dependencies
Patch3:  libwmf-0.2.8.4-deps.patch
#convert libwmf-config to a pkg-config to avoid multilib conflicts
Patch4:  libwmf-0.2.8.4-multiarchdevel.patch
#CVE-2006-3376 Integer overflow in player.c
Patch5:  libwmf-0.2.8.4-intoverflow.patch
#Don't export the modified embedded GD library symbols, to avoid conflicts with
#the external one
Patch6:  libwmf-0.2.8.4-reducesymbols.patch
#CVE-2009-1364, Use-after-free vulnerability in the modified embedded GD
#library
Patch7:  libwmf-0.2.8.4-useafterfree.patch
# adapt to standalone gdk-pixbuf
Patch8:  libwmf-0.2.8.4-pixbufloaderdir.patch
# CVE-2007-0455
Patch9:  libwmf-0.2.8.4-CVE-2007-0455.patch
# CVE-2007-3472
Patch10: libwmf-0.2.8.4-CVE-2007-3472.patch
# CVE-2007-3473
Patch11: libwmf-0.2.8.4-CVE-2007-3473.patch
# CVE-2006-2906 affects GIFs, which is not implemented here
# CVE-2006-4484 affects GIFs, which is not implemented here
# CVE-2007-3474 affects GIFs, which is not implemented here
# CVE-2007-3475 affects GIFs, which is not implemented here
# CVE-2007-3476 affects GIFs, which is not implemented here
# CVE-2007-3477
Patch12: libwmf-0.2.8.4-CVE-2007-3477.patch
# CVE-2007-3478 affects shared ttf files across threads, which is not implemented here
# CVE-2007-2756
Patch13: libwmf-0.2.8.4-CVE-2007-2756.patch
# CAN-2004-0941
Patch14: libwmf-0.2.8.4-CAN-2004-0941.patch
# CVE-2009-3546
Patch15: libwmf-0.2.8.4-CVE-2009-3546.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=925929
Patch16: libwmf-aarch64.patch
# CVE-2015-0848+CVE-2015-4588
Patch17: libwmf-0.2.8.4-CVE-2015-0848+CVE-2015-4588.patch
# CVE-2015-4695
Patch18: libwmf-0.2.8.4-CVE-2015-4695.patch
# CVE-2015-4696
Patch19: libwmf-0.2.8.4-CVE-2015-4696.patch
# CVE-2019-6978
Patch20: 0001-merge-in-fixes-for-libgd-CVE-2019-6978.patch
# rhbz#1840569
Patch21: libwmf-0.2.8.4.newurwfonts.patch

Requires: urw-fonts
Requires: %{name}-lite = %{version}-%{release}
Requires(post): gdk-pixbuf2
Requires(postun): gdk-pixbuf2
BuildRequires: gtk2-devel, libtool, libxml2-devel, libpng-devel
BuildRequires: libjpeg-devel, libXt-devel, libX11-devel, dos2unix, libtool

%description
A library for reading and converting Windows MetaFile vector graphics (WMF).

%package lite
Summary: Windows Metafile parser library
Group: System Environment/Libraries

%description lite
A library for parsing Windows MetaFile vector graphics (WMF).

%package devel
Summary: Support files necessary to compile applications with libwmf
Group: Development/Libraries
Requires: libwmf = %{version}-%{release}
Requires: gtk2-devel, libxml2-devel, libjpeg-devel

%description devel
Libraries, headers, and support files necessary to compile applications 
using libwmf.

%prep
%setup -q
%patch0  -p1 -b .nodocs
%patch1  -p1 -b .relocatablefonts
%patch2  -p1 -b .fallbackfont
%patch3  -p1 -b .deps
%patch4  -p1 -b .multiarchdevel
%patch5  -p1 -b .intoverflow
%patch6  -p1 -b .reducesymbols.patch
%patch7  -p1 -b .useafterfree.patch
%patch8  -p1 -b .pixbufloaderdir
%patch9  -p1 -b .CVE-2007-0455
%patch10 -p1 -b .CVE-2007-3472
%patch11 -p1 -b .CVE-2007-3473
%patch12 -p1 -b .CVE-2007-3477
%patch13 -p1 -b .CVE-2007-2756
%patch14 -p1 -b .CAN-2004-0941
%patch15 -p1 -b .CVE-2009-3546
%patch16 -p1 -b .aarch64
%patch17 -p1 -b .CVE-2015-0848+CVE-2015-4588
%patch18 -p1 -b .CVE-2015-4695
%patch19 -p1 -b .CVE-2015-4696
%patch20 -p1 -b .CVE-2019-6978
%patch21 -p1 -b .newurwfonts
f=README ; iconv -f iso-8859-2 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f

%build
rm configure.ac
ln -s patches/acconfig.h acconfig.h
autoreconf -i -f
%configure --with-libxml2 --disable-static --disable-dependency-tracking --with-gsfontdir=/usr/share/fonts/urw-base35
make %{?_smp_mflags}
dos2unix doc/caolan/*.html

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_includedir}/libwmf/gd
find doc -name "Makefile*" -exec rm {} \;

#we're carrying around duplicate fonts
rm -rf $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/*afm
rm -rf $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/*pfb
sed -i $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/fontmap -e 's#libwmf/fonts#fonts/urw-base35#g'

%post
/sbin/ldconfig
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :

%post lite -p /sbin/ldconfig

%postun 
/sbin/ldconfig
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :

%postun lite -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libwmf-*.so.*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.so
%{_bindir}/wmf2svg
%{_bindir}/wmf2gd
%{_bindir}/wmf2eps
%{_bindir}/wmf2fig
%{_bindir}/wmf2x
%{_bindir}/libwmf-fontmap
%{_datadir}/libwmf/

%files lite
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/libwmflite-*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/*.html
%doc doc/*.png
%doc doc/*.gif
%doc doc/html
%doc doc/caolan
%{_libdir}/*.so
%{_libdir}/pkgconfig/libwmf.pc
%{_includedir}/libwmf
%{_bindir}/libwmf-config


%changelog
* Wed May 27 2020 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-44
- Resolves: rhbz#1840569 adapt to new urw-fonts

* Mon Mar 30 2020 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-43
- Resolves: rhbz#1679005 CVE-2019-6978

* Wed Sep 02 2015 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-42
- Related: rhbz#1239162 fix patch context

* Tue Jul 07 2015 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-41
- Resolves: rhbz#1239162 CVE-2015-0848 CVE-2015-4588 CVE-2015-4695 CVE-2015-4696

* Mon May 08 2015 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-40
- Resolves: rhbz#1227431 CVE-2015-0848 libwmf: heap overflow when decoding BMP images

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.2.8.4-39
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.2.8.4-38
- Mass rebuild 2013-12-27

* Thu Apr 04 2013 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-37
- Resolves: rhbz#925929 support aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 0.2.8.4-35
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.2.8.4-34
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 0.2.8.4-31
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 07 2010 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-29
- drop bogus buildrequires

* Mon Dec 06 2010 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-28
- Resolves: rhbz#660161 security issues

* Mon Oct 18 2010 Parag Nemade <paragn AT fedoraproject.org> - 0.2.8.4-27
- Merge-review cleanup (#226058)

* Thu Jul 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-26
- Move docs into -lite subpackage that all the rest require to
  fulfil subpackage licencing rules

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.2.8.4-25
- Remove explicit file deps

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.2.8.4-23
- Adapt to standalone gdk-pixbuf

* Fri Apr 16 2010 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-22
- Clarify licences

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-20
- Resolves: CVE-2009-1364

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.2.8.4-18
- Split libwmflite (WMF parser) into -lite subpackage (#432651).
- Build with dependency tracking disabled.
- Convert docs to UTF-8.

* Wed Aug 29 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-17
- rebuild

* Thu Aug 02 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-16
- I wrote it and still had to check the headers to see if I had
  cut and pasted "and later" into then

* Thu May 24 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-15
- drop duplicate font metrics

* Thu Feb 15 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-14
- remove use of archaic autotools

* Fri Feb 09 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-13
- Resolves: rhbz#222734 no need for Makefiles in doc dirs

* Tue Jan 16 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-12
- Resolves: rhbz#222734 no need for Makefiles in doc dirs

* Thu Nov 16 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-11
- Resolves: rhbz#215925 reduce exported symbols

* Fri Jul 14 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-10
- retweak for 64bit

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.2.8.4-9.1
- rebuild

* Wed Jul 12 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-9
- CVE-2006-3376 libwmf integer overflow

* Tue May 16 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-8
- rh#191971# BuildRequires

* Fri May  5 2006 Matthias Clasen <mclasen@redhat.com> 0.2.8.4-7
- Rebuild against the new GTK+
- Require GTK+ 2.9.0

* Tue May 02 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-6
- add a .pc and base libwmf-devel on pkg-config output

* Tue Feb 28 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-5
- rh#143096# extra deps according to libwmf-config

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.2.8.4-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.2.8.4-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 19 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-4
- rh#178275# match srvg gtk2 _host usage for pixbuf loaders

* Tue Jan 03 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-3
- add libwmf-0.2.8.4-fallbackfont.patch for rh#176620#

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0.2.8.4-2.1
- rebuilt

* Wed Nov 23 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-2
- rh#173299# modify pre/post requires

* Thu Jul 28 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-1
- get patches merged upstream
- drop integrated libwmf-0.2.8.3-warnings.patch
- drop integrated libwmf-0.2.8.3-noextras.patch
- drop integrated libwmf-0.2.8.3-rh154813.patch

* Tue Jul 26 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-9
- rh#154813# wmf upsidedown, spec (what of is there is) says that
  this shouldn't happen, but...

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-8
- rebuild with gcc4

* Thu Dec 16 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-7
- RH#143096# No need for extra X libs to be linked against

* Tue Nov  2 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-6
- #rh137878# Extra BuildRequires

* Thu Oct  7 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-5
- #rh134945# Extra BuildRequires

* Wed Sep  1 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-4
- #131373# cleanup compiletime warnings

* Thu Jul  8 2004 Matthias Clasen <mclasen@redhat.com> - 0.2.8.3-3
- Update to use the new update-gdk-pixbuf-loaders script in gtk2-2.4.1-2

* Thu May 20 2004 Caolan McNamara <caolanm@redhat.com>
- Initial version
