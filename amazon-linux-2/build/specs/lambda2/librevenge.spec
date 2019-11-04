%global apiversion 0.0

Name: librevenge
Version: 0.0.2
Release: 2%{?dist}.0.2
Summary: A base library for writing document import filters

# src/lib/RVNGOLEStream.{h,cpp} are BSD
License: (LGPLv2+ or MPLv2.0) and BSD
URL: http://sourceforge.net/p/libwpd/wiki/librevenge/
Source: http://downloads.sourceforge.net/libwpd/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(zlib)

Patch0: 0001-rhbz-1248443-unbounded-heap-allocation.patch

Prefix: %{_prefix}

%description
%{name} is a base library for writing document import filters. It has
interfaces for text documents, vector graphics, spreadsheets and
presentations.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --disable-werror --enable-pretty-printers
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

%files
%license COPYING.*
%{_libdir}/%{name}-%{apiversion}.so.*
%{_libdir}/%{name}-generators-%{apiversion}.so.*
%{_libdir}/%{name}-stream-%{apiversion}.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}
%exclude /usr/share/gdb/auto-load

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Aug 05 2015 David Tardon <dtardon@redhat.com> - 0.0.2-2
- Resolves: rhbz#1248443 unbounded heap allocation

* Wed Dec 24 2014 David Tardon <dtardon@redhat.com> - 0.0.2-1
- new upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 David Tardon <dtardon@redhat.com> - 0.0.1-1
- new upstream release

* Tue May 27 2014 David Tardon <dtardon@redhat.com> - 0.0.0-2
- remove extra dirs from filelist

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 0.0.0-1
- initial import
