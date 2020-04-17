%define         gstreamer       gstreamer
%define         majorminor      0.10
%define         gstreamer_version %{majorminor}.36

Name:           %{gstreamer}-plugins-base
Version:        %{gstreamer_version}
Release:        18%{?dist}
Summary:        GStreamer streaming media framework base plug-ins

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
#Source:         http://gstreamer.freedesktop.org/src/gst-plugins-base/pre/gst-plugins-base-%{version}.tar.bz2
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-%{version}.tar.xz
# https://bugzilla.gnome.org/show_bug.cgi?id=652342 - fixes RB CD rip

Requires:       %{gstreamer} >= %{gstreamer_version}
Requires:       iso-codes
BuildRequires:  %{gstreamer}-devel >= %{gstreamer_version}
BuildRequires:  iso-codes-devel
BuildRequires:  gobject-introspection-devel >= 0.6.3

BuildRequires:  gettext
BuildRequires:  gcc-c++

BuildRequires:  alsa-lib-devel
BuildRequires:  cdparanoia-devel
BuildRequires:  gtk2-devel
BuildRequires:  libgudev1-devel
BuildRequires:  libogg-devel >= 1.0
BuildRequires:  liboil-devel >= 0.3.6
BuildRequires:  libtheora-devel >= 1.0
BuildRequires:  libvisual-devel
BuildRequires:  libvorbis-devel >= 1.0
BuildRequires:  libXv-devel
BuildRequires:  orc-devel >= 0.4.11
BuildRequires:  pango-devel
BuildRequires:  pkgconfig
Obsoletes:      gstreamer-plugins

BuildRequires:  chrpath

# documentation
BuildRequires:  gtk-doc >= 1.3

Patch0: 0001-missing-plugins-Remove-the-mpegaudioversion-field.patch
Patch1: 0001-audioresample-Fix-build-on-x86-if-emmintrin.h-is-ava.patch
Patch2: 0002-audioresample-It-s-HAVE_EMMINTRIN_H-not-HAVE_XMMINTR.patch
Patch3: 0001-typefind-bounds-check-windows-ico-detection.patch
Patch4: fix-gst-init.patch
Patch5: fix-docs.patch

Prefix: %{_prefix}

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This package contains a set of well-maintained base plug-ins.

%prep
%setup -q -n gst-plugins-base-%{version}
%patch0 -p1 -b .mpegaudioversion
%patch1 -p1 -b .0001
%patch2 -p1 -b .0002
%patch3 -p1 -b .0003
%patch4 -p1 -b .0004
%patch5 -p1 -b .0005

%build
%configure \
  --with-package-name='Fedora gstreamer-plugins-base package' \
  --with-package-origin='http://download.fedora.redhat.com/fedora' \
  --enable-experimental \
  --disable-gtk-doc \
  --enable-orc \
  --disable-gnome_vfs \
  --disable-static

make %{?_smp_mflags} ERROR_CFLAGS=""

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove rpath.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstadder.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstalsa.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstapp.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudioconvert.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstcdparanoia.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstdecodebin.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstdecodebin2.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstencodebin.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstffmpegcolorspace.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstogg.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstpango.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstplaybin.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgsttheora.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgsttypefindfunctions.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideoscale.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvolume.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvorbis.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstaudio-0.10.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstcdda-0.10.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstriff-0.10.so.*

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_bindir}/gst-visualise*
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/gst-visualise*

%files
%defattr(-, root, root)
%license COPYING

# libraries
%{_libdir}/libgstinterfaces-%{majorminor}.so.*
%{_libdir}/libgstaudio-%{majorminor}.so.*
%{_libdir}/libgstcdda-%{majorminor}.so.*
%{_libdir}/libgstfft-%{majorminor}.so.*
%{_libdir}/libgstriff-%{majorminor}.so.*
%{_libdir}/libgsttag-%{majorminor}.so.*
%{_libdir}/libgstnetbuffer-%{majorminor}.so.*
%{_libdir}/libgstrtp-%{majorminor}.so.*
%{_libdir}/libgstvideo-%{majorminor}.so.*
%{_libdir}/libgstpbutils-%{majorminor}.so.*
%{_libdir}/libgstrtsp-%{majorminor}.so.*
%{_libdir}/libgstsdp-%{majorminor}.so.*
%{_libdir}/libgstapp-%{majorminor}.so.*

# gobject-introspection files
%{_libdir}/girepository-1.0/GstApp-0.10.typelib
%{_libdir}/girepository-1.0/GstAudio-0.10.typelib
%{_libdir}/girepository-1.0/GstFft-0.10.typelib
%{_libdir}/girepository-1.0/GstInterfaces-0.10.typelib
%{_libdir}/girepository-1.0/GstNetbuffer-0.10.typelib
%{_libdir}/girepository-1.0/GstPbutils-0.10.typelib
%{_libdir}/girepository-1.0/GstRiff-0.10.typelib
%{_libdir}/girepository-1.0/GstRtp-0.10.typelib
%{_libdir}/girepository-1.0/GstRtsp-0.10.typelib
%{_libdir}/girepository-1.0/GstSdp-0.10.typelib
%{_libdir}/girepository-1.0/GstTag-0.10.typelib
%{_libdir}/girepository-1.0/GstVideo-0.10.typelib

# base plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstadder.so
%{_libdir}/gstreamer-%{majorminor}/libgstapp.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiorate.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioresample.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiotestsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstdecodebin.so
%{_libdir}/gstreamer-%{majorminor}/libgstdecodebin2.so
%{_libdir}/gstreamer-%{majorminor}/libgstencodebin.so
%{_libdir}/gstreamer-%{majorminor}/libgstffmpegcolorspace.so
%{_libdir}/gstreamer-%{majorminor}/libgstgdp.so
%{_libdir}/gstreamer-%{majorminor}/libgstgio.so
%{_libdir}/gstreamer-%{majorminor}/libgstplaybin.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubparse.so
%{_libdir}/gstreamer-%{majorminor}/libgsttcp.so
%{_libdir}/gstreamer-%{majorminor}/libgsttypefindfunctions.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideorate.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoscale.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideotestsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstvolume.so

# base plugins with dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstalsa.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdparanoia.so
%{_libdir}/gstreamer-%{majorminor}/libgstlibvisual.so
%{_libdir}/gstreamer-%{majorminor}/libgstogg.so
%{_libdir}/gstreamer-%{majorminor}/libgstpango.so
%{_libdir}/gstreamer-%{majorminor}/libgsttheora.so
%{_libdir}/gstreamer-%{majorminor}/libgstvorbis.so
%{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
%{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so

%package -n gstreamer-plugins-base-tools
Summary:        tools for GStreamer streaming media framework base plugins
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}
Prefix: %{_prefix}

%description -n gstreamer-plugins-base-tools
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This package contains the command-line tools for the base plugins.
These include:

* gst-discoverer

%files -n gstreamer-plugins-base-tools
%defattr(-, root, root, -)
%{_bindir}/gst-discoverer-%{majorminor}

%exclude %{_includedir}
%exclude %{_datadir}
%exclude %{_libdir}/pkgconfig/*.pc
%exclude %{_libdir}/libgstaudio-%{majorminor}.so
%exclude %{_libdir}/libgstinterfaces-%{majorminor}.so
%exclude %{_libdir}/libgstnetbuffer-%{majorminor}.so
%exclude %{_libdir}/libgstriff-%{majorminor}.so
%exclude %{_libdir}/libgstrtp-%{majorminor}.so
%exclude %{_libdir}/libgsttag-%{majorminor}.so
%exclude %{_libdir}/libgstvideo-%{majorminor}.so
%exclude %{_libdir}/libgstcdda-%{majorminor}.so
%exclude %{_libdir}/libgstpbutils-%{majorminor}.so
%exclude %{_libdir}/libgstrtsp-%{majorminor}.so
%exclude %{_libdir}/libgstsdp-%{majorminor}.so
%exclude %{_libdir}/libgstfft-%{majorminor}.so
%exclude %{_libdir}/libgstapp-%{majorminor}.so

%changelog
* Thu Apr 16 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.36-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.36-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.36-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 06 2016 Wim Taymans <wtaymans@redhat.com> - 0.10.36-15
- typefind: bounds check windows ico detection
  (rhbz#1401949)
- fix build of docs and gir files

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.36-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.36-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Wim Taymans <wtaymans@redhat.com> - 0.10.36-12
- Remove rpath. Fixes #1154695

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.36-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.10.36-10
- Rebuilt for gobject-introspection 1.41.4

* Tue Jun 10 2014 Wim Taymans <wtaymans@redhat.com> - 0.10.36-9
- Improve conditional SSE and SSE2 compilation. Fixes #1106735 

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.36-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.10.36-7
- Call ldconfig in %%post* scriptlets.
- Fix bogus dates in %%changelog.

* Mon Oct 14 2013 Dan Horák <dan[at]danny.cz> - 0.10.36-6
- drop BR: PyXML (https://fedoraproject.org/wiki/Features/RemovePyXML), fixes #992440

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 07 2012 Bastien Nocera <bnocera@redhat.com> 0.10.36-3
- Add patch for MP3 codec installation problems (#680809)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Benjamin Otte <otte@redhat.com> 0.10.36-1
- Update to 0.10.36

* Fri Feb 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.35-5
- libgudev-devel -> libgudev1-devel. Would have been nice if this was announced

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 29 2011 Adam Williamson <awilliam@redhat.com> - 0.10.35-3
- backport a fix for GNOME #652342, fixing Rhythmbox CD rip to FLAC

* Thu Jul 21 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 0.10.35-2
- Remove gtk-doc dependency from -devel-docs package and 
  own the two gtk-doc directories instead (#604365).

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.10.35-1
- Update to 0.10.35

* Tue May 10 2011 Benjamin Otte <otte@redhat.com> 0.10.33-1
- Update to 0.10.33

* Sun May 01 2011 Benjamin Otte <otte@redhat.com> 0.10.32.4-1
- Update prerelease

* Wed Apr 27 2011 Benjamin Otte <otte@redhat.com> 0.10.32.3-1
- Update prerelease

* Mon Apr 18 2011 Benjamin Otte <otte@redhat.com> 0.10.32.2-1
- Update to prerelease

* Tue Jan 25 2011 Benjamin Otte <otte@redhat.com> 0.10.32-1
- Update to 0.10.32

* Sun Jan 16 2011 Matthias Clasen <mclasen@redhat.com> 0.10.31.3-2
- Drop explicit, unused liboil dependency

* Wed Jan 12 2011 Benjamin Otte <otte@redhat.com> 0.10.31.3-1
- Update to prerelease

* Wed Dec 01 2010 Benjamin Otte <otte@redhat.com> 0.10.31-1
- Update to 0.10.31
- Add tools subpackage

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> 0.10.30.4-1
- Update to 0.10.30.4
- Minor spec file cleanups

* Mon Nov 08 2010 Bastien Nocera <bnocera@redhat.com> 0.10.30-3
- Rebuild with new gobject-introspection

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.10.30-2
- Rebuild with new gobject-introspection

* Thu Jul 15 2010 Benjamin Otte <otte@redhat.com> 0.10.30-1
- Update to 0.10.30

* Wed Jul 07 2010 Benjamin Otte <otte@redhat.com> 0.10.29.4-1
- Update prerelease

* Wed Jun 30 2010 Benjamin Otte <otte@redhat.com> 0.10.29.3-1
- Update prerelease

* Sun Jun 27 2010 Benjamin Otte <otte@redhat.com> 0.10.29.2-1
- Upate to prerelease

* Wed Apr 28 2010 Benjamin Otte <otte@redhat.com> 0.10.29-1
- Update to 0.10.29

* Tue Apr 27 2010 Benjamin Otte <otte@redhat.com> 0.10.28.3-2
- Make a noarch devel-docs subpackage to avoid conflicts

* Mon Apr 26 2010 Benjamin Otte <otte@redhat.com> 0.10.28.3-1
- Update pre-release

* Thu Apr 15 2010 Benjamin Otte <otte@redhat.com> 0.10.28.2-1
- Update pre-release

* Mon Mar 15 2010 Benjamin Otte <otte@redhat.com> 0.10.28-3
- BuildRequire iso-codes-devel (#573040)

* Mon Mar 15 2010 Benjamin Otte <otte@redhat.com> 0.10.28-2
- Require iso-codes (#573040)

* Tue Mar 09 2010 Benjamin Otte <otte@redhat.com> 0.10.28-1
- Update to 0.10.28

* Mon Mar 08 2010 Benjamin Otte <otte@redhat.com> 0.10.27-1
- Update to 0.10.27

* Thu Mar 04 2010 Benjamin Otte <otte@redhat.com> 0.10.26.4-1
- Update pre-release
- Add gobject-introspection support

* Thu Feb 25 2010 Benjamin Otte <otte@redhat.com> 0.10.26.3-1
- Update to pre-release

* Fri Feb 19 2010 Benjamin Otte <otte@redhat.com> 0.10.26.2-1
- Update to pre-release

* Thu Feb 11 2010 Benjamin Otte <otte@redhat.com> 0.10.26-3
- Patch Makefile.in, too and not just Makefile.am

* Thu Feb 11 2010 Benjamin Otte <otte@redhat.com> 0.10.26-2
- Fix build to conform to new DSO rules

* Thu Feb 11 2010 Benjamin Otte <otte@redhat.com> 0.10.26-1
- Update to 0.10.26

* Fri Feb 05 2010 Benjamin Otte <otte@redhat.com> 0.10.25.3-1
- Update pre-release

* Wed Jan 27 2010 Bastien Nocera <bnocera@redhat.com> 0.10.25.2-1
- Update to pre-release

* Mon Nov 30 2009 Bastien Nocera <bnocera@redhat.com> 0.10.25.1-2
- Update to snapshot

* Fri Nov 06 2009 Bastien Nocera <bnocera@redhat.com> 0.10.25-6
- Fix hangs when loading a movie with an associated subtitle in Totem

* Tue Nov 03 2009 Bastien Nocera <bnocera@redhat.com> 0.10.25-5
- Update volume notification patch

* Thu Oct 29 2009 Bastien Nocera <bnocera@redhat.com> 0.10.25-4
- Make playbin push volume changes to the front-end

* Tue Oct 27 2009 Bastien Nocera <bnocera@redhat.com> 0.10.25-3
- Fix audio disappearing with newer pulsesink

* Tue Oct 13 2009 Bastien Nocera <bnocera@redhat.com> 0.10.25-2
- Add patches to fix some playbin2 bugs (#518880)

* Mon Oct 05 2009 Bastien Nocera <bnocera@redhat.com> 0.10.25-1
- Update to 0.10.25
- Require a gstreamer of the same version as us (#503707)

* Thu Oct 01 2009 Bastien Nocera <bnocera@redhat.com> 0.10.24.4-1
- Update to pre-release

* Wed Aug 26 2009 Adam Jackson <ajax@redhat.com> 0.10.24-2
- avf-support.patch: Add AVF file recognition (gnome #593117)

* Wed Aug 05 2009 Bastien Nocera <bnocera@redhat.com> 0.10.24-1
- Update to 0.10.24

* Tue Jul 28 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23.4-1
- Update to 0.10.23.4

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.23.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23.3-2
- Remove old patches (the input-selector has been moved to be
  an internal playbin2 plugin)

* Tue Jul 21 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23.3-1
- Udpate to 0.10.23.3

* Thu Jul 16 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23.2-1
- Update to 0.10.23.2

* Fri Jun 19 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23-2
- Move input-selector plugin from -bad to -base (#506767)

* Mon May 11 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23-1
- Update to 0.10.23

* Sat May 09 2009 Bastien Nocera <bnocera@redhat.com> 0.10.22.6-1
- Update to 0.10.22.6

* Fri May 08 2009 Bastien Nocera <bnocera@redhat.com> 0.10.22.5-1
- Update to 0.10.22.5

* Wed May 06 2009 Bastien Nocera <bnocera@redhat.com> 0.10.22.4-1
- Update to 0.10.22.4

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 - Bastien Nocera <bnocera@redhat.com> - 0.10.22-1
- Update to 0.10.22
- Remove upstreamed patches

* Tue Jan 13 2009 - Bastien Nocera <bnocera@redhat.com> - 0.10.21-4
- Avoid deadlocks when PulseAudio disappears

* Thu Jan 1 2009 - Rex Dieter <rdieter@fedoraproject.org> - 0.10.21-3
- rebuild for pkgconfig deps (#478577)

* Fri Oct 03 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.21-2
- Update the gstreamer requirement
- Add a gtk2-devel BR, so that the test-colorkey program will be built

* Fri Oct 03 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.21-1
- Update to 0.10.21

* Wed Sep 24 2008 Jeremy Katz <katzj@redhat.com> - 0.10.20-6
- gst-visualize is just a test program that we don't really need to include 
  and having it means that perl gets pulled into small images (#462620)

* Fri Sep 12 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.20-4
- Another rebuild

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.20-3
- Rebuild for new RPM provides

* Sat Aug 23 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.20-2
- Fix useless codeina popup when playing recent ogg files (#458404)

* Wed Jun 18 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.20-1
- Update to 0.10.20

* Wed Jun 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.19-6
- Add patch full of gio fixes

* Mon Jun 02 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.19-5
- Let the package build its own documentation

* Sat May 24 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.19-4
- Remove the gnome-vfs plugin, and see what breaks

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10.19-3
- fix license tag

* Fri Apr 18 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.19-2
- Add patch to avoid sync problems in the ALSA sink when a specific
  track has both playback and record flags

* Fri Apr 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.19-1
- Update to 0.10.19

* Tue Mar 25 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.18-1
- Update to 0.10.18
- Re-enable the libvisual plugins

* Sun Mar 09 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.17.2-4
- Disable libvisual for now (#435771)

* Tue Mar 04 2008 Adam Jackson <ajax@redhat.com> 0.10.17.2-3
- gstpb-0.10.15-cd-speed.patch: Set default CD read speed to something
  sensible. (#431178)
- s/Fedora Core/Fedora/
- Don't even bother building static libs.

* Tue Mar 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.17.2-2
- Enable the GIO plugin

* Tue Mar 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.17.2-1
- Update to 0.10.17.2 pre-release

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.10.17-2
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.17-1
- Update to 0.10.17

* Tue Jan 29 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.16-1
- Update to 0.10.16

* Sun Jan 20 2008  Matthias Clasen  <mclasen@redhat.com> - 0.10.15-3
- Fix upgrade path

* Mon Jan 07 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.15-2
- Add upstream patch to fix default track selection on Thinkpads
  (#344911)

* Sat Nov 17 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.15-1
- Update to 0.10.15

* Thu Oct 18 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.14-6
- Add patch to fix playback of short Ogg Vorbis files (#328851)

* Wed Aug 29 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.14-5
- Add patch to avoid critical warning when getting information about
  missing codecs
- Up liboil requirement

* Tue Aug 28 2007 Adam Jackson <ajax@redhat.com> 0.10.14-4
- BuildReq on libvisual and add the plugin. (#253491)

* Wed Aug 15 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.14-3
- Up requirement for liboil for PPC machines (#252179)

* Sat Aug 04 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.14-2
- Update to 0.10.14
- Add RTSP and SDP helper libraries

* Tue Jun 05 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.13-2
- Add missing files

* Tue Jun 05 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.13-1
- Update to 0.10.13

* Fri May 18 2007 Adam Jackson <ajax@redhat.com> 0.10.12-3
- Add directory ownership claims to %%files devel. (#240238)

* Thu Mar 08 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.12-2
- Remove the patch to disable docs, install the docs by hand instead
  Add libgstpbutils to the files

* Thu Mar 08 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.12-1
- Update to 0.10.12

* Wed Jan 24 2007 Adam Jackson <ajax@redhat.com>
- Minor spec cleanups (#186550)

* Tue Dec 12 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.11-1
- Update to 0.10.11

* Mon Oct 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.10-1
- Update to 0.10.10

* Fri Jul 28 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.9-3
- Re-add docs

* Thu Jul 27 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.9-2
- Disable gtk-doc to fix multilib conflicts

* Thu Jul 20 2006 John (J5) Palmieri <johnp@redhat.com> - 0.10.9-1
- Update to 0.10.9

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> 0.10.7-1
- Update to 0.10.7

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 0.10.3-3
- really add BuildRequires: cdparanoia-devel (#179034)

* Mon Feb 20 2006 John (J5) Palmieri <johnp@redhat.com> - 0.10.3-2
- Obsolete gstreamer-plugins (Bug #182098)

* Fri Feb 10 2006 Christopher Aillon <caillon@redhat.com> - 0.10.3-1
- Update to 0.10.3

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.10.2-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Warren Togami <wtogami@redhat.com> - 0.10.2-2
- buildreq cdparanoia-devel (#179034 thias)

* Wed Jan 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.10.2-1
- Upgrade to 0.10.2
- Require gstreamer-0.10.2
- Add libgstcdda and libcdparanoia to the %files section

* Fri Jan 06 2006 John (J5) Palmieri <johnp@redhat.com> - 0.10.1-1
- New upstream version
- gst-launch removed from upstream

* Sat Dec 17 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-1
- Fedora Development build

* Wed Dec 14 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.2
- new glib build

* Mon Dec 05 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.1
- new release

* Thu Dec 01 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.7-0.gst.1
- new release with 0.10 majorminor
- remove sinesrc
- replace ximage with ximagesink
- update libs

* Sat Nov 12 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.5-0.gst.1
- new release

* Mon Oct 24 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-0.gst.1
- added audiotestsrc plugin
- new release

* Mon Oct 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-0.gst.1
- new release

* Fri Sep 02 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- clean up a little

* Fri May 6 2005 Christian Schaller <christian at fluendo dot com>
- Added libgstaudiorate and libgstsubparse to spec file

* Thu May 5 2005 Christian Schaller <christian at fluendo dot com>
- first attempt at spec file for gst-plugins-base
