Name: libunistring
Version: 0.9.3
Release: 9%{?dist}.0.2
Group: System Environment/Libraries
Summary: GNU Unicode string library
License: LGPLv3+
Url: http://www.gnu.org/software/libunistring/
Source0: http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: bundled(gnulib)

Prefix: %{_prefix}

%description
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).

%prep
%setup -q

%build
%configure --disable-static --disable-rpath
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%defattr(-,root,root,-)
%license COPYING COPYING.LIB
%{_libdir}/%{name}.so.*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.9.3-9
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.3-8
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Akira TAGOH <tagoh@redhat.com> - 0.9.3-5
- Fix a typo in %%preun. (#737638)

* Tue May 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.9.3-4
- Add bundled(gnulib) provides

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun May 23 2010 Pádraig Brady <P@draigBrady.com> 0.9.3-1
- Update to 0.9.3
* Thu Nov 19 2009 Pádraig Brady <P@draigBrady.com> 0.9.1-3
- Remove glibc-devel and texinfo build deps
* Thu Nov 19 2009 Pádraig Brady <P@draigBrady.com> 0.9.1-2
- Changes as per initial review by panemade@gmail.com
* Tue Nov 17 2009 Pádraig Brady <P@draigBrady.com> 0.9.1-1
- Initial version

