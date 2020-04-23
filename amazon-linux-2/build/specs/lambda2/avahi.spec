%global _hardened_build 1
%global __python %{__python2}

Name:             avahi
Version:          0.6.31
Release: 19%{?dist}.0.1
Summary:          Local network service discovery
License:          LGPLv2+
URL:              http://avahi.org
Requires:         dbus
Requires:         expat
Requires:         libdaemon >= 0.11
Requires:         %{name}-libs = %{version}-%{release}
BuildRequires:    automake
BuildRequires:    autoconf
BuildRequires:    libtool
BuildRequires:    dbus-devel >= 0.90
BuildRequires:    dbus-glib-devel >= 0.70
BuildRequires:    dbus-python
BuildRequires:    libxml2-python
BuildRequires:    gtk2-devel
BuildRequires:    gtk3-devel >= 2.99.0
#BuildRequires:    gobject-introspection-devel
BuildRequires:    qt3-devel
BuildRequires:    qt4-devel
BuildRequires:    libglade2-devel
BuildRequires:    libdaemon-devel >= 0.11
BuildRequires:    glib2-devel
BuildRequires:    libcap-devel
BuildRequires:    expat-devel
BuildRequires:    python
BuildRequires:    gdbm-devel
BuildRequires:    pygtk2
BuildRequires:    intltool
BuildRequires:    perl-XML-Parser
BuildRequires:    systemd

Source0:          http://avahi.org/download/%{name}-%{version}.tar.gz
Patch0000:        avahi-0.6.30-mono-libdir.patch
Patch0001:        0001-man-correct-short-option-to-print-version-string.patch
Patch0002:        0002-man-add-description-for-t-option.patch
Patch0003:        0003-dbus-don-t-crash-if-we-can-t-determine-alternative-s.patch
Patch0004:        0004-avahi-core-reserve-space-for-record-data-when-size-e.patch
Patch0005:        0005-Remove-prefix-home-lennart-tmp-avahi-from-references.patch
Patch0006:        0006-Silently-ignore-invalid-DNS-packets.patch
Patch0007:        0007-avahi-daemon-don-t-add-0pointer.de-and-zeroconf.org-.patch
Patch0008:        0008-avahi_server_set_browse_domains-check-the-provided-d.patch
Patch0009:        0009-Fix-not-publishing-entries-if-a-probing-interface-is.patch
Patch0010:        0010-avahi-ui-Replace-usage-of-deprecated-GTK-Stock-Items.patch
Patch0011:        0011-avahi-ui-replace-gtk_vbox_new-with-gtk_box_new-for-G.patch
Patch0012:        0012-avahi-ui-Cannot-use-g_object_unref-to-free-GdkCursor.patch
Patch0013:        0013-avahi-ui-Remove-deprecated-usage-of-gtk_widget_push_.patch

# due to FTBFS caused by Gtk changes introduced in RHEL-7.2
Patch1000:        avahi-0.6.31-no-deprecations.patch

Prefix: %{_prefix}

%description
Avahi is a system which facilitates service discovery on
a local network -- this means that you can plug your laptop or
computer into a network and instantly be able to view other people who
you can chat with, find printers to print to or find files being
shared. This kind of technology is already found in MacOS X (branded
'Rendezvous', 'Bonjour' and sometimes 'ZeroConf') and is very
convenient.

%package tools
Summary:          Command line tools for mDNS browsing and publishing
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Prefix: %{_prefix}

%description tools
Command line tools that use avahi to browse and publish mDNS services.

%package glib
Summary:          Glib libraries for avahi
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Prefix: %{_prefix}

%description glib
Libraries for easy use of avahi from glib applications.

%package gobject
Summary:          GObject wrapper library for Avahi
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-glib = %{version}-%{release}
Prefix: %{_prefix}

%description gobject
This library contains a GObject wrapper for the Avahi API

%package libs
Summary:          Libraries for avahi run-time use
Prefix: %{_prefix}

%description libs
The avahi-libs package contains the libraries needed
to run programs that use avahi.

%package compat-howl
Summary:          Libraries for howl compatibility
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Obsoletes:        howl-libs
Provides:         howl-libs
Prefix: %{_prefix}

%description compat-howl
Libraries that are compatible with those provided by the howl package.

%package compat-libdns_sd
Summary:          Libraries for Apple Bonjour mDNSResponder compatibility
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Prefix: %{_prefix}

%description compat-libdns_sd
Libraries for Apple Bonjour mDNSResponder compatibility.

%package autoipd
Summary:          Link-local IPv4 address automatic configuration daemon (IPv4LL)
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Prefix: %{_prefix}

%description autoipd
avahi-autoipd implements IPv4LL, "Dynamic Configuration of IPv4
Link-Local Addresses"  (IETF RFC3927), a protocol for automatic IP address
configuration from the link-local 169.254.0.0/16 range without the need for a
central server. It is primarily intended to be used in ad-hoc networks which
lack a DHCP server.

%package dnsconfd
Summary:          Configure local unicast DNS settings based on information published in mDNS
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Prefix: %{_prefix}

%description dnsconfd
avahi-dnsconfd connects to a running avahi-daemon and runs the script
/etc/avahi/dnsconfd.action for each unicast DNS server that is announced on the
local LAN. This is useful for configuring unicast DNS servers in a DHCP-like
fashion with mDNS.

%prep
%autosetup -S git

%build
autoreconf -fi
%configure \
        --with-distro=fedora \
        --disable-monodoc \
        --with-avahi-user=avahi \
        --with-avahi-group=avahi \
        --with-avahi-priv-access-group=avahi \
        --with-autoipd-user=avahi-autoipd \
        --with-autoipd-group=avahi-autoipd \
        --enable-introspection=no \
        --enable-compat-libdns_sd \
        --enable-compat-howl \
        --disable-mono \
        --disable-python \
;
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} \( -name '*.a' -o -name '*.la' \) -exec rm {} \;

# remove example
rm -f %{buildroot}%{_sysconfdir}/avahi/services/ssh.service
rm -f %{buildroot}%{_sysconfdir}/avahi/services/sftp-ssh.service

# remove avahi-discover-standalone
rm -f $RPM_BUILD_ROOT%{_bindir}/avahi-discover-standalone

# create /var/run/avahi-daemon to ensure correct selinux policy for it:
mkdir -p %{buildroot}%{_localstatedir}/run/avahi-daemon
mkdir -p %{buildroot}%{_localstatedir}/lib/avahi-autoipd

# remove the documentation directory - let % doc handle it:
rm -rf %{buildroot}%{_datadir}/%{name}-%{version}

# Make /etc/avahi/etc/localtime owned by avahi:
mkdir -p %{buildroot}%{_sysconfdir}/avahi/etc
touch %{buildroot}%{_sysconfdir}/avahi/etc/localtime

rm -f %{buildroot}%{_sysconfdir}/rc.d/init.d/avahi-daemon
rm -f %{buildroot}%{_sysconfdir}/rc.d/init.d/avahi-dnsconfd

%files
%dir %{_sysconfdir}/avahi
%dir %{_sysconfdir}/avahi/etc
%ghost %{_sysconfdir}/avahi/etc/localtime
%config(noreplace) %{_sysconfdir}/avahi/hosts
%dir %{_sysconfdir}/avahi/services
%ghost %dir %{_localstatedir}/run/avahi-daemon
%config(noreplace) %{_sysconfdir}/avahi/avahi-daemon.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/avahi-dbus.conf
%{_sbindir}/avahi-daemon
%dir %{_datadir}/avahi
%{_datadir}/avahi/*.dtd
%{_datadir}/avahi/service-types
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Avahi.service
%{_libdir}/libavahi-core.so.*

%files autoipd
%{_sbindir}/avahi-autoipd
%config(noreplace) %{_sysconfdir}/avahi/avahi-autoipd.action
%attr(1770,avahi-autoipd,avahi-autoipd) %dir %{_localstatedir}/lib/avahi-autoipd/

%files dnsconfd
%config(noreplace) %{_sysconfdir}/avahi/avahi-dnsconfd.action
%{_sbindir}/avahi-dnsconfd

%files tools
%{_bindir}/*
%exclude %{_bindir}/b*

%files libs
%{_libdir}/libavahi-common.so.*
%{_libdir}/libavahi-client.so.*

%files glib
%{_libdir}/libavahi-glib.so.*

%files gobject
%{_libdir}/libavahi-gobject.so.*

%files compat-howl
%{_libdir}/libhowl.so.*

%files compat-libdns_sd
%{_libdir}/libdns_sd.so.*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/libavahi-qt3.so.*
%exclude %{_libdir}/libavahi-qt4.so.*
%exclude %{_libdir}/libavahi-ui-gtk3.so.*
%exclude %{_libdir}/libavahi-ui.so.*
%exclude %{_datadir}/locale
%exclude %{_datadir}/applications/*.desktop
%exclude %{_datadir}/avahi/interfaces/*.ui
%exclude %{_unitdir}

%changelog
* Thu Apr 23 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Nov 09 2017 Michal Sekletar <msekleta@redhat.com> - 0.6.31-19
- exclude avahi-discover from avahi-tools package (#1421229)

* Tue Nov 07 2017 Michal Sekletar <msekleta@redhat.com> - 0.6.31-18
- create home directory for avahi-autoipd user (#1416287)
- get rid of the dangling symlink to avahi-discover in debuginfo package (#1421229)

* Mon Jul 04 2016 Michal Sekletar <msekleta@redhat.com> - 0.6.31-17
- fix crash due to use of deprecated Gtk3 API (#1263720)
- don't add 0pointer.de and zeroconf.org to default browse list (#1340837)
- fix not publishing entries if a probing interface is removed (#1222646)

* Thu Dec 17 2015 Michal Sekletar <msekleta@redhat.com> - 0.6.31-16
- silently ignore non-valid DNS response packets (#1290890)

* Tue Apr 21 2015 Michal Sekletar <msekleta@redhat.com> - 0.6.31-15
- enable hardened build (#1092506)
- fix short option for --version, document -t option of avahi-autoipd (#948583)
- fix crashes in D-Bus methods GetAlternativeHostName and GetAlternativeServiceName (#1003688)
- fix bug when avahi-daemon ended up in a tight loop (#1081801)
- remove prefix /home/lennart/tmp/avahi from references in man pages (#1120233)

* Mon Dec  8 2014 Michal Sekletar <msekleta@redhat.com> - 0.6.31-14
- remove dependency on the main package from avahi-libs (#1170681)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.6.31-13
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.6.31-12
- Mass rebuild 2013-12-27

* Sat Feb 02 2013 Kalev Lember <kalevlember@gmail.com> - 0.6.31-11
- Correct a typo in inter-subpackage deps

* Fri Feb  1 2013 Matthias Clasen <mclasen@redhat.com> - 0.6.31-10
- Tighten inter-subpackage deps

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 0.6.31-9
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.6.31-8
- fix path to ldconfig

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.6.31-7
- rebuild against new libjpeg

* Tue Aug  7 2012 Lennart Poettering <lpoetter@redhat.com> - 0.6.31-6
- Use new systemd macros
- Other modernizations

* Mon Aug 6 2012 Stef Walter <stefw@redhat.com> - 0.6.31-5
- Don't ship ssh service by default file since openssh-server isn't
  running by default, and shouldn't be advertised without user
  confirmation.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.31-3
- Merge F-17 into master
- ARM has mono

* Tue Feb 14 2012 Lennart Poettering <lpoetter@redhat.com> - 0.6.31-2
- Fix tarball

* Tue Feb 14 2012 Lennart Poettering <lpoetter@redhat.com> - 0.6.31-1
- New upstream release

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Christian Krause <chkr@fedoraproject.org> - 0.6.30-6
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> 0.6.30-5
- Rebuild to break bogus libpng dep

* Mon Aug 22 2011 Lennart Poettering <lpoetter@redhat.com> - 0.6.30-4
- Remove sysv init script (#714649)

* Thu May  5 2011 Bill Nottingham <notting@redhat.com> - 0.6.30-3
- fix versioning on triggers

* Tue May  3 2011 Lennart Poettering <lpoetter@redhat.com> - 0.6.30-2
- Enable Avahi by default
- https://bugzilla.redhat.com/show_bug.cgi?id=647831

* Mon Apr  4 2011 Lennart Poettering <lpoetter@redhat.com> - 0.6.30-1
- New upstream release

* Wed Mar  9 2011 Lennart Poettering <lpoetter@redhat.com> - 0.6.29-1
- New upstream release
- Fixes CVE-2011-1002 among other things

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.28-9
- Rebuild against new gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 2 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.28-7
- Rebuild against new gtk

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.28-6
- Rebuild against new gtk

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.28-5
- Rebuild against new gtk

* Wed Nov 24 2010 Dan Horák <dan[at]danny.cz> - 0.6.28-4
- Updated the archs without mono

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.28-3
- Rebuild against newer gtk3

* Wed Oct 27 2010 paul <paul@all-the-johnsons.co.uk> - 0.6.28-2
- rebuilt

* Tue Oct  5 2010 Lennart Poettering <lpoetter@redhat.com> - 0.6.28-1
- New upstream release

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 0.6.27-3
- convert from systemd-install to systemctl enable

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.27-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> 0.6.27-1
- New upstream release

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> 0.6.26-4
- On request of Colin Walters, disable introspection again for now.

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> 0.6.26-3
- Fix systemd unit installation

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> 0.6.26-2
- Add missing dependencies

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> 0.6.26-1
- New upstream release

* Mon Apr 19 2010 Bastien Nocera <bnocera@redhat.com> 0.6.25-7
- Split avahi libraries in -libs

* Mon Jan 25 2010 Lennart Poettering <lpoetter@redhat.com> - 0.6.25-6
- Move avahi-discover from avahi-tools to avahi-ui-tools
- https://bugzilla.redhat.com/show_bug.cgi?id=513768

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Karsten Hopp <karsten@redhat.com> 0.6.25-4
- Build *-sharp & *-ui-sharp for s390x

* Thu Jun 11 2009 Matthias Clasen <mclasen@redhat.com> - 0.6.25-4
- Use %%find_lang

* Tue May 26 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.25-3
- Create avahi-ui-sharp-devel package for pkgconfig dep-chain (#477308).

* Mon May 25 2009 Xavier Lamien <laxathom@fedoraproject.org> - 0.6.25-2
- Build arch ppc64 for *-sharp & *-ui-sharp.

* Mon Apr 13 2009 Lennart Poettering <lpoetter@redhat.com> - 0.6.25-1
- New upstream release

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Lennart Poettering <lpoetter@redhat.com> - 0.6.24-1
- New upstream release

* Wed Dec  3 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.22-13
- Fix libtool errors

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.22-12
- Rebuild for Python 2.6

* Wed Jun 04 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.6.22-11
- qt4 bindings (#446904)
- devel: BR: pkgconfig
- nuke rpaths

* Thu Mar 27 2008 Lennart Poettering <lpoetter@redhat.com> - 0.6.22-10
- Add release part to package dependencies (Closed #311601)

* Mon Mar 10 2008 Christopher Aillon <caillon@redhat.com> - 0.6.22-9
- The qt3 subpackage should (Build)Require: qt3

* Mon Mar 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.6.22-8
- updated (completed) German translation by Fabian Affolter (#427090)

* Thu Feb 21 2008 Adam Tkac <atkac redhat com> - 0.6.22-7
- really rebuild against new libcap

* Sun Feb 17 2008 Adam Tkac <atkac redhat com> - 0.6.22-6
- rebuild against new libcap

* Sat Feb 09 2008 Dennis Gilmore <dennis@ausil.us> - 0.6.22-5
- sparc64 does not have mono

* Tue Dec 18 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.6.22-4
- Make bvnc call vncviewer instead of xvncviewer
- Let ui-tools depend on necessary packages

* Mon Dec 17 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.22-3
- Add missing intltool dependency

* Mon Dec 17 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.22-2
- Fix mistag

* Mon Dec 17 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.22-1
- resolves #274731, #425491: New upstream version

* Tue Sep 25 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.21-6
- resolves #279301: fix segfault when no domains are configured in resolv.conf (pulled from upstream SVN r1525)

* Thu Sep 6 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.21-5
- resolves #249044: Update init script to use runlevel 96
- resolves #251700: Fix assertion in libdns_sd-compat

* Thu Sep 6 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.21-4
- Ship ssh static service file by default, don't ship ssh-sftp by default
- resolves: #269741: split off avahi-ui-tools package
- resolves: #253734: add missing dependency on avahi-glib-devel to avahi-ui-devel

* Tue Aug 28 2007 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.21-3
- resolves: #246875: Initscript Review

* Sun Aug 12 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.21-2
- Fix avahi-browse --help output

* Sun Aug 12 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.21-1
- New upstream release

* Thu Aug 9 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.20-7
- Fix tagging borkage

* Thu Aug 9 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.20-6
- fix avahi-autoipd corrupt packet bug
- drop dependency on python for the main package

* Wed Jul 11 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.20-5
- add two patches which are important to get RR updating work properly.
  Will be part of upstream 0.6.21

* Thu Jul  5 2007 Dan Williams <dcbw@redhat.com> - 0.6.20-4
- Add Requires(pre): shadow-utils for avahi-autoipd package

* Mon Jun 25 2007 Bill Nottingham <notting@redhat.com> - 0.6.20-3
- fix %%endif typo

* Mon Jun 25 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.20-2
- add gtk-sharp2-devel to build deps

* Fri Jun 22 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.20-1
- upgrade to new upstream 0.6.20
- fix a few rpmlint warnings
- create avahi-autoipd user
- no longer create avahi user with a static uid, move to dynamic uids
- drop a couple of patches merged upstream
- Provide "howl" and "howl-devel"
- Split off avahi-autoipd and avahi-dnsconfd
- Introduce avahi-ui packages for the first time
- Reload D-Bus config after installation using dbus-send
- add a couple of missing ldconfig invocations

* Mon Mar 12 2007 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.17-1
- upgrade to new upstream 0.6.17
- redundant patches removal
- removed auto* stuff from specfile since that was no longer needed
- Resolves: #232205: 'service {avahi-dnsconfd,avahi-daemon} status'
  returns 0 when the service is stopped

* Fri Feb  2 2007 Christopher Aillon <cailloN@redhat.com> - 0.6.16-3
- Remove bogus mono-libdir patches

* Tue Jan 23 2007 Jeremy Katz <katzj@redhat.com> - 0.6.16-2
- nuke bogus avahi-sharp -> avahi-devel dep

* Mon Jan 22 2007 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.16-1.fc7
- Resolves: #221763: CVE-2006-6870 Maliciously crafted packed can DoS avahi daemon
- upgrade to new upstream
- patch revision
- Resolves: #218140: avahi configuration file wants a non-existent group

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 0.6.15-4
- rebuild against python 2.5

* Mon Nov 27 2006 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.15-3
- automake-1.10 required for building

* Mon Nov 27 2006 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.15-2
- automake-1.9 required for building

* Fri Nov 24 2006 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.15-1
- Upgrade to 0.6.15
- patches revision

* Mon Sep 18 2006 Martin Stransky <stransky@redhat.com> - 0.6.11-6
- added patch from #206445 - ia64: unaligned access errors seen
  during startup of avahi-daemon
- removed unused patches

* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> - 0.6.11-5
- Maintain the security context on the localtime file

* Wed Aug 23 2006 Martin Stransky <stransky@redhat.com> - 0.6.11-4
- fix for #204710 - /etc/init.d/avahi-dnsconfd missing line
  continuation slash (\) in description

* Wed Aug 23 2006 Martin Stransky <stransky@redhat.com> - 0.6.11-3
- added fix for #200767 - avahi-dnsconfd Segmentation fault
  with invalid command line argument
- added dist tag

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.6.11-2.fc6
- add BR for dbus-glib-devel
- fix deprecated functions

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.11-1.fc6
- Upgrade to upstream version 0.6.11
- fix bug 195674: set 'use-ipv6=yes' in avahi-daemon.conf
- fix bug 197414: avahi-compat-howl and avahi-compat-dns-sd symlinks
- fix bug 198282: avahi-compat-{howl-devel,dns-sd-devel} Requires:

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Tue Jun 13 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.10-3.FC6
- rebuild for broken mono deps

* Tue Jun 06 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.10-2.FC6
- fix bug 194203: fix permissions on /var/run/avahi-daemon

* Tue May 30 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.10-1.FC6
- Upgrade to upstream version 0.6.10
- fix bug 192080: split avahi-compat-libdns_sd into separate package
                  (same goes for avahi-compat-howl)

* Tue May 02 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-9.FC6
- fix avahi-sharp issues for banshee - patches from caillon@redhat.com

* Thu Apr 20 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-9.FC6
- fix bug 189427: correct avahi-resolve --help typo

* Mon Mar 20 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-8.FC6
- fix bug 185972: remove ellipses in initscript
- fix bug 185965: make chkconfigs unconditional

* Thu Mar 16 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-6
- Fix bug 185692: install avahi-sharp into %{_prefix}/lib, not %{_libdir}

* Thu Mar 09 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-4
- fix scriptlet error introduced by last fix:
  if user has disabled avahi-daemon, do not enable it during post

* Wed Mar 08 2006 Bill Nottingham <notting@redhat.com> - 0.6.9-2
- fix scriplet error during installer
- move service-types* to the tools package (avoids multilib conflicts)

* Tue Mar 07 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-1
- Upgrade to upstream version 0.6.9

* Thu Feb 23 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.8-1
- Upgrade to upstream version 0.6.8
- fix bug 182462: +Requires(post): initscripts, chkconfig, ldconfig

* Fri Feb 17 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.7-1
- Upgrade to upstream version 0.6.7

* Fri Feb 17 2006 Karsten Hopp <karsten@redhat.de> - 0.6.6-4
- BuildRequires pygtk2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.6-3.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.6-3
- rebuild for new gcc (again)
- further fix for bug 178746: fix avahi-dnsconfd initscript

* Tue Feb 07 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.6-2
- rebuild for new gcc, glibc, glibc-kernheaders

* Wed Feb 01 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.6-1
- fix bug 179448: mis-alignment of input cmsghdr msg->msg_control buffer on ia64
- Upgrade to 0.6.6

* Thu Jan 26 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.5-1
- Upgrade to upstream version 0.6.5
- Make /etc/avahi/etc and /etc/avahi/etc/localtime owned by avahi
  package; copy system localtime into chroot in post

* Mon Jan 23 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.4-4
- fix bug 178689: copy localtime to chroot
- fix bug 178784: fix avahi-dnsconfd initscript

* Fri Jan 20 2006 Peter Jones <pjones@redhat.com> - 0.6.4-3
- fix subsystem locking in the initscript

* Thu Jan 19 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.4-2
- fix bug 178127: fully localize the initscript

* Mon Jan 16 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.4-1
- Upgrade to upstream version 0.6.4

* Thu Jan 12 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.3-2
- fix bug 177610: Enable mono support with new avahi-sharp package
- fix bug 177609: add gdbm / gdbm-devel Requires for avahi-browse

* Mon Jan 09 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.3-1
- Upgrade to upstream version 0.6.3
- fix bug 177148: initscript start should not fail if avahi-daemon running

* Thu Dec 22 2005 Jason Vas Dias <jvdias@redhat.com> - 0.6.1-3
- move initscripts from /etc/init.d to /etc/rc.d/init.d

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec 09 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6.1-2
- fix bug 175352: Do not chkconfig --add avahi-daemon
  if user has already configured it

* Wed Dec 07 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6.1-1
- Upgrade to 0.6.1

* Mon Dec 05 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6-6
- fix bug 174799 - fix .spec file files permissions

* Fri Dec 02 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6-5
- python-twisted has been removed from the FC-5 distribution - disable its use

* Thu Dec 01 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6-4
- Rebuild for dbus-0.6 - remove use of DBUS_NAME_FLAG_PROHIBIT_REPLACEMENT

* Wed Nov 30 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6-3
- fix bug 172047 - tools should require python-twisted
- fix bug 173985 - docs directory permissions

* Mon Nov 21 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6-1
- Upgrade to upstream version 0.6 - now provides 'avahi-howl-compat'
  libraries / includes.

* Mon Nov 14 2005 Jason Vas Dias<jvdias@redhat.com> - 0.5.2-7
- fix bug 172034: fix ownership of /var/run/avahi-daemon/
- fix bug 172772: .spec file improvements from matthias@rpmforge.net

* Mon Oct 31 2005 Jason Vas Dias<jvdias@redhat.com> - 0.5.2-6
- put back avahi-devel Obsoletes: howl-devel

* Mon Oct 31 2005 Alexander Larsson <alexl@redhat.com> - 0.5.2-5
- Obsoletes howl, howl-libs, as we want to get rid of them on updates
- No provides yet, as the howl compat library is in Avahi 0.6.0.

* Sun Oct 30 2005 Florian La Roche <laroche@redhat.com>
- disable the Obsoletes: howl until the transition is complete

* Fri Oct 28 2005 Jason Vas Dias<jvdias@redhat.com> - 0.5.2-3
- change initscript to start avahi-daemon AFTER messagebus

* Wed Oct 26 2005 Karsten Hopp <karsten@redhat.de> 0.5.2-2
- add buildrequires dbus-python

* Fri Oct 21 2005 Alexander Larsson <alexl@redhat.com> - 0.5.2-1
- Initial package
