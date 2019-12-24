Name: wkhtmltox
Version: 0.12.5
Release: 1%{?dist}
Epoch: 1
Summary: convert HTML to PDF and various image formats using QtWebkit
Group: utils
License: LGPLv3
Url: http://wkhtmltopdf.org/

# Source was downloaded using:
# curl -sSL -O https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox-0.12.5-1.centos7.x86_64.rpm
Source0: %{name}-%{version}-1.centos7.x86_64.rpm

BuildRequires: rpm
BuildRequires: cpio

Requires: ca-certificates
Requires: fontconfig
Requires: freetype
Requires: libX11
Requires: libXext
Requires: libXrender
Requires: libjpeg
Requires: libpng
Requires: openssl
Requires: xorg-x11-fonts-75dpi
Requires: xorg-x11-fonts-Type1
Requires: zlib

Prefix: %{_prefix}

%description
convert HTML to PDF and various image formats using QtWebkit

%install
rm -rf %{buildroot} && mkdir -p %{buildroot}

pushd %{buildroot}
  rpm2cpio %{SOURCE0} | cpio -idm
popd

mv %{buildroot}/usr/local %{buildroot}%{_prefix}

%files
%{_bindir}/wkhtmltoimage
%{_bindir}/wkhtmltopdf
%{_libdir}/libwkhtmltox.so.*

%exclude %{_mandir}
%exclude %{_includedir}
%exclude %{_libdir}/*.so
