%global gem_name redis

Name: rubygem-%{gem_name}
Version: 3.2.2
Release: 5%{?dist}
Summary: A Ruby client library for Redis
Group: Development/Languages
License: MIT
URL: https://github.com/redis/redis-rb
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: redis-test.conf
# Minitest 5 support
# A variation of this patch has been submitted upstream at
# https://github.com/redis/redis-rb/pull/445
Patch0: rubygem-redis-3.2.2-minitest.patch
%if 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: redis
BuildArch: noarch
%if 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

Prefix: %{_prefix}

%description
A Ruby client that tries to match Redis' API one-to-one, while still
providing an idiomatic interface. It features thread-safety,
client-side sharding, pipelining, and an obsession for performance.

%prep
gem unpack %{SOURCE0}

%setup -q -T -D -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Minitest 5 support
# https://github.com/redis/redis-rb/pull/445
%patch0 -p1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
rm -r %{buildroot}%{gem_instdir}/test

%files
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%exclude %{gem_cache}
%exclude %{gem_dir}/doc
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/*.md
%exclude %{gem_instdir}/*.gemspec
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/benchmarking
%exclude %{gem_instdir}/examples

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 08 2016 Greg Hellings <greg.hellings@gmail.com> - 3.2.2-2
- Update for rpmlint check
- Remove tests

* Mon Feb 08 2016 Greg Hellings <greg.hellings@gmail.com> - 3.2.2-1
- New upstream

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Feb 15 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.2.1-1
- Update to 3.2.1 (RHBZ #1192389)
- Remove Fedora 19 compatibility macros
- Use static test.conf, since upstream uses a dynamic ERB template now
- Correct comment about IPv6 support

* Mon Dec 15 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.2.0-1
- Update to 3.2.0 (RHBZ #1173070)
- Drop unneeded BRs
- Use %%license macro
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Unconditionally pass tests for now (RHBZ #1173070)

* Mon Jun 09 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.1.0-1
- Update to 3.1.0
- Remove gem2rpm comment
- Patch for Minitest 5

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 3.0.7-1
- Update to 3.0.7

* Tue Sep 03 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 3.0.4-3
- Move %%exclude .gitignore to -doc
- Reference to redis related bug

* Thu Jun 27 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 3.0.4-2
- Fix failing test
- Remove redis from Requires
- Exclude dot file

* Sun Jun 23 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 3.0.4-1
- Initial package
