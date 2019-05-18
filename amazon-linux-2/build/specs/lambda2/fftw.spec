Name:           fftw
Version:        3.3.3
Release: 8%{?dist}.0.2
Summary:        A Fast Fourier Transform library
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.fftw.org
Source0:        http://www.fftw.org/fftw-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# OpenMP support not available on RHEL 4
%if 0%{?rhel} == 4
BuildRequires:  gcc-g77
%global openmp 0
%else
BuildRequires:  gcc-gfortran
%global openmp 1
%endif

%global quad 0
# Quad precision support only available with gcc >= 4.6
%if 0%{?fedora} >= 15
# and only on these arches
%ifarch %{ix86} x86_64 ia64
%global quad 1
%endif
%endif

# For check phase
BuildRequires:  time
BuildRequires:  perl

Prefix: %{_prefix}


%description
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

%package libs
Summary:        FFTW run-time library
Group:          System Environment/Libraries
Provides:       fftw3 = %{version}-%{release}
Obsoletes:      fftw3 < 3.3
# Libs branched from rpm containing binaries in version 3.3
Obsoletes:      fftw < 3.3
# Libs rearranged in 3.3.1-2
Obsoletes:	fftw-libs-threads < %{version}-%{release}
Obsoletes:	fftw-libs-openmp < %{version}-%{release}

# Pull in the actual libraries
Requires:	 %{name}-libs-single%{?_isa} = %{version}-%{release}
Requires:	 %{name}-libs-double%{?_isa} = %{version}-%{release}
Requires:	 %{name}-libs-long%{?_isa} = %{version}-%{release}
%if %{quad}
Requires:	 %{name}-libs-quad%{?_isa} = %{version}-%{release}
%endif

Prefix: %{_prefix}

%description libs
This is a dummy package package, pulling in the individual FFTW
run-time libraries.


%package libs-double
Summary:        FFTW library, double precision
Group:          Development/Libraries
Prefix: %{_prefix}

%description libs-double
This package contains the FFTW library compiled in double precision.

%package libs-single
Summary:        FFTW library, single precision
Group:          Development/Libraries
Prefix: %{_prefix}

%description libs-single
This package contains the FFTW library compiled in single precision.

%package libs-long
Summary:        FFTW library, long double precision 
Group:          Development/Libraries
Prefix: %{_prefix}

%description libs-long
This package contains the FFTW library compiled in long double
precision.

%if %{quad}
%package libs-quad
Summary:        FFTW library, quadruple
Group:          Development/Libraries
Prefix: %{_prefix}

%description libs-quad
This package contains the FFTW library compiled in quadruple
precision.
%endif

%prep
%setup -q

%build
%if 0%{?rhel} == 4
# System fortran compiler is g77
export F77=g77
%else
# Configure uses g77 by default, if present on system
export F77=gfortran
%endif

BASEFLAGS="--enable-shared --disable-dependency-tracking --enable-threads"

%if %{openmp}
BASEFLAGS+=" --enable-openmp"
%endif

# Precisions to build
prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad

# Corresponding flags
prec_flags[0]=--enable-single
prec_flags[1]=--enable-double
prec_flags[2]=--enable-long-double
prec_flags[3]=--enable-quad-precision

%ifarch %{ix86} x86_64
# Enable SSE2 support for x86 and x86_64
# (no avx as it is claimed to drastically slower)
for((i=0;i<2;i++)); do
 prec_flags[i]+=" --enable-sse2"
done
%endif

%ifarch arm
# Compile support for NEON instructions
for((i=0;i<2;i++)); do
 prec_flags[i]+=" --enable-neon"
done
%endif

#%ifarch ppc ppc64
## Compile support for Altivec instructions
#for((i=0;i<2;i++)); do
 #prec_flags[i]+=" --enable-altivec"
#done
#%endif

# Loop over precisions
%if %{quad}
for((iprec=0;iprec<4;iprec++))
%else
for((iprec=0;iprec<3;iprec++))
%endif
do
 mkdir ${prec_name[iprec]}${ver_name[iver]}
 cd ${prec_name[iprec]}${ver_name[iver]}
 ln -s ../configure .
 %{configure} ${BASEFLAGS} ${prec_flags[iprec]} --disable-static
 sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
 sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
 make %{?_smp_mflags}
 cd ..
done

%install
%if %{quad}
for ver in single double long quad
%else
for ver in single double long
%endif
do
 make -C $ver install DESTDIR=%{buildroot}
done

%files
%defattr(-,root,root,-)
%{_bindir}/fftw*-wisdom*

%files libs
%defattr(-,root,root,-)

%files libs-single
%defattr(-,root,root,-)
%license COPYING COPYRIGHT
%{_libdir}/libfftw3f.so.*
%{_libdir}/libfftw3f_threads.so.*
%if %{openmp}
%{_libdir}/libfftw3f_omp.so.*
%endif

%files libs-double
%defattr(-,root,root,-)
%license COPYING COPYRIGHT
%{_libdir}/libfftw3.so.*
%{_libdir}/libfftw3_threads.so.*
%if %{openmp}
%{_libdir}/libfftw3_omp.so.*
%endif

%files libs-long
%defattr(-,root,root,-)
%license COPYING COPYRIGHT
%{_libdir}/libfftw3l.so.*
%{_libdir}/libfftw3l_threads.so.*
%if %{openmp}
%{_libdir}/libfftw3l_omp.so.*
%endif

%if %{quad}
%files libs-quad
%defattr(-,root,root,-)
%license COPYING COPYRIGHT
%{_libdir}/libfftw3q.so.*
%{_libdir}/libfftw3q_threads.so.*
%if %{openmp}
%{_libdir}/libfftw3q_omp.so.*
%endif
%endif

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_infodir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.3.3-8
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.3.3-7
- Mass rebuild 2013-12-27

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 PPC Secondary Arch Admin <karsten@redhat.com> 3.3.3-5
- disable altivec flag again, that works with single precision only

* Mon Dec 24 2012 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-4
- Fix typo: should be %%ix86 instead of %%x86. Now should have SSE2 support
  on x86 as well.

* Tue Dec 18 2012 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-3
- After consultation with upstream, enable SSE2 also on x86, altivec on ppc
  and ppc64 and NEON on arm.

* Tue Dec 18 2012 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-2
- Enable SSE2 on x86_64.

* Mon Nov 26 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-1
- Update to 3.3.3.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Orion Poplawski <orion@cora.nwra.com> - 3.3.2-1
- Update to 3.3.2
- Drop alignment patch

* Fri Apr 27 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.1-3
- Fix FTBFS with gcc 4.7.

* Thu Apr 26 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.1-2
- Reorganized libraries (BZ #812981).

* Mon Feb 27 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Dan Horák <dan[at]danny.cz> - 3.3-4
- libquadmath exists only on x86/x86_64 and ia64

* Mon Oct 10 2011 Rex Dieter <rdieter@fedoraproject.org> 3.3-3
- -devel: Provides: fftw3-devel (#744758)
- -static: Provides: fftw3-static
- drop %%_isa from Obsoletes

* Sat Jul 30 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3-2
- Conditionalize OpenMP and quadruple precision support based on capabilities
  of system compiler.

* Thu Jul 28 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3-1
- Update to 3.3.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 9 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-4
- Get rid of rpath.

* Sat Jan 9 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-3
- Branch out developers' manual to -doc.

* Sat Jan 2 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-2
- Add check phase.
- Cosmetic changes to spec file (unified changelog format, removed unnecessary
  space).
- Use rm instead of find -delete, as latter is not present on EPEL-4.
- Generalize obsoletes of fftw3 packages. Add Obsoletes: fftw3-static.

* Fri Jan 1 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-1
- Update to 3.2.2.
- Make file listings more explicit.
- Don't use file dependencies for info.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Conrad Meyer <konrad@tylerc.org> - 3.2.1-1
- Bump to 3.2.1.

* Thu Dec 4 2008 Conrad Meyer <konrad@tylerc.org> - 3.2-1
- Bump to 3.2.

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1.2-7
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1.2-6
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 Quentin Spencer <qspencer@users.sf.net> 3.1.2-5
- Rebuild for F8.

* Fri Jul 27 2007 Quentin Spencer <qspencer@users.sf.net> 3.1.2-4
- Split static libs into separate package (bug 249686).

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 3.1.2-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.2-2
- BuildRequires: pkgconfig for -devel (bug 206444).

* Fri Sep  8 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.2-1
- New release.

* Fri Jun  2 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.1-1
- New upstream release.

* Fri Feb 24 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-4
- Re-enable static libs (bug 181897).
- Build long-double version of libraries (bug 182587).

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-3
- Add Obsoletes and Provides.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-2
- Rebuild for Fedora Extras 5.
- Disable static libs.
- Remove obsolete configure options.

* Wed Feb  1 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-1
- Upgrade to the 3.x branch, incorporating changes from the fftw3 spec file.
- Add dist tag.

* Mon May 23 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.1.5-8
- BuildReq gcc-gfortran (#156490).

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.1.5-7
- rebuild on all arches
- buildrequire compat-gcc-32-g77

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 2.1.5-5
- Bump release to provide Extras upgrade path.

* Tue Apr 06 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.4
- BuildReq gcc-g77.

* Mon Sep 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.3
- Dropped post/preun scripts for info.

* Wed Sep 17 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.2
- Remove aesthetic comments.
- buildroot -> RPM_BUILD_ROOT.
- post/preun for info files.

* Mon Apr 07 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.1
- Updated to 2.1.5.

* Tue Apr 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.4-0.fdr.2
- Added Epoch:0.
- Added ldconfig to post and postun.

* Sun Mar 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 2.1.4-0.fdr.1
- Updated to 2.1.4.

* Fri Mar 14 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 2.1.3-0.fdr.1
- Fedorafied.

* Mon Oct 21 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.
