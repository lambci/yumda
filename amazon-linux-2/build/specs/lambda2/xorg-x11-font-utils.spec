%define pkgname font-utils
%define mkfontscale 1.1.3

Summary: X.Org X11 font utilities
Name: xorg-x11-%{pkgname}
# IMPORTANT: If package ever gets renamed to something else, remove the Epoch line!
Epoch: 1
Version: 7.5
Release: 21%{?dist}
License: MIT
Group: User Interface/X
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/app/bdftopcf-1.1.tar.bz2
Source1: ftp://ftp.x.org/pub/individual/app/fonttosfnt-1.0.4.tar.bz2
Source2: ftp://ftp.x.org/pub/individual/app/mkfontdir-1.0.7.tar.bz2
Source3: ftp://ftp.x.org/pub/individual/app/mkfontscale-%{mkfontscale}.tar.bz2
Source4: ftp://ftp.x.org/pub/individual/font/font-util-1.3.1.tar.bz2
# helper script used in %post for xorg-x11-fonts
Source5: xorg-x11-fonts-update-dirs
Source6: xorg-x11-fonts-update-dirs.1

Patch2: mkfontscale-examine-all-encodings.patch

BuildRequires: pkgconfig(xfont) pkgconfig(x11)
BuildRequires: libfontenc-devel >= 0.99.2-2
BuildRequires: freetype-devel
BuildRequires: zlib-devel
BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-util-macros

Provides: %{pkgname}
Provides: bdftopcf, fonttosfnt, mkfontdir, mkfontscale, ucs2any

# bdftruncate isn't a perl script anymore (repackaged in f18)
Provides: bdftruncate = %{epoch}:%{version}-%{release}
Obsoletes: bdftruncate < %{epoch}:%{version}-%{release}

Prefix: %{_prefix}

%description
X.Org X11 font utilities required for font installation, conversion,
and generation.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4
oldpwd=$(pwd)
cd mkfontscale-%{mkfontscale}
%patch2 -p1 -b .all-encodings
cd ${oldpwd}

%build
# Build all apps
{
   for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util ; do
      oldpwd=$(pwd)
      cd $app-*
      # this --with-mapdir should be redundant?
      autoreconf -vif
      %configure --with-mapdir=%{_datadir}/X11/fonts/util
      make
      cd ${oldpwd}
   done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
    for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util; do
		oldpwd=$(pwd)
		cd $app-*
		make install DESTDIR=$RPM_BUILD_ROOT
		cd ${oldpwd}
	done
	for i in */README ; do
		[ -s $i ] && cp $i README-$(echo $i | sed 's/-[0-9].*//')
	done
	for i in */COPYING ; do
		grep -q stub $i || cp $i COPYING-$(echo $i | sed 's/-[0-9].*//')
	done
}

install -m 744 %{SOURCE5} ${RPM_BUILD_ROOT}%{_bindir}/xorg-x11-fonts-update-dirs
sed -i "s:@DATADIR@:%{_datadir}:" ${RPM_BUILD_ROOT}%{_bindir}/xorg-x11-fonts-update-dirs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING-bdftopcf COPYING-[c-z]*
%{_bindir}/bdftopcf
%{_bindir}/bdftruncate
%{_bindir}/fonttosfnt
%{_bindir}/mkfontdir
%{_bindir}/mkfontscale
%{_bindir}/ucs2any
%{_bindir}/xorg-x11-fonts-update-dirs
%dir %{_datadir}/X11/fonts
%dir %{_datadir}/X11/fonts/util
%{_datadir}/X11/fonts/util/map-*
%{_datadir}/aclocal/fontutil.m4

%exclude %{_mandir}
%exclude %{_libdir}/pkgconfig/fontutil.pc

%changelog
* Thu Apr 2 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu May 17 2018 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-21
- Rebase to F28 (#1564630)

* Tue May 12 2015 Peter Robinson <pbrobinson@redhat.com> 1:7.5-20
- rebuild

* Wed Aug 06 2014 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-19
- Add a man page for xorg-x11-fonts-update-dirs (#948841)

* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 7.5-18.1
- Mass rebuild

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:7.5-18
- Mass rebuild 2013-12-27

* Thu Jul 04 2013 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-17
- Ok, this time fix the right changelog date. Well, the wrong one, I mean.
 
* Thu Jul 04 2013 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-16
- Fix a changelog date, some checking tools keep reminding me.

* Thu May 30 2013 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-15
- Fix call to ttmkfdir (#967619)

* Wed May 22 2013 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-14
- mkfontscale 1.1.0
- mkfontdir 1.0.7
- bdftopcf 1.0.4
- Document mkfontscale's -u/-U in the man page (#948841)

* Mon Apr 08 2013 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-13
- Fix opendir error message during font install, missing encodingsdir/large
  was missing (#928305)

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 7.5-12
- autoreconf for aarch64

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-10
- Add the epoch to the Provides bdftruncate. bdftruncate had an epoch for
  years, make sure that stays alive

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 01 2012 Adam Jackson <ajax@redhat.com> 7.5-8
- font-util 1.3.0
- Un-subpackage bdftruncate, it's not a perl script anymore.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Matěj Cepl <mcepl@redhat.com> - 1:7.5-5
- pushd/popd are slightly evil, removing (#664701, #664699)

* Wed Nov 24 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-4
- Fix need_ttmkfdir test in xorg-x11-fonts-update-dirs script (#655925)

* Fri Nov 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-3
- Add xorg-x11-fonts-update-dirs, a script to automake mkfontscale and
  friends as well as generate encodings directories during %post (used by
  xorg-x11-fonts). (#634039)

* Mon Nov 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-2
- mkfontdir 1.0.6

* Mon Nov 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-1
- font-util 1.2.0
- mkfontscale 1.0.8
- bdftopcf 1.0.3

* Tue Oct 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.4-3
- font-util 1.1.2

* Fri Jul 09 2010 Peter Hutterer <peter.hutterer@redhat.com> 1:7.4-2
- Fix build for missing bdftruncate COPYING file.

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 7.4-1
- Install COPYING for bdftruncate too.

* Fri Apr 09 2010 Matěj Cepl <mcepl@redhat.com> - 1:7.2-12
- examine all platform=3 encodings (fixes #578460)

* Tue Nov 10 2009 Adam Jackson <ajax@redhat.com> 7.2-11
- font-util 1.1.0

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 7.2-10
- mkfontscale 1.0.7
- mkfontdir 1.0.5

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 7.2-8
- Un-require xorg-x11-filesystem
- Other general spec cleanup.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 7.2-6
- Fix license tag.

* Mon Jul 07 2008 Adam Jackson <ajax@redhat.com> 7.2-5
- Fix Source url for font-util.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:7.2-4
- Autorebuild for GCC 4.3

* Mon Dec 10 2007 Adam Jackson <ajax@redhat.com> 1:7.2-3
- Move bdftruncate (and its perl dependency) to a subpackage.
- %%doc for the non-empty READMEs and non-stub COPYINGs.

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1:7.2-2
- Rebuild for build id

* Thu Apr 26 2007 Adam Jackson <ajax@redhat.com> 1:7.2-1
- bdftopcf 1.0.1
- Superstition bump to 7.2-1

* Mon Mar 26 2007 Adam Jackson <ajax@redhat.com> 1:7.1-5
- mkfontdir 1.0.3

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1:7.1-4.fc7
- fonttosfnt 1.0.3

* Thu Aug 17 2006 Adam Jackson <ajackson@redhat.com> 1:7.1-3
- Remove X11R6 symlinks.

* Fri Jul 14 2006 Adam Jackson <ajackson@redhat.com> 1:7.1-2
- Added fonttosfnt-1.0.1-freetype22-build-fix.patch to fix a build failure
  with new freetype 2.2.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:7.1-1.1
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1:7.1-1
- Update to font-util-1.0.1 from X11R7.1
- Set package version to X11 release the tarballs are based from.

* Wed Apr 26 2006 Adam Jackson <ajackson@redhat.com> 1:1.0.2-2
- Update mkfontdir

* Wed Feb 22 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-3
- Remove "Obsoletes: xorg-x11-font-utils" as the package should not obsolete
  itself.  Leftover from the original package template it seems.  (#182439)

* Fri Feb 17 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-2
- Added with_X11R6_compat macro to conditionalize inclusion of mkfontdir and
  mkfontscale symlinks in the old X11R6 locations, pointing to the X11R7
  binaries.  This will provide backward compatibilty for Fedora Core 5, however
  3rd party developers and rpm package maintainers should update to using the
  new X11R7 locations immediately, as these compatibility links are temporary,
  and will be removed from a future OS release.
- Remove system directories from file manifest to appease the banshees.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-1
- Updated all utilities to the versions shipped in X11R7.0.

* Thu Dec 15 2005 Mike A. Harris <mharris@redhat.com> 1:1.0.0-1
- Updated all utilities to version 1.0.0 from X11R7 RC4.
- Updated font-util-1.0.0-mapdir-use-datadir-fix.patch to work with RC4.
- Added font-util-1.0.0-autoconf-add-with-fontdir-option.patch to add a new
  variable "fontdir" to the fontutil.pc file which all of the font packages
  can autodetect and use instead of having to put manual fontdir overrides
  in every single rpm package.

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.2-1
- Updated bdftopcf, fonttosfnt to version 0.99.3, and mkfontdir, mkfontscale,
  and font-util to version 0.99.2 from X11R7 RC3.
- Changed manpage dir from man1x back to man1 due to another upstream change.
- Added fontutil.m4 to file manifest.

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.1-1
- Changed package version to 0.99.1 to match the upstream font-util tarball
  version, and added "Epoch: 1" to the package for upgrades.
- Added font-util-0.99.1-mapdir-use-datadir-fix.patch to fix the font-util
  mapfiles data to install into datadir instead of libdir (#173943)
- Added "Requires(pre): libfontenc >= 0.99.2-2" to force a version of
  libfontenc to be installed that fixes bug #173453, and to also force it
  to be installed before xorg-x11-font-utils in a multi-package rpm
  transaction, which will ensure that when font packages get installed
  during upgrades via anaconda or yum, that the right libfontenc is being
  used by mkfontscale/mkfontdir.
- Added ">= 0.99.2-2" to BuildRequires for libfontenc, as a convenience to
  people rebuilding xorg-x11-font-utils, as they'll need to install the new
  libfontenc now anyway before they can install the font-utils package.

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 6.99.99.902-2
- require newer filesystem (#172610)

* Wed Nov 09 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.902-1
- Updated bdftopcf, fonttosfnt, mkfontdir, mkfontscale to version 0.99.1 from
  X11R7 RC1.

* Wed Nov 09 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-3
- Glob util/map-* files in file manifest.
- Added missing "Obsoletes: xorg-x11-font-utils".
- Added "BuildRequires: pkgconfig".

* Sun Nov 06 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-2
- Added font-util-0.99.1 to package, from X11R7 RC1 release, which provides
  ucs2any, bdftruncate.

* Wed Oct 26 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-1
- Updated bdftopcf, fonttosfnt, mkfontdir, mkfontscale to version 0.99.1 from
  X11R7 RC1.
- Bumped package version to 6.99.99.901, the X11R7 RC1 release version tag.
- Updated file manifest to to find the manpages in "man1x".

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-1
- Initial build.
