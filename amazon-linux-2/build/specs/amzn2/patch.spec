%define _trivial .0
%define _buildid .2
Release: 12%{?dist}%{?_trivial}%{?_buildid}
# CVE-2019-13636 patch
Patch1000: patch-2.7.x-CVE-2019-13636.patch
# CVE-2019-13636 patch
%patch1000 -p1 -b .CVE-2019-13636

* Wed Jul 09 2020 Sai Harsha <ssuryad@amazon.com> - 2.7.1-12
- Fix CVE-2019-13636
