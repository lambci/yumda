%define         gstreamer       gstreamer
%define         majorminor      0.10

%define         _glib2                  2.22
%define         _libxml2                2.4.0
%define         _gobject-introspection  0.6.3

%define _trivial .0
%define _buildid .1
Name:           %{gstreamer}
Version:        0.10.36
Release: 7%{?dist}.0.2
Summary:        GStreamer streaming media framework runtime

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
#Source:         http://gstreamer.freedesktop.org/src/gstreamer/pre/gstreamer-%{version}.tar.xz
Source:         http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       gstreamer-tools >= %{version}

BuildRequires:  glib2-devel >= %{_glib2}
BuildRequires:  libxml2-devel >= %{_libxml2}
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  m4
BuildRequires:  check-devel
BuildRequires:  gtk-doc >= 1.3
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  gobject-introspection-devel >= %{_gobject-introspection}
# We need to use the system libtool or else we end up with RPATHs
BuildRequires:  libtool

# because AM_PROG_LIBTOOL was used in configure.ac
BuildRequires:  gcc-c++

# For the GStreamer RPM provides
Patch0:         gstreamer-0.10.36-bison3.patch
Patch1:         gstreamer-inspect-rpm-format.patch
Patch2:         fix-docs.patch
Source1:        gstreamer.prov
Source2:        gstreamer.attr

### documentation requirements
BuildRequires:  python2
BuildRequires:  openjade
BuildRequires:  jadetex
BuildRequires:  libxslt
BuildRequires:  docbook-style-dsssl
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-utils
BuildRequires:  transfig
BuildRequires:  netpbm-progs
BuildRequires:  tetex-dvips
BuildRequires:  ghostscript
%if !0%{?rhel}
BuildRequires:  xfig
%endif

Prefix: %{_prefix}

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

%package -n gstreamer-tools
Summary:        common tools and files for GStreamer streaming media framework
Group:          Applications/Multimedia
# gst-feedback uses these
Requires:       which, pkgconfig
Prefix: %{_prefix}

%description -n gstreamer-tools
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new   
plugins.

This package contains wrapper scripts for the command-line tools that work
with different major/minor versions of GStreamer.

%prep
%setup -q

%patch0 -p1 -b .bison3
%patch1 -p1 -b .rpm-provides
%patch2 -p1 -b .fix-docs

%build
%configure \
  --with-package-name='Fedora Core gstreamer package' \
  --with-package-origin='http://download.fedora.redhat.com/fedora' \
  --disable-gtk-doc \
  --enable-debug \
  --disable-tests --disable-examples

make %{?_smp_mflags} ERROR_CFLAGS="" LIBTOOL="%{_bindir}/libtool"

%install  
rm -rf $RPM_BUILD_ROOT

# Install doc temporarily in order to be included later by rpm
make install DESTDIR=$RPM_BUILD_ROOT

# Clean out files that should not be part of the rpm. 
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# Create empty cache directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/gstreamer-%{majorminor}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%license COPYING
%{_libdir}/libgstreamer-%{majorminor}.so.*
%{_libdir}/libgstbase-%{majorminor}.so.*
%{_libdir}/libgstcontroller-%{majorminor}.so.*
%{_libdir}/libgstdataprotocol-%{majorminor}.so.*
%{_libdir}/libgstnet-%{majorminor}.so.*
%{_libexecdir}/gstreamer-%{majorminor}/

%dir %{_libdir}/gstreamer-%{majorminor}
%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoreindexers.so

%{_libdir}/girepository-1.0/Gst-0.10.typelib
%{_libdir}/girepository-1.0/GstBase-0.10.typelib
%{_libdir}/girepository-1.0/GstCheck-0.10.typelib
%{_libdir}/girepository-1.0/GstController-0.10.typelib
%{_libdir}/girepository-1.0/GstNet-0.10.typelib

%{_bindir}/gst-feedback-%{majorminor}
%{_bindir}/gst-inspect-%{majorminor}
%{_bindir}/gst-launch-%{majorminor}
%{_bindir}/gst-typefind-%{majorminor}
%{_bindir}/gst-xmlinspect-%{majorminor}
%{_bindir}/gst-xmllaunch-%{majorminor}

%files -n gstreamer-tools
%defattr(-, root, root, -)
%{_bindir}/gst-feedback
%{_bindir}/gst-inspect
%{_bindir}/gst-launch
%{_bindir}/gst-typefind
%{_bindir}/gst-xmlinspect
%{_bindir}/gst-xmllaunch

%exclude %{_includedir}
%exclude %{_datadir}
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/libgstreamer-%{majorminor}.so
%exclude %{_libdir}/libgstdataprotocol-%{majorminor}.so
%exclude %{_libdir}/libgstbase-%{majorminor}.so
%exclude %{_libdir}/libgstcheck-%{majorminor}.so*
%exclude %{_libdir}/libgstcontroller-%{majorminor}.so
%exclude %{_libdir}/libgstnet-%{majorminor}.so

%changelog
* Thu Apr 16 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.10.36-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.10.36-6
- Mass rebuild 2013-12-27

* Fri Jul 19 2013 Bastien Nocera <bnocera@redhat.com> 0.10.36-5
- Remove unused PyXML BR

* Thu Jul 17 2013 Matthias Clasen <mclasen@redhat.com> 0.10.36-4
- Fix a bogus BR found by rpmdiff

* Wed Mar 27 2013 Adam Jackson <ajax@redhat.com> 0.10.36-3
- Tweak BRs for RHEL

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Benjamin Otte <otte@redhat.com> 0.10.36-1
- Update to 0.10.36

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> 0.10.35-1
- Update to 0.10.35

* Sat May 14 2011 Benjamin Otte <otte@redhat.com> 0.10.34-1
- Update to 0.10.34

* Tue May 10 2011 Benjamin Otte <otte@redhat.com> 0.10.33-1
- Update to 0.10.33 

* Sun May 01 2011 Benjamin Otte <otte@redhat.com> 0.10.32.4-1
- Update prerelease

* Wed Apr 27 2011 Benjamin Otte <otte@redhat.com> 0.10.32.3-1
- Update prerelease

* Mon Apr 18 2011 Benjamin Otte <otte@redhat.com> 0.10.32.2-1
- Update to prerelease

* Mon Mar 21 2011 Panu Matilainen <pmatilai@redhat.com> 0.10.32-4
- Adjust provides generation for rpm >= 4.9.0

* Mon Mar 21 2011 Bastien Nocera <bnocera@redhat.com> 0.10.32-3
- Make it possible to auto-install GStreamer elements by name

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Benjamin Otte <otte@redhat.com> 0.10.32-1
- Update to 0.10.32

* Tue Jan 11 2011 Benjamin Otte <otte@redhat.com> 0.10.31.3-1
- Update to prerelease

* Fri Jan 07 2011 Benjamin Otte <otte@redhat.com> 0.10.31.2-1
- Update to prerelease

* Wed Dec 01 2010 Benjamin Otte <otte@redhat.com> 0.10.31-1
- Update to 0.10.31

* Mon Nov 08 2010 Bastien Nocera <bnocera@redhat.com> 0.10.30-6
- Rebuild against newer gobject-introspection

* Sun Nov 07 2010 Dan Horák <dan[at]danny.cz> 0.10.30-5
- Fix build with make 3.82

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> 0.10.30-4
- Rebuild against newer gobject-introspection

* Thu Sep 02 2010 Bastien Nocera <bnocera@redhat.com> 0.10.30-3
- Make gstreamer.prov faster by avoiding non-"libgst" files early
  Patch from Dominique Leuenberger <dimstar@opensuse.org>

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.10.30-2
- Rebuild with new gobject-introspection

* Thu Jul 15 2010 Benjamin Otte <otte@redhat.com> 0.10.30-1
- Update to 0.10.30

* Wed Jul 07 2010 Benjamin Otte <otte@redhat.com> 0.10.29.4-1
- Update prerelease

* Wed Jun 30 2010 Benjamin Otte <otte@redhat.com> 0.10.29.3-1
- Update prerelease

* Sun Jun 27 2010 Benjamin Otte <otte@redhat.com> 0.10.29.2-1
- Update to prerelease

* Mon Jun 07 2010 Bastien Nocera <bnocera@redhat.com> 0.10.29-2
- Add patch to fix download buffering in Totem

* Wed Apr 28 2010 Benjamin Otte <otte@redhat.com> 0.10.29-1
- Update to 0.10.29

* Tue Apr 27 2010 Benjamin Otte <otte@redhat.com> 0.10.28.3-2
- Make a noarch devel-docs subpackage to avoid conflicts

* Thu Apr 26 2010 Benjamin Otte <otte@redhat.com> 0.10.28.3-1
- Update pre-release

* Thu Apr 15 2010 Benjamin Otte <otte@redhat.com> 0.10.28.2-1
- Update pre-release

* Mon Mar 15 2010 Benjamin Otte <otte@redhat.com> 0.10.28-2
- Fix crashes when plugin init fails (#572800)

* Tue Mar 09 2010 Benjamin Otte <otte@redhat.com> 0.10.28-1
- Update to 0.10.28

* Sun Mar 07 2010 Benjamin Otte <otte@redhat.com> 0.10.27-1
- Update to 0.10.27

* Thu Mar 04 2010 Benjamin Otte <otte@redhat.com> 0.10.26.4-1
- Update pre-release
- Add gobject-introspection support

* Thu Feb 25 2010 Benjamin Otte <otte@redhat.com> 0.10.26.3-1
- Update to pre-release

* Fri Feb 19 2010 Benjamin Otte <otte@redhat.com> 0.10.26.2-1
- Update to pre-release

* Fri Feb 11 2010 Benjamin Otte <otte@redhat.com> 0.10.26-1
- Update to 0.10.26

* Fri Feb 05 2010 Benjamin Otte <otte@redhat.com> 0.10.25.3-1
- Update pre-release

* Wed Jan 27 2010 Bastien Nocera <bnocera@redhat.com> 0.10.25.2-1
- Update to pre-release

* Mon Nov 30 2009 Bastien Nocera <bnocera@redhat.com> 0.10.25.1-2
- Update to snapshot

* Mon Oct 05 2009 Bastien Nocera <bnocera@redhat.com> 0.10.25-1
- Update to 0.10.25

* Thu Oct 01 2009 Bastien Nocera <bnocera@redhat.com> 0.10.24.4-1
- Update to pre-release

* Wed Aug 05 2009 Bastien Nocera <bnocera@redhat.com> 0.10.24-1
- Update to 0.10.24

* Tue Jul 28 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23.4-1
- Update to 0.10.23.4

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.23.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23.3-1
- Update to 0.10.23.3

* Thu Jul 16 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23.2-1
- Update to 0.10.23.2

* Wed Jun 10 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23-2
- Update gst-inspect patch to ignore rank none plugins

* Mon May 11 2009 Bastien Nocera <bnocera@redhat.com> 0.10.23-1
- Update to 0.10.23

* Wed May 06 2009 Bastien Nocera <bnocera@redhat.com> 0.10.22.4-1
- Update to 0.10.22.4

* Thu Feb 26 2009 Warren Togami <wtogami@redhat.com> - 0.10.22-4
- Move req on which and pkgconfig to gstreamer-tools

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Adam Jackson <ajax@redhat.com> 0.10.22-2
- Re-enable parallel build. (#486196)

* Tue Jan 20 2009 - Bastien Nocera <bnocera@redhat.com> - 0.10.22-1
- Update to 0.10.22
- Remove upstreamed patches, update rpm provides patch

* Mon Jan 05 2009 - Bastien Nocera <bnocera@redhat.com> - 0.10.21-4
- Fix build with newer version of bison

* Thu Jan 01 2009 Rex Dieter <rdieter@fedoraprojet.org> - 0.10.21-3
- rebuild for pkgconfig deps (#478576)

* Tue Nov 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10.21-2
- fix gnome bz 555631 with patch from upstream cvs
- use system libtool to prevent rpaths

* Fri Oct 03 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.21-1
- Update to 0.10.21

* Sun Sep 14 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.20-6
- Hopefully fix RPM provides problem when the GStreamer plugin
  requires a library installed by the package itself

* Fri Sep 12 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.20-5
- Update rpm provides script and patch to:
  - filter out errors
  - only run gst-inspect on gstreamer plugins
  - print out protocol handlers provides correctly

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.20-4
- Add the rpm scripts install in /usr/lib/rpm, not under libdir on 64-bit

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.20-3
- Update filelist as well

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.20-2
- Update gstreamer provides work for the new RPM, see #438225

* Wed Jun 18 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.20-1
- Update to 0.10.20

* Mon Jun 02 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.19-3
- Package more documentation (#240656)

* Wed May 21 2008 - Tom "spot" Callaway <tcallawa@redhat.com> - 0.10.19-2
- fix license tag

* Fri Apr 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.19-1
- Update to 0.10.19

* Wed Mar 19 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.18-1
- Update to 0.10.18
- Add patch to gst-inspect to generate RPM provides
- Add RPM find-provides script

* Tue Mar 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.17.2-1
- Update to 0.10.17.2 pre-release

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.10.17-2
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.17-1
- Update to 0.10.17

* Tue Jan 29 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.16-1
- Update to 0.10.16

* Fri Nov 16 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.15-1
- Update to 0.10.15

* Mon Oct  1 2007 Matthias Clasen <mclasen@redhat.com> - 0.10.14-4
- Add missing Requires (#312671)

* Tue Aug 14 2007 Matthias Clasen <mclasen@redhat.com> - 0.10.14-3
- Require check-devel (#251956)

* Sat Aug 04 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.14-1
- Update to 0.10.14

* Tue Jun 05 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.13-2
- Remove upstreamed docs patch

* Tue Jun 05 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.13-1
- Update to 0.10.13

* Thu Mar 08 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.12-1
- Update to 0.10.12

* Tue Feb 13 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.11-2
- Remove Requires on packages that BuildRequire us

* Tue Dec 12 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.11-1
- Update to 0.10.11

* Fri Oct 27 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.10-2
- Cleanups
- Attempt to fix multilib conflicts

* Mon Oct 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.10-1
- Update to 0.10.10

* Thu Jul 27 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.9-2
- Disable gtk-doc to fix multilib conflicts

* Thu Jul 20 2006 John (J5) Palmieri <johnp@redhat.com> - 0.10.9-1
- Update to new upstream version

* Wed Jul 19 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.8-4
- Re-add the gstreamer-plugins-good dependency

* Wed Jul 19 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.8-3.2
- Temporarily break the dependency cycle with gsteamer-plugins-good

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.10.8-3.1
- rebuild

* Wed Jun 28 2006 Karsten Hopp <karsten@redhat.de> 0.10.8-3
- remove RPATH pointing to RPM_BUILD_ROOT (#196870)

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.8-2
- Rebuild

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.8-1
- Update to 0.10.8

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 0.10.6-1
- Update to 0.10.6

* Tue Feb 14 2006 Rik van Riel <riel@redhat.com> - 0.10-3-3
- Obsolete gstreamer-plugins (#181296)

* Mon Feb 13 2006 Christopher Aillon <caillon@redhat.com> - 0.10.3-2
- Rebuild

* Fri Feb 10 2006 Christopher Aillon <caillon@redhat.com> - 0.10.3-1
- Update to 0.10.3

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.10.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.10.2-1
- Upgrade to 0.10.2

* Fri Jan 06 2006 John (J5) Palmieri <johnp@redhat.com> - 0.10.1-1
- New upstream version

* Fri Dec 16 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-1
- rebuilt for Fedora Core Development

* Wed Dec 14 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.2
- rebuilt against newer GLib and friends

* Mon Dec 05 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.1
- new release

* Thu Dec 01 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.7-0.gst.1
- new release, with 0.10 majorminor
- removed compprep and complete
- added plugins docs
- renamed libgstcorelements, libgstcoreindexers
- added libgstnet

* Sat Nov 12 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.5-0.gst.1
- new release

* Mon Oct 24 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-0.gst.1
- new release

* Mon Oct 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-0.gst.1
- new release

* Thu Sep 08 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.2-0.gst.1
- added libgstcheck
- new release

* Thu Jun 09 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-0.gst.1
- first development series release

* Tue May 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.10-0.gst.1
- new release
- up glib2 to 2.4 because disting on 2.4 builds marshalling code needing 2.4

* Mon May 02 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.9.2-0.gst.1
- new prerelease

* Tue Feb 08 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.9-0.gst.1
- new release
- switch back to the gst tag since fedora.us is gone

* Thu Feb 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.8.2-0.fdr.1
- new prerelease

* Thu Dec 23 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.8-0.fdr.1
- new upstream release

* Fri Dec 17 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.7.2-0.fdr.1
- new prerelease
- added fair gthread scheduler

* Wed Oct 06 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.7-0.fdr.1
- update for new GStreamer release

* Tue Oct 05 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.6-0.fdr.1
- update for new GStreamer release

* Sun Sep 26 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.5.3-0.fdr.1
- update for new GStreamer prerelease

* Sun Sep 12 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.5.2-0.fdr.1
- update for new GStreamer prerelease

* Mon Aug 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.5-0.fdr.1
- update for new GStreamer release

* Thu Aug 12 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.4.2-0.fdr.1
- update for new GStreamer prerelease
- set package name and origin

* Tue Jul 20 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.4-0.fdr.1
- update for new GStreamer release
- unbreak the postun script by not removing the cache dir

* Tue Jul 20 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.3.3-0.fdr.1: update for new GStreamer prerelease

* Fri Jul 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.3.2-0.fdr.1: update for new GStreamer prerelease

* Sat Jun 05 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.3-0.fdr.1: update for new GStreamer release

* Fri Jun 04 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.2-0.fdr.1: update for new GStreamer release

* Thu Apr 15 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.1-0.fdr.1: update for new GStreamer release

* Thu Apr 15 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- add entry schedulers, clean up scheduler file section

* Tue Mar 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.0-0.fdr.1: update for new GStreamer release, renamed base to gstreamer

* Tue Mar 09 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.6-0.fdr.1: updated for new GStreamer release, with maj/min set to 0.8

* Mon Mar 08 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.5-0.fdr.3: fix postun script

* Fri Mar 05 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.5-0.fdr.2: new release

* Wed Feb 11 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.4-0.fdr.1: synchronize with Matthias's package

* Sat Feb 07 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- make the package name gstreamer07 since this is an unstable release

* Wed Feb 04 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- put versioned tools inside base package, and put unversioned tools in tools

* Mon Dec 01 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- changed documentation buildrequires

* Sun Nov 09 2003 Christian Schaller <Uraeus@gnome.org>
- Fix spec to handle new bytestream library 

* Sun Aug 17 2003 Christian Schaller <uraeus@gnome.org>
- Remove docs build from RPM as the build is broken
- Fix stuff since more files are versioned now
- Remove wingo schedulers
- Remove putbits stuff

* Sun May 18 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- devhelp files are now generated by gtk-doc, changed accordingly

* Sun Mar 16 2003 Christian F.K. Schaller <Uraeus@gnome.org>
- Add gthread scheduler

* Sat Dec 07 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- define majorminor and use it everywhere
- full parallel installability

* Tue Nov 05 2002 Christian Schaller <Uraeus@linuxrising.org>
- Add optwingo scheduler
* Sat Oct 12 2002 Christian Schaller <Uraeus@linuxrising.org>
- Updated to work better with default RH8 rpm
- Added missing unspeced files
- Removed .a and .la files from buildroot

* Sat Sep 21 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added gst-md5sum

* Tue Sep 17 2002 Thomas Vander Stichele <thomas@apestaart.org>
- adding flex to buildrequires

* Fri Sep 13 2002 Christian F.K. Schaller <Uraeus@linuxrising.org>
- Fixed the schedulers after the renaming
* Sun Sep 08 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added transfig to the BuildRequires:

* Sat Jun 22 2002 Thomas Vander Stichele <thomas@apestaart.org>
- moved header location

* Mon Jun 17 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added popt
- removed .la

* Fri Jun 07 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added release of gstreamer to req of gstreamer-devel
- changed location of API docs to be in gtk-doc like other gtk-doc stuff
- reordered SPEC file

* Mon Apr 29 2002 Thomas Vander Stichele <thomas@apestaart.org>
- moved html docs to gtk-doc standard directory

* Tue Mar 5 2002 Thomas Vander Stichele <thomas@apestaart.org>
- move version defines of glib2 and libxml2 to configure.ac
- add BuildRequires for these two libs

* Sun Mar 3 2002 Thomas Vander Stichele <thomas@apestaart.org>
- put html docs in canonical place, avoiding %doc erasure
- added devhelp support, current install of it is hackish

* Sat Mar 2 2002 Christian Schaller <Uraeus@linuxrising.org>
- Added documentation to build

* Mon Feb 11 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added libgstbasicscheduler
- renamed libgst to libgstreamer

* Fri Jan 04 2002 Christian Schaller <Uraeus@linuxrising.org>
- Added configdir parameter as it seems the configdir gets weird otherwise

* Thu Jan 03 2002 Thomas Vander Stichele <thomas@apestaart.org>
- split off gstreamer-editor from core
- removed gstreamer-gnome-apps

* Sat Dec 29 2001 Rodney Dawes <dobey@free.fr>
- Cleaned up the spec file for the gstreamer core/plug-ins split
- Improve spec file

* Sat Dec 15 2001 Christian Schaller <Uraeus@linuxrising.org>
- Split of more plugins from the core and put them into their own modules
- Includes colorspace, xfree and wav
- Improved package Require lines
- Added mp3encode (lame based) to the SPEC

* Wed Dec 12 2001 Christian Schaller <Uraeus@linuxrising.org>
- Thomas merged mpeg plugins into one
* Sat Dec 08 2001 Christian Schaller <Uraeus@linuxrising.org>
- More minor cleanups including some fixed descriptions from Andrew Mitchell

* Fri Dec 07 2001 Christian Schaller <Uraeus@linuxrising.org>
- Added logging to the make statement

* Wed Dec 05 2001 Christian Schaller <Uraeus@linuxrising.org>
- Updated in preparation for 0.3.0 release

* Fri Jun 29 2001 Christian Schaller <Uraeus@linuxrising.org>
- Updated for 0.2.1 release
- Split out the GUI packages into their own RPM
- added new plugins (FLAC, festival, quicktime etc.)

* Sat Jun 09 2001 Christian Schaller <Uraeus@linuxrising.org>
- Visualisation plugins bundled out togheter
- Moved files sections up close to their respective descriptions

* Sat Jun 02 2001 Christian Schaller <Uraeus@linuxrising.org>
- Split the package into separate RPMS, 
  putting most plugins out by themselves.

* Fri Jun 01 2001 Christian Schaller <Uraeus@linuxrising.org>
- Updated with change suggestions from Dennis Bjorklund

* Tue Jan 09 2001 Erik Walthinsen <omega@cse.ogi.edu>
- updated to build -devel package as well

* Sun Jan 30 2000 Erik Walthinsen <omega@cse.ogi.edu>
- first draft of spec file

