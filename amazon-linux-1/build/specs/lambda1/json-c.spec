%define _buildid .8

%global reldate 20130402

Name:		json-c
Version:	0.11
Release: 6%{?_buildid}%{?dist}
Summary:	A JSON implementation in C
Group:		Development/Libraries
License:	MIT
URL:		https://github.com/json-c/json-c/wiki
Source0:	https://github.com/json-c/json-c/archive/json-c-%{version}-%{reldate}.tar.gz

# increaser parser strictness (for php compatibility)
Patch0:		https://github.com/json-c/json-c/pull/90.patch
Patch1:		https://github.com/json-c/json-c/pull/94.patch

# Disable default compiler warning flags
Patch2:		json-c-0.11-cflags.patch

# Fix CVE issues CVE-2013-6370 and CVE-2013-6371, patch backported from upstream
Patch3:		json-c-0.11-cve.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	libtool autoconf

%description
JSON-C implements a reference counting object model that allows you to easily
construct JSON objects in C, output them as JSON formatted strings and parse
JSON formatted strings back into the C representation of JSON objects.

%package devel
Summary:	Development headers and library for json-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the development headers and library for json-c.


%package doc
Summary:	Reference manual for json-c
Group:		Documentation
%if 0%{?fedora} > 10 || 0%{?rhel}>5 || 0%{?amzn}
BuildArch:	noarch
%endif

%description doc
This package contains the reference manual for json-c.

%prep
%setup -q -n json-c-json-c-%{version}-%{reldate}

%patch0 -p1 -b .strict90
%patch1 -p1 -b .strict94
%patch2 -p1 -b .cflags
%patch3 -p1 -b .cve

# regenerate auto stuff to avoid rpath issue and cve stuff
autoreconf -fi

for doc in ChangeLog; do
 iconv -f iso-8859-1 -t utf8 $doc > $doc.new &&
 touch -r $doc $doc.new &&
 mv $doc.new $doc
done


%build
%configure --enable-shared --disable-static --disable-rpath --enable-rdrand
# parallel build is broken for now, make %{?_smp_mflags}
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Get rid of la files
rm -rf %{buildroot}%{_libdir}/*.la

# yum cannot replace a dir by a link
# so switch the dir names
rm %{buildroot}%{_includedir}/json
mv %{buildroot}%{_includedir}/json-c \
   %{buildroot}%{_includedir}/json
ln -s json \
   %{buildroot}%{_includedir}/json-c

%check
make check

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README README.html
%{_libdir}/libjson.so.*
%{_libdir}/libjson-c.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/json
%{_includedir}/json-c
%{_libdir}/libjson.so
%{_libdir}/libjson-c.so
%{_libdir}/pkgconfig/json.pc
%{_libdir}/pkgconfig/json-c.pc

%files doc
%defattr(-,root,root,-)
%doc doc/html/*


%changelog
* Wed Sep 17 2014 Tom Kirchner <tjk@amazon.com>
- import source package F20/json-c-0.11-6.fc20

* Wed Apr 09 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.11-7
- Address CVE-2013-6371 and CVE-2013-6370 (BZ #1085676 and #1085677).
- Enabled rdrand support.

* Mon Feb 10 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.11-6
- Bump spec.

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.11-5
- Run test suite during build.
- Drop empty NEWS from docs.

* Tue Nov 5 2013 Heath Petty <hpetty@amazon.com>
- Made the dev package noarch

* Wed Oct 2 2013 Heath Petty <hpetty@amazon.com>
- import source package EPEL/json-c-0.11-4.el6

* Tue Sep 10 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.11-4
- Remove default warning flags so that package builds on EPEL as well.

* Sat Aug 24 2013 Remi Collet <remi@fedoraproject.org> - 0.11-3
- increase parser strictness for php

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Remi Collet <remi@fedoraproject.org> - 0.11-1
- update to 0.11
- fix source0
- enable both json and json-c libraries

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Cristian Gafton <gafton@amazon.com>
- import source package EPEL6/json-c-0.10-2.el6

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

* Wed Jul 20 2011 Cristian Gafton <gafton@amazon.com>
- import source package EPEL6/json-c-0.9-1.el6

* Tue Jul 19 2011 Cristian Gafton <gafton@amazon.com>
- setup complete for package json-c

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 06 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.9-1
- First release.
