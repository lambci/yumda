# INFO: Package contains data-only, no binaries, so no debuginfo is needed
%define debug_package %{nil}

#global gitdate 20110415
#global gitversion 19a0026b5

Summary: X Keyboard Extension configuration data
Name: xkeyboard-config
Version: 2.20
Release: 1%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
License: MIT
Group: User Interface/X
URL: http://www.freedesktop.org/wiki/Software/XKeyboardConfig
%if 0%{?gitdate}
Source0:    %{name}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0: http://xorg.freedesktop.org/archive/individual/data/xkeyboard-config/%{name}-%{version}.tar.bz2
%endif

Patch01: 0001-Revert-rules-Move-Finnish-DAS-layout-to-extras.patch

BuildArch: noarch

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: xkbcomp
BuildRequires: perl(XML::Parser)
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: git-core
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: glib2-devel
BuildRequires: xorg-x11-proto-devel libX11-devel
BuildRequires: libxslt

Prefix: %{_prefix}

%description
This package contains configuration data used by the X Keyboard Extension 
(XKB), which allows selection of keyboard layouts when using a graphical 
interface. 

%prep
%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%if 0%{?gitdate}
git checkout -b fedora
sed -i 's/git/&+ssh/' .git/config
if [ -z "$GIT_COMMITTER_NAME" ]; then
    git config user.email "x@fedoraproject.org"
    git config user.name "Fedora X Ninjas"
fi
git commit -am "%{name} %{version}"
%else
git init
if [ -z "$GIT_COMMITTER_NAME" ]; then
    git config user.email "x@fedoraproject.org"
    git config user.name "Fedora X Ninjas"
fi
git add .
git commit -a -q -m "%{name} %{version} baseline."
%endif

git am -p1 %{patches} < /dev/null

%build
AUTOPOINT="intltoolize --automake --copy" autoreconf -v --force --install || exit 1
%configure \
    --enable-compat-rules \
    --with-xkb-base=%{_datadir}/X11/xkb \
    --disable-xkbcomp-symlink \
    --with-xkb-rules-symlink=xorg

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Remove unnecessary symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/xkb/compiled

# Create filelist
{
   FILESLIST=${PWD}/files.list
   pushd $RPM_BUILD_ROOT
   find .%{_datadir}/X11/xkb -type d | sed -e "s/^\./%dir /g" > $FILESLIST
   find .%{_datadir}/X11/xkb -type f | sed -e "s/^\.//g" >> $FILESLIST
   popd
}

%files -f files.list
%defattr(-,root,root,-)
%license COPYING
%{_datadir}/X11/xkb/rules/xorg
%{_datadir}/X11/xkb/rules/xorg.lst
%{_datadir}/X11/xkb/rules/xorg.xml

%exclude %{_mandir}
%exclude %{_localedir}
%exclude %{_datadir}/pkgconfig

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Feb 08 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.20-1
- xkeyboard-config 2.20 (#1401753)

* Tue Jun 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 2.14-1
- xkeyboard-config 2.14 (#1194871)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.9-4
- Mass rebuild 2013-12-27

* Wed Jul 17 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.9-3
- Fix changelog - percent sign needs to be escaped

* Wed Jul 17 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.9-2
- Fix up three bogus changelog dates

* Thu May 30 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.9-1
- xkeyboard-config 2.9

* Wed May 15 2013 Daniel Drake <dsd@laptop.org> 2.8-3
- Add upstream patches for OLPC mechanical keyboard support

* Tue Apr 16 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8-2
- Fix a bunch of language codes (#952510, #952519)

* Thu Jan 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8-1
- xkeyboard-config 2.8

* Wed Jan 02 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.7-4
- Fix Mali layout previously mapped to in(mal) (#647433)

* Wed Nov 14 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.7-3
- Rebuild with fixed xkbcomp, re-create the right directory listing (not
  that anyone actually uses it)

* Wed Oct 31 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.7-2
- Fix {?dist} tag

* Thu Sep 27 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7-1
- xkeyboard-config 2.7

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6-2
- Revert broken fix for is keyboard (#826220)

* Thu May 31 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6-1
- xkeyboard-config 2.6
- change source URL, 2.6 is in a different directory
- force autoreconf, update to use intltoolize as autopoint

* Wed May 23 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.1-2
- Add upstream patch to fix OLPC azerty keyboard

* Thu Feb 02 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.5.1-1
- xkeyboard-config 2.5.1

* Mon Jan 23 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.5-1
- xkeyboard-config 2.5

* Thu Jan 19 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.4.1-4
- Move Ungrab and ClearGrab from the default layout to option
  grab:break_actions (#783044)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.4.1-2
- Change Serbian layouts to mark the cyrillic ones (#769751)

* Wed Oct 05 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.4.1-1
- xkeyboard-config 2.4.1
- change source URL from ftp.x.org to http://xorg.freedesktop.org, ftp takes
  too long to update

* Tue Jun 14 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.3-2
- Add 0001-Use-XSL-to-generate-man-page-from-the-rules-XML.patch, ship
  man-page
- Fix up broken git repo initialization when building from a tarball

* Thu Jun 02 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.3-1
- xkeyboard-config 2.3

* Fri Apr 15 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-2.20110415git19a0026b5
- Snapshot from git to fix French Canadian layouts (#694472)

* Wed Apr 06 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-1
- xkeyboard-config 2.2.1, 2.2 had a broken configure check
- Add new BR and don't disable build/runtime deps checks

* Mon Apr 04 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.2-1
- xkeyboard-config 2.2
- reinstate the git bits removed in previous commit

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.99-2
- Update to 2.1.99 release

* Fri Mar 11 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99-1.20110311-git9333b2f3
- add bits required to build from git
- update to today's git snapshot

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.1-1
- xkeyboard-config 2.1

* Thu Nov 25 2010 Bastien Nocera <bnocera@redhat.com> 2.0-2
- Use new touchpad toggle keysyms

* Wed Sep 29 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.0-1
- xkeyboard-config 2.0

* Mon Aug 16 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.9-1
- xkeyboard-config 1.9
- update Source URL, hosted on x.org now.
- add -devel package for pkgconfig file added in 1.9.
- drop upstreamed patches.

* Tue Jul 20 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8-6
- spec file cleanup. Patch by Parag An (#226562)

* Tue May 04 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8-5
- 0001-Remove-duplicate-BKSL-key-mappings-from-hin-wx-layou.patch: remove
  the duplicate mapping from hin-wx layout, it breaks iok (FDO 26947).

* Tue Apr 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8-4
- Move F-12 patches forward, upstream is a bit unresponsive.

* Tue Mar 02 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8-3
- only package files in /usr/share/X11/xkb (#569400)

* Fri Feb 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8-2
- Package the translations too (#563815).

* Mon Feb 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8-1
- xkeyboard-config 1.8

* Fri Jan 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7-3
- Remove xkbdata provides. The xkbdata provides was introduced when
  xorg-x11-drv-xkbdata moved to xkeyboard-config. It's purpose was mainly to
  protect against future renamings of this module which is unlikely to
  happen anytime soon.

* Wed Jan 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7-2
- Specify version for xkbdata provides and obsoletes. According to the
  changelog, the last xkbdata version was 1.0.1-8. Although xkeyboard-config
  restarted the versioning, by now we're well above 1.0, so a simple
  Provides is enough.

* Wed Jan 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7-1
- xkeyboard-config 1.7

* Tue Aug 18 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6-3
- xkeyboard-config-1.6-caps-super.patch: add caps:super option (#505187)
- xkeyboard-config-1.6-caps-hyper.patch: add caps:hyper option (#505187)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 29 2009 Peter Hutterer <peter.hutterer@redhat.com> - 1.6-1
- xkeyboard-config 1.6
- Dropping all patches, merged upstream.

* Tue Apr 07 2009 Peter Hutterer <peter.hutterer@redhat.com> - 1.5-5
- xkeyboard-config-1.5-terminate.patch: remove Terminate_Server from default
  pc symbols, add terminate:ctrl_alt_bksp.

* Thu Mar 05 2009 Peter Hutterer <peter.hutterer@redhat.com> - 1.5-4
- xkeyboard-config-1.5-suspend-hibernate.patch: Map I213 to XF86Suspend, and
  I255 to XF86Hibernate.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5-2
- xkeyboard-config-1.5-evdevkbds.patch: include model-specifics when using
  evdev.

* Mon Feb 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 
- purge obsolete patches.

* Wed Jan 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5-1
- xkeyboard-config 1.5

* Tue Jan 27 2009 Bernie Innocenti <bernie@codewiz.org> 1.4-9
- Backport fix for the it(olpc) layout

* Mon Jan 05 2009 Peter Hutterer <peter.hutterer@redhat.com> - 1.4-8
- xkeyboard-config-1.4-abnt2.patch: fix , and . mixup in abnt2 (#470153)

* Mon Nov 24 2008 Peter Hutterer <peter.hutterer@redhat.com> - 1.4-7
- Switch to using git patches, modelled after xorg-x11-server.
- CVS remove unused patches.

* Sat Nov 22 2008 Matthias Clasen <mclasen@redhat.com> - 1.4-6
- Improve %%summary and %%description
- Better URL

* Thu Nov 13 2008 Peter Hutterer  <peter.hutterer@redhat.com> - 1.4-5
- xkeyboard-config-1.4-jp-tilde.patch: TLDE in jp is Zenkaku/Hankaku, and BKSL
  should be bracket right/brace right (#469537).

* Fri Oct 24 2008 Peter Hutterer  <peter.hutterer@redhat.com> - 1.4-4
- xkeyboard-config-1.4-battery.patch: add XF86 syms for Battery, Bluetooth,
  Wlan and UWB to usinet.

* Tue Oct 14 2008 Peter Hutterer  <peter.hutterer@redhat.com> - 1.4-3
- xkeyboard-config-1.4-tj-variant.patch: add legacy and basic tj layouts
  (#455796)

* Wed Oct  1 2008 Matthias Clasen  <mclasen@redhat.com> - 1.4-2
- Update to 1.4

* Mon Sep 29 2008 Peter Hutterer  <peter.hutterer@redhat.com> - 1.3-2
- xkeyboard-config-1.3-AC11-mapping-is.patch: fix AC11 mapping for icelandic
  keyboard layout (#241564)

* Wed May 28 2008 Matthias Clasen  <mclasen@redhat.com> - 1.3-1
- Update to 1.3

* Mon Apr 14 2008 Matthias Clasen  <mclasen@redhat.com> - 1.2-3
- Also add back and forward keys to pc105 (#441398)

* Wed Apr  9 2008 Matthias Clasen  <mclasen@redhat.com> - 1.2-2
- Make pc105 have inet keys, not 100% correct, but better than
  having the kbd driver report "us+inet" which confused XKB and
  higher layers (#441398)

* Thu Feb  7 2008 Matthias Clasen  <mclasen@redhat.com> - 1.2-1
- Update to 1.2
- Remove upstreamed olpc patches

* Mon Nov 19 2007 Bernardo Innocenti <bernie@codewiz.org> 1.1-5.20071119cvs
- Upgrade xkeyboard-config snapshot to cvs20071119
- Add olpc-xkeyboard-config-af.patch
- Add olpc-xkeyboard-config-kz-group.patch
- Add olpc-xkeyboard-config-ng-group.patch
- Add olpc-xkeyboard-config-ng-h.patch
- Remove olpc-xkeyboard-config-ara-fixes.patch (integrated upstream)
- Remove olpc-xkeyboard-config-br-accents.patch (integrated upstream)
- Remove olpc-xkeyboard-config-es-accents.patch (integrated upstream)
- Remove olpc-xkeyboard-config-us-typo.patch (integrated upstream)

* Sat Oct 27 2007 Bernardo Innocenti <bernie@codewiz.org> 1.1-5.20071009cvs
- Add olpc-xkeyboard-config-ara-fixes.patch
- Add olpc-xkeyboard-config-br-accents.patch
- Add olpc-xkeyboard-config-es-accents.patch
- Add olpc-xkeyboard-config-us-typo.patch

* Tue Oct 09 2007 Bernardo Innocenti <bernie@codewiz.org> - 1.1-4.20071009cvs
- Upgrade xkeyboard-config snapshot to cvs20071009

* Sat Oct 06 2007 Bernardo Innocenti <bernie@codewiz.org> - 1.1-4.20071006cvs
- Resync with Fedora Development
- Upgrade xkeyboard-config snapshot to cvs20071006

* Sat Oct  6 2007 Matthias Clasen <mclasen@redhat.com> - 1.1-3
- Somehow the Dell M65 model lost its vendor

* Wed Sep 26 2007 Matthias Clasen <mclasen@redhat.com> - 1.1-2
- Pick up the respun 1.1 release

* Wed Sep 26 2007 Matthias Clasen <mclasen@redhat.com> - 1.1-1
- Update to 1.1
- Drop upstreamed patches

* Wed Sep  5 2007 Matthias Clasen <mclasen@redhat.com> - 1.0-1
- Update to 1.0
- Drop upstreamed patches
- Update remaining patches

* Tue Sep 04 2007 Bernardo Innocenti <bernie@codewiz.org> - 0.8.20070829cvs
- Update OLPC patch to take11 (use old evdev key name for the "view source"
  key)

* Tue Sep 04 2007 Bernardo Innocenti <bernie@codewiz.org> - 0.8.20070829cvs
- Downgrade xkeyboard-config snapshot to cvs20070829 to revert
  recent evdev changes (the version of xkbcomp we ship chokes on them).

* Fri Aug 31 2007 Bernardo Innocenti <bernie@codewiz.org> - 0.7.20070831cvs
- Update OLPC patch to take10 (integrate changes requested by
  upstream reviewer)

* Wed Aug 22 2007 Bernardo Innocenti <bernie@codewiz.org> - 0.6.20070820cvs
- Update OLPC patch to take9 (fix 'h' key on us layout)

* Wed Aug 22 2007 Bernardo Innocenti <bernie@codewiz.org> - 0.5.20070820cvs
- Update OLPC patch to take8 (don't use olpc variant for et layout)

* Wed Aug 22 2007 Bernardo Innocenti <bernie@codewiz.org> - 0.4.20070820cvs
- Update OLPC patch to take7

* Mon Aug 20 2007 Bernardo Innocenti <bernie@codewiz.org> - 0.3.20070820cvs
- Update to CVS snapshot 20070820

* Fri Jun 29 2007 Bernardo Innocenti <bernie@codewiz.org> - 0.2.20070629cvs
- Update to CVS snapshot 20070629
- Add OLPC patch
- Drop patches already integrated upstream

* Fri Sep  1 2006 Alexander Larsson <alexl@redhat.com> - 0.8-7
- Update macbook patch to be closer to what got in upstream
- (kp enter is ralt, not the option key)

* Fri Sep  1 2006 Matthias Clasen <mclasen@redhat.com> - 0.8-6
- Add support for Korean 106 key keyboards (204158)

* Tue Aug 29 2006 Alexander Larsson <alexl@redhat.com> - 0.8-5
- Add MacBook model and geometry, plus alt_win option

* Tue Aug 22 2006 Matthias Clasen <mclasen@redhat.com> 0.8-4
- Fix geometry description for Thinkpads
- Add a Kinesis model
- Add Dell Precision M65 geometry and model

* Tue Aug 22 2006 Adam Jackson <ajackson@redhat.com> 0.8-3
- Add Compose semantics to right Alt when that's ISO_Level3_Shift (#193922)

* Fri Jul 07 2006 Mike A. Harris <mharris@redhat.com> 0.8-2
- Rename spec file from xorg-x11-xkbdata to xkeyboard-config.spec

* Fri Jul 07 2006 Mike A. Harris <mharris@redhat.com> 0.8-1
- Renamed package from 'xorg-x11-xkbdata' to 'xkeyboard-config' to match the
  upstream project name and tarball.  I kept the rpm changelog intact however
  to preserve history, so all entries older than today, are from the
  prior 'xorg-x11-xkbdata' package.  (#196229,197939)
- Added "Obsoletes: xorg-x11-xkbdata"
- Removed 'pre' script from spec file, as that was a temporary hack to help
  transition from modular X.Org xkbdata to modular xkeyboard-config during
  FC5 development.  The issue it resolved is not present in any officially
  released distribution release or updates, so the hack is no longer needed.

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-8.xkbc0.8.0
- Embed xkeyboard-config version in Release field so we can tell from the
  filename what is really in this package without having to look in the
  spec file.  We should rename the package to xkeyboard-config and restart
  the versioning.

* Tue Jun 06 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-8
- Added "BuildRequires: perl(XML::Parser)" for (#194188)

* Sat Mar 04 2006 Ray Strode <rstrode@redhat.com> 1.0.1-7
- Update to 0.8.

* Wed Mar 01 2006 Ray Strode <rstrode@redhat.com> 1.0.1-6
- Turn on compat symlink (bug 183521)

* Tue Feb 28 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-5
- Fixed rpm pre script upgrade/install testing
- Rebuild package as 1.0.1-5 in rawhide, completing the transition to
  xkeyboard-config.

* Tue Feb 28 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-4.0.7.xkbcfg.5
- Added rpm pre script, to pre-remove the symbols/pc during package upgrades,
  to avoid an rpm cpio error if the X11R7.0 modular xkbdata package is already
  installed, because rpm can not replace a directory with a file.  

* Fri Feb 24 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-4.0.7.xkbcfg.1
- Package renamed to xorg-x11-xkbdata and version/release tweaked since it
  is too late to add new package names to Fedora Core 5 development.
- Added "Provides: xkeyboard-config" virtual provide.

* Fri Feb 24 2006 Mike A. Harris <mharris@redhat.com> 0.7-1
- Initial package created with xkeyboard-config-0.7.

* Tue Feb 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Added xkbdata-1.0.1-greek-fix-bug181313.patch to fix (#181313,181313)
- Added xkbdata-1.0.1-cz-fix-bug177362.patch to fix (#177362,178892)

* Thu Feb 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added xkbdata-1.0.1-sysreq-fix-bug175661.patch to fix (#175661)

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated to xbitmaps 1.0.1 from X11R7.0

* Sat Dec 17 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated to xbitmaps 1.0.0 from X11R7 RC4.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Add a few missing rpm 'dir' directives to file manifest.
- Bump release, and build as a 'noarch' package.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated to xkbdata 0.99.1 from X11R7 RC2.
