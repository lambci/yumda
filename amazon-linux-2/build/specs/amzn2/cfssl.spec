%define debug_package %{nil}

%global commit             9c06c53d4dfb9c0272c983a26ea10a6a2da12392
%global shortcommit        %(c=%{commit}; echo ${c:0:7})

Name:	        cfssl
Version:	1.2.0
Release:	1.1.git%{shortcommit}%{?dist}
Summary:	Cloudflare's PKI and TLS toolkit

Group:		Development/Tools
License:	BSD-2-Clause
URL:		https://github.com/cloudflare/cfssl

# Source0 tarball file %{name}.tar.gz was created with the following commands.
#
# mkdir -p cfssl/go/src/github.com/cloudflare
# cd cfssl/go
# export GOPATH=$PWD
# cd src/github.com/cloudflare
# git clone https://github.com/cloudflare/cfssl
# cd cfssl
# git checkout 9c06c53d4dfb9c0272c983a26ea10a6a2da12392
# go get -d ./...
# cd $GOPATH/../..
# tar cf - cfssl | gzip -9 > cfssl.tar.gz
Source0:	%{name}.tar.gz

BuildRoot:      %{name}
BuildRequires:  golang >= 1.6

%description
CFSSL is CloudFlare's PKI/TLS swiss army knife. It is both a command line tool
and an HTTP API server for signing, verifying, and bundling TLS certificates.
It requires Go 1.6+ to build.

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
%setup -n %{name}

%build
export GOPATH=%{_builddir}/%{name}/go
cd %{_builddir}/%{name}/go/src/github.com/cloudflare/%{name}
go install ./cmd/...

%install
%{__rm} -rf %{buildroot}
%{__install} -pD -m 755 "%{_builddir}/%{name}/go/bin/cfssl" %{buildroot}%{_bindir}/cfssl
%{__install} -pD -m 755 "%{_builddir}/%{name}/go/bin/cfssljson" %{buildroot}%{_bindir}/cfssljson
%{__install} -pD -m 755 "%{_builddir}/%{name}/go/bin/mkbundle" %{buildroot}%{_bindir}/mkbundle
%{__install} -pD -m 755 "%{_builddir}/%{name}/go/bin/multirootca" %{buildroot}%{_bindir}/multirootca

%files
%defattr(0755,root,root,-)
%{_bindir}/cfssl
%{_bindir}/cfssljson
%{_bindir}/mkbundle
%{_bindir}/multirootca

%changelog
* Fri Jun  9 2017 <hnakamur@gmail.com> - 1.2.0-1.1.9c06c53
- Initial release
