Summary: Shared MIME information database
Name: shared-mime-info
Version: 1.8
Release: 4%{?dist}
License: GPLv2+
Group: System Environment/Base
URL: http://freedesktop.org/Software/shared-mime-info
Source0: http://people.freedesktop.org/~hadess/%{name}-%{version}.tar.xz
Source1: gnome-mimeapps.list
# Generated with:
# for i in `cat /home/hadess/Projects/jhbuild/totem/data/mime-type-list.txt | grep -v audio/flac | grep -v ^#` ; do if grep MimeType /home/hadess/Projects/jhbuild/rhythmbox/data/rhythmbox.desktop.in.in | grep -q "$i;" ; then echo "$i=rhythmbox.desktop;org.gnome.Totem.desktop;" >> totem-defaults.list ; else echo "$i=org.gnome.Totem.desktop;" >> totem-defaults.list ; fi ; done ; for i in `cat /home/hadess/Projects/jhbuild/totem/data/uri-schemes-list.txt | grep -v ^#` ; do echo "x-scheme-handler/$i=org.gnome.Totem.desktop;" >> totem-defaults.list ; done
Source2: totem-defaults.list
# Generated with:
# for i in `grep MimeType= /usr/share/applications/org.gnome.FileRoller.desktop | sed 's/MimeType=//' | sed 's/;/ /g'` application/x-source-rpm ; do if ! `grep -q $i defaults.list` ; then echo $i=org.gnome.FileRoller.desktop\; >> file-roller-defaults.list ; fi ; done
Source3: file-roller-defaults.list
# Generated with:
# for i in `grep MimeType= /usr/share/applications/eog.desktop | sed 's/MimeType=//' | sed 's/;/ /g'` ; do echo $i=eog.desktop\; >> eog-defaults.list ; done
Source4: eog-defaults.list

# Work-around for https://bugs.freedesktop.org/show_bug.cgi?id=40354
Patch0: 0001-Remove-sub-classing-from-OO.o-mime-types.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libxml2-devel
BuildRequires:  glib2-devel
BuildRequires:  gettext
# For intltool:
BuildRequires: perl(XML::Parser) intltool

Requires(post): glib2
Requires(post): coreutils

# Disable pkgconfig autodep
%global __requires_exclude ^/usr/bin/pkg-config$

%description
This is the freedesktop.org shared MIME info database.

Many programs and desktops use the MIME system to represent the types of
files. Frequently, it is necessary to work out the correct MIME type for
a file. This is generally done by examining the file's name or contents,
and looking up the correct MIME type in a database.

%prep
%autosetup

%build
%configure --disable-silent-rules --disable-update-mimedb
# not smp safe, pretty small package anyway
make

%install
# speed build a bit
PKGSYSTEM_ENABLE_FSYNC=0 \
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_datadir}/mime -type d \
| sed -e "s|^$RPM_BUILD_ROOT|%%dir |" > %{name}.files
find $RPM_BUILD_ROOT%{_datadir}/mime -type f -not -path "*/packages/*" \
| sed -e "s|^$RPM_BUILD_ROOT|%%ghost |" >> %{name}.files

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
install -m 644 %SOURCE1 $RPM_BUILD_ROOT/%{_datadir}/applications/gnome-mimeapps.list
cat %SOURCE2 >> $RPM_BUILD_ROOT/%{_datadir}/applications/gnome-mimeapps.list
cat %SOURCE3 >> $RPM_BUILD_ROOT/%{_datadir}/applications/gnome-mimeapps.list
cat %SOURCE4 >> $RPM_BUILD_ROOT/%{_datadir}/applications/gnome-mimeapps.list

# Support fallback/generic mimeapps.list (currently based on gnome-mimeapps.list), see
# https://lists.fedoraproject.org/pipermail/devel/2015-July/212403.html
# https://bugzilla.redhat.com/show_bug.cgi?id=1243049
cp $RPM_BUILD_ROOT%{_datadir}/applications/gnome-mimeapps.list \
   $RPM_BUILD_ROOT%{_datadir}/applications/mimeapps.list

## remove bogus translation files
## translations are already in the xml file installed
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/*


%post
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null ||:

%posttrans
%{_bindir}/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null ||:

%files -f %{name}.files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README NEWS HACKING shared-mime-info-spec.xml
%{_bindir}/*
%{_datadir}/mime/packages/*
%{_datadir}/applications/mimeapps.list
%{_datadir}/applications/gnome-mimeapps.list
# better to co-own this dir than to pull in pkgconfig
%dir %{_datadir}/pkgconfig
%{_datadir}/pkgconfig/shared-mime-info.pc
%{_mandir}/man*/*

%changelog
* Wed Sep 20 2017 Bastien Nocera <bnocera@redhat.com> - 1.8-4
+ shared-mime-info-1.8-4
- Fix CSV files being associated with LibreOffice Math instead
  of LibreOffice Calc
- Resolves: #1438589

* Wed Mar 22 2017 Bastien Nocera <bnocera@redhat.com> - 1.8-3
+ shared-mime-info-1.8-3
- Remove triggers, they're not supported in RHEL 7.4's RPM
Resolves: #1433916

* Wed Mar 01 2017 Bastien Nocera <bnocera@redhat.com> - 1.8-2
+ shared-mime-info-1.8-2
- Rebase to 1.8
Resolves: #1387045

* Fri Jul 17 2015 Matthias Clasen <mclasen@redhat.com> 1.1-9
- Add support for raw disk images
  Related: #1211198

* Tue Jun 30 2015 Ray Strode <rstrode@redhat.com> 1.1-8
- Update default file assocations to match rebased names
  Resolves: #1235413

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.1-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1-6
- Mass rebuild 2013-12-27

* Sat Jun  8 2013 Matthias Clasen <mclasen@redhat.com> - 1.1-5
- Drop pkgconfig dep, instead co-own /usr/share/pkgconfig

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.1-4
- Update for file-roller desktop file vendor prefix removal

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.1-3
- Update for eog desktop file vendor prefix removal

* Sun Feb 17 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.1-2
- De-vendorize defaults.list (https://fedorahosted.org/fesco/ticket/1077)

* Wed Feb 13 2013 Bastien Nocera <bnocera@redhat.com> 1.1-1
- Update to 1.1

* Fri Nov 30 2012 Bastien Nocera <bnocera@redhat.com> 1.0-6
- Open src.rpm files in file-roller instead of PackageKit

* Mon Nov 05 2012 Bastien Nocera <bnocera@redhat.com> 1.0-6
- Rebuild file-roller's default list

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Rex Dieter <rdieter@fedoraproject.org> 
- 1.0-4
- defaults.list: s/mozilla-firefox/firefox/ (see #736558)
- defaults.list: s/gpk-install-file/gpk-install-local-file/
- defaults.list: application/x-catalog=gpk-install-catalog.desktop (#770019) 

* Fri May 11 2012 Bastien Nocera <bnocera@redhat.com> 1.0-3
- Use gnome-disk-image-mounter from gnome-disk-utility to handle
  CD images by default (#820403)

* Wed Mar  7 2012 Matthias Clasen <mclasen@redhat.com> - 1.0-2
- Own/%%ghost files generated by update-mime-database from
  freedesktop.org.xml (patch by Ville Skyttä, #716451))

* Tue Jan 17 2012 Bastien Nocera <bnocera@redhat.com> 1.0-1
- Update to 1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Jon Masters <jcm@jonmasters.org> 0.91-6
- Fix interpretation of MP3 files as application/x-designer (#755472)

* Mon Oct 24 2011 Rex Dieter <rdieter@fedoraproject.org> 0.91-5
- s/mozilla-firefox.desktop/firefox.desktop/ (f17+, #736558)

* Thu Oct 13 2011 Bastien Nocera <bnocera@redhat.com> 0.91-4
- Make Evolution the default calendar (and not Gedit...)

* Thu Oct 13 2011 Bastien Nocera <bnocera@redhat.com> 0.91-3
- Make shotwell the default for camera roll handling
- Make shotwell-viewer the default image viewer (for the
  image types it handles)
- Prefer Rhythmbox to Totem for music files

* Sun Sep 18 2011 Bastien Nocera <bnocera@redhat.com> 0.91-2
- Fix changelog entries

* Sun Sep 18 2011 Bastien Nocera <bnocera@redhat.com> 0.91-1
- Update to 0.91

* Thu Aug 25 2011 Bastien Nocera <bnocera@redhat.com> 0.90-9
- Never try to load OO.o files in file-roller

* Thu May 26 2011 Bastien Nocera <bnocera@redhat.com> 0.90-8
- Fix LibreOffice associations (patch from Caolan McNamara, #707971)

* Thu Apr 21 2011 Bastien Nocera <bnocera@redhat.com> 0.90-7
- Fix name of nautilus.desktop file (#698502)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Bastien Nocera <bnocera@redhat.com> 0.90-5
- Auto-generate file-roller's bindings as well

* Wed Dec 08 2010 Bastien Nocera <bnocera@redhat.com> 0.90-4
- Update defaults.list and update for newer desktop names,
  with help from Edward Sheldrake (#659457)

* Tue Dec 07 2010 Bastien Nocera <bnocera@redhat.com> 0.90-3
- Add Firefox as the default for application/xhtml+xml
  (#660657)

* Wed Dec 01 2010 Bastien Nocera <bnocera@redhat.com> 0.90-2
- Update list of defaults, adding new mime-types for Totem,
  as well as scheme handlers, and install defaults for
  Evolution and Firefox

* Wed Dec 01 2010 Bastien Nocera <bnocera@redhat.com> 0.90-1
- Update to 0.90

* Thu Nov  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.80-2
- rebuild for new libxml

* Thu Sep 30 2010 Bastien Nocera <bnocera@redhat.com> 0.80-1
- Update to 0.80

* Tue Jul  6 2010 Colin Walters <walters@verbum.org> - 0.71-4
- Fix previous change to be Requires(post); spotted by
  Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>

* Sat Jul  3 2010 Colin Walters <walters@verbum.org> - 0.71-3
- Requires(pre) on glib, since update-mime-database uses it
- Remove /dev/null redirection, we should see future errors
  And really, RPM is dumb here - this stuff needs to go to
  log files.

* Tue Jun 01 2010 Bastien Nocera <bnocera@redhat.com> 0.71-2
- Update some OO.o defaults, patch from Caolan McNamara

* Mon Feb 01 2010 Bastien Nocera <bnocera@redhat.com> 0.71-1
- Update to 0.71

* Tue Oct 06 2009 Bastien Nocera <bnocera@redhat.com> 0.70-1
- Update to 0.70

* Thu Sep 24 2009 - Caolán McNamara <caolanm@redhat.com> - 0.60-5
- Resolves: rhbz#508559 openoffice.org desktop files changed name

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 04 2009 - Bastien Nocera <bnocera@redhat.com> - 0.60-3
- Remove Totem as handling Blu-ray and HD-DVD
- Use brasero-ncb.desktop instead of nautilus-cd-burner for blank devices
- Update media mime-types for Rhythmbox/Totem

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 - Bastien Nocera <bnocera@redhat.com> - 0.60-1
- Update to 0.60

* Mon Dec 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.51-6
- Update with comments from Orcan Ogetbil <orcanbahri@yahoo.com>

* Wed Nov 26 2008 - Julian Sikorski <belegdol[at]gmail[dot]com> - 0.51-5
- Fix text/plain, gedit installs gedit.desktop and not gnome-gedit.desktop

* Wed Oct 29 2008 - Bastien Nocera <bnocera@redhat.com> - 0.51-4
- Add patch to avoid picture CD being anything with a pictures directory
  (#459365)

* Thu Oct 02 2008 - Bastien Nocera <bnocera@redhat.com> - 0.51-3
- Use evince, not tetex-xdvi.desktop for DVI files (#465242)

* Mon Sep 01 2008 - Bastien Nocera <bnocera@redhat.com> - 0.51-2
- Use Firefox and not redhat-web as the default app for HTML files (#452184)

* Wed Jul 23 2008 - Bastien Nocera <bnocera@redhat.com> - 0.51-1
- Update to 0.51

* Tue Jul 22 2008 - Bastien Nocera <bnocera@redhat.com> - 0.50-1
- Update to 0.50

* Sat Jun 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.40-2
- update license tag

* Wed Jun 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.40-1
- Update to 0.40

* Mon May 12 2008 - Bastien Nocera <bnocera@redhat.com> - 0.30-1
- Update to 0.30

* Fri May  2 2008 David Zeuthen <davidz@redhat.com> - 0.23-9
- Fix defaults for x-content/image-dcf (#445032)

* Thu Apr 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.23-8
- Make mount-archive.desktop the default for iso images (#442960)

* Tue Apr 15 2008 Matthias Clasen <mclasen@redhat.com> - 0.23-7
- Update the desktop file name for Gimp, too

* Tue Apr 15 2008 Matthias Clasen <mclasen@redhat.com> - 0.23-6
- Change default for rpm to gpk-install-file (#442485)

* Thu Mar 27 2008 - Bastien Nocera <bnocera@redhat.com> - 0.23-5
- Make Totem the default for the mime-types it handles (#366101)
- And make sure Rhythmbox is the second default only for the mime-types
  it handles

* Thu Mar 20 2008 Matthias Clasen <mclasen@redhat.com> - 0.23-4
- Change default for rpm to pk-install-file

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.23-3
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Matthias Clasen <mclasen@redhat.com> - 0.23-2
- Add defaults for content types

* Tue Dec 18 2007 - Bastien Nocera <bnocera@redhat.com> - 0.23-1
- Update to 0.23

* Tue Nov 13 2007 - Bastien Nocera <bnocera@redhat.com> - 0.22-5
- Remove Totem as the default music/movie player, it will be the
  default for movies, as only it handles them, and Rhythmbox can
  handle missing plugins now

* Mon Nov 05 2007 - Bastien Nocera <bnocera@redhat.com> - 0.22-4
- Make Totem the default for the mime-types it handles (#366101)

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 0.22-3
- Rebuild for PPC toolchain bug
- BuildRequires: gawk

* Tue Aug 21 2007 - Bastien Nocera <bnocera@redhat.com> - 0.22-2
- Don't say that webcal files are handled by evolution-2.0, it can't
- Disable vCard mapping as well, as evolution doesn't handle it
  (See http://bugzilla.gnome.org/show_bug.cgi?id=309073)

* Mon Jul 30 2007 - Bastien Nocera <bnocera@redhat.com> - 0.22-1
- Update to 0.22

* Tue Apr 17 2007 - Bastien Nocera <bnocera@redhat.com> - 0.20-2
- Fix the dia association (#194313)

* Tue Feb 06 2007 - Bastien Nocera <bnocera@redhat.com> - 0.20-1
- Update to 0.20, and remove outdated patches

* Fri Nov 10 2006 Christopher Aillon <caillon@redhat.com> - 0.19-2
- Alias image/pdf to application/pdf

* Fri Aug 25 2006 Christopher Aillon <caillon@redhat.com> - 0.19-1
- Update to 0.19

* Wed Jul 26 2006 Matthias Clasen <mclasen@redhat.com> - 0.18-2
- add an inode/directory entry to defaults.list (#187021)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.18-1.1
- rebuild

* Wed Jul  5 2006 Kristian Høgsberg <krh@redhat.com> - 0.18-1
- Update to 0.18 and drop backported patches.

* Thu Jun 29 2006 Kristian Høgsberg <krh@redhat.com> - 0.17-3
- Adding PDF fix backported from CVS.

* Wed Mar 22 2006 Matthias Clasen <mclasen@redhat.com> - 0.17-2
- Backport upstream change to fix postscript vs. matlab confusion

* Thu Mar 16 2006 Matthias Clasen <mclasen@redhat.com> - 0.17-1
- Update to 0.17

* Mon Feb 13 2006 Ray Strode <rstrode@redhat.com> - 0.16.cvs20060212-3
- add gthumb as fallback

* Mon Feb 13 2006 Ray Strode <rstrode@redhat.com> - 0.16.cvs20060212-2
- make eog the default image viewer

* Sun Feb 12 2006 Christopher Aillon <caillon@redhat.com> - 0.16.cvs20060212-1
- Newer CVS snapshot

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.16.cvs20051219-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Caolan McNamara <caolanm@redhat.com> - 0.16.cvs20051219-2
- rh#179138# add openoffice.org as preferred app for oasis formats 

* Mon Dec 19 2005 Matthias Clasen <mclasen@redhat.com> - 0.16.cvs20051219-1
- Newer cvs snapshot

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Matthias Clasen <mclasen@redhat.com> - 0.16.cvs20051201-1
- Incorporate upstream changes

* Wed Nov 02 2005 John (J5) Palmieri <johnp@redhat.com> - 0.16.cvs20051018-2
- Change all refs of eog to gthumb in defaults.list

* Tue Oct 18 2005 Matthias Clasen <mclasen@redhat.com> - 0.16.cvs20051018-1
- Incorporate upstream changes

* Wed Oct 12 2005 Matthias Clasen <mclasen@redhat.com> - 0.16-6
- Add glade to defaults.list

* Mon Oct  3 2005 Matthias Clasen <mclasen@redhat.com> - 0.16-5
- Make sure Type1 fonts are recognized as such (#160909)

* Fri Jun 17 2005 David Zeuthen <davidz@redhat.com> - 0.16-4
- Add MIME-types for .pcf Cisco VPN settings files (fdo #3560)

* Fri May 20 2005 Dan Williams <dcbw@redhat.com> - 0.16-3
- Update OpenOffice.org desktop file names. #155353
- WordPerfect default now OOo Writer, since Abiword is in Extras

* Sun Apr  3 2005 David Zeuthen <davidz@redhat.com> - 0.16-2
- Make Evince the default for application/pdf and application/postscript
- Remove remaining references to gnome-ggv (application/x-gzpostscript and
  image/x-eps) as this is no longer in the distribution

* Fri Apr  1 2005 David Zeuthen <davidz@redhat.com> - 0.16-1
- Update to upstream release 0.16
- Drop all patches as they are in the new upstream release

* Wed Mar  9 2005 David Zeuthen <davidz@redhat.com> - 0.15-11
- Add mimetypes for OOo2 (#150546)

* Mon Oct 18 2004 Alexander Larsson <alexl@redhat.com> - 0.15-10
- Fix for mime sniffing on big-endian

* Thu Oct 14 2004 Colin Walters <walters@redhat.com> - 0.15-9
- Handle renaming of hxplay.desktop to realplay.desktop

* Wed Oct 13 2004 Matthias Clasen <mclasen@redhat.com> - 0.15-8
- Handle XUL files. #134122

* Wed Oct 13 2004 Colin Walters <walters@redhat.com> - 0.15-7
- Make helix default for ogg and mp3, will switch wav/flac too 
  when support is added

* Wed Oct  6 2004 Alexander Larsson <alexl@redhat.com> - 0.15-6
- Change default pdf viewer to ggv

* Tue Sep  7 2004 Alexander Larsson <alexl@redhat.com> - 0.15-4
- Fixed evo desktop file reference in defaults.list

* Mon Sep  6 2004 Caolan McNamara <caolanm@redhat.com> - 0.15-3
- wpd can be opened in abiword, but not in openoffice.org (#114907)

* Fri Sep  3 2004 Alexander Larsson <alexl@redhat.com> - 0.15-2
- Add list of default apps (#131643)

* Mon Aug 30 2004 Jonathan Blandford <jrb@redhat.com> 0.15-1
- bump version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar 22 2004 Alex Larsson <alexl@redhat.com> 0.14-1
- update to 0.14

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Alexander Larsson <alexl@redhat.com> 0.13-1
- 0.13

* Fri Jan 16 2004 Alexander Larsson <alexl@redhat.com> mime-info
- Initial build.
