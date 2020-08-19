Name:	    cfssl
Version:	1.4.1
Release:	1%{?dist}
Summary:	Cloudflare's PKI and TLS toolkit

Group:		Development/Tools
License:	BSD-2-Clause
URL:		https://github.com/cloudflare/cfssl

# curl -sSL https://github.com/cloudflare/cfssl/archive/v1.4.1.tar.gz > cfssl.tar.gz
Source0:	%{name}.tar.gz

BuildRoot:      %{name}-%{version}
BuildRequires:  golang >= 1.6

%description
CFSSL is CloudFlare's PKI/TLS swiss army knife. It is both a command line tool
and an HTTP API server for signing, verifying, and bundling TLS certificates.
It requires Go 1.12+ to build.

Note that certain linux distributions have certain algorithms removed
(RHEL-based distributions in particular), so the golang from the official
repositories will not work. Users of these distributions should install go
manually to install CFSSL.

CFSSL consists of:

* a set of packages useful for building custom TLS PKI tools
* the cfssl program, which is the canonical command line utility using the
  CFSSL packages.
* the multirootca program, which is a certificate authority server that can
  use multiple signing keys.
* the mkbundle program is used to build certificate pool bundles.
* the cfssljson program, which takes the JSON output from the cfssl and
  multirootca programs and writes certificates, keys, CSRs, and bundles to disk.

%prep
%setup -n %{name}-%{version}

%build
make %{?_smp_mflags} VERSION=%{version}

%install
%{__rm} -rf %{buildroot}

for bin in cfssl cfssl-bundle cfssl-certinfo cfssl-newkey cfssl-scan cfssljson mkbundle multirootca; do
  %{__install} -pD -m 755 bin/${bin} %{buildroot}%{_bindir}/${bin}
done

%files
%defattr(0755,root,root,-)
%{_bindir}/*

%changelog
* Tue Aug 18 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jun  9 2017 <hnakamur@gmail.com> - 1.2.0-1.1.9c06c53
- Initial release
