%global gitexecdir          %{_libexecdir}/git-core

Name:           git
Version:        2.26.2
Release:        1%{?rcrev}%{?dist}
Summary:        Fast Version Control System
License:        GPLv2
URL:            https://git-scm.com/
Source0:        https://mirrors.edge.kernel.org/pub/software/scm/git/%{?rcrev:testing/}%{name}-%{version}%{?rcrev}.tar.xz
Source1:        https://mirrors.edge.kernel.org/pub/software/scm/git/%{?rcrev:testing/}%{name}-%{version}%{?rcrev}.tar.sign

# Junio C Hamano's key is used to sign git releases, it can be found in the
# junio-gpg-pub tag within git.
#
# (Note that the tagged blob in git contains a version of the key with an
# expired signing subkey.  The subkey expiration has been extended on the
# public keyservers, but the blob in git has not been updated.)
#
# https://git.kernel.org/cgit/git/git.git/tag/?h=junio-gpg-pub
# https://git.kernel.org/cgit/git/git.git/blob/?h=junio-gpg-pub&id=7214aea37915ee2c4f6369eb9dea520aec7d855b
Source9:        gpgkey-junio.asc

BuildRequires:  expat-devel
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  libcurl-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  sed
BuildRequires:  zlib-devel >= 1.2

Requires:       git-core = %{version}-%{release}

# Obsolete gnome-keyring credential helper (remove in Fedora 29)
Obsoletes:      git-gnome-keyring < 2.11.1-4

Prefix: %{_prefix}

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs common set of tools which are usually using with
small amount of dependencies. To install all git packages, including
tools for integrating with other SCMs, install the git-all meta-package.

%package core
Summary:        Core package of git with minimal functionality
Requires:       openssh-clients
Requires:       zlib >= 1.2
Prefix: %{_prefix}

%description core
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git-core rpm installs really the core tools with minimal
dependencies. Install git package for common set of tools.
To install all git packages, including tools for integrating with
other SCMs, install the git-all meta-package.

%prep
# Verify GPG signatures
gpghome="$(mktemp -qd)" # Ensure we don't use any existing gpg keyrings
key="%{SOURCE9}"
src="%{SOURCE0}"
# Ignore noisy output from GnuPG 2.0, used on EL <= 7
# https://bugs.gnupg.org/gnupg/issue1555
gpg2 --dearmor --quiet --batch --yes $key >/dev/null
# Upstream signs the uncompressed tarballs
tar=${src/%.xz/}
xz -dc $src > $tar
gpgv2 --homedir "$gpghome" --quiet --keyring $key.gpg $tar.sign $tar
rm -rf "$tar" "$gpghome" # Cleanup tar files and tmp gpg home dir

# Ensure a blank line follows autosetup, el6 chokes otherwise
# https://bugzilla.redhat.com/1310704
%autosetup -p1 -n %{name}-%{version}%{?rcrev}

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
cat << \EOF > config.mak
CFLAGS = %{optflags}
LDFLAGS = %{__global_ldflags}
prefix = %{_prefix}

USE_LIBPCRE = 1
GNU_ROFF = 1

NO_GETTEXT = 1
NO_PERL = 1
NO_TCLTK = 1
NO_PYTHON = 1
INSTALL_SYMLINKS = 1

EOF

%build
# Improve build reproducibility
export TZ=UTC
export SOURCE_DATE_EPOCH=$(date -r version +%%s 2>/dev/null)
%make_build

%install
%make_install

# quiet some rpmlint complaints
chmod -R g-w %{buildroot}
chmod a-x %{buildroot}%{gitexecdir}/git-mergetool--lib
# These files probably are not needed
find . -regex '.*/\.\(git\(attributes\|ignore\)\|perlcriticrc\)' -delete
find contrib -type f -print0 | xargs -r0 chmod -x

%files
%{gitexecdir}/git-difftool
%{gitexecdir}/git-difftool--helper
%{gitexecdir}/git-filter-branch
%{gitexecdir}/git-instaweb
%{gitexecdir}/git-request-pull

%files core
%license COPYING
# exclude is best way here because of troubles with symlinks inside git-core/
%exclude %{gitexecdir}/git-difftool
%exclude %{gitexecdir}/git-difftool--helper
%exclude %{gitexecdir}/git-filter-branch
%exclude %{gitexecdir}/git-instaweb
%exclude %{gitexecdir}/git-request-pull
%{gitexecdir}
%{_bindir}/git
%{_bindir}/git-receive-pack
%{_bindir}/git-shell
%{_bindir}/git-upload-archive
%{_bindir}/git-upload-pack
%dir %{_datadir}/git-core/templates

%exclude %{_datadir}/git-core/templates/*
%exclude %{gitexecdir}/git-add--interactive
%exclude %{gitexecdir}/git-cvsserver
%exclude %{_bindir}/git-cvsserver

%changelog
* Mon Apr 20 2020 Michael Hart <michael@lambci.org> - 2.26.2-1
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Nov 26 2018 Todd Zullinger <tmz@pobox.com> - 2.17.2-2
- apply upstream run-command PATH fix (CVE-2018-19486)

* Fri Oct 05 2018 Todd Zullinger <tmz@pobox.com> - 2.17.2-1
- Update to 2.17.2 (CVE-2018-17456)

* Thu Jun 14 2018 Todd Zullinger <tmz@pobox.com> - 2.17.1-3
- Apply upstream zlib buffer handling patch (#1582555)

* Wed May 30 2018 Todd Zullinger <tmz@pobox.com>
- Disable jgit tests on s390x, they're unreliable
- Use %%make_build and %%make_install
- add -p: fix counting empty context lines in edited patches

* Tue May 29 2018 Todd Zullinger <tmz@pobox.com> - 2.17.1-2
- packfile: Correct zlib buffer handling (#1582555)

* Tue May 29 2018 Todd Zullinger <tmz@pobox.com> - 2.17.1-1
- Update to 2.17.1 (CVE-2018-11233, CVE-2018-11235)

* Thu May 24 2018 Todd Zullinger <tmz@pobox.com> - 2.17.0-4
- Fix segfault in rev-parse with invalid input (#1581678)
- Move TEST_SHELL_PATH setting to config.mak

* Mon Apr 16 2018 Todd Zullinger <tmz@pobox.com> - 2.17.0-3
- Move linkcheck macro to existing fedora/rhel > 7 block
- Re-enable t5000-tar-tree.sh test on f28

* Fri Apr 13 2018 Pavel Cahyna <pcahyna@redhat.com>
- Use BuildRequires: perl-interpreter per the packaging guidelines
- Update conditions for future RHEL

* Tue Apr 10 2018 Todd Zullinger <tmz@pobox.com> - 2.17.0-2
- Require perl-generators on EL > 7

* Mon Apr 09 2018 Todd Zullinger <tmz@pobox.com>
- daemon: use --log-destination=stderr with systemd
- daemon: fix condition for redirecting stderr
- git-svn: avoid uninitialized value warning

* Sun Apr 08 2018 Todd Zullinger <tmz@pobox.com>
- Clean up redundant and unneeded Requires

* Sat Apr 07 2018 Todd Zullinger <tmz@pobox.com>
- Remove Git::LoadCPAN to ensure we use only system perl modules

* Mon Apr 02 2018 Todd Zullinger <tmz@pobox.com>
- Allow git-p4 subpackage to be toggled via --with/--without
- Use %%bcond_(with|without) to enable/disable python3
- Add support for disabling python2

* Mon Apr 02 2018 Todd Zullinger <tmz@pobox.com> - 2.17.0-1
- Update to 2.17.0

* Wed Mar 28 2018 Todd Zullinger <tmz@pobox.com> - 2.17.0-0.2.rc2
- Update to 2.17.0-rc2

* Tue Mar 27 2018 Todd Zullinger <tmz@pobox.com>
- Allow cvs subpackage to be toggled via --with/--without

* Tue Mar 27 2018 Joe Orton <jorton@redhat.com>
- Disable CVS support on EL > 7

* Tue Mar 27 2018 Todd Zullinger <tmz@pobox.com> - 2.17.0-0.1.rc1.2
- Add missing perl(Mail::Address) requirement (#1561086)

* Thu Mar 22 2018 Todd Zullinger <tmz@pobox.com> - 2.17.0-0.1.rc1.1
- Drop .py extension from contrib/hooks/multimail/git_multimail.py
- Remove unnecessary "chmod +x contrib/hooks/*"

* Wed Mar 21 2018 Todd Zullinger <tmz@pobox.com> - 2.17.0-0.1.rc1
- Update to 2.17.0-rc1

* Fri Mar 16 2018 Todd Zullinger <tmz@pobox.com>
- Add findutils BuildRequires, improve 'find | xargs' calls

* Thu Mar 15 2018 Todd Zullinger <tmz@pobox.com> - 2.17.0-0.0.rc0
- Update to 2.17.0-rc0
- Adjust for simplified perl install
- Require git-core rather than git for git-daemon
- Rename gitweb httpd config file
- Install contrib/diff-highlight (#1550251)

* Thu Mar 15 2018 Todd Zullinger <tmz@pobox.com>
- Use symlinks instead of hardlinks for installed binaries

* Fri Feb 23 2018 Todd Zullinger <tmz@pobox.com>
- Improve hardening flags for EL-6 & EL-7

* Fri Feb 16 2018 Todd Zullinger <tmz@pobox.com> - 2.16.2-1
- Update to 2.16.2
- Add gawk, gcc, make, and sed BuildRequires

* Wed Feb 07 2018 Todd Zullinger <tmz@pobox.com> - 2.16.1-3
- Order %%files and %%packages sections by name
- Remove obsolete %%defattr
- Don't package contrib/svn-fe in %%doc
- Split git-subtree into a separate package

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Todd Zullinger <tmz@pobox.com> - 2.16.1-2
- git-svn: avoid segfaults in 'git svn branch', re-enable t9128, t9141, and
  t9167
- Drop obsolete BuildRoot, Group, %%clean, and buildroot cleanup

* Mon Jan 22 2018 Todd Zullinger <tmz@pobox.com> - 2.16.1-1
- Update to 2.16.1
- Avoid python dependency in git-core (#1536471)

* Thu Jan 18 2018 Todd Zullinger <tmz@pobox.com> - 2.16.0-1
- Update to 2.16.0
- Use 'prove' as test harness, enable shell tracing
- Disable t5000-tar-tree.sh on x86 in f28

* Fri Jan 12 2018 Todd Zullinger <tmz@pobox.com>
- Add %%{emacs_filesystem} to simplify emacs support
- Use .in template for git@.service to ensure paths are substituted

* Thu Jan 11 2018 Todd Zullinger <tmz@pobox.com>
- Update BuildRequires for tests

* Mon Jan 08 2018 Todd Zullinger <tmz@pobox.com>
- Avoid excluding non-existent .py[co] files in %%doc
- Remove obsolete gnome-keyring credential helper

* Sun Jan 07 2018 Todd Zullinger <tmz@pobox.com>
- Explicitly enable tests which may be skipped opportunistically

* Sat Dec 30 2017 Todd Zullinger <tmz@pobox.com>
- Fix perl requires filtering on EL-6

* Thu Nov 30 2017 Todd Zullinger <tmz@pobox.com> - 2.15.1-3
- Include verbose logs in build output for 'make test' failures
- Use %%autosetup macro to unpack and patch source
- Remove second make invocation for doc build/install
- Fix builds using '--without docs'
- Mark git-core-docs sub-package noarch
- Avoid failures in svnserve tests when run in parallel
- Run tests in parallel by default on Fedora
- Skip 'git svn branch' tests which fail intermittently
- Re-enable grep tests on s390x

* Wed Nov 29 2017 Todd Zullinger <tmz@pobox.com> - 2.15.1-2
- Fix debuginfo for gnome-keyring and libsecret credential helpers

* Tue Nov 28 2017 Todd Zullinger <tmz@pobox.com> - 2.15.1-1
- Update to 2.15.1

* Tue Nov 21 2017 Todd Zullinger <tmz@pobox.com>
- Add tcl/tk BuildRequires
- Enable support for release candidate builds

* Tue Nov 07 2017 Todd Zullinger <tmz@pobox.com> - 2.15.0-2
- Fix git-clone memory exhaustion (CVE-2017-15298)
  Resolves: #1510455, #1510457
- Disable cross-directory hardlinks
- Drop ancient obsoletes for git and git-arch
- Update summary/description of numerous subpackages
- Fix shebang in a few places to silence rpmlint complaints
- Fix t9020-remote-svn failure when setting PYTHON_PATH
- Rename %%gitcoredir to %%gitexecdir; upstream uses the latter
- Move commands which no longer require perl into git-core
- Move filter-branch out of core, it needs perl now
- Improve test suite coverage

* Mon Oct 30 2017 Todd Zullinger <tmz@pobox.com> - 2.15.0-1
- Update to 2.15.0

* Mon Oct 23 2017 Todd Zullinger <tmz@pobox.com> - 2.14.3-1
- Update to 2.14.3

* Tue Sep 26 2017 Todd Zullinger <tmz@pobox.com> - 2.14.2-2
- Update to 2.14.2

* Thu Aug 10 2017 Todd Zullinger <tmz@pobox.com> - 2.14.1-2
- Rebuild for rpm-4.14 bug (#1480407)

* Thu Aug 10 2017 Todd Zullinger <tmz@pobox.com> - 2.14.1-1
- Update to 2.14.1 (resolves CVE-2017-1000117)

* Tue Aug 08 2017 Iryna Shcherbina <ishcherb@redhat.com> - 2.14.0-2
- Add a build-time dependency on python2-devel for p4
  Resolves: #1479713
- Skip all grep tests on s390x for now because it failes intermittently

* Fri Aug 04 2017 Todd Zullinger <tmz@pobox.com> - 2.14.0-1
- Update to 2.14.0
- Use pcre2 library
- git-p4: explicitly require python2

* Tue Aug 01 2017 Todd Zullinger <tmz@pobox.com> - 2.13.4-1
- Update to 2.13.4
- Remove EL-5 and old Fedora conditionals

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2.13.3-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 20 2017 Petr Stodulka <pstodulk@redhat.com> - 2.13.3-2
- Move documentation files from all subpackages into the %%{_pkgdocdir}
  directory, so links inside doc and man files are correct
  Resolves: #1357438
- Quiet a few rpmlint complaints regarding hidden files in contrib dir
- Remove explicit libcurl requirement from git-core

* Thu Jul 13 2017 Gwyn Ciesla <limburgher@gmail.com> - 2.13.3-1
- Update to 2.13.3

* Sun Jun 25 2017 Todd Zullinger <tmz@pobox.com> - 2.13.2-1
- Update to 2.13.2
- Skip grep tests which fail intermittently on s390x

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.13.1-2
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Todd Zullinger <tmz@pobox.com> - 2.13.1-1
- Update to 2.13.1

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.13.0-3
- Perl 5.26 rebuild

* Wed May 17 2017 Todd Zullinger <tmz@pobox.com> - 2.13.0-2
- Use default, collision-detecting SHA1 implementation

* Tue May 09 2017 Todd Zullinger <tmz@pobox.com> - 2.13.0-1
- Update to 2.13.0 (resolves CVE-2017-8386)

* Wed Mar 29 2017 Gwyn Ciesla <limburgher@gmail.com> - 2.12.2-1
- Update to 2.12.2

* Tue Mar 21 2017 Gwyn Ciesla <limburgher@gmail.com> - 2.12.1-1
- Update to 2.12.1

* Mon Feb 27 2017 Jon Ciesla <limburgher@gmail.com> - 2.12.0-1
- Update to 2.12.0

* Fri Feb 17 2017 Petr Stodulka <pstodulk@redhat.com> - 2.11.1-3
- remove non-ASCII characters from description and title of packages
- fix requiremets
- fix spec to be compatible for other systems
- remove deprecated credential-gnome-keyring

* Fri Feb 17 2017 Todd Zullinger <tmz@pobox.com> - 2.11.1-3
- Remove unnecessary rsync requirement from git-core
- Move gnome-keyring credential helper from git-core to git
- Enable libsecret credential helper
- Run git test suite
- Use %%{_mandir} in git/git-core file list filters
- Fix version of emacs-git and emacs-git-el provides
- Clean up contrib/{credential,subtree} to avoid cruft in git-core-doc
- Fix a number of macro-in-comment warnings from rpmlint

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Jon Ciesla <limburgher@gmail.com> - 2.11.1-1
- Update to 2.11.1

* Wed Nov 30 2016 Jon Ciesla <limburgher@gmail.com> - 2.11.0-1
- Update to 2.11.0

* Mon Oct 31 2016 Jon Ciesla <limburgher@gmail.com> - 2.10.2-1
- Update to 2.10.2

* Tue Oct 04 2016 Jon Ciesla <limburgher@gmail.com> - 2.10.1-1
- Update to 2.10.1

* Sat Sep 03 2016 Todd Zullinger <tmz@pobox.com> - 2.10.0-1
- Update to 2.10.0

* Mon Aug 15 2016 Jon Ciesla <limburgher@gmail.com> - 2.9.3-1
- Update to 2.9.3.

* Fri Jul 15 2016 Jon Ciesla <limburgher@gmail.com> - 2.9.2-1
- Update to 2.9.2.

* Tue Jul 12 2016 Jon Ciesla <limburgher@gmail.com> - 2.9.1-1
- Update to 2.9.1.

* Tue Jun 14 2016 Jon Ciesla <limburgher@gmail.com> - 2.9.0-1
- Update to 2.9.0.

* Wed Jun 08 2016 Jon Ciesla <limburgher@gmail.com> - 2.8.4-1
- Update to 2.8.4.

* Fri May 20 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.8.3-2
- Perl 5.24 rebuild

* Thu May 19 2016 Todd Zullinger <tmz@pobox.com> - 2.8.3-1
- Update to 2.8.3

* Thu May 19 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.8.2-5
- Perl 5.24 re-rebuild of bootstrapped packages

* Wed May 18 2016 Todd Zullinger <tmz@pobox.com> - 2.8.2-4
- Use perl(MOD::NAME) format for perl-DBD-SQLite and perl-Digest-MD5 deps
- Define __global_ldflags on EL < 7 (#1337137)

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.8.2-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.8.2-2
- Perl 5.24 rebuild

* Fri Apr 29 2016 Todd Zullinger <tmz@pobox.com> - 2.8.2-1
- Update to 2.8.2

* Mon Apr 11 2016 Todd Zullinger <tmz@pobox.com> - 2.8.1-3
- Set LDFLAGS for hardened builds (#1289728)

* Wed Apr 06 2016 Paolo Bonzini <pbonzini@redhat.com> - 2.8.1-2
- Install git-credentials-netrc (#1303358)

* Tue Apr 05 2016 Jon Ciesla <limburgher@gmail.com> - 2.8.1-1
- Update to 2.8.1.

* Tue Mar 29 2016 Neal Gompa <ngompa13{%}gmail{*}com> - 2.8.0-1
- Update to 2.8.0
- Use license macro for COPYING

* Sun Mar 27 2016 Todd Zullinger <tmz@pobox.com> - 2.7.4-2
- Use https for URL / Source and smaller tar.xz files
- Check upstream GPG signatures in %%prep

* Tue Mar 22 2016 Konrad Scherer <Konrad.Scherer@windriver.com>
- Workaround missing git subtree documentation in prebuilt docs (bug 1320210)
- Only add git-cvsserver binary once if the core dir matches the bin dir as it
  does on el5 (bug 1320210)

* Tue Mar 22 2016 Todd Zullinger <tmz@pobox.com>
- Conditionalize bash-completion pkg-config usage for EL <= 6 (bug 1320210)

* Fri Mar 18 2016 David Woodhouse <dwmw2@infradead.org> - 2.7.4-1
- Update to 2.7.4 (for CVE-2016-2315, CVE-2016-2324)
  Resolves: #1318220

* Mon Mar 14 2016 Jon Ciesla <limburgher@gmail.com> - 2.7.3-1
- Update to 2.7.3.

* Tue Feb 23 2016 Jon Ciesla <limburgher@gmail.com> - 2.7.2-1
- Update to 2.7.2.

* Sat Feb 06 2016 Jon Ciesla <limburgher@gmail.com> - 2.7.1-1
- Update to 2.7.1.

* Thu Feb 04 2016 Petr Stodulka <pstodulk@redhat.com> - 2.7.0-3
- remove all '.gitignore' files from packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Jon Ciesla <limburgher@gmail.com> - 2.7.0-1
- Update to 2.7.0.
- Infinite loop patch appears obsolete.

* Wed Dec 09 2015 Jon Ciesla <limburgher@gmail.com> - 2.6.4-1
- Update to 2.6.4.

* Fri Nov 27 2015 Petr Stodulka <pstodulk@redhat.com> - 2.6.3-2
- found 2 perl scripts in git-core, move them to git package
  (#1284688)

* Fri Nov 06 2015 Jon Ciesla <limburgher@gmail.com> - 2.6.3-1
- Update to 2.6.3.

* Tue Nov 03 2015 Petr Stodulka <pstodulk@gmail.com> - 2.6.2-2
- provides failback for the macro _pkgdocdir (#1277550)

* Sat Oct 17 2015 Jon Ciesla <limburgher@gmail.com> - 2.6.2-1
- Update to 2.6.2.

* Tue Oct 06 2015 Jon Ciesla <limburgher@gmail.com> - 2.6.1-1
- Update to 2.6.1.

* Tue Sep 29 2015 Jon Ciesla <limburgher@gmail.com> - 2.6.0-1
- Update to 2.6.0.

* Fri Sep 18 2015 Jon Ciesla <limburgher@gmail.com> - 2.5.3-1
- Update to 2.5.3.

* Fri Sep 11 2015 Jon Ciesla <limburgher@gmail.com> - 2.5.2-1
- Update to 2.5.2.

* Sat Aug 29 2015 Petr Stodulka <pstodulk@redhat.com> - 2.5.1-1
- Update to 2.5.1

* Tue Jul 28 2015 Jon Ciesla <limburgher@gmail.com> - 2.5.0-1
- Update to 2.5.0.

* Thu Jul 16 2015 Petr Stodulka <pstodulk@redhat.com> - 2.4.6-1
- New upstream release 2.4.6

* Tue Jul  7 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 2.4.5-2
- Comply with modern Emacs packaging guidelines on recent Fedora
  No longer split out emacs-git and emacs-git-el sub-packages on recent Fedora
  Require emacs-filesystem on recent Fedora (#1234552)

* Fri Jun 26 2015 Jon Ciesla <limburgher@gmail.com> - 2.4.5-1
- Update to 2.4.5.

* Mon Jun 22 2015  Petr Stodulka <pstodulk@gmail.com> - 2.4.4-2
- git-svn - added requires for perl-Digest-MD5 (#1218176)
- solve troubles with infinite loop due to broken symlink (probably
  shouldn't be problem here, but it's reproducible manually)
  (#1204193)

* Tue Jun 16 2015 Jon Ciesla <limburgher@gmail.com> - 2.4.4-1
- Update to 2.4.4.

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.3-4
- Perl 5.22 re-rebuild of bootstrapped packages

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.3-3
- Perl 5.22 rebuild

* Mon Jun 08 2015 Petr Stodulka <pstodulk@redhat.com> - 2.4.3-2
- separate documentation files from git-core package to git-core-doc
  including core man pages

* Sat Jun 06 2015 Jon Ciesla <limburgher@gmail.com> - 2.4.3-1
- Update to 2.4.3.

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com>
- Perl 5.22 rebuild

* Wed Jun 03 2015 Petr Stodulka <pstodulk@redhat.com> - 2.4.2-2
- split create subpackage git-core (perl-less) from git package
- git package requires git-core and it has same tool set as
  before
- relevant docs are part of git-core package too
- removed proved and obsoletes in git for git-core

* Tue May 26 2015 Jon Ciesla <limburgher@gmail.com> - 2.4.2-1
- Update to 2.4.2.

* Thu May 14 2015 Jon Ciesla <limburgher@gmail.com> - 2.4.1-1
- Update to 2.4.1.

* Fri May 01 2015 Jon Ciesla <limburgher@gmail.com> - 2.4.0-1
- Update to 2.4.0.

* Tue Apr 28 2015 Jon Ciesla <limburgher@gmail.com> - 2.3.7-1
- Update to 2.3.7.

* Wed Apr 22 2015 Jon Ciesla <limburgher@gmail.com> - 2.3.6-1
- Update to 2.3.6.

* Mon Apr 06 2015 Jon Ciesla <limburgher@gmail.com> - 2.3.5-1
- Update to 2.3.5.

* Tue Mar 24 2015 Petr Stodulka <pstodulk@redhat.com> - 2.3.4-1
- Update to 2.3.4.

* Mon Mar 16 2015 Jon Ciesla <limburgher@gmail.com> - 2.3.3-1
- Update to 2.3.3.

* Mon Mar 09 2015 Jon Ciesla <limburgher@gmail.com> - 2.3.2-1
- Update to 2.3.2.

* Fri Feb 27 2015 Jon Ciesla <limburgher@gmail.com> - 2.3.1-1
- Update to 2.3.1.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.3.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Feb 06 2015 Jon Ciesla <limburgher@gmail.com> - 2.3.0-1
- Update to 2.3.0.

* Tue Jan 27 2015 Ville Skyttä <ville.skytta@iki.fi> - 2.2.2-2
- Install bash completion to %%{_datadir}/bash-completion/completions

* Fri Jan 23 2015 Jon Ciesla <limburgher@gmail.com> - 2.2.2-1
- Update to 2.2.2.

* Thu Jan 08 2015 Jon Ciesla <limburgher@gmail.com> - 2.2.1-1
- Update to 2.2.1.

* Thu Dec 11 2014 Petr Stodulka <pstodulk@redhat.com> - 2.2.0-3
- removed subpackage git-hg which is replaced by git-remote-hg from
  separated package

* Fri Nov 28 2014 Petr Stodulka <pstodulk@redhat.com> - 2.2.0-2
- removed subpackage git-bzr which is replaced by git-remote-bzr from
  separated package

* Fri Nov 28 2014 Petr Stodulka <pstodulk@redhat.com> - 2.2.0-1
- 2.2.0

* Fri Oct 24 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.1.0-5
- Rename the git.service into git@.service fixing
  https://bugzilla.redhat.com/980574

* Mon Sep 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.0-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.0-3
- Perl 5.20 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.0-2
- Disable requires perl(Term::ReadKey) when perl bootstraping

* Mon Aug 18 2014 Ondrej Oprala <ooprala@redhat.com - 2.1.0-1
- 2.1.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Ondrej Oprala <ooprala@redhat.com - 2.0.4-1
- 2.0.4

* Mon Jul 28 2014 Ondrej Oprala <ooprala@redhat.com - 2.0.3-1
- 2.0.3

* Fri Jul 11 2014 Ondrej Oprala <ooprala@redhat.com - 2.0.1-1
- 2.0.1

* Tue Jun 10 2014 Ondrej Oprala <ooprala@redhat.com> - 2.0.0-4
- Change source URLs, as googlecode doesn't have up-to-date tarballs

* Tue Jun 10 2014 Ondrej Oprala <ooprala@redhat.com> - 2.0.0-3
- Conditionalize an ancient obsolete

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Ondrej Oprala <ooprala@redhat.com> - 2.0.0-1
- Update to 2.0.0

* Mon May 19 2014 Jon Ciesla <limburgher@gmail.com> - 1.9.3-1
- Update to 1.9.3

* Mon Feb 17 2014 Ondrej Oprala <ooprala@redhat.com> - 1.9.0-1
- Update to 1.9.0

* Thu Jan 16 2014 Todd Zullinger <tmz@pobox.com> - 1.8.5.3-2
- Drop unused python DESTIR patch
- Consolidate settings for Fedora 19+ and EL 7+
- Use new rpm filtering on Fedora 19+ and EL 7+
- Rebuild with file-5.14-14 (#1026760)

* Thu Jan 16 2014 Ondrej Oprala <ooprala@redhat.com> - 1.8.5.3-1
* Update to 1.8.5.3

* Wed Dec 18 2013 Ondrej Oprala <ooprala@redhat.com> - 1.8.5.2-1
* Update to 1.8.5.2

* Wed Nov 13 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.8.4.2-2
- Fix htmldir when doc dir is unversioned (#993779).

* Tue Oct 29 2013 Todd Zullinger <tmz@pobox.com> - 1.8.4.2-1
- Update to 1.8.4.2 (#1024497)

* Sat Oct 05 2013 Todd Zullinger <tmz@pobox.com>
- Add mercurial version requirement to git-hg, for those rebuilding on EL

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1.8.3.1-2
- Perl 5.18 rebuild

* Fri Jun 14 2013 Todd Zullinger <tmz@pobox.com> - 1.8.3.1-1
- Update to 1.8.3.1
- Add bzr and hg subpackages, thanks to Michael Scherer (#974800)

* Mon May 13 2013 Jon Ciesla <limburgher@gmail.com> - 1.8.2.1-4
- Fix typo introduced in 1.8.2-3, fixed desktop tag.

* Wed May  1 2013 Tom Callaway <spot@fedoraproject.org> - 1.8.2.1-3
- conditionalize systemd vs xinetd
- cleanup systemd handling (it was not quite right in -2)

* Tue Apr 30 2013 Tom Callaway <spot@fedoraproject.org> - 1.8.2.1-2
- switch to systemd instead of xinetd (bz 737183)

* Sun Apr 14 2013 Todd Zullinger <tmz@pobox.com> - 1.8.2.1-1
- Update to 1.8.2.1
- Exclude optional perl(YAML::Any) dependency on EL-5

* Wed Apr 10 2013 Jon Ciesla <limburgher@gmail.com> - 1.8.2-3
- Drop desktop vendor tag for >= f19.

* Wed Mar 27 2013 Todd Zullinger <tmz@pobox.com> - 1.8.2-2
- Require perl(Term::ReadKey) for git add --interactive (#928328)
- Drop DESTDIR from python instlibdir
- Fix bogus changelog dates

* Tue Mar 19 2013 Adam Tkac <atkac redhat com> - 1.8.2-1
- update to 1.8.2
- 0001-DESTDIR-support-in-contrib-subtree-Makefile.patch has been merged

* Tue Feb 26 2013 Todd Zullinger <tmz@pobox.com> - 1.8.1.4-2
- Update asciidoc requirements, drop unsupported ASCIIDOC7
- Define GNU_ROFF to force ASCII apostrophes in manpages (so copy/paste works)
- Install tcsh completion (requires manual setup by users)
- Clean up dist conditionals, don't pretend to support EL-4 builds
- Use prebuilt documentation on EL-5, where asciidoc is too old
- Respect gitexecdir variable in git-subtree install

* Wed Feb 20 2013 Adam Tkac <atkac redhat com> - 1.8.1.4-1
- update to 1.8.1.4

* Wed Jan 30 2013 Adam Tkac <atkac redhat com> - 1.8.1.2-1
- update to 1.8.1.2
- own directories which should be owned (#902517)

* Thu Jan 03 2013 Adam Tkac <atkac redhat com> - 1.8.1-1
- update to 1.8.1
- build git-svn as arch subpkg due to new git-remote-testsvn binary

* Tue Dec 11 2012 Adam Tkac <atkac redhat com> - 1.8.0.2-1
- update to 1.8.0.2

* Thu Dec 06 2012 Adam Tkac <atkac redhat com> - 1.8.0.1-2
- don't install some unneeded credential-gnome-keyring stuff

* Thu Nov 29 2012 Adam Tkac <atkac redhat com> - 1.8.0.1-1
- update to 1.8.0.1
- include git-subtree in git rpm (#864651)

* Mon Oct 29 2012 Adam Tkac <atkac redhat com> - 1.8.0-1
- update to 1.8.0
- include git-credential-gnome-keyring helper in git pkg
- 0001-cvsimport-strip-all-inappropriate-tag-strings.patch was merged

* Thu Oct 25 2012 Adam Tkac <atkac redhat com> - 1.7.12.1-2
- move git-prompt.sh into usr/share/git-core/contrib/completion (#854061)

* Thu Sep 27 2012 Adam Tkac <atkac redhat com> - 1.7.12.1-1
- update to 1.7.12.1
- cvsimport should skip more characters (#850640)

* Thu Aug 23 2012 Todd Zullinger <tmz@pobox.com> - 1.7.12-2
- Install git-prompt.sh which provides __git_ps1()

* Wed Aug 22 2012 Adam Tkac <atkac redhat com> - 1.7.12-1
- update to 1.7.12

* Wed Aug 15 2012 Todd Zullinger <tmz@pobox.com> - 1.7.11.5-1
- Update to 1.7.11.5
- Add git-p4 subpackage (#844008)

* Tue Aug 07 2012 Adam Tkac <atkac redhat com> - 1.7.11.4-1
- update to 1.7.11.4

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 25 2012 Todd Zullinger <tmz@pobox.com> - 1.7.11.2-2
- Split perl(Git::SVN) into its own package (#843182)

* Mon Jul 16 2012 Adam Tkac <atkac redhat com> - 1.7.11.2-1
- update to 1.7.11.2

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.7.10.4-2
- Perl 5.16 rebuild

* Fri Jun 15 2012 Adam Tkac <atkac redhat com> - 1.7.10.4-1
- update to 1.7.10.4

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 1.7.10.2-2
- Perl 5.16 rebuild

* Mon May 14 2012 Adam Tkac <atkac redhat com> - 1.7.10.2-1
- update to 1.7.10.2

* Thu May 03 2012 Adam Tkac <atkac redhat com> - 1.7.10.1-1
- update to 1.7.10.1

* Tue Apr 10 2012 Adam Tkac <atkac redhat com> - 1.7.10-1
- update to 1.7.10

* Fri Mar 30 2012 Adam Tkac <atkac redhat com> - 1.7.9.5-1
- update to 1.7.9.5

* Thu Mar 08 2012 Adam Tkac <atkac redhat com> - 1.7.9.3-1
- update to 1.7.9.3

* Wed Feb 15 2012 Todd Zullinger <tmz@pobox.com> - 1.7.9.1-1
- Update to 1.7.9.1
- Fix EPEL builds (rpm doesn't accept multiple -f options in %%files)

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.7.9-2
- Rebuild against PCRE 8.30

* Mon Jan 30 2012 Adam Tkac <atkac redhat com> - 1.7.9-1
- update to 1.7.9

* Thu Jan 19 2012 Adam Tkac <atkac redhat com> - 1.7.8.4-1
- update to 1.7.8.4

* Thu Jan 12 2012 Adam Tkac <atkac redhat com> - 1.7.8.3-1
- update to 1.7.8.3

* Mon Jan 02 2012 Adam Tkac <atkac redhat com> - 1.7.8.2-1
- update to 1.7.8.2

* Fri Dec 23 2011 Adam Tkac <atkac redhat com> - 1.7.8.1-1
- update to 1.7.8.1

* Wed Dec 07 2011 Adam Tkac <atkac redhat com> - 1.7.8-1
- update to 1.7.8

* Tue Nov 29 2011 Adam Tkac <atkac redhat com> - 1.7.7.4-1
- update to 1.7.7.4

* Thu Nov 10 2011 Adam Tkac <atkac redhat com> - 1.7.7.3-1
- update to 1.7.7.3

* Mon Nov 07 2011 Adam Tkac <atkac redhat com> - 1.7.7.2-1
- update to 1.7.7.2

* Tue Nov 01 2011 Adam Tkac <atkac redhat com> - 1.7.7.1-1
- update to 1.7.7.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-2
- Rebuilt for glibc bug#747377

* Thu Oct 20 2011 Adam Tkac <atkac redhat com> - 1.7.7-1
- update to 1.7.7
  - git-1.6-update-contrib-hooks-path.patch is no longer needed

* Mon Sep 26 2011 Adam Tkac <atkac redhat com> - 1.7.6.4-1
- update to 1.7.6.4

* Wed Sep 07 2011 Todd Zullinger <tmz@pobox.com> - 1.7.6.2-1
- Update to 1.7.6.2
- Fixes incompatibility caused by git push --quiet fix
  http://thread.gmane.org/gmane.comp.version-control.git/180652

* Mon Aug 29 2011 Todd Zullinger <tmz@pobox.com> - 1.7.6.1-2
- Build with PCRE support (#734269)

* Fri Aug 26 2011 Todd Zullinger <tmz@pobox.com> - 1.7.6.1-1
- Update to 1.7.6.1
- Include gpg signature for tarball in SRPM

* Fri Aug 05 2011 Todd Zullinger <tmz@pobox.com> - 1.7.6-5
- Fix git push --quiet, thanks to Clemens Buchacher (#725593)
- Obsolete git-arch as needed

* Tue Jul 26 2011 Todd Zullinger <tmz@pobox.com> - 1.7.6-4
- Drop git-arch on fedora >= 16, the tla package has been retired
- Rework most spec file dist conditionals to make future changes easier

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.7.6-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.7.6-2
- Perl mass rebuild

* Wed Jun 29 2011 Adam Tkac <atkac redhat com> - 1.7.6-1
- update to 1.7.6

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.7.5.4-2
- Perl mass rebuild

* Thu Jun 09 2011 Adam Tkac <atkac redhat com> - 1.7.5.4-1
- update to 1.7.5.4

* Tue May 24 2011 Adam Tkac <atkac redhat com> - 1.7.5.2-1
- update to 1.7.5.2

* Thu May 05 2011 Adam Tkac <atkac redhat com> - 1.7.5.1-1
- update to 1.7.5.1

* Wed Apr 27 2011 Adam Tkac <atkac redhat com> - 1.7.5-1
- update to 1.7.5

* Mon Apr 11 2011 Adam Tkac <atkac redhat com> - 1.7.4.4-1
- update to 1.7.4.4

* Mon Mar 28 2011 Adam Tkac <atkac redhat com> - 1.7.4.2-1
- update to 1.7.4.2
- move man3/Git.3pm file to perl-Git subpkg (#664889)
- add perl-DBD-SQLite dependency to git-cvs (#602410)

* Sun Feb 13 2011 Todd Zullinger <tmz@pobox.com> - 1.7.4.1-1
- Update to 1.7.4.1
- Clean up documentation settings (the defaults changed in 1.7.4)
- Improve EL-5 compatibility, thanks to Kevin Fenzi for emacs testing

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Adam Tkac <atkac redhat com> - 1.7.4-1
- update to 1.7.4

* Wed Jan 19 2011 Adam Tkac <atkac redhat com> - 1.7.3.5-1
- update to 1.7.3.5

* Thu Dec 16 2010 Adam Tkac <atkac redhat com> - 1.7.3.4-1
- update to 1.7.3.4

* Mon Dec 06 2010 Adam Tkac <atkac redhat com> - 1.7.3.3-1
- update to 1.7.3.3

* Fri Oct 22 2010 Adam Tkac <atkac redhat com> - 1.7.3.2-1
- update to 1.7.3.2

* Thu Sep 30 2010 Adam Tkac <atkac redhat com> - 1.7.3.1-1
- update to 1.7.3.1

* Wed Sep 29 2010 jkeating - 1.7.3-3
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Todd Zullinger <tmz@pobox.com> - 1.7.3-2
- Ensure the release notes are included in %%doc

* Sun Sep 19 2010 Todd Zullinger <tmz@pobox.com> - 1.7.3-1
- Update to 1.7.3

* Tue Sep 07 2010 Adam Tkac <atkac redhat com> - 1.7.2.3-1
- update to 1.7.2.3

* Fri Aug 20 2010 Adam Tkac <atkac redhat com> - 1.7.2.2-1
- update to 1.7.2.2

* Fri Jul 30 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.7.2.1-2
- cherry-pick: "Do not unquote + into ' ' in URLs"

* Thu Jul 29 2010 Todd Zullinger <tmz@pobox.com> - 1.7.2.1-1
- Update to git-1.7.2.1

* Thu Jul 22 2010 Adam Tkac <atkac redhat com> - 1.7.2-1
- update to 1.7.2

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> - 1.7.1.1-1
- update to 1.7.1.1

* Fri Jun 25 2010 Adam Tkac <atkac redhat com> - 1.7.1-2
- rebuild against new perl

* Tue May 04 2010 Todd Zullinger <tmz@pobox.com> - 1.7.1-1
- git-1.7.1
- Fix conditionals for EL-6
- Comply with Emacs add-on packaging guidelines (#573423), Jonathan Underwood
  - Place elisp source files in separate emacs-git-el package
  - Place git support files in own directory under site-lisp
  - Use Emacs packaging macros

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.7.0.1-2
- Mass rebuild with perl-5.12.0

* Mon Mar 01 2010 Todd Zullinger <tmz@pobox.com> - 1.7.0.1-1
- git-1.7.0.1

* Sat Feb 13 2010 Todd Zullinger <tmz@pobox.com> - 1.7.0-1
- git-1.7.0
- Link imap-send with libcrypto (#565147)
- Disable building of unused python remote helper libs

* Tue Jan 26 2010 Todd Zullinger <tmz@pobox.com> - 1.6.6.1-1
- git-1.6.6.1
- Use %%{gitcoredir}/git-daemon as xinetd server option, for SELinux (#529682)
- Make %%{_var}/lib/git the default gitweb projectroot (#556299)
- Include gitweb/INSTALL file as documentation, the gitweb README refers to it
- Ship a short example gitweb config file (%%{_sysconfdir}/gitweb.conf)
- Remove long fixed xinetd IPv6 workaround on Fedora (#557528)
- Install missing gitweb.js (#558740)

* Wed Dec 23 2009 Todd Zullinger <tmz@pobox.com> - 1.6.6-1
- git-1.6.6

* Fri Dec 11 2009 Todd Zullinger <tmz@pobox.com> - 1.6.5.6-1
- git-1.6.5.6

* Sun Dec 06 2009 Todd Zullinger <tmz@pobox.com> - 1.6.5.5-1
- git-1.6.5.5

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.6.5.3-2
- rebuild against perl 5.10.1

* Sat Nov 21 2009 Todd Zullinger <tmz@pobox.com> - 1.6.5.3-1
- git-1.6.5.3
- Only BR perl(Error) on Fedora and RHEL >= 5
- Use config.mak to set build options
- Improve compatibility with EPEL
- Replace $RPM_BUILD_ROOT with %%{buildroot}
- Fix Obsoletes for those rebuilding on EL-4

* Mon Oct 26 2009 Todd Zullinger <tmz@pobox.com> - 1.6.5.2-1
- git-1.6.5.2
- Drop asciidoc --unsafe option, it should not be needed anymore
- Don't use install -t/-T, they're not compatible with older coreutils
- Don't use -perm /a+x with find, it's incompatible with older findutils

* Sat Oct 17 2009 Todd Zullinger <tmz@pobox.com> - 1.6.5.1-1
- git-1.6.5.1

* Sun Oct 11 2009 Todd Zullinger <tmz@pobox.com> - 1.6.5-1
- git-1.6.5

* Mon Sep 28 2009 Todd Zullinger <tmz@pobox.com> - 1.6.5-0.2.rc2
- git-1.6.5.rc2
- Enable Linus' block-sha1 implementation

* Wed Sep 16 2009 Todd Zullinger <tmz@pobox.com> - 1.6.4.4-1
- git-1.6.4.4

* Sun Sep 13 2009 Todd Zullinger <tmz@pobox.com> - 1.6.4.3-1
- git-1.6.4.3

* Sun Aug 30 2009 Todd Zullinger <tmz@pobox.com> - 1.6.4.2-1
- git-1.6.4.2

* Sat Aug 22 2009 Todd Zullinger <tmz@pobox.com> - 1.6.4.1-1
- git-1.6.4.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.6.4-2
- rebuilt with new openssl

* Wed Jul 29 2009 Todd Zullinger <tmz@pobox.com> - 1.6.4-1
- git-1.6.4

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 28 2009 Todd Zullinger <tmz@pobox.com> - 1.6.3.3-1
- git-1.6.3.3
- Move contributed hooks to %%{_datadir}/git-core/contrib/hooks (bug 500137)
- Fix rpmlint warnings about Summary and git-mergetool--lib missing shebang

* Fri Jun 19 2009 Todd Zullinger <tmz@pobox.com> - 1.6.3.2-3
- Temporarily disable asciidoc's safe mode until bug 506953 is fixed

* Fri Jun 19 2009 Todd Zullinger <tmz@pobox.com> - 1.6.3.2-2
- Fix git-daemon hang on invalid input (CVE-2009-2108, bug 505761)

* Fri Jun 05 2009 Todd Zullinger <tmz@pobox.com> - 1.6.3.2-1
- git-1.6.3.2
- Require emacs >= 22.2 for emacs support (bug 495312)
- Add a .desktop file for git-gui (bug 498801)
- Set ASCIIDOC8 and ASCIIDOC_NO_ROFF to correct documentation issues,
  the sed hack to fix bug 485161 should no longer be needed
- Escape newline in git-daemon xinetd description (bug 502393)
- Add xinetd to git-daemon Requires (bug 504105)
- Organize BuildRequires/Requires, drop redundant expat Requires
- Only build noarch subpackages on Fedora >= 10
- Only build emacs and arch subpackages on Fedora
- Handle curl/libcurl naming for EPEL and Fedora

* Fri Apr 03 2009 Todd Zullinger <tmz@pobox.com> - 1.6.2.2-1
- git-1.6.2.2
- Include contrib/ dir in %%doc (bug 492490)
- Don't set DOCBOOK_XSL_172, fix the '\&.ft' with sed (bug 485161)
- Ignore Branches output from cvsps-2.2b1 (bug 490602)
- Remove shebang from bash-completion script
- Include README in gitweb subpackage

* Mon Mar 09 2009 Todd Zullinger <tmz@pobox.com> - 1.6.2-1
- git-1.6.2
- Include contrib/emacs/README in emacs subpackage
- Drop upstreamed git-web--browse patch

* Tue Feb 24 2009 Todd Zullinger <tmz@pobox.com> - 1.6.1.3-2
- Require perl(Authen::SASL) in git-email (bug 483062)
- Build many of the subpackages as noarch
- Update URL field

* Mon Feb 09 2009 Todd Zullinger <tmz@pobox.com> 1.6.1.3-1
- git-1.6.1.3
- Set htmldir so "git help -w <command>" works
- Patch git-web--browse to not use "/sbin/start" to browse
- Include git-daemon documentation in the git-daemon package

* Thu Jan 29 2009 Josh Boyer <jwboyer@gmail.com> 1.6.1.2-1
- git-1.6.1.2

* Mon Jan 26 2009 Todd Zullinger <tmz@pobox.com> 1.6.1.1-1
- git-1.6.1.1
- Make compile more verbose

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> 1.6.1-2
- rebuild with new openssl

* Sat Jan 03 2009 Todd Zullinger <tmz@pobox.com> 1.6.1-1
- Install git-* commands in %%{_libexecdir}/git-core, the upstream default
- Remove libcurl from Requires, rpm will pick this up automatically
- Consolidate build/install options in %%make_git (Roland McGrath)
- Include DirectoryIndex in gitweb httpd-config (bug 471692)
- Define DOCBOOK_XSL_172 to fix minor manpage issues
- Rename %%{_var}/lib/git-daemon to %%{_var}/lib/git
- Preserve timestamps on installed files
- Quiet some rpmlint complaints
- Use macros more consistently

* Sat Dec 20 2008 Todd Zullinger <tmz@pobox.com> 1.6.0.6-1
- git-1.6.0.6
- Fixes a local privilege escalation bug in gitweb
  (http://article.gmane.org/gmane.comp.version-control.git/103624)
- Add gitk Requires to git-gui (bug 476308)

* Thu Dec 11 2008 Josh Boyer <jboyer@gmail.com> 1.6.0.5-1
- git-1.6.0.5

* Mon Nov 17 2008 Seth Vidal <skvidal at fedoraproject.org>
- switch from /srv/git to /var/lib/git-daemon for packaging rules compliance

* Fri Nov 14 2008 Josh Boyer <jwboyer@gmail.com> 1.6.0.4-1
- git-1.6.0.4

* Wed Oct 22 2008 Josh Boyer <jwboyer@gmail.com> 1.6.0.3-1
- git-1.6.0.3
- Drop curl requirement in favor of libcurl (bug 449388)
- Add requires for SMTP-SSL perl module to make git-send-email work (bug 443615)

* Thu Aug 28 2008 James Bowes <jbowes@redhat.com> 1.6.0.1-1
- git-1.6.0.1

* Thu Jul 24 2008 James Bowes <jbowes@redhat.com> 1.5.6-4
- git-1.5.6.4

* Thu Jun 19 2008 James Bowes <jbowes@redhat.com> 1.5.6-1
- git-1.5.6

* Tue Jun  3 2008 Stepan Kasal <skasal@redhat.com> 1.5.5.3-2
- use tar.bz2 instead of tar.gz

* Wed May 28 2008 James Bowes <jbowes@redhat.com> 1.5.5.3-1
- git-1.5.5.3

* Mon May 26 2008 James Bowes <jbowes@redhat.com> 1.5.5.2-1
- git-1.5.5.2

* Mon Apr 21 2008 James Bowes <jbowes@redhat.com> 1.5.5.1-1
- git-1.5.5.1

* Wed Apr 09 2008 James Bowes <jbowes@redhat.com> 1.5.5-1
- git-1.5.5

* Fri Apr 04 2008 James Bowes <jbowes@redhat.com> 1.5.4.5-3
- Remove the last two requires on git-core.

* Wed Apr 02 2008 James Bowes <jbowes@redhat.com> 1.5.4.5-2
- Remove a patch that's already upstream.

* Fri Mar 28 2008 James Bowes <jbowes@redhat.com> 1.5.4.5-1
- git-1.5.4.5

* Wed Mar 26 2008 James Bowes <jbowes@redhat.com> 1.5.4.4-4
- Own /etc/bash_completion.d in case bash-completion isn't installed.

* Tue Mar 25 2008 James Bowes <jbowes@redhat.com> 1.5.4.4-3
- Include the sample hooks from contrib/hooks as docs (bug 321151).
- Install the bash completion script from contrib (bug 433255).
- Include the html docs in the 'core' package again (bug 434271).

* Wed Mar 19 2008 James Bowes 1.5.4.4-2
- Obsolete git <= 1.5.4.3, to catch going from F8 to rawhide/F9

* Thu Mar 13 2008 James Bowes <jbowes@redhat.com> 1.5.4.4-1
- git-1.5.4.4

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.4.3-3
- rebuild for new perl (again)

* Sun Feb 24 2008 Bernardo Innocenti <bernie@codewiz.org> 1.5.4.3-2
- Do not silently overwrite /etc/httpd/conf.d/git.conf

* Sat Feb 23 2008 James Bowes <jbowes@redhat.com> 1.5.4.3-1
- git-1.5.4.3
- Include Kristian Høgsberg's changes to rename git-core to
  git and git to git-all.

* Sun Feb 17 2008 James Bowes <jbowes@redhat.com> 1.5.4.2-1
- git-1.5.4.2

* Mon Feb 11 2008 Jeremy Katz <katzj@redhat.com> - 1.5.4.1-2
- Add upstream patch (e62a641de17b172ffc4d3a803085c8afbfbec3d1) to have 
  gitweb rss feeds point be commitdiffs instead of commit

* Sun Feb 10 2008 James Bowes <jbowes@redhat.com> 1.5.4.1-1
- git-1.5.4.1

* Tue Feb 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.4-3
- rebuild for new perl

* Sun Feb 03 2008 James Bowes <jbowes@redhat.com> 1.5.4-1
- Add BuidRequires on gettext.

* Sat Feb 02 2008 James Bowes <jbowes@redhat.com> 1.5.4-1
- git-1.5.4

* Tue Jan 08 2008 James Bowes <jbowes@redhat.com> 1.5.3.8-1
- git-1.5.3.8

* Fri Dec 21 2007 James Bowes <jbowes@redhat.com> 1.5.3.7-2
- Have git metapackage require explicit versions (bug 247214)

* Mon Dec 03 2007 Josh Boyer <jwboyer@gmail.com> 1.5.3.7-1
- git-1.5.3.7

* Tue Nov 27 2007 Josh Boyer <jwboyer@gmail.com> 1.5.3.6-1
- git-1.5.3.6
- git-core requires perl(Error) (bug 367861)
- git-svn requires perl(Term:ReadKey) (bug 261361)
- git-email requires perl-Git (bug 333061)

* Wed Oct 24 2007 Lubomir Kundrak <lkundrak@redhat.com> 1.5.3.4-2
- git-Perl requires Error package

* Tue Oct 09 2007 James Bowes <jbowes@redhat.com> 1.5.3.4-1
- git-1.5.3.4

* Sun Sep 30 2007 James Bowes <jbowes@redhat.com> 1.5.3.3-1
- git-1.5.3.3

* Wed Sep 26 2007 James Bowes <jbowes@redhat.com> 1.5.3.2-1
- git-1.5.3.2

* Thu Sep 06 2007 Josh Boyer <jwboyer@jdub.homelinux.org> 1.5.3.1-2
- Include git-gui and git-citool docs

* Thu Sep 06 2007 Josh Boyer <jwboyer@jdub.homelinux.org> 1.5.3.1-1
- git-1.5.3.1-1

* Thu Aug 23 2007 James Bowes <jbowes@redhat.com> 1.5.2.5-1
- git-1.5.2.5-1

* Fri Aug 03 2007 Josh Boyer <jwboyer@jdub.homelinux.org> 1.5.2.4-1
- git-1.5.2.4-1

* Tue Jul 03 2007 Josh Boyer <jwboyer@jdub.homelinux.org> 1.5.2.2-3
- Add git-daemon and gitweb packages

* Thu Jun 21 2007 Josh Boyer <jwboyer@jdub.homelinux.org> 1.5.2.2-2
- Add emacs-git package (#235431)

* Mon Jun 18 2007 James Bowes <jbowes@redhat.com> 1.5.2.2-1
- git-1.5.2.2

* Fri Jun 08 2007 James Bowes <jbowes@redhat.com> 1.5.2.1-1
- git-1.5.2.1

* Sun May 13 2007 Quy Tonthat <qtonthat@gmail.com>
- Added lib files for git-gui
- Added Documentation/technical (As needed by Git Users Manual)

* Tue May 8 2007 Quy Tonthat <qtonthat@gmail.com>
- Added howto files

* Fri Mar 30 2007 Chris Wright <chrisw@redhat.com> 1.5.0.6-1
- git-1.5.0.6

* Mon Mar 19 2007 Chris Wright <chrisw@redhat.com> 1.5.0.5-1
- git-1.5.0.5

* Tue Mar 13 2007 Chris Wright <chrisw@redhat.com> 1.5.0.3-1
- git-1.5.0.3

* Fri Mar 2 2007 Chris Wright <chrisw@redhat.com> 1.5.0.2-2
- BuildRequires perl-devel as of perl-5.8.8-14 (bz 230680)

* Mon Feb 26 2007 Chris Wright <chrisw@redhat.com> 1.5.0.2-1
- git-1.5.0.2

* Tue Feb 13 2007 Nicolas Pitre <nico@cam.org>
- Update core package description (Git isn't as stupid as it used to be)

* Mon Feb 12 2007 Junio C Hamano <junkio@cox.net>
- Add git-gui and git-citool.

* Sun Dec 10 2006 Chris Wright <chrisw@redhat.com> 1.4.4.2-2
- no need to install manpages executable (bz 216790)
- use bytes for git-cvsserver

* Sun Dec 10 2006 Chris Wright <chrisw@redhat.com> 1.4.4.2-1
- git-1.4.4.2

* Mon Nov 6 2006 Jindrich Novy <jnovy@redhat.com> 1.4.2.4-2
- rebuild against the new curl

* Tue Oct 17 2006 Chris Wright <chrisw@redhat.com> 1.4.2.4-1
- git-1.4.2.4

* Wed Oct 4 2006 Chris Wright <chrisw@redhat.com> 1.4.2.3-1
- git-1.4.2.3

* Fri Sep 22 2006 Chris Wright <chrisw@redhat.com> 1.4.2.1-1
- git-1.4.2.1

* Mon Sep 11 2006 Chris Wright <chrisw@redhat.com> 1.4.2-1
- git-1.4.2

* Thu Jul 6 2006 Chris Wright <chrisw@redhat.com> 1.4.1-1
- git-1.4.1

* Tue Jun 13 2006 Chris Wright <chrisw@redhat.com> 1.4.0-1
- git-1.4.0

* Thu May 4 2006 Chris Wright <chrisw@redhat.com> 1.3.3-1
- git-1.3.3
- enable git-email building, prereqs have been relaxed

* Thu May 4 2006 Chris Wright <chrisw@redhat.com> 1.3.2-1
- git-1.3.2

* Fri Apr 28 2006 Chris Wright <chrisw@redhat.com> 1.3.1-1
- git-1.3.1

* Wed Apr 19 2006 Chris Wright <chrisw@redhat.com> 1.3.0-1
- git-1.3.0

* Mon Apr 10 2006 Chris Wright <chrisw@redhat.com> 1.2.6-1
- git-1.2.6

* Wed Apr 5 2006 Chris Wright <chrisw@redhat.com> 1.2.5-1
- git-1.2.5

* Wed Mar 1 2006 Chris Wright <chrisw@redhat.com> 1.2.4-1
- git-1.2.4

* Wed Feb 22 2006 Chris Wright <chrisw@redhat.com> 1.2.3-1
- git-1.2.3

* Tue Feb 21 2006 Chris Wright <chrisw@redhat.com> 1.2.2-1
- git-1.2.2

* Thu Feb 16 2006 Chris Wright <chrisw@redhat.com> 1.2.1-1
- git-1.2.1

* Mon Feb 13 2006 Chris Wright <chrisw@redhat.com> 1.2.0-1
- git-1.2.0

* Wed Feb 1 2006 Chris Wright <chrisw@redhat.com> 1.1.6-1
- git-1.1.6

* Tue Jan 24 2006 Chris Wright <chrisw@redhat.com> 1.1.4-1
- git-1.1.4

* Sun Jan 15 2006 Chris Wright <chrisw@redhat.com> 1.1.2-1
- git-1.1.2

* Tue Jan 10 2006 Chris Wright <chrisw@redhat.com> 1.1.1-1
- git-1.1.1

* Tue Jan 10 2006 Chris Wright <chrisw@redhat.com> 1.1.0-1
- Update to latest git-1.1.0 (drop git-email for now)
- Now creates multiple packages:
-        git-core, git-svn, git-cvs, git-arch, gitk

* Mon Nov 14 2005 H. Peter Anvin <hpa@zytor.com> 0.99.9j-1
- Change subpackage names to git-<name> instead of git-core-<name>
- Create empty root package which brings in all subpackages
- Rename git-tk -> gitk

* Thu Nov 10 2005 Chris Wright <chrisw@osdl.org> 0.99.9g-1
- zlib dependency fix
- Minor cleanups from split
- Move arch import to separate package as well

* Tue Sep 27 2005 Jim Radford <radford@blackbean.org>
- Move programs with non-standard dependencies (svn, cvs, email)
  into separate packages

* Tue Sep 27 2005 H. Peter Anvin <hpa@zytor.com>
- parallelize build
- COPTS -> CFLAGS

* Fri Sep 16 2005 Chris Wright <chrisw@osdl.org> 0.99.6-1
- update to 0.99.6

* Fri Sep 16 2005 Horst H. von Brand <vonbrand@inf.utfsm.cl>
- Linus noticed that less is required, added to the dependencies

* Sun Sep 11 2005 Horst H. von Brand <vonbrand@inf.utfsm.cl>
- Updated dependencies
- Don't assume manpages are gzipped

* Thu Aug 18 2005 Chris Wright <chrisw@osdl.org> 0.99.4-4
- drop sh_utils, sh-utils, diffutils, mktemp, and openssl Requires
- use RPM_OPT_FLAGS in spec file, drop patch0

* Wed Aug 17 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.99.4-3
- use dist tag to differentiate between branches
- use rpm optflags by default (patch0)
- own %%{_datadir}/git-core/

* Mon Aug 15 2005 Chris Wright <chrisw@osdl.org>
- update spec file to fix Buildroot, Requires, and drop Vendor

* Sun Aug 07 2005 Horst H. von Brand <vonbrand@inf.utfsm.cl>
- Redid the description
- Cut overlong make line, loosened changelog a bit
- I think Junio (or perhaps OSDL?) should be vendor...

* Thu Jul 14 2005 Eric Biederman <ebiederm@xmission.com>
- Add the man pages, and the --without docs build option

* Thu Jul 7 2005 Chris Wright <chris@osdl.org>
- initial git spec file
