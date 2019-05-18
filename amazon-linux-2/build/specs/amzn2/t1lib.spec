Name:           t1lib
Version:        5.1.2
Release: 14%{?dist}.0.2

Summary:        PostScript Type 1 font rasterizer

Group:          Applications/Publishing
License:        LGPLv2+
URL:            ftp://sunsite.unc.edu/pub/Linux/libs/graphics/t1lib-%{version}.lsm
Source0:        ftp://sunsite.unc.edu/pub/Linux/libs/graphics/t1lib-%{version}.tar.gz
Patch0:         http://ftp.de.debian.org/debian/pool/main/t/t1lib/t1lib_5.1.2-3.diff.gz
Patch1:         t1lib-5.1.2-segf.patch
# Fixes CVE-2010-2642, CVE-2011-0433
# http://bugzilla.redhat.com/show_bug.cgi?id=679732
Patch2:         t1lib-5.1.2-afm-fix.patch
# Fixes CVE-2011-0764, CVE-2011-1552, CVE-2011-1553, CVE-2011-1554
# http://bugzilla.redhat.com/show_bug.cgi?id=692909
Patch3:         t1lib-5.1.2-type1-inv-rw-fix.patch
# Add aarch64 support
# https://bugzilla.redhat.com/show_bug.cgi?id=926603
Patch4:         t1lib-5.1.2-aarch64.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libXaw-devel

Requires(post): coreutils, findutils

%description
T1lib is a rasterizer library for Adobe Type 1 Fonts. It supports
rotation and transformation, kerning underlining and antialiasing. It
does not depend on X11, but does provides some special functions for
X11.

AFM-files can be generated from Type 1 font files and font subsetting
is possible.

%package        apps
Summary:        t1lib demo applications
Group:          Applications/Text
Requires:       %{name} = %{version}-%{release}

%description    apps
Sample applications using t1lib

%package        devel
Summary:        Header files and development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files and development files for %{name}.

%package        static
Summary:        Static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description    static
This package contains static libraries for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .segf
%patch2 -p1 -b .afm-fix
%patch3 -p1 -b .type1-inv-rw-fix
%patch4 -p1 -b .aarch64

# use debian patches directly instead of duplicating them
#patch -p1 < debian/patches/segfault.diff -b -z .segf
patch -p1 < debian/patches/no-config.diff
patch -p1 < debian/patches/no-docs.diff
patch -p1 < debian/patches/lib-cleanup.diff

iconv -f latin1 -t utf8 < Changes > Changes.utf8
touch -r Changes Changes.utf8
mv Changes.utf8 Changes


%build
%configure
make %{?_smp_mflags} without_doc
touch -r lib/t1lib/t1lib.h.in lib/t1lib.h
touch -r lib/t1lib/t1libx.h lib/t1libx.h
ln README.t1lib-%{version} README
sed -e 's;/usr/share/X11/fonts;%{_datadir}/X11/fonts;' \
  -e 's;/usr/share/fonts/type1;%{_datadir}/fonts %{_datadir}/texmf/fonts;' \
  -e 's;/etc/t1lib/;%{_datadir}/t1lib/;' \
 debian/t1libconfig > t1libconfig
touch -r README.t1lib-%{version} t1libconfig

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
rm $RPM_BUILD_ROOT%{_libdir}/libt1*.la
chmod a+x $RPM_BUILD_ROOT%{_libdir}/libt1*.so.*

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}
install -p -m 644 debian/man/FontDatabase.5 $RPM_BUILD_ROOT%{_mandir}/man5/
install -p -m 644 debian/man/t1libconfig.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install -p -m 644 debian/man/type1afm.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install -p -m 644 debian/man/xglyph.1 $RPM_BUILD_ROOT%{_mandir}/man1/
touch -r README.t1lib-%{version} $RPM_BUILD_ROOT%{_mandir}/man?/*.*

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -p -m 755 t1libconfig $RPM_BUILD_ROOT%{_sbindir}/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/t1lib/
touch $RPM_BUILD_ROOT%{_datadir}/t1lib/{FontDatabase,t1lib.config}

%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
%{_sbindir}/t1libconfig --force > /dev/null

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc Changes LGPL LICENSE README
%dir %{_datadir}/t1lib
%ghost %verify(not size mtime md5) %{_datadir}/t1lib/t1lib.config
%ghost %verify(not size mtime md5) %{_datadir}/t1lib/FontDatabase
%{_libdir}/libt1.so.*
%{_libdir}/libt1x.so.*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sbindir}/t1libconfig

%files apps
%defattr(-,root,root,-)
%{_bindir}/type1afm
%{_bindir}/xglyph
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc doc/t1lib_doc.pdf
%{_includedir}/t1lib*.h
%{_libdir}/libt1.so
%{_libdir}/libt1x.so

%files static
%defattr(-,root,root,-)
%{_libdir}/libt1.a
%{_libdir}/libt1x.a


%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 5.1.2-14
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 5.1.2-13
- Mass rebuild 2013-12-27

* Tue Mar 26 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 5.1.2-12
- Added support for aarch64 (aarch64 patch)
  Resolves: rhbz#926603

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 5.1.2-9
- Add patch to fix CVE-2010-2642, CVE-2011-0433 (afm-fix patch)
- New version of patch for CVE-2011-0764, also fixes CVE-2011-1552,
  CVE-2011-1553, CVE-2011-1554 (type1-inv-rw-fix patch)
  Resolves: rhbz#772899
- Add explicit NVR requires to apps subpackage (consumes libt1(x).so)
- Fix rpmlint warning (mixed-use-of-spaces-and-tabs)

* Tue Jan  3 2012 José Matos <jamatos@fedoraproject.org> - 5.1.2-8
- Add patch to fix CVE-2011-0764

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May 26 2010 José Matos <jamatos@fc.up.pt> - 5.1.2-6
- Use updated debian patch (thanks to Patrice Dumas). (#587885)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 5.1.2-4
- Split demo apps to a subpackage to isolate libXaw deps

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.1.2-2
- Autorebuild for GCC 4.3

* Sat Jan 12 2008 Patrice Dumas <pertusus[AT]free.fr> - 5.1.2-1
- update to 5.1.2

* Tue Jan  8 2008 Patrice Dumas <pertusus[AT]free.fr> - 5.1.1-7
- add X libs BuildRequires (#353861)

* Tue Jan  8 2008 Patrice Dumas <pertusus[AT]free.fr> - 5.1.1-6
- apply debian patch
- use debian patches directly

* Sat Jan  5 2008 Patrice Dumas <pertusus[AT]free.fr> - 5.1.1-5
- silence t1libconfig when the directories don't exist (#183108)

* Sat Jan  5 2008 Patrice Dumas <pertusus[AT]free.fr> - 5.1.1-4
- separate subpackage for static library
- keep timestamps
- add more paths to t1libconfig and use rpm macros for those paths
- fix the -maxdepth position in find
- put t1lib.config and FontDatabase in %%{_datadir} these are not
  config files, they are generated
- fix a segfault in t1lib with long TYPE1 lines

* Thu Sep 27 2007 José Matos <jamatos[AT]fc.up.pt> - 5.1.1-3
- Apply patch to fix CVE-2007-4033

* Tue Aug 28 2007 José Matos <jamatos[AT]fc.up.pt> - 5.1.1-2
- License fix, rebuild for devel (F8).

* Thu Jun  7 2007 José Matos <jamatos[AT]fc.up.pt> - 5.1.1-1
- Update to 5.1.1.
- Remove t1lib-5.1.0-destdir.patch (applied upstream).

* Sun Apr 22 2007 José Matos <jamatos[AT]fc.up.pt> - 5.1.0-9
- Add Requires(post).

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 5.1.0-8
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.0-7
- Rebuild for FC-6.

* Sun Feb 26 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 5.1.0-6
- Change X11 font path to Fedora Core 5's default (#183108, Ville Skyttä)

* Tue Feb 14 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 5.1.0-5
- Rebuild for Fedora Extras 5

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 5.1.0-4
- %%ghost-ing config files, also making sure they're regenerated

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 5.1.0-3
- rebuild

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 5.1.0-2
- remove unneeded %%{_datadir}/t1lib contents
- cleanup

* Tue Sep 27 2005 Michael A. Peters <mpeters@mac.com> - 5.1.0-1
- updated version
- remove Patch0 (in upstream), added Patch6
- Does not BuildRequire xfree/xorg devel
- no longer BuildRequire autoconf (Patch0 removed)

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 5.0.2-3
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Mar 11 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:5.0.2-0.fdr.1
- Updated to 5.0.2.

* Sat Feb  7 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:5.0.0-0.fdr.3
- Converted spec file to UTF-8.
- Synchronised patches with Debian (unstable) t1lib-5.0.0.

* Thu Nov 27 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:5.0.0-0.fdr.2
- Added URL (bug 880).
- Eliminated funny typo in configure script (bug 880).

* Sun Oct 26 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:5.0.0-0.fdr.1
- Initial RPM release.

