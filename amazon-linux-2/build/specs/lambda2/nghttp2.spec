Summary: Experimental HTTP/2 client, server and proxy
Name: nghttp2
Version: 1.39.2
Release: 1%{?dist}
License: MIT
URL: https://nghttp2.org/
Source0: https://github.com/tatsuhiro-t/nghttp2/releases/download/v%{version}/nghttp2-%{version}.tar.xz
BuildRequires: CUnit-devel
BuildRequires: c-ares-devel
BuildRequires: gcc-c++
BuildRequires: libev-devel
BuildRequires: openssl-devel
BuildRequires: python3-devel
BuildRequires: zlib-devel

Requires: libnghttp2%{?_isa} = %{version}-%{release}

Prefix: %{_prefix}

%description
This package contains the HTTP/2 client, server and proxy programs.


%package -n libnghttp2
Summary: A library implementing the HTTP/2 protocol
Prefix: %{_prefix}

%description -n libnghttp2
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.


%prep
%setup -q

# make fetch-ocsp-response use Python 3
sed -e '1 s|^#!/.*python|&3|' -i script/fetch-ocsp-response

%build
%configure PYTHON=%{__python3}              \
    --disable-hpack-tools                   \
    --disable-python-bindings               \
    --disable-static                        \
    --without-libxml2 \
    --without-systemd

# avoid using rpath
sed -i libtool                              \
    -e 's/^runpath_var=.*/runpath_var=/'    \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/'

make %{?_smp_mflags} V=1


%install
%make_install


%files
%{_bindir}/h2load
%{_bindir}/nghttp
%{_bindir}/nghttpd
%{_bindir}/nghttpx
%{_datadir}/nghttp2

%files -n libnghttp2
%license COPYING
%{_libdir}/libnghttp2.so.*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}


%changelog
* Sun Sep 29 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Aug 14 2019 Kamil Dudka <kdudka@redhat.com> 1.39.2-1
- update to the latest upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.39.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Kamil Dudka <kdudka@redhat.com> 1.39.1-1
- update to the latest upstream release

* Tue Jun 11 2019 Kamil Dudka <kdudka@redhat.com> 1.39.0-1
- update to the latest upstream release

* Thu Apr 18 2019 Kamil Dudka <kdudka@redhat.com> 1.38.0-1
- update to the latest upstream release

* Fri Mar 08 2019 Kamil Dudka <kdudka@redhat.com> 1.37.0-1
- update to the latest upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 18 2019 Kamil Dudka <kdudka@redhat.com> 1.36.0-1
- update to the latest upstream release

* Mon Dec 10 2018 Kamil Dudka <kdudka@redhat.com> 1.35.1-1
- update to the latest upstream release

* Fri Nov 23 2018 Kamil Dudka <kdudka@redhat.com> 1.35.0-1
- update to the latest upstream release

* Thu Oct 04 2018 Kamil Dudka <kdudka@redhat.com> 1.34.0-1
- update to the latest upstream release

* Mon Sep 03 2018 Kamil Dudka <kdudka@redhat.com> 1.33.0-1
- use python3 for build
- update to the latest upstream release

* Mon Aug 27 2018 Kamil Dudka <kdudka@redhat.com> 1.32.1-1
- update to the latest upstream bugfix release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 09 2018 Kamil Dudka <kdudka@redhat.com> 1.32.0-1
- update to the latest upstream release

* Fri Apr 13 2018 Kamil Dudka <kdudka@redhat.com> 1.31.1-1
- update to the latest upstream release (fixes CVE-2018-1000168)

* Thu Mar 15 2018 Kamil Dudka <kdudka@redhat.com> 1.31.0-2
- make fetch-ocsp-response use Python 3

* Tue Feb 27 2018 Kamil Dudka <kdudka@redhat.com> 1.31.0-1
- update to the latest upstream release

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> 1.30.0-3
- add explicit BR for the gcc-c++ compiler

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Kamil Dudka <kdudka@redhat.com> 1.30.0-1
- update to the latest upstream release

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.29.0-2
- Switch to %%ldconfig_scriptlets

* Tue Dec 19 2017 Kamil Dudka <kdudka@redhat.com> 1.29.0-1
- update to the latest upstream release

* Sun Nov 26 2017 Kamil Dudka <kdudka@redhat.com> 1.28.0-1
- update to the latest upstream release

* Wed Oct 25 2017 Kamil Dudka <kdudka@redhat.com> 1.27.0-1
- update to the latest upstream release

* Wed Sep 20 2017 Kamil Dudka <kdudka@redhat.com> 1.26.0-1
- update to the latest upstream release

* Fri Aug 18 2017 Kamil Dudka <kdudka@redhat.com> 1.25.0-1
- update to the latest upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sat Jul 29 2017 Florian Weimer <fweimer@redhat.com> - 1.24.0-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Kamil Dudka <kdudka@redhat.com> 1.24.0-2
- drop workaround for a GCC bug that has been fixed (#1358845)

* Sun Jul 02 2017 Kamil Dudka <kdudka@redhat.com> 1.24.0-1
- update to the latest upstream release

* Tue May 30 2017 Kamil Dudka <kdudka@redhat.com> 1.23.1-1
- update to the latest upstream release

* Sat May 27 2017 Kamil Dudka <kdudka@redhat.com> 1.23.0-1
- update to the latest upstream release

* Mon Apr 24 2017 Kamil Dudka <kdudka@redhat.com> 1.22.0-1
- update to the latest upstream release

* Mon Apr 10 2017 Kamil Dudka <kdudka@redhat.com> 1.21.1-1
- update to the latest upstream release

* Mon Mar 27 2017 Kamil Dudka <kdudka@redhat.com> 1.21.0-1
- update to the latest upstream release

* Sun Feb 26 2017 Tomasz Torcz <ttorcz@fedoraproject.org> - 1.20.0-1
- package systemd unit file (#1426929)
- update to latest upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Kamil Dudka <kdudka@redhat.com> 1.19.0-1
- update to the latest upstream release

* Thu Jan 05 2017 Kamil Dudka <kdudka@redhat.com> 1.18.1-1
- update to the latest upstream release

* Tue Dec 27 2016 Kamil Dudka <kdudka@redhat.com> 1.18.0-1
- update to the latest upstream release (requires c-ares for apps)

* Mon Nov 28 2016 Kamil Dudka <kdudka@redhat.com> 1.17.0-1
- update to the latest upstream release

* Tue Nov 15 2016 Kamil Dudka <kdudka@redhat.com> 1.16.1-1
- update to the latest upstream release

* Mon Oct 24 2016 Kamil Dudka <kdudka@redhat.com> 1.16.0-1
- update to the latest upstream release

* Mon Sep 26 2016 Kamil Dudka <kdudka@redhat.com> 1.15.0-1
- update to the latest upstream release

* Mon Sep 12 2016 Kamil Dudka <kdudka@redhat.com> 1.14.1-1
- update to the latest upstream release

* Thu Aug 25 2016 Kamil Dudka <kdudka@redhat.com> 1.14.0-1
- update to the latest upstream release

* Tue Jul 26 2016 Kamil Dudka <kdudka@redhat.com> 1.13.0-2
- prevent nghttpx from crashing on armv7hl (#1358845)

* Thu Jul 21 2016 Kamil Dudka <kdudka@redhat.com> 1.13.0-1
- update to the latest upstream release

* Mon Jun 27 2016 Kamil Dudka <kdudka@redhat.com> 1.12.0-1
- update to the latest upstream release

* Sun May 29 2016 Kamil Dudka <kdudka@redhat.com> 1.11.1-1
- update to the latest upstream release

* Thu May 26 2016 Kamil Dudka <kdudka@redhat.com> 1.11.0-1
- update to the latest upstream release

* Mon Apr 25 2016 Kamil Dudka <kdudka@redhat.com> 1.10.0-1
- update to the latest upstream release

* Sun Apr 03 2016 Kamil Dudka <kdudka@redhat.com> 1.9.2-1
- update to the latest upstream release

* Tue Mar 29 2016 Kamil Dudka <kdudka@redhat.com> 1.9.1-1
- update to the latest upstream release

* Thu Feb 25 2016 Kamil Dudka <kdudka@redhat.com> 1.8.0-1
- update to the latest upstream release

* Thu Feb 11 2016 Kamil Dudka <kdudka@redhat.com> 1.7.1-1
- update to the latest upstream release (fixes CVE-2016-1544)

* Fri Feb 05 2016 Kamil Dudka <kdudka@redhat.com> 1.7.0-3
- make the package compile with gcc-6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Kamil Dudka <kdudka@redhat.com> 1.7.0-1
- update to the latest upstream release

* Fri Dec 25 2015 Kamil Dudka <kdudka@redhat.com> 1.6.0-1
- update to the latest upstream release (fixes CVE-2015-8659)

* Thu Nov 26 2015 Kamil Dudka <kdudka@redhat.com> 1.5.0-1
- update to the latest upstream release

* Mon Oct 26 2015 Kamil Dudka <kdudka@redhat.com> 1.4.0-1
- update to the latest upstream release

* Thu Sep 24 2015 Kamil Dudka <kdudka@redhat.com> 1.3.4-1
- update to the latest upstream release

* Wed Sep 23 2015 Kamil Dudka <kdudka@redhat.com> 1.3.3-1
- update to the latest upstream release

* Wed Sep 16 2015 Kamil Dudka <kdudka@redhat.com> 1.3.2-1
- update to the latest upstream release

* Mon Sep 14 2015 Kamil Dudka <kdudka@redhat.com> 1.3.1-1
- update to the latest upstream release

* Mon Aug 31 2015 Kamil Dudka <kdudka@redhat.com> 1.3.0-1
- update to the latest upstream release

* Mon Aug 17 2015 Kamil Dudka <kdudka@redhat.com> 1.2.1-1
- update to the latest upstream release

* Sun Aug 09 2015 Kamil Dudka <kdudka@redhat.com> 1.2.0-1
- update to the latest upstream release

* Wed Jul 15 2015 Kamil Dudka <kdudka@redhat.com> 1.1.1-1
- update to the latest upstream release

* Tue Jun 30 2015 Kamil Dudka <kdudka@redhat.com> 1.0.5-1
- packaged for Fedora (#1237247)
