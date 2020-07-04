%define _trivial .0
%define _buildid .4
%global reldate 20130402

Name:		json-c
Version:	0.11
Release:	4%{?dist}%{?_trivial}%{?_buildid}
Summary:	A JSON implementation in C
Group:		Development/Libraries
License:	MIT
URL:		https://github.com/json-c/json-c/wiki
Source0:	https://github.com/json-c/json-c/archive/json-c-%{version}-%{reldate}.tar.gz

Patch0:		json-c-CVE-2013-6371.patch

#amazon patches
Patch500: json-c-fallthrough.diff
Patch1002: Fix-CVE-2020-12762.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: libtool

Prefix: %{_prefix}

%description
JSON-C implements a reference counting object model that allows you to easily
construct JSON objects in C, output them as JSON formatted strings and parse
JSON formatted strings back into the C representation of JSON objects.

%prep
%setup -q -n json-c-json-c-%{version}-%{reldate}

%patch0 -p1 -b .cve20136371
%patch500 -p1 -b .fallthrough
%patch1002 -p1

# regenerate auto stuff to avoid rpath issue
autoreconf -fi


%build
%configure \
  --enable-shared \
  --disable-static \
  --disable-rpath \
  --enable-rdrand
# parallel build is broken for now, make %{?_smp_mflags}
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Get rid of la files
rm -rf %{buildroot}%{_libdir}/*.la


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libjson.so.*
%{_libdir}/libjson-c.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig


%changelog
* Sat Jul 4 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Jun 16 2020 Jeremiah Mahler <jmmahler@amazon.com> - 0.11-4.amzn2.0.4
- fix for CVE-2020-12762

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 0.11-4
- fix has collision CVE-2013-6371
- fix buffer overflow CVE-2013-6370
- enable upstream test suite

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.11-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.11-2
- Mass rebuild 2013-12-27

* Mon Apr 29 2013 Remi Collet <remi@fedoraproject.org> - 0.11-1
- update to 0.11
- fix source0
- enable both json and json-c libraries

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 24 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.10-2
- Compile and install json_object_iterator using Remi Collet's fix (BZ #879771).

* Sat Nov 24 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.10-1
- Update to 0.10 (BZ #879771).

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Jiri Pirko <jpirko@redhat.com> - 0.9-4
- add json_tokener_parse_verbose, and return NULL on parser errors

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 06 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.9-1
- First release.
