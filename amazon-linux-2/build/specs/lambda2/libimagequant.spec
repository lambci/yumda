Name:           libimagequant
Version:        2.12.5
Release:        1%{?dist}
Summary:        Palette quantization library

License:        GPLv3+ and MIT
URL:            https://github.com/ImageOptim/libimagequant
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# Fix shared library permissions
Patch0:         libimagequant_solibperm.patch

BuildRequires:  gcc

Prefix: %{_prefix}

%description
Small, portable C library for high-quality conversion of RGBA images to 8-bit
indexed-color (palette) images.


%prep
%autosetup -p1


%build
%configure --with-openmp
%make_build


%install
%make_install

# Don't ship static library
rm -f %{buildroot}%{_libdir}/%{name}.a


%files
%license COPYRIGHT
%{_libdir}/%{name}.so.0

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig


%changelog
* Thu Apr 30 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Jul 29 2019 Sandro Mani <manisandro@gmail.com> - 2.12.5-1
- Update to 2.12.5

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 27 2019 Sandro Mani <manisandro@gmail.com> - 2.12.3-1
- Update to 2.12.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 29 2018 Sandro Mani <manisandro@gmail.com> - 2.12.2-1
- Update to 2.12.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 08 2018 Sandro Mani <manisandro@gmail.com> - 2.12.1-1
- Update to 2.12.1

* Mon Mar 12 2018 Sandro Mani <manisandro@gmail.com> - 2.11.10-1
- Update to 2.11.10

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 2.11.7-3
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Sandro Mani <manisandro@gmail.com> - 2.11.7-1
- Update to 2.11.7

* Thu Jan 18 2018 Sandro Mani <manisandro@gmail.com> - 2.11.6-1
- Update to 2.11.6

* Mon Nov 27 2017 Sandro Mani <manisandro@gmail.com> - 2.11.4-1
- Update to 2.11.4

* Sat Nov 11 2017 Sandro Mani <manisandro@gmail.com> - 2.11.3-1
- Update to 2.11.3

* Sun Nov 05 2017 Sandro Mani <manisandro@gmail.com> - 2.11.2-1
- Update to 2.11.2

* Mon Oct 30 2017 Sandro Mani <manisandro@gmail.com> - 2.11.0-1
- Update to 2.11.0

* Tue Aug 08 2017 Sandro Mani <manisandro@gmail.com> - 2.10.2-1
- Update to 2.10.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 09 2017 Sandro Mani <manisandro@gmail.com> - 2.10.1-1
- Update to 2.10.1

* Mon Jul 03 2017 Sandro Mani <manisandro@gmail.com> - 2.10.0-1
- Update to 2.10.0

* Thu Apr 06 2017 Sandro Mani <manisandro@gmail.com> - 2.9.1-1
- Update to 2.9.1

* Sat Mar 04 2017 Sandro Mani <manisandro@gmail.com> - 2.9.0-1
- Update to 2.9.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Sandro Mani <manisandro@gmail.com> - 2.8.2-2
- Use %%name and %%url to reduce text

* Mon Jan 02 2017 Sandro Mani <manisandro@gmail.com> - 2.8.2-1
- Initial package
