Summary: A C library for multiple-precision floating-point computations
Name: mpfr
Version: 3.1.1
Release: 4%{?dist}.0.2
URL: http://www.mpfr.org/
Source0: http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.xz
# GFDL  (mpfr.texi, mpfr.info and fdl.texi)
License: LGPLv3+ and GPLv3+ and GFDL
Group: System Environment/Libraries
BuildRequires: autoconf libtool gmp-devel
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: gmp >= 4.2.1

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package devel
Summary: Development tools A C library for mpfr library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: gmp-devel

%description devel
Header files and documentation for using the MPFR 
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package.  You'll also need to
install the mpfr package.

%prep
%setup -q

%build
%configure --disable-assert
make %{?_smp_mflags}

%install
iconv  -f iso-8859-1 -t utf-8 doc/mpfr.info > doc/mpfr.info.aux
mv doc/mpfr.info.aux doc/mpfr.info
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libmpfr.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/libmpfr.a
cd ..
mkdir $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT/%{_docdir}/%{name}/ $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/mpfr.info.gz ]; then
    /sbin/install-info %{_infodir}/mpfr.info.gz %{_infodir}/dir || :
fi

%preun devel
if [ "$1" = 0 ]; then
    if [ -f %{_infodir}/mpfr.info.gz ]; then
	/sbin/install-info --delete %{_infodir}/mpfr.info.gz %{_infodir}/dir || :
    fi
fi

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LESSER NEWS README
%{_libdir}/libmpfr.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmpfr.so
%{_includedir}/*.h
%{_infodir}/mpfr.info*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.1.1-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.1.1-3
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 26 2012 Peter Schiffer <pschiffe@redhat.com> - 3.1.1-1
- resolves: #837563
  update to 3.1.1

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Peter Schiffer <pschiffe@redhat.com> - 3.1.0-1
- resolves: #743237
  update to 3.1.0
- removed compatibility symlinks and provides

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.0.0-4.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 3.0.0-4.1
- rebuild with new gmp

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec  7 2010 Dan Horák <dan[at]danny.cz> 3.0.0-3
- update the compat Provides for non-x86 arches

* Wed Dec  1 2010 Ivana Hutarova Varekova <varekova@redhat.com> 3.0.0-2
- fix -devel description (see 603021#c3)

* Tue Nov 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> 3.0.0-1
- update to 3.0.0
- created links and provides to .1

* Fri Dec 18 2009 Ivana Hutarova Varekova <varekova@redhat.com> 2.4.2-1
- update to 2.4.2

* Fri Nov 13 2009 Ivana Varekova <varekova@redhat.com> 2.4.1-5
- fix 537328 - mpfr-devel should "Requires: gmp-devel"

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.4.1-4
- Use lzma compressed upstream tarball.

* Mon Aug 10 2009 Ivana Varekova <varekova redhat com> 2.4.1-3
- fix installation with --excludedocs option (#515958)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 11 2009 Ivana Varekova <varekova@redhat.com> - 2.4.1-1
- update to 2.4.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Ivana Varekova <varekova@redhat.com> - 2.4.0-1
- update to 2.4.0

* Wed Oct 15 2008 Ivana Varekova <varekova@redhat.com> - 2.3.2-1
- update to 2.3.2

* Mon Jul 21 2008 Ivana Varekova <varekova@redhat.com> - 2.3.1-1
- update to 2.3.1

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.0-3
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Ivana Varekova <varekova@redhat.com> 2.3.0-2
- rebuilt

* Thu Sep 20 2007 Ivana Varekova <varekova@redhat.com> 2.3.0-1
- update to 2.3.0
- fix license flag

* Mon Aug 20 2007 Ivana Varekova <varekova@redhat.com> 2.2.1-2
- spec file cleanup (#253440)

* Mon Jan 16 2007 Ivana Varekova <varekova@redhat.com> 2.2.1-1
- started

