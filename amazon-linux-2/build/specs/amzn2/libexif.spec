Summary:	Library for extracting extra information from image files
Name:		libexif
Version:	0.6.22
Release:	1%{?dist}
Group:		System Environment/Libraries
License:	LGPLv2+
URL:		https://libexif.github.io/
%global tarball_version %(echo %{version} | sed -e 's|\\.|_|g')
Source0:	https://github.com/libexif/libexif/archive/libexif-%{tarball_version}-release.tar.gz
Source1:        strip-gettext-nondeterminism

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig

# For strip-gettext-nondeterminism
BuildRequires:  perl(Time::Piece)

%description
Most digital cameras produce EXIF files, which are JPEG files with
extra tags that contain information about the image. The EXIF library
allows you to parse an EXIF file and read the data from those tags.

%package devel
Summary:	Files needed for libexif application development
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The libexif-devel package contains the libraries and header files
for writing programs that use libexif.

%package doc
Summary:	The EXIF Library API documentation
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description doc
API Documentation for programmers wishing to use libexif in their programs.

%prep
%autosetup -n libexif-libexif-%{tarball_version}-release -p1

%build
autoreconf -fiv
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name "*.la" -exec rm -v {} \;
rm -rf %{buildroot}%{_datadir}/doc/libexif
cp -R doc/doxygen-output/libexif-api.html .
iconv -f latin1 -t utf-8 < COPYING > COPYING.utf8; cp COPYING.utf8 COPYING
iconv -f latin1 -t utf-8 < README > README.utf8; cp README.utf8 README
find %{buildroot} -type f -name '*.mo' -exec %{SOURCE1} {} \;
%find_lang libexif-12

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libexif-12.lang
%doc COPYING README NEWS
%{_libdir}/libexif.so.12*

%files devel
%{_includedir}/libexif
%{_libdir}/*.so
%{_libdir}/pkgconfig/libexif.pc

%files doc
%doc libexif-api.html

%changelog
* Thu Jun 04 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 0.6.22-1
- Upgrade to 0.6.22
- Resolves: #1841316

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.6.21-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.6.21-5
- Mass rebuild 2013-12-27

* Wed Mar 27 2013 Petr Šabata <contyk@redhat.com> - 0.6.21-4
- Run autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Petr Šabata <contyk@redhat.com> - 0.6.21-1
- 0.6.21 bump
- A security bugfixing release (CVE-2012-2812, CVE-2012-2813, CVE-2012-2814,
  CVE-2012-2836, CVE-2012-2837, CVE-2012-2840, CVE-2012-2841 & CVE-2012-2845)
- Drop the pre-generated docs and introduce a doc subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar 18 2011 Petr Sabata <psabata@redhat.com> - 0.6.20-1
- 0.6.20 bump
- Repackaging prehistoric libexif-docs, introducing version string in filename
- Buildroot cleanup

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May 26 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.6.19-1
- libexif 0.6.19
- fixes #589283

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Caolán McNamara <caolanm@redhat.com> - 0.6.16-2
- rebuild to get a pkgconfig(libexif) provides

* Tue Feb  5 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.16-1
- Update to 0.6.16
- Drop obsolete patch

* Tue Feb  5 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.15-6
- Convert doc files to utf-8 (#240838)

* Sat Dec 15 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.15-5
- Add patch for CVE-2007-6351. Fixes bug #425641
- Add patch for CVE-2007-6352. Fixes bug #425641

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.6.15-4
- Rebuild for selinux ppc32 issue.

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.15-3
- Update the license field

* Wed Jun 13 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.15-2
- Add patch for CVE-2007-4168. Fix bug #243892

* Wed May 30 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.15-1
- Update to 0.6.15
- Drop obsolete patch

* Thu May 24 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.13-4
- Add patch for CVE-2007-2645.

* Sun Feb  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.13-3
- Package review cleanups
- Avoid multilib conflicts by using pregenerated docs

* Wed Jul 26 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.13-2
- Rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6.13-1.1
- rebuild

* Tue May 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.13-1
- Update to 0.6.13
- Drop upstreamed patches
- Don't ship static libraries

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.12-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.6.12-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri May  6 2005 Matthias Clasen <mclasen@redhat.com>
- Prevent infinite recursion (#156365)

* Sun Apr 24 2005 Matthias Clasen <mclasen@redhat.com>
- Fix MakerNote handling (#153282)

* Mon Mar 28 2005 Matthias Clasen <mclasen@redhat.com>
- Update to 0.6.12

* Tue Mar  8 2005 Marco Pesenti Gritti <mpg@redhat.com>
- Add libexif-0.5.12-buffer-overflow.patch 

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> 
- Rebuild with gcc4

* Wed Nov  9 2004 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Use %%find_lang macro.
- Add %%doc files, including mandatory copy of the LGPL license.
- Use %{?_smp_mflags}
- Improve the descriptions

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec 22 2003 Matt Wilson <msw@redhat.com> 
- Initial build.

