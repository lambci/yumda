Name:		orc
Version:	0.4.26
Release: 1%{?dist}.0.2
Summary:	The Oil Run-time Compiler

Group:		System Environment/Libraries
License:	BSD
URL:		http://cgit.freedesktop.org/gstreamer/orc/
Source0:        http://gstreamer.freedesktop.org/src/orc/%{name}-%{version}.tar.xz

BuildRequires:	gtk-doc, libtool

Prefix: %{_prefix}

%description
Orc is a library and set of tools for compiling and executing
very simple programs that operate on arrays of data.  The "language"
is a generic assembly language that represents many of the features
available in SIMD architectures, including saturated addition and
subtraction, and many arithmetic operations.


%prep
%setup -q
NOCONFIGURE=1 autoreconf -vif


%build
%configure --disable-static --enable-gtk-doc

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

# Remove unneeded files.
find %{buildroot}/%{_libdir} -name \*.a -or -name \*.la -delete
rm -rf %{buildroot}/%{_libdir}/orc

touch -r stamp-h1 %{buildroot}%{_includedir}/%{name}-0.4/orc/orc-stdint.h   


%files
%license COPYING
%{_libdir}/liborc-*.so.*
%{_bindir}/orc-bugreport

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}
%exclude %{_bindir}/orcc


%changelog
* Thu Apr 16 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Mar 09 2017 Wim Taymans <wtaymans@redhat.com> - 0.4.26-1
- Update to 0.4.26
- Remove upstreamed patches
- Resolves: #1430051

* Thu Aug 13 2015 Wim Taymans <wtaymans@redhat.com> - 0.4.22-5
- Run backup functions on s390x instead of emulation
- Fix load of parameters smaller than 64 bits
- Related: rhbz#1249506

* Thu Aug 13 2015 Wim Taymans <wtaymans@redhat.com> - 0.4.22-4
- Fix unit test on ppc64le
- Resolves: rhbz#1252498

* Wed Jul 8 2015 Wim Taymans <wtaymans@redhat.com> - 0.4.22-3
- Fix loading of 64bit parameters on big endian
- Related: #1234325

* Wed Mar 25 2015 Wim Taymans <wtaymans@redhat.com> - 0.4.22-2
- Don't run tests during build
- add new source
- remove old patches, add new patch
- Resolves: #1174391

* Fri Aug 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.22-1
- Update to 0.4.22
- Resolves: #1174391

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.4.17-5
- Mass rebuild 2014-01-24

* Wed Jan 08 2014 Benjamin Otte <otte@redhat.com> - 0.4.17-4
- Don't run tests during build
Resolves: 1048890

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.4.17-3
- Mass rebuild 2013-12-27

* Wed Feb 20 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.17-2
- Fix typo rhbz#817944

* Wed Feb 20 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.17-1
- Update to latest upstream release
- Removed obsolete patches

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Daniel Drake <dsd@laptop.org> - 0.4.16-7
- Fix fallback path when register allocation fails
- Fixes gstreamer-1.0 crash on OLPC XO-1.75

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 07 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.16-5
- Updated subdir patch.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.16-4
- Rebuilt for glibc bug#747377

* Sun Oct 16 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.16-3
- Add Fedora specific patch for tempfiles in subdirs

* Sun Oct 16 2011 Daniel Drake <dsd@laptop.org> - 0.4.16-2
- Add upstream patches to fix gstreamer crash on Geode (#746185)

* Mon Oct 03 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.16-1
- Update to 0.4.16
- Fixing regression introdcued by 0.4.15 (#742534 and #734911)

* Mon Sep 26 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.15-1
- Update to 0.4.15

* Mon Jun 20 2011 Peter Robinson <pbrobinson@gmail.com> - 0.4.14-3
- Add ARM platforms to the make check exclusion

* Sat May 07 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.14-2
- Add orc-bugreport to the main package (#702727)

* Sat Apr 30 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.14-1
- Update to 0.4.14

* Tue Apr 19 2011 Fabian Deutsch <fabiand@fedorpaproject.org> - 0.4.13-1
- Update to 0.4.13, another bug fixing release

* Fri Apr 15 2011 Fabian Deutsch <fabiand@fedorpaproject.org> - 0.4.12-1
- Update to 0.4.12, a bug fixing release

* Wed Feb 23 2011 Karsten Hopp <karsten@redhat.com> 0.4.11-3
- don't run tests on ppc, ppc64

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.11-1
- Update to 0.4.11.
- More bug fixes for CPUs that do not have backends, mmx and sse.

* Fri Oct 08 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.10-1
- Update to 0.4.10.
- Fixes some bugs related to SELinux.

* Mon Sep 06 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.9-1
- Update to 0.4.9, a pimarily bug fixing release.

* Thu Aug 19 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.7-1
- Updated to 0.4.7.

* Thu Jul 22 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.6-1
- Updated to 0.4.6.
- New orc-bugreport added.

* Tue Jul 13 2010 Dan Horák <dan[at]danny.cz> - 0.4.5-3
- don't run test on s390(x)

* Sun Jun 13 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.5-2
- Added removed testing libraries to package.

* Sun Jun 13 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.5-1
- Updated to 0.4.5.
- Removed testing libraries from package.

* Mon Apr 05 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.4-2
- Docs as noarch.
- Sanitize timestamps of header files.
- orcc in -compiler subpackage.

* Tue Mar 30 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.4-1
- Updated to 0.4.4: Includes bugfixes for x86_64.

* Wed Mar 17 2010 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.3-2
- Running autoreconf to prevent building problems.
- Added missing files to docs.
- Added examples to devel docs.

* Thu Mar 04 2010 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.3-1
- Updated to 0.4.3

* Sun Oct 18 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-4
- Removed unused libdir

* Sun Oct 18 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-3
- Specfile cleanup
- Removed tools subpackage
- Added docs subpackage

* Sat Oct 03 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-2
- Use orc as pakage name
- spec-file cleanup
- Added devel requirements
- Removed an rpath issue

* Fri Oct 02 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-1
- Initial release

