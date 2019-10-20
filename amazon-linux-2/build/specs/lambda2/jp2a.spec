%global srcurl  https://github.com/cslarsen/%{name}

Name:           jp2a
Version:        1.0.7
Release:        1%{?dist}
Summary:        Small utility that converts JPG images to ASCII (text) using libjpeg

License:        GPLv2+
URL:            https://csl.name/%{name}
Source0:        %{srcurl}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf automake gcc
BuildRequires:  pkgconfig(libcurl)
# FIXME epel7 has no pkgconfig for libjpeg
#BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  libjpeg-devel

Prefix: %{_prefix}

%description
jp2a is a simple JPEG to ASCII converter. jp2a is very flexible.
It can use ANSI colors and html in output.
jp2a can also download and convert images from Internet via command line.


%prep
%autosetup
autoreconf -vi


%build
%configure --with-jpeg-prefix=%{_prefix} 
%make_build


%install
%make_install


%files
%license COPYING LICENSES
%{_bindir}/%{name}

%exclude %{_mandir}


%changelog
* Sun Oct 20 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Sat Jun 17 2017 Raphael Groner <projects.rg@smart.ms> - 1.0.7-1
- initial
