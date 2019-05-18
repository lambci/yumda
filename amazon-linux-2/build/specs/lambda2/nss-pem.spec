Name:       nss-pem
Version:    1.0.3
Release:    5%{?dist}
Summary:    PEM file reader for Network Security Services (NSS)

License:    MPLv1.1
URL:        https://github.com/kdudka/nss-pem
Source0:    https://github.com/kdudka/nss-pem/releases/download/%{name}-%{version}/%{name}-%{version}.tar.xz

Patch1:     0001-nss-pem-1.0.3-drop-wait-for-slot-event-cb.patch

# update object ID while reusing a certificate (#1610998)
Patch2:     0002-nss-pem-1.0.3-key-reload.patch

BuildRequires: cmake
BuildRequires: nss-pkcs11-devel

# require at least the version of nss that nss-pem was built against (#1428965)
Requires: nss%{?_isa} >= %(nss-config --version 2>/dev/null || echo 0)

# make the nss-pem pkg conflict with all nss builds with bundled nss-pem
Conflicts: nss%{?_isa} < 3.28.2-2.el7

Prefix: %{_prefix}

%description
PEM file reader for Network Security Services (NSS), implemented as a PKCS#11
module.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
mkdir build
cd build
%cmake ../src
make %{?_smp_mflags} VERBOSE=yes

%install
cd build
make install DESTDIR=%{buildroot}

%files
%license COPYING
%{_libdir}/libnsspem.so

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Aug 08 2018 Kamil Dudka <kdudka@redhat.com> 1.0.3-5
- update object ID while reusing a certificate (#1610998)

* Wed Apr 26 2017 Kamil Dudka <kdudka@redhat.com> 1.0.3-4
- fix missing prototypes detected by Covscan

* Tue Apr 25 2017 Kamil Dudka <kdudka@redhat.com> 1.0.3-3
- remove implementation of the WaitForSlotEvent callback (#1445384)

* Mon Mar 06 2017 Kamil Dudka <kdudka@redhat.com> 1.0.3-2
- require at least the version of nss that nss-pem was built against (#1428965)

* Wed Mar 01 2017 Kamil Dudka <kdudka@redhat.com> 1.0.3-1
- update to latest upstream bugfix release (#1427917)

* Tue Feb 14 2017 Kamil Dudka <kdudka@redhat.com> 1.0.2-2
- explicitly conflict with all nss builds with bundled nss-pem

* Tue Jan 24 2017 Kamil Dudka <kdudka@redhat.com> 1.0.2-1
- imported into RHEL-7
