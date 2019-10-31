
Name:    pinentry
Version: 0.8.1
Release: 17%{?dist}.0.2
Summary: Collection of simple PIN or passphrase entry dialogs

Group:   Applications/System
# qt & qt4 subpackage have different license, see subpackage definitions
License: GPLv2+
URL:     http://www.gnupg.org/aegypten/
Source0: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.gz.sig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# borrowed from opensuse
Source10: pinentry-wrapper

## Patches not yet in SVN
Patch53: 0001-Fix-qt4-pinentry-window-created-in-the-background.patch

## Backported patches
Patch200: 0001-Add-wide-char-support-to-pinentry-curses.patch
Patch201: 0001-Check-if-we-are-on-tty-before-initializing-curses.patch

BuildRequires: gettext-devel
BuildRequires: autoconf, automake
BuildRequires: libcap-devel
BuildRequires: ncurses-devel

Provides: %{name}-curses = %{version}-%{release}

Prefix: %{_prefix}

%description
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the curses (text) based version of the PIN entry dialog.


%prep
%setup -q

%patch53 -p1 -b .rhbug_589532
%patch200 -p1
%patch201 -p1

# patch200 changes configure.ac so we need to regenerate
./autogen.sh

%build

%configure \
  --disable-rpath \
  --disable-dependency-tracking \
  --disable-pinentry-gtk \
  --disable-pinentry-gtk2 \
  --without-libcap \
  --disable-pinentry-qt \
  --disable-pinentry-qt4 \
  --without-x

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -p -m755 -D %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/pinentry

# unpackaged files
rm -f $RPM_BUILD_ROOT%{_infodir}/dir


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/pinentry-curses
%{_bindir}/pinentry

%exclude %{_infodir}

%changelog
* Wed Oct 30 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Mar 17 2016 Boris Ranto <branto@redhat.com> - 0.8.1-17
- actually apply the previous patch in the spec file
- resolves: rhbz#1058972

* Fri Feb 19 2016 Boris Ranto <branto@redhat.com> - 0.8.1-16
- curses: detect non-tty environment and exit gracefully
- resolves: rhbz#1058972

* Fri Feb 19 2016 Boris Ranto <branto@redhat.com> - 0.8.1-15
- rewrite the pinentry-wrapper shell script to better handle corner cases
- resolves: rhbz#1231229

* Thu Jan 30 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-14
- Add wide-char support to pinentry-curses
- Resolves: rhbz#1059729

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.8.1-13
- Mass rebuild 2014-01-24

* Wed Jan 15 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-12
- Provide final fallback to pinetry-curses
- Resolves: #rhbz1002599

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.8.1-11
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-9
- Fix macros expansions so that conditionals work

* Mon Nov 12 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-8
- Fix up licenses for qt and qt4 subpackages (#875875)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> 0.8.1-5
- Rebuild for new libpng

* Tue Jul 26 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-4
- Improve wrapper to fallback to curses even with DISPLAY set (#622077)

* Fri Feb 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-3
- Fix pinentry-curses running as root by disabling capabilities (#677670)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-1
- Updated to latest upstream version (0.8.1)

* Fri May  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.0-3
- Fix X11 even race with gtk (#589998)
- Fix qt4 problems with creating window in the background (#589532)

* Thu Apr 29 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-2
- -qt: build as qt4 version, and drop qt3 support (f13+ only)

* Tue Apr 27 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.0-1
- pinentry-0.8.0
- pinentry-gtk keyboard grab fail results in SIGABRT (#585422)

* Sun Apr 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-5
- pinentry-gtk -g segfaults on focus change (#520236)

* Sun Sep 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-4
- Errors installing with --excludedocs (#515925)

* Sun Sep 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-3
- drop alternatives, use app-wrapper instead (borrowed from opensuse)
- -qt4 experimental subpkg, -qt includes qt3 version again  (#523488)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-1
- pinentry-0.7.6
- -qt switched qt4 version, where applicable (f9+, rhel6+)
- fixup scriptlets

* Sat Apr 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.5-1
- pinentry-0.7.5

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.7.4-5
- pinentry failed massrebuild attempt for GCC 4.3 (#434400)

* Tue Mar 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.7.4-4
- s/qt-devel/qt3-devel/ (f9+)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.4-3
- Autorebuild for GCC 4.3

* Sun Feb 17 2008 Adam Tkac <atkac redhat com> - 0.7.4-2
- rebuild against new libcap

* Sun Dec 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.4-1
- pinentry-0.7.4
- BR: libcap-devel

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.3-2
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.3-1
- pinentry-0.7.3
- License: GPLv2+

* Thu May 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.2-15
- respin (for ppc64)

* Mon Dec 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.7.2-14
- -14 respin (to help retire ATrpms pinentry pkg)

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.7.2-3
- fc6 respin

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.7.2-2
- fc6 respin

* Wed Mar 01 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Tue Oct 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.2-1
- 0.7.2, docs patch applied upstream.
- Switch to GTK2 in -gtk.
- Fine tune dependencies.
- Build with dependency tracking disabled.
- Clean up obsolete pre-FC2 support.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.7.1-4
- rebuilt

* Wed Jun 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.1-0.fdr.3
- BuildRequires qt-devel >= 3.2.

* Sat May 22 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.1-0.fdr.2
- Spec cleanups.

* Sat Apr 24 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.1-0.fdr.1
- Update to 0.7.1.

* Fri Dec 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.0-0.fdr.1
- Update to 0.7.0.
- Split GTK+ and QT dialogs into subpackages.

* Thu Jul 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.9-0.fdr.1
- Update to 0.6.9.
- Smoother experience with --excludedocs.
- Don't change alternative priorities on upgrade.

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.8-0.fdr.1
- Update to current Fedora guidelines.

* Wed Feb 12 2003 Warren Togami <warren@togami.com> 0.6.8-1.fedora.3
- info/dir temporary workaround

* Sat Feb  8 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.6.8-1.fedora.1
- First Fedora release.
