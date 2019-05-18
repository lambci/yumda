Name:           jemalloc
Version:        3.6.0

Release:        1%{?dist}
Summary:        General-purpose scalable concurrent malloc implementation

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.canonware.com/jemalloc/
Source0:        http://www.canonware.com/download/jemalloc/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Remove pprof, as it already exists in google-perftools
Patch0:         jemalloc-3.5.1.no_pprof.patch
# ARMv5tel has no atomic operations
Patch2:         jemalloc-armv5-force-atomic.patch
# RHEL5/POWER has no atomic operations
Patch3:         jemalloc-3.0.0.atomic_h_ppc_32bit_operations.patch
BuildRequires:  /usr/bin/xsltproc

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of %{name}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0

%patch2 -p1 -b .armv5tel
%ifarch ppc ppc64
%if 0%{?rhel} == 5
%patch3 -b .ppc
%endif
%endif

%build
%configure
make %{?_smp_mflags}


%check
make check


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Install this with doc macro instead
rm %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html

# None of these in fedora
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_libdir}/libjemalloc.so.*
%{_bindir}/jemalloc.sh
%doc COPYING README VERSION
%doc doc/jemalloc.html
%ifarch ppc ppc64
%if 0%{?rhel} == 5
%doc COPYING.epel5-ppc
%endif
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/jemalloc
%{_libdir}/libjemalloc.so
%{_mandir}/man3/jemalloc.3*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Mon Mar 31 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.6.0-1
- New upstream release. This release fixes a critical regression 

* Fri Mar 28 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.5.1-1
- New upstream release
- Updated nopprof patch to match new release
- Fixed a few bogus changelog entries

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.4.0-1
- New upstream release

* Mon Mar 11 2013 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.3.1-1
- New upstream release
- Dropped s390 patch, it's in upstream now.

* Fri Jan 25 2013 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.3.0-1
- New upstream release
 
* Mon Nov 19 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.2.0-1
- New upstream release
 
* Tue Oct 23 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.1.0-1
- New upstream release
- Removed ptmalloc_lock_all patch, it is merged upstream

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.0.0-2
- Added a patch from upstream, fixing a crash in ptmalloc_lock_all,
  closing #824646

* Mon May 14 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.0.0-1
- New upstream release
- Updated no_pprof patch to match new release
- Updated s390 patch to match new relase
- Added make check
- Added new script jemalloc.sh
- Added a patch for atomic operations on epel5/ppc

* Sat Apr 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.2.5-5
- Improve ARM patch

* Fri Apr 20 2012 Dennis Gilmore <dennis@ausil.us> - 2.2.5-4
- no attomics on armv5tel

* Wed Feb 08 2012 Dan Horák <dan[at]danny.cz> - 2.2.5-3
- substitute version information in the header (#788517)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 06 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.5-1
- New upstream release, closes #75618

* Sun Nov 06 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.4-1
- New upstream release

* Thu Oct 13 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.3-1
- New upstream release, closes #735057

* Mon Aug 01 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.2-1
- New upstream release, closes #727103
- Updated no_pprof patch for 2.2.2

* Thu Mar 31 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.1-1
- New upstream release

* Sun Mar 27 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.0-1
- New upstream release
- Updated no_pprof patch for 2.2.0

* Tue Mar 15 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.3-2
- New upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.1-1
- New upstream release

* Wed Jan 05 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.0-1
- New upstream release
- Updated patch to remove pprof
- Added html doc and xsltproc as a requirement to build it

* Sat Dec 11 2010 Dan Horák <dan[at]danny.cz> - 2.0.1-3
- fix build on s390

* Thu Nov 18 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.0.1-2
- Added a patch that removes pprof, as it already exists in the
  google-perftools package
- Cosmetic fixes as requested in the package review (rhbz#653682)

* Mon Nov 15 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.0.1-1
- First cut of an rpm distribution of jemalloc
