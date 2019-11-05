
#0 to bootstrap libproxy circle dependencies - 1 normal case
%global _with_webkitgtk3 0
%global _with_gnome3 0
%global _with_mozjs 0
%global _with_gnome 0
%global _with_kde 0
%global _with_networkmanager 0
%global _with_python 0

%define _trivial .0
%define _buildid .2
Name:           libproxy
Version:        0.4.11
Release: 10%{?svn}%{?dist}.0.3
Summary:        A library handling all the details of proxy configuration

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://code.google.com/p/libproxy/

Source0:        http://libproxy.googlecode.com/files/libproxy-%{version}%{?svn}.tar.gz
Patch0:         libproxy-0.4.10-mozjs.patch
Patch1:         0001-pacrunner_mozjs-Also-support-mozjs-17.0.patch
Patch3:         libproxy-0.4.11-fdleak.patch
Patch4:         libproxy-0.4.11-crash.patch

BuildRequires:  python-devel
BuildRequires:  libmodman-devel >= 2.0.1
BuildRequires:  cmake >= 2.6.0

Prefix: %{_prefix}

%description
libproxy offers the following features:

    * extremely small core footprint (< 35K)
    * no external dependencies within libproxy core
      (libproxy plugins may have dependencies)
    * only 3 functions in the stable external API
    * dynamic adjustment to changing network topology
    * a standard way of dealing with proxy settings across all scenarios
    * a sublime sense of joy and accomplishment 


%package        bin
Summary:        Binary to test %{name}
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Prefix: %{_prefix}

%description    bin
The %{name}-bin package contains the proxy binary for %{name}


%prep
%setup -q
%patch0 -p1 -b .orig
%patch1 -p1 -b .orig
%patch3 -p1 -b .fdleak
%patch4 -p1 -b .crash

%build
%{cmake} \
  -DMODULE_INSTALL_DIR=%{_libdir}/%{name}/%{version}/modules \
  -DWITH_PERL=OFF \
  -DWITH_GNOME=OFF \
  -DWITH_GNOME3=OFF \
  -DWITH_WEBKIT=OFF \
  -DWITH_WEBKIT3=OFF \
  -DWITH_MOZJS=OFF \
  -DWITH_PYTHON=OFF \
   .
make VERBOSE=1 %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

#In case all modules are disabled
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/%{version}/modules

%files 
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/modules

%files bin
%defattr(-,root,root,-)
%{_bindir}/proxy

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Jul 12 2016 Dan Winship <danw@redhat.com> - 0.4.11-10
- Rebuild for mozjs soname bump (#1353447)

* Fri Mar 20 2015 Dan Winship <danw@redhat.com> - 0.4.11-8
- Fix pacrunner crash (#1201658)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.4.11-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.4.11-5
- Mass rebuild 2013-12-27

* Mon Jul  8 2013 Dan Winship <danw@redhat.com> - 0.4.11-4.el7.1
- Rebuild to fix RPM changelog

* Mon Jun 03 2013 Colin Walters <walters@redhat.com> - 0.4.11-4
- Add patch to build with mozjs17, use it by default

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan  3 2013 Dan Winship <danw@redhat.com> - 0.4.11-2
- Minor dependency fixes

* Mon Dec 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.11-1
- Update to 0.4.11 -  CVE-2012-5580

* Tue Oct 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.10-1
- Update to 0.4.10
- Fix CVE-2012-4504

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.7-4
- Add upstream patches to use js rather than xulrunner
- Add patch to fix FTBFS on gcc 4.7
- Cleanup spec for latest updates and remove obsolete bits

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.4.7-2
- Rebuild for new libpng

* Tue Jun 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.7-1
- Update to 0.4.7
- libproxy-1.0.pc is now reliable starting with 0.4.7

* Tue Apr 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.7-0.1svn20110412
- Update to 0.4.7 svn20110412
- Add support for webkitgtk3
- Add support for xulrunner 2.0
- fix #683015 - libproxy fails with autoconfiguration
- fix #683018 - libproxy needs BR: NetworkManager-glib-devel  (f14)
- Manually fix libproxy-1.0.pc version field - #664781 / #674854

* Wed Nov 24 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-3
- Fix mozjs/webkit obsoletion - rhbz#656849
- Workaround unreliable Version field in pkg-config - rhbz#656484

* Sun Nov 07 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-1
- Update to 0.4.6
- Fix python module not arch dependant

* Mon Sep 06 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.5-2
- Update to 0.4.5
- Disable mozjs on fedora >= 15
- Disable webkit
- Add libproxy bootstrap option to disable modules.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 13 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.4-6
- Fix libproxy-1.0.pc

* Mon Jul 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-5
- Re-enable mozjs and webkit

* Mon Jul 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-4
- Disable mozjs to get around a build error temporarily

* Mon Jul 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-3
- Disable webkit subpackage in order to resolve circular dep

* Sat Jul 03 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-2
- Fix missing BuildRequires: libmodman-devel

* Sun Jun 13 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-1
- Update to 0.4.4
- Removed install workarounds (fixed upstream)
- Removed patches (fixed upstream)
- Moved -python to noarch
- Downgrade cmake requirement (upstream change)
- Disabled perl bindings
- Run tests

* Thu Mar 11 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.1-4
- Add missing libXmu-devel

* Sun Feb 21 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.1-4
- Globalism and update gecko to 1.9.2
- Avoid rpath on _libdir
- Fix BR for kde4 to kdelibs-devel

* Sun Dec 27 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1
- Avoid dependecies on -python and -bin subpackages
- Create -networkmanager sub-package.

* Thu Sep 24 2009 kwizart < kwizart at gmail.com > - 0.3.0-1
- Update to 0.3.0

* Thu Sep 17 2009 kwizart < kwizart at gmail.com > - 0.2.3-12
- Remove Requirement of %%{name}-pac virtual provides 
  from the main package - #524043

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  9 2009 kwizart < kwizart at gmail.com > - 0.2.3-10
- Rebuild for webkit
- Raise requirement for xulrunner to 1.9.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 kwizart < kwizart at gmail.com > - 0.2.3-8
- Merge NetworkManager module into the main libproxy package
- Main Requires the -python and -bin subpackage 
 (splitted for multilibs compliance).

* Fri Oct 24 2008 kwizart < kwizart at gmail.com > - 0.2.3-7
- Disable Gnome/KDE default support via builtin modules.
 (it needs to be integrated via Gconf2/neon instead).

* Tue Oct 21 2008 kwizart < kwizart at gmail.com > - 0.2.3-6
- Disable Obsoletes.
- Requires ev instead of evr for optionnals sub-packages.

* Tue Oct 21 2008 kwizart < kwizart at gmail.com > - 0.2.3-5
- Use conditionals build.

* Mon Sep 15 2008 kwizart < kwizart at gmail.com > - 0.2.3-4
- Remove plugin- in the name of the packages

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 0.2.3-3
- Move proxy.h to libproxy/proxy.h
  This will prevent it to be included in the default include path
- Split main to libs and util and use libproxy to install all

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 0.2.3-2
- Rename binding-python to python
- Add Requires: gecko-libs >= %%{gecko_version}
- Fix some descriptions
- Add plugin-webkit package
 
* Fri Jul 11 2008 kwizart < kwizart at gmail.com > - 0.2.3-1
- Convert to Fedora spec

* Fri Jun 6 2008 - dominique-rpm@leuenberger.net
- Updated to version 0.2.3
* Wed Jun 4 2008 - dominique-rpm@leuenberger.net
- Extended spec file to build all available plugins
* Tue Jun 3 2008 - dominique-rpm@leuenberger.net
- Initial spec file for Version 0.2.2

