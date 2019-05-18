#define  prever     rc3
#define  prever_dot .rc3
#define  postver    a

Summary:  The Advanced Linux Sound Architecture (ALSA) library
Name:     alsa-lib
Version:  1.1.4.1
Release:  2%{?prever_dot}%{?dist}
License:  LGPLv2+
Group:    System Environment/Libraries
URL:      http://www.alsa-project.org/

Source:   ftp://ftp.alsa-project.org/pub/lib/%{name}-%{version}%{?prever}%{?postver}.tar.bz2
Source10: asound.conf
Source11: modprobe-dist-alsa.conf
Source12: modprobe-dist-oss.conf
Patch0:   alsa-lib-1.1.4.1-post.patch
Patch1:   alsa-lib-1.1.0-config.patch

BuildRequires:  doxygen
BuildRequires:  autoconf automake libtool
Requires(post): /sbin/ldconfig, coreutils

%description
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.

This package includes the ALSA runtime libraries to simplify application
programming and provide higher level functionality as well as support for
the older OSS API, providing binary compatibility for most OSS programs.

%package  devel
Summary:  Development files from the ALSA library
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.

This package includes the ALSA development libraries for developing
against the ALSA libraries and interfaces.

%prep
%setup -q -n %{name}-%{version}%{?prever}%{?postver}
%patch0 -p1 -b .post
%patch1 -p1 -b .config
autoreconf -f -i

%build
%configure --disable-aload --with-plugindir=%{_libdir}/alsa-lib --disable-alisp

# Remove useless /usr/lib64 rpath on 64bit archs
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1
make doc

%install
make DESTDIR=%{buildroot} install

# We need the library to be available even before /usr might be mounted
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libasound.so.* %{buildroot}/%{_lib}
ln -snf ../../%{_lib}/libasound.so.2 %{buildroot}%{_libdir}/libasound.so

# Install global configuration files
mkdir -p -m 755 %{buildroot}/etc
install -p -m 644 %{SOURCE10} %{buildroot}/etc

# Install the modprobe files for ALSA
mkdir -p -m 755 %{buildroot}/lib/modprobe.d/
install -p -m 644 %{SOURCE11} %{buildroot}/lib/modprobe.d/dist-alsa.conf
# bug#926973, place this file to the doc directory
mkdir -p -m 755 %{buildroot}%{_defaultdocdir}/%{name}/
install -p -m 644 %{SOURCE12} %{buildroot}%{_defaultdocdir}/%{name}/modprobe-dist-oss.conf

# Create UCM directory
mkdir -p %{buildroot}/%{_datadir}/alsa/ucm
# Remove all UCM files (should be selected by architecture)
rm -rf %{buildroot}/%{_datadir}/alsa/ucm/*
# Remove smixer .so modules
rm -rf %{buildroot}/%{_libdir}/alsa-lib/smixer

#Remove libtool archives.
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING TODO doc/asoundrc.txt
# file is as old as 0.2.0 / Red Hat bugzilla #510212
#doc Changelog
%{_defaultdocdir}/%{name}/modprobe-dist-oss.conf
%config %{_sysconfdir}/asound.conf
/%{_lib}/libasound.so.*
%{_bindir}/aserver
#%{_libdir}/alsa-lib/
%{_datadir}/alsa/
/lib/modprobe.d/dist-*

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/
%{_includedir}/alsa/
%{_includedir}/sys/asoundlib.h
%{_libdir}/libasound.so
%{_libdir}/pkgconfig/alsa.pc
%{_datadir}/aclocal/alsa.m4

%changelog
* Sun Oct 22 2017 Jaroslav Kysela <jkysela@redhat.com> - 1.1.4.1-2
- Updated to 1.1.4.1
- Resolves: rhbz#1485645

* Wed Mar  1 2017 Jaroslav Kysela <jkysela@redhat.com> - 1.1.3-3
- Updated to 1.1.3
- Resolves: rhbz#1399508

* Mon Jun  6 2016 Jaroslav Kysela <jkysela@redhat.com> - 1.1.1-1
- Updated to 1.1.1
- Resolves: rhbz#1297932

* Tue Sep 16 2014 Jaroslav Kysela <jkysela@redhat.com> - 1.0.28-2
- Fix minor coverity bug

* Mon Sep 15 2014 Jaroslav Kysela <jkysela@redhat.com> - 1.0.28-1
- Updated to 1.0.28
- Resolves: rhbz#1112204

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.0.27.2-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.27.2-2
- Mass rebuild 2013-12-27

* Mon Jul 08 2013 Jaroslav Kysela <perex@perex.cz> - 1.0.27.2-1
- Updated to 1.0.27.2

* Thu May 30 2013 Jaroslav Kysela <perex@perex.cz> - 1.0.27.1-2
- Fixed bug#953352

* Tue May 21 2013 Jaroslav Kysela <perex@perex.cz> - 1.0.27.1-1
- Updated to 1.0.27.1

* Tue May 07 2013 Rex Dieter <rdieter@fedoraproject.org> 1.0.27-3
- pull in upstream fix for building in C90 mode

* Thu Apr 11 2013 Jaroslav Kysela <perex@perex.cz> - 1.0.27-2
- move dist-oss.conf to doc as modprobe-dist-oss.conf

* Thu Apr 11 2013 Jaroslav Kysela <perex@perex.cz> - 1.0.27-1
- Updated to 1.0.27

* Wed Apr 03 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.0.26-4
- Add upstream patch to explicitly include sys/types.h

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.26-2
- Create and own ucm directory so alsaucm doesn't crash.
- Cleanup and modernise spec

* Thu Sep  6 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.26-1
- Updated to 1.0.26

* Thu Jul 26 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0.25-6
- Don't package ancient ChangeLog that ends at alsa-lib 0.2.0 (#510212).

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  2 2012 Josh Boyer <jwboyer@redhat.com> - 1.0.25-4
- Install ALSA related module conf files

* Wed Feb  1 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.25-3
- Remove the pulse audio configuration from /etc/asound.conf

* Sat Jan 28 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.25-1
- Updated to 1.0.25 final

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Jaroslav Kysela <jkysela@redhat.com> - 1.0.24-1
- Updated to 1.0.24 final

* Tue Nov  9 2010 Jochen Schmitt <Jochen herr-schmitt de> 1.0.23-2
- Set plugindir to %%{_libdir}/alsa-lib (bz#651507)

* Fri Apr 16 2010 Jaroslav Kysela <jkysela@redhat.com> - 1.0.23-1
- Updated to 1.0.23 final

* Mon Dec 28 2009 Jaroslav Kysela <jkysela@redhat.com> - 1.0.22-1
- Updated to 1.0.22 final
- Fix file descriptor leak in pcm_hw plugin
- Fix sound distortions for S24_LE - softvol plugin

* Wed Sep  9 2009 Jaroslav Kysela <jkysela@redhat.com> - 1.0.21-3
- Add Speaker and Beep control names to mixer weight list
- Fix redhat bug #521988

* Wed Sep  2 2009 Jaroslav Kysela <jkysela@redhat.com> - 1.0.21-1
- Updated to 1.0.21 final

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May  6 2009 Jaroslav Kysela <jkysela@redhat.com> - 1.0.20-1
- Updated to 1.0.20 final

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Jaroslav Kysela <jkysela@redhat.com> - 1.0.19-2
- Make doxygen documentation same for all architectures (bz#465205)

* Tue Jan 20 2009 Jaroslav Kysela <jkysela@redhat.com> - 1.0.19-1
- Updated to 1.0.19 final

* Tue Nov  4 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.18-7
- Updated to 1.0.18 final

* Wed Sep 10 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.18-6.rc3
- fix /etc directory issue

* Wed Sep 10 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.18-5.rc3
- move alsactl.conf to alsa-utils package

* Wed Sep 10 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.18-4.rc3
- fixed spec file
- fixed package version number (1.0.18-3.rc3 was tagged by accident)

* Wed Sep 10 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.18-1.rc3
- updated to 1.0.18rc3
- moved /etc/alsa configuration files back to /usr/share/alsa
- removed pulse default patch (moved to /etc/asound.conf)
- added /etc/asound.conf and /etc/alsa/alsactl.conf
- disable /dev/aload device checking (obsolete for 2.6 kernels)

* Fri Aug 15 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.17-3
- updated to 1.0.17a

* Mon Jul 21 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.17-2
- added four patches from upstream (to better support pulseaudio)

* Mon Jul 21 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.17-1
- updated to 1.0.17 final

* Thu Apr  3 2008 Jim Radford <radford@blackbean.org> - 1.0.16-3
- Fix multilib doxygen conflicts

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.16-2
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Martin Stransky <stransky@redhat.com> 1.0.16-1
- updated to 1.0.16 final

* Mon Oct 29 2007 Martin Stransky <stransky@redhat.com> 1.0.15-1
- updated to 1.0.15 final

* Wed Oct 17 2007 Lennart Poettering <lpoetter@redhat.com> 1.0.15-0.3.rc3
- Add hook to /etc/alsa/alsa.conf so that /etc/alsa/default-pulse.conf
  is loaded when it exists. This allows us to enable the pulse plugin by
  default depending on whether it is installed or not.

* Mon Oct 15 2007 Martin Stransky <stransky@redhat.com> 1.0.15-0.3.rc3
- updated to 1.0.15rc3

* Thu Sep 20 2007 Matthias Saou <http://freshrpms.net/> 1.0.15-0.2.rc2
- Update License field.
- Use configdir instead of sysconfdir hacks (cleaner).
- Remove redundant optflags overriding.
- Switch to using main "version", and merge "postver" since this is the right
  way of doing things (see NamingGuidelines#NonNumericRelease).
- Remove static library.
- Mark all of /etc/alsa as config, but not "noreplace".
- Remove useless rpath on 64bit archs.

* Wed Sep 19 2007 Martin Stransky <stransky@redhat.com> 1.0.15-0.1.rc2
- updated to 1.0.15rc2

* Thu Aug 16 2007 Martin Stransky <stransky@redhat.com> 1.0.14-3
- updated to 1.0.14a

* Wed Aug 15 2007 Lennart Poettering <lpoetter@redhat.com> 1.0.14-2
- fixed #251307 - fix plugindir directory specification
- fix build with newer glibc where open() is a macro

* Wed Jul 25 2007 Martin Stransky <stransky@redhat.com> 1.0.14-1
- bumped release number
- fixed #246011 - alsa-lib should own /usr/lib/alsa-lib/smixer

* Thu Jun 7  2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.5
- new upstream

* Tue Apr 10 2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.4.rc3
- added fix for #233764 - unowned directories

* Thu Mar 8  2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.3.rc3
- new upstream

* Fri Jan 19 2007 Martin Stransky <stransky@redhat.com> 1.0.14-0.2.rc2
- new upstream

* Mon Dec 11 2006 Martin Stransky <stransky@redhat.com> 1.0.14-0.1.rc1
- new upstream

* Fri Aug 25 2006 Martin Stransky <stransky@redhat.com> 1.0.12-2
- new upstream

* Mon Aug 07 2006 Martin Stransky <stransky@redhat.com> 1.0.12-1.rc2
- new upstream

* Thu Jul 20 2006 Martin Stransky <stransky@redhat.com> 1.0.12-1.rc1
- new upstream
- removed ainit (no longer needed in the new upstream)

* Wed Jul 19 2006 Jesse Keating <jkeating@redhat.com> - 1.0.11-6.rc2
- fix release for upgrade path

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.11-3.rc2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.11-3.rc2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.11-3.rc2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 3 2006 Martin Stransky <stransky@redhat.com> 1.0.11-3.rc2
- fix for #179446 - don't remove old SHM memory/keys during login

* Fri Jan 13 2006 Martin Stransky <stransky@redhat.com> 1.0.11-2.rc2
- fix for #169729 - Kernel update makes snd-atiixp-modem & slmodemd fail
- new ainit (0.7) should fix some problems with root users

* Thu Jan 12 2006 Martin Stransky <stransky@redhat.com> 1.0.11-1.rc2
- new upstream version

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.0.10rf-4
- rebuilt

* Fri Dec 9 2005 Martin Stransky <stransky@redhat.com> 1.0.10rf-3
- rights for shared memory have been moved to config files

* Fri Dec 2 2005 Martin Stransky <stransky@redhat.com> 1.0.10rf-2
- fix in spec file (#159046)

* Thu Nov 24 2005 Martin Stransky <stransky@redhat.com> 1.0.10rf-1
- new upstream version

* Tue Sep 27 2005 Martin Stransky <stransky@redhat.com> 1.0.10rc1-2
- fixes in config files, new ainit (for #166086)

* Tue Sep 27 2005 Martin Stransky <stransky@redhat.com> 1.0.10rc1-1
- new upstream version

* Wed Jul 20 2005 Martin Stransky <stransky@redhat.com> 1.0.9rf-3
- check for /var/run/console/console.lock (#162982)

* Thu Jun 16 2005 Martin Stransky <stransky@redhat.com> 1.0.9rf-2
- fix for #159411

* Mon May 30 2005 Martin Stransky <stransky@redhat.com> 1.0.9rf-1
- New upstream version
- moved alsacard utility to alsa-utils

* Fri May 27 2005 Martin Stransky <stransky@redhat.com> 1.0.9rc4-2
- alsacard utility for s-c-s

* Tue May 24 2005 Bill Nottingham <notting@redhat.com> 1.0.9rc4-1
- update to 1.0.9rc4 (#157180, #158547)

* Wed May 18 2005 Martin Stransky <stransky@redhat.com> 1.0.9rc2-5
- fix for #130593
- new ainit (dmix/dsnoop is default only for cards which really need it)
- fix dsnoop
- add fix for mixer (from https://bugs.gentoo.org/attachment.cgi?id=58918)

* Wed May 04 2005 Than Ngo <than@redhat.com> 1.0.9rc2-4
- apply patch to fix artsd daemon crash #156592

* Tue May 3  2005 Martin Stransky <stransky@redhat.com> 1.0.9rc2-3
- fixed ainit (#156278, #156505)

* Thu Apr 28 2005 David Woodhouse <dwmw2@redhat.com> 1.0.9rc2-2
- Fix bogus use of fgetc() in ainit. (#156278)

* Fri Apr 22 2005 Martin Stransky <stransky@redhat.com> 1.0.9rc2-1
- updated to 1.0.9rc2
- add ainit tool
- dmix is now default pcm device

* Mon Mar  7 2005 Martin Stransky <stransky@redhat.com> 1.0.8-4.devel
- gcc4 patch

* Tue Feb 15 2005 Martin Stransky <stransky@redhat.com> 1.0.8-3.devel
- add $RPM_OPT_FLAGS to CFLAGS

* Fri Feb 11 2005 Martin Stransky <stransky@redhat.com> 1.0.8-2.devel
- add alpha patch (#147388, thx to Sergey Tikhonov)
- fix alsa-mixer on ICH6 system (#146607)

* Wed Jan 26 2005 Martin Stransky <stransky@redhat.com> 1.0.8-1.devel
- update to 1.0.8
- temporarily removed alsa-lib-1.0.7-asym-config.patch

* Mon Jan 10 2005 Martin Stransky <stransky@redhat.com> 1.0.7-3.devel
- fix #144518 - stack protection control

* Sat Jan 08 2005 Colin Walters <walters@redhat.com> 1.0.7-2
- New patch alsa-lib-1.0.7-asym-config.patch, sets up asym
  in the default config file and makes it easy to make it
  the default via an environment variable.  Also increases the
  default dmix buffer variables.
- Mark /etc/alsa/alsa.conf as a config file, and use sysconfdir
  variable

* Thu Jan 06 2005 Colin Walters <walters@redhat.com> 1.0.7-1
- New upstream version

* Tue Nov 30 2004 Bill Nottingham <notting@redhat.com> 1.0.6-6
- fix bad assertion that trips up gstreamer (fixes GNOME bug #159647)
- undef gets in case it's a macro (#141423)

* Thu Oct 14 2004 Bill Nottingham <notting@redhat.com> 1.0.6-3
- move libraries & data to root fs, needed at boot time

* Mon Aug 30 2004 Bill Nottingham <notting@redhat.com> 1.0.6-1
- update to 1.0.6

* Fri Jul  2 2004 Bill Nottingham <notting@redhat.com> 1.0.5-1
- update to 1.0.5

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 17 2004 Colin Walters <walters@redhat.com> 1.0.4-1
- New upstream version

* Mon May 03 2004 Colin Walters <walters@redhat.com> 1.0.3a-2
- Add patch to avoid assert()ing on errors

* Thu Mar 11 2004 Bill Nottingham <notting@redhat.com> 1.0.3a-1
- update to 1.0.3a

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 28 2004 Bill Nottingham <notting@redhat.com> 1.0.2-1
- update to 1.0.2

* Thu Dec 11 2003 Bill Nottingham <notting@redhat.com> 1.0.0rc2-1
- update to 1.0.0rc2

* Mon Dec  1 2003 Bill Nottingham <notting@redhat.com> 0.9.8-3
- fix various specfile issues, including License: tag (#111153)

* Wed Nov 26 2003 Than Ngo <than@redhat.com> 0.9.8-2
- fixed dependant libraries check on x86_64

* Tue Nov  4 2003 Bill Nottingham <notting@redhat.com> - 0.9.8-1
- initial build, modify spec file from Matthias Saou
