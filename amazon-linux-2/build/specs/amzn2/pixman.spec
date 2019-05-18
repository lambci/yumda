%define gitdate 20070827
%define gitrev 8ff7213f39edc1b2b8b60d6b0cc5d5f14ca1928d

Name:           pixman
Version:        0.34.0
Release: 1%{?dist}.0.2
Summary:        Pixel manipulation library

Group:          System Environment/Libraries
License:        MIT
URL:            http://cgit.freedesktop.org/pixman/
#VCS:		git://git.freedesktop.org/git/pixman
# To make git snapshots:
# ./make-pixman-snapshot.sh %{?gitrev}
# if no revision specified, makes a new one from HEAD.
Source0:	http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
Source1:	make-pixman-snapshot.sh

BuildRequires:  automake autoconf libtool pkgconfig

%description
Pixman is a pixel manipulation library for X and cairo.

%package devel
Summary: Pixel manipulation library development package
Group: Development/Libraries
Requires: %{name}%{?isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development library for pixman.

%prep
%setup -q

%build
%configure \
%ifarch %{arm}
  --disable-arm-iwmmxt --disable-arm-iwmmxt2 \
%endif
  --disable-static

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libpixman-1*.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/pixman-1
%{_includedir}/pixman-1/pixman.h
%{_includedir}/pixman-1/pixman-version.h
%{_libdir}/libpixman-1*.so
%{_libdir}/pkgconfig/pixman-1.pc

%changelog
* Thu Feb 11 2016 Oded Gabbay <ogabbay@redhat.com> - 0.34.0-1
- pixman 0.34.0

* Thu Jul 02 2015 Oded Gabbay <ogabbay@redhat.com> - 0.32.6-3
- Re-enable VMX fast paths on ppc64le and apply patches that fix them

* Mon May 11 2015 Adam Jackson <ajax@redhat.com> 0.32.6-2
- Fix devel's requirement on the base package to include %%{?isa}

* Tue Mar 17 2015 Adam Jackson <ajax@redhat.com> 0.32.6-1
- pixman 0.32.6

* Fri Nov 07 2014 Adam Jackson <ajax@redhat.com> 0.32.4-4
- Disable (broken) VMX fast paths on ppc64le for now

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.32.4-3
- Mass rebuild 2014-01-24

* Mon Jan 6 2014 Soren Sandmann <ssp@redhat.com> 0.32.4-2
- changelog fixes

* Mon Jan 6 2014 Soren Sandmann <ssp@redhat.com> 0.32.4-1
- pixman 0.32.4, bug 1043746

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.30.0-2
- Mass rebuild 2013-12-27

* Wed May 8 2013 Soren Sandmann <ssp@redhat.com> 0.30.0-1
- pixman 0.30.0

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.28.0-3
- Disable iwmmxt on ARM as it's broken b.fd.o # 55519

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 7 2012 Soren Sandmann <ssp@redhat.com> 0.28.0-1
- pixman 0.28.0

* Thu Oct 25 2012 Soren Sandmann <ssp@redhat.com> 0.27.4-1
- pixman 0.27.4

* Fri Aug 10 2012 Soren Sandmann <ssp@redhat.com> 0.27.2-1
- pixman 0.27.2

* Tue Jul 31 2012 Soren Sandmann <ssp@redhat.com> 0.26.2-5
- Remove openmp patch

* Mon Jul 30 2012 Adam Jackson <ajax@redhat.com> 0.26.2-4
- Disable openmp patch in RHEL for the moment

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.26.2-2
- run autoreconf to properly pull in gomp

* Thu Jul  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.26.2-1
- update to 0.26.2
- drop upstreamed patch

* Tue Jun 26 2012 Soren Sandmann <ssp@redhat.com> - 0.26.0-4
- Add -fopenmp to CFLAGS and LDFLAGS on the make command line instead
  of in Makefile.am.

* Tue Jun 26 2012 Soren Sandmann <ssp@redhat.com> - 0.26.0-3
- Add -fopenmp to pixman-sse2.c CFLAGS

* Tue Jun 26 2012 Soren Sandmann <ssp@redhat.com> - 0.26.0-2
- Add experimental patch to use OpenMP
  If this causes your X server to misbehave, please file bugs.

* Wed May 30 2012 Soren Sandmann <ssp@redhat.com> - 0.26.0-1
- update to 0.26.0
- patch to add missing emms instructions
- reenable iwmmxt since configure should now detect if it can't built

* Tue May 15 2012 Dennis Gilmore <dennis@ausil.us> - 0.25.6-2
- rely on runtime cpu detection for arm optimisations
- disable failing to build iwmmxt

* Tue May 15 2012 Soren Sandmann <ssp@redhat.com>
- pixman 0.25.6

* Thu Mar 29 2012 Dennis Gilmore <dennis@ausil.us> 0.25.2-2
- always disable iwmmxt  and disable neon and simd unless building armv7hnl

* Mon Mar 26 2012 Soren Sandmann <ssp@redhat.com> 0.25.2-1
- pixman 0.25.2

* Thu Mar 15 2012 Adam Jackson <ajax@redhat.com> 0.24.4-1
- pixman 0.24.4

* Thu Jan 19 2012 Soren Sandmann <ssp@redhat.com> 0.24.2-1
- pixman 0.24.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 7 2011 Soren Sandmann <ssp@redhat.com> 0.24.0-1
- pixman 0.24.0

* Tue Oct 11 2011 Soren Sandmann <ssp@redhat.com> 0.23.6-1
- pixman 0.23.6

* Thu Oct 06 2011 Soren Sandmann <ssp@redhat.com> 0.23.4-1
- pixman 0.23.4

* Tue Jul 05 2011 Adam Jackson <ajax@redhat.com> 0.22.2-1
- pixman 0.22.2

* Tue May 3 2011 Soren Sandmann <ssp@redhat.com> - 0.22.0-1
  pixman 0.22.0

* Wed Apr 20 2011 Soren Sandmann <ssp@redhat.com> - 0.21.8-1
  pixman 0.21.8

* Thu Feb 24 2011 Soren sandmann <ssp@redhat.com> - 0.21.6-1
- pixman 0.21.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Soren Sandmann <ssp@redhat.com> - 0.20.2-1
- pixman 0.20.2

* Wed Oct 27 2010 Soren Sandmann <ssp@redhat.com> - 0.20.0-1
- pixman 0.20.0

* Mon Oct 25 2010 Matthias Clasen <mclasen@redhat.com> - 0.19.6-1
- Update to 0.19.6

* Mon Sep 6 2010 Soren Sandmann <ssp@redhat.com> - 0.19.2-1
- pixman 0.19.2

* Thu Apr 1 2010 Soren Sandmann <ssp@redhat.com> - 0.18.0-1
- pixman 0.18.0

* Wed Mar 17 2010 Soren Sandmann <ssp@redhat.com> - 0.17.12-1
- pixman 0.17.12

* Fri Mar 5 2010 Soren Sandmann <ssp@redhat.com> - 0.17.10-1
- pixman 0.17.10

* Thu Feb 25 2010 Soren Sandmann <ssp@redhat.com> - 0.17.8-1
- pixman 0.17.8

* Mon Jan 18 2010 Soren Sandmann <ssp@redhat.com> - 0.17.6-1
- pixman 0.17.6

* Mon Jan 18 2010 Soren Sandmann <ssp@redhat.com> - 0.17.4-1
- pixman 0.17.4

* Wed Dec 2 2009 Soren Sandmann <ssp@redhat.com> - 0.17.2-1
- pixman 0.17.2

* Mon Sep 28 2009 Soren Sandmann <ssp@redhat.com> - 0.16.2-1
- pixman 0.16.2

* Fri Aug 28 2009 Soren Sandmann <ssp@redhat.com> - 0.16.0-1
- pixman 0.16.0

* Tue Aug 11 2009 Soren Sandmann <ssp@redhat.com> - 0.15.20-1
- pixman 0.15.20

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.15.18-3
- Use bzipped upstream tarball.
- Fix URL.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Soren Sandmann <ssp@redhat.com> 0.15.18-1
- pixman 0.15.18

* Mon Jul 13 2009 Soren Sandmann <ssp@redhat.com> 0.15.16-1
- pixman 0.15.16

* Wed Jun 24 2009 Soren Sandmann <ssp@redhat.com> 0.15.14-1
- pixman 0.15.14

* Wed Jun 17 2009 Soren Sandmann <ssp@redhat.com> 0.15.12-1
- pixman 0.15.12

* Fri Jun 5 2009 Soren Sandmann <ssp@redhat.com> 0.15.10-1
- pixman 0.15.10

* Sat May 30 2009 Soren Sandmann <ssp@redhat.com> 0.15.8-1
- pixman 0.15.8

* Fri May 22 2009 Soren Sandmann <ssp@redhat.com> 0.15.6-2
- pixman 0.15.6

* Fri May 15 2009 Soren Sandmann <ssp@redhat.com> 0.15.4-1
- pixman 0.15.4

* Wed May 13 2009 Soren Sandmann <ssp@redhat.com> 0.15.2-3
- Remove patch to implement new clipping rules as it was completely broken.

* Tue May 12 2009 Soren Sandmann <ssp@redhat.com> 0.15.2-2
- Add patch to implement new clipping rules.

* Thu Apr 16 2009 Soren Sandmann <ssp@redhat.com> 0.15.2-1
- pixman 0.15.2

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 7 2009 Soren Sandmann <sandmann@redhat.com> 0.14.0-1
- pixman 0.14.0

* Tue Dec 16 2008 Adam Jackson <ajax@redhat.com> 0.13.2-1
- pixman 0.13.2

* Sun Dec 14 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 0.12.0-3
- Rebuild for pkgconfig provides

* Tue Nov 18 2008 Dan Williams <dcbw@redhat.com> 0.12.0-2
- Actually build with the altivec detection fix (rh #472000, #451831)

* Wed Sep 17 2008 Soren Sandmann <sandmann@redhat.com> 0.12.0-1
- Upgrade to 0.12.0. Drop stripes patch.

* Wed Sep 10 2008 Soren Sandmann <sandmann@redhat.com> 0.11.10-2
- Add patch to fix stripes in the Nautilus selection retangle.

* Sat Sep 6 2008 Soren Sandmann <sandmann@redhat.com> 0.11.10-1
- Upgrade to 0.11.10. Drop altivec patch.

* Thu Jul 17 2008 Soren Sandmann <sandmann@redhat.com> 0.11.8-1
- Upgrade to 0.11.8. Drop altivec patch.

* Wed Jun 25 2008 Soren Sandmann <sandmann@redhat.com> 0.11.6-1
- Upgrade to 0.11.6. Drop fix for leak.

* Tue Jun 17 2008 David Woodhouse <dwmw2@infradead.org> 0.11.4-3
- Fix Altivec detection breakage (#451831)

* Fri Jun 13 2008 Soren Sandmann <sandmann@redhat.com> 0.11.4-2
- Plug bad leak (cherrypicked from master)

* Mon Jun  9 2008 Soren Sandmann <sandmann@redhat.com> 0.11.4-1
- Update to 0.11.4

* Mon Jun  9 2008 Soren Sandmann <sandmann@redhat.com> 0.11.2-1
- Update to 0.11.2

* Thu Apr  3 2008 Soren Sandmann <sandmann@redhat.com> 0.10.0-1
- Update to 0.10.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.6-4
- Autorebuild for GCC 4.3

* Wed Oct 31 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.9.6-3
- Third time's the charm.

* Wed Oct 31 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.9.6-2
- Second try.

* Wed Oct 31 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.9.6-1
- Update to 0.9.6 release.

* Wed Sep 05 2007 Adam Jackson <ajax@redhat.com> 0.9.5-1
- Update to 0.9.5 release.

* Mon Aug 27 2007 Adam Jackson <ajax@redhat.com> 0.9.0-7.20070827
- New snapshot

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> 0.9.0-4.20070824
- New snapshot

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 0.9.0-3.20070724
- rebuild for toolchain bug

* Tue Jul 24 2007 Adam Jackson <ajax@redhat.com> 0.9.0-2.20070724
- Re-add it, %%dir is not the same as adding a dir whole.

* Tue Jul 24 2007 Adam Jackson <ajax@redhat.com> 0.9.0-1.20070724
- Remove redundant header from %%files devel.

* Fri May 18 2007 Adam Jackson <ajax@redhat.com> 0.9.0-0.20070724
- git build so I can build git X.
