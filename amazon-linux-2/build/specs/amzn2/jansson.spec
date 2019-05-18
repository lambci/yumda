Name:		jansson
Version:	2.10
Release: 1%{?dist}.0.2
Summary:	C library for encoding, decoding and manipulating JSON data

Group:		System Environment/Libraries
License:	MIT
URL:		http://www.digip.org/jansson/
Source0:	http://www.digip.org/jansson/releases/jansson-%{version}.tar.bz2

BuildRequires:	python-sphinx

%description
Small library for parsing and writing JSON documents.

%package devel
Summary: Header files for jansson
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for developing applications making use of jansson.

%package devel-doc
Summary: Development documentation for jansson
BuildArch: noarch

%description devel-doc
Development documentation for jansson.

%prep
%setup -q

%if 0%{?rhel} == 6
%{__sed} -i 's/code-block:: shell/code-block:: none/g' doc/*.rst
%endif

%build
%configure --disable-static
make %{?_smp_mflags}
make html

%check
make check

%install
make install INSTALL="install -p" DESTDIR="$RPM_BUILD_ROOT"
rm "$RPM_BUILD_ROOT%{_libdir}"/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE CHANGES
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*

%files devel-doc
%doc doc/_build/html/*

%changelog
* Fri Mar 10 2017 Nathaniel McCallum <npmccallum@redhat.com> - 2.10-1
- Update to 2.10 [1389805]
- Merge spec file with Fedora

* Fri Mar 14 2014 Jiri Pirko <jpirko@redhat.com> 2.4-6
- Fix multilib conflicts by creating devel-doc package [1076415]

* Thu Feb 13 2014 Jiri Pirko <jpirko@redhat.com> 2.4-5
- Change hash function, randomize hashes [1063831]

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.4-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.4-3
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jiri Pirko <jpirko@redhat.com> 2.4-1
- Update to Jansson 2.4.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Jiri Pirko <jpirko@redhat.com> 2.3-1
- Update to Jansson 2.3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 11 2011 Sean Middleditch <sean@middleditch.us> 2.1-1
- Update to Jansson 2.1.
- Drop Sphinx patch, no longer necessary.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 03 2010 Sean Middleditch <sean@middleditch.us> 1.3-1
- Update to Jansson 1.3.
- Disable warnings-as-errors for Sphinx documentation.

* Thu Jan 21 2010 Sean Middleditch <sean@middleditch.us> 1.2-1
- Update to Jansson 1.2.

* Thu Jan 11 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-4
- Update jansson description per upstream's suggestions.
- Removed README from docs.

* Thu Jan 09 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-3
- Correct misspelling of jansson in the pkg-config file.

* Thu Jan 09 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-2
- Fix Changelog dates.
- Mix autoheader warning.
- Added make check.
- Build and install HTML documentation in -devel package.

* Thu Jan 07 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-1
- Initial packaging for Fedora.
