# Pass --without docs to rpmbuild if you don't want the documentation
%bcond_without docs

# Pass --without tests to rpmbuild if you don't want to run the tests
%bcond_without tests

%global gitexecdir          %{_libexecdir}/git-core

# Settings for Fedora > 29 and EL > 7
%if 0%{?fedora} > 29 || 0%{?rhel} > 7
%bcond_with                 python2
%else
%bcond_without              python2
%endif

# Settings for Fedora >= 29 and EL > 7
%if 0%{?fedora} >= 29 || 0%{?rhel} > 7
%global gitweb_httpd_conf   gitweb.conf
%else
%global gitweb_httpd_conf   git.conf
%endif

# Settings for Fedora and EL > 7
%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without              python3
# linkchcker is not available on EL <= 7
%bcond_without              linkcheck
%global use_glibc_langpacks 1
%global use_perl_generators 1
%global use_perl_interpreter 1
%else
%bcond_with                 python3
%bcond_with                 linkcheck
%global use_glibc_langpacks 0
%global use_perl_generators 0
%global use_perl_interpreter 0
%endif

# Settings for Fedora and EL >= 7
%if 0%{?fedora} || 0%{?rhel} >= 7
%global bashcomp_pkgconfig  1
%global bashcompdir         %(pkg-config --variable=completionsdir bash-completion 2>/dev/null)
%global bashcomproot        %(dirname %{bashcompdir} 2>/dev/null)
%global emacs_filesystem    1
%global libsecret           1
%global use_new_rpm_filters 1
%global use_systemd         1
%else
%global bashcomp_pkgconfig  0
%global bashcompdir         %{_sysconfdir}/bash_completion.d
%global bashcomproot        %{bashcompdir}
%global emacs_filesystem    0
%global libsecret           0
%global use_new_rpm_filters 0
%global use_systemd         0
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%endif

# Allow cvs subpackage to be toggled via --with/--without
# Disable cvs subpackage by default on EL > 7
%if 0%{?rhel} > 7
%bcond_with                 cvs
%else
%bcond_without              cvs
%endif

# Allow p4 subpackage to be toggled via --with/--without
# Disable by default if we lack python2 support
%if %{without python2}
%bcond_with                 p4
%else
%bcond_without              p4
%endif

# Hardening flags for EL-7
%if 0%{?rhel} == 7
%global _hardened_build     1
%endif

# Hardening flags for EL-6
%if 0%{?rhel} == 6
%global build_cflags        %{build_cflags} -fPIC -pie
%global build_ldflags       -Wl,-z,relro -Wl,-z,now
%endif

# Define for release candidates
#global rcrev   .rc0

%global _trivial .0
%global _buildid .2
%global tarball_version 2.23.0

Name:           git
Version:        2.23.1
Release:        0%{?rcrev}%{?dist}%{?_trivial}%{?_buildid}
Summary:        Fast Version Control System
License:        GPLv2
URL:            https://git-scm.com/
Source0:        https://www.kernel.org/pub/software/scm/git/%{?rcrev:testing/}%{name}-%{tarball_version}%{?rcrev}.tar.xz
Source1:        https://www.kernel.org/pub/software/scm/git/%{?rcrev:testing/}%{name}-%{tarball_version}%{?rcrev}.tar.sign

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

# Local sources begin at 10 to allow for additional future upstream sources
Source11:       git.xinetd.in
Source12:       git-gui.desktop
Source13:       gitweb-httpd.conf
Source14:       gitweb.conf.in
Source15:       git@.service.in
Source16:       git.socket

# Script to print test failure output (used in %%check)
Source99:       print-failed-test-output

# https://bugzilla.redhat.com/490602
Patch0:         git-cvsimport-Ignore-cvsps-2.2b1-Branches-output.patch

# Amazon patches
Patch10001:     v2.23.0-to-v2.23.1.patch

%if %{with docs}
# pod2man is needed to build Git.3pm
BuildRequires:  %{_bindir}/pod2man
BuildRequires:  asciidoc >= 8.4.1
BuildRequires:  xmlto
%if %{with linkcheck}
BuildRequires:  linkchecker
%endif
# endif with linkcheck
%endif
# endif with docs
BuildRequires:  desktop-file-utils
BuildRequires:  emacs
BuildRequires:  expat-devel
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gnupg2
BuildRequires:  libcurl-devel
%if %{libsecret}
BuildRequires:  libsecret-devel
%endif
# endif libsecret
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  perl(Error)
BuildRequires:  perl(Test)
%if %{use_perl_generators}
BuildRequires:  perl-generators
%endif
# endif use_perl_generators
%if %{use_perl_interpreter}
BuildRequires:  perl-interpreter
%else
BuildRequires:  perl
%endif
# endif use_perl_interpreter
%if %{bashcomp_pkgconfig}
BuildRequires:  pkgconfig(bash-completion)
%endif
# endif bashcomp_pkgconfig
BuildRequires:  sed
%if %{use_systemd}
# For macros
BuildRequires:  systemd
%endif
# endif use_systemd
BuildRequires:  tcl
BuildRequires:  tk
BuildRequires:  zlib-devel >= 1.2

%if %{with tests}
# Test suite requirements
BuildRequires:  acl
%if 0%{?fedora} >= 27 || 0%{?rhel} > 7
# Needed by t5540-http-push-webdav.sh
BuildRequires: apr-util-bdb
%endif
# endif fedora >= 27
BuildRequires:  bash
%if %{with cvs}
BuildRequires:  cvs
BuildRequires:  cvsps
%endif
# endif with cvs
%if %{use_glibc_langpacks}
# glibc-all-langpacks and glibc-langpack-is are needed for GETTEXT_LOCALE and
# GETTEXT_ISO_LOCALE test prereq's, glibc-langpack-en ensures en_US.UTF-8.
BuildRequires:  glibc-all-langpacks
BuildRequires:  glibc-langpack-en
BuildRequires:  glibc-langpack-is
%endif
# endif use_glibc_langpacks
%if 0%{?fedora} && 0%{?fedora} < 30
BuildRequires:  gnupg
%endif
# endif fedora < 30
%if 0%{?fedora} || 0%{?rhel} > 8
BuildRequires:  gnupg2-smime
%endif
# endif fedora or el > 8
%if 0%{?fedora} || ( 0%{?rhel} && ( 0%{?rhel} == 6 || 0%{?rhel} >= 7 && %{_arch} != ppc64 ))
BuildRequires:  highlight
%endif
# endif fedora, el-6, or el7-ppc64
BuildRequires:  httpd
%if 0%{?fedora} && ! ( 0%{?fedora} > 30 || %{_arch} == i386 || %{_arch} == s390x )
BuildRequires:  jgit
%endif
# endif fedora (except i386 and s390x)
BuildRequires:  mod_dav_svn
BuildRequires:  perl(App::Prove)
BuildRequires:  perl(CGI)
BuildRequires:  perl(CGI::Carp)
BuildRequires:  perl(CGI::Util)
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(HTTP::Date)
BuildRequires:  perl(IO::Pty)
BuildRequires:  perl(JSON)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(Mail::Address)
BuildRequires:  perl(Memoize)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::HiRes)
%if %{with python2}
BuildRequires:  python2-devel
%endif
# endif with python2
%if %{with python3}
BuildRequires:  python3-devel
%endif
# endif with python3
BuildRequires:  subversion
BuildRequires:  subversion-perl
BuildRequires:  time
%endif
# endif with tests

Requires:       git-core = %{version}-%{release}
Requires:       git-core-doc = %{version}-%{release}
%if ! %{defined perl_bootstrap}
Requires:       perl(Term::ReadKey)
%endif
# endif ! defined perl_bootstrap
Requires:       perl-Git = %{version}-%{release}

%if %{emacs_filesystem} && %{defined _emacs_version}
Requires:       emacs-filesystem >= %{_emacs_version}
%endif
# endif emacs_filesystem

# Obsolete git-cvs if it's disabled
%if %{without cvs}
Obsoletes:      git-cvs < %{?epoch:%{epoch}:}%{version}-%{release}
%endif
# endif without cvs

# Obsolete gnome-keyring credential helper (remove after Fedora 29)
%if 0%{?fedora} && 0%{?fedora} < 30
Obsoletes:      git-gnome-keyring < 2.17.2-2
%endif
# endif fedora < 30

# Obsolete git-p4 if it's disabled
%if %{without p4}
Obsoletes:      git-p4 < %{?epoch:%{epoch}:}%{version}-%{release}
%endif
# endif without p4

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs common set of tools which are usually using with
small amount of dependencies. To install all git packages, including
tools for integrating with other SCMs, install the git-all meta-package.

%package all
Summary:        Meta-package to pull in all git tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}
%if %{with cvs}
Requires:       git-cvs = %{version}-%{release}
%endif
# endif with cvs
Requires:       git-email = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
%if %{with p4}
Requires:       git-p4 = %{version}-%{release}
%endif
# endif with p4
Requires:       git-subtree = %{version}-%{release}
Requires:       git-svn = %{version}-%{release}
Requires:       git-instaweb = %{version}-%{release}
Requires:       gitk = %{version}-%{release}
Requires:       perl-Git = %{version}-%{release}
%if ! %{defined perl_bootstrap}
Requires:       perl(Term::ReadKey)
%endif
# endif ! defined perl_bootstrap
%if ! %{emacs_filesystem}
Requires:       emacs-git = %{version}-%{release}
%endif
# endif ! emacs_filesystem
%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

%package core
Summary:        Core package of git with minimal functionality
Requires:       less
Requires:       openssh-clients
Requires:       zlib >= 1.2
%description core
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git-core rpm installs really the core tools with minimal
dependencies. Install git package for common set of tools.
To install all git packages, including tools for integrating with
other SCMs, install the git-all meta-package.

%package core-doc
Summary:        Documentation files for git-core
BuildArch:      noarch
Requires:       git-core = %{version}-%{release}
%description core-doc
Documentation files for git-core package including man pages.

%if %{with cvs}
%package cvs
Summary:        Git tools for importing CVS repositories
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       cvs
Requires:       cvsps
Requires:       perl(DBD::SQLite)
%description cvs
%{summary}.
%endif
# endif with cvs

%package daemon
Summary:        Git protocol daemon
Requires:       git-core = %{version}-%{release}
%if %{use_systemd}
Requires:       systemd
Requires(post): systemd
Requires(preun):  systemd
Requires(postun): systemd
%else
Requires:       xinetd
%endif
# endif use_systemd
%description daemon
The git daemon for supporting git:// access to git repositories

%package email
Summary:        Git tools for sending patches via email
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(Authen::SASL)
Requires:       perl(Net::SMTP::SSL)
%description email
%{summary}.

%if ! %{emacs_filesystem}
%package -n emacs-git
Summary:        Git version control system support for Emacs
Requires:       git = %{version}-%{release}
BuildArch:      noarch
Requires:       emacs(bin) >= %{_emacs_version}
Obsoletes:      emacs-git-el < 2.18.0-0.0
Provides:       emacs-git-el = %{version}-%{release}
%description -n emacs-git
%{summary}.
%endif
# endif ! emacs_filesystem

%package -n gitk
Summary:        Git repository browser
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       tk >= 8.4
%description -n gitk
%{summary}.

%package -n gitweb
Summary:        Simple web interface to git repositories
BuildArch:      noarch
Requires:       git = %{version}-%{release}
%description -n gitweb
%{summary}.

%package gui
Summary:        Graphical interface to Git
BuildArch:      noarch
Requires:       gitk = %{version}-%{release}
Requires:       tk >= 8.4
%description gui
%{summary}.

%package instaweb
Summary:        Repository browser in gitweb
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       gitweb = %{version}-%{release}

%description instaweb
A simple script to set up gitweb and a web server for browsing the local
repository.

%if %{with p4}
%package p4
Summary:        Git tools for working with Perforce depots
BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       git = %{version}-%{release}
%description p4
%{summary}.
%endif
# endif with p4

%package -n perl-Git
Summary:        Perl interface to Git
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%description -n perl-Git
%{summary}.

%package -n perl-Git-SVN
Summary:        Perl interface to Git::SVN
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%description -n perl-Git-SVN
%{summary}.

%package subtree
Summary:        Git tools to merge and split repositories
Requires:       git-core = %{version}-%{release}
%description subtree
Git subtrees allow subprojects to be included within a subdirectory
of the main project, optionally including the subproject's entire
history.

%package svn
Summary:        Git tools for interacting with Subversion repositories
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(Digest::MD5)
%if ! %{defined perl_bootstrap}
Requires:       perl(Term::ReadKey)
%endif
# endif ! defined perl_bootstrap
Requires:       subversion
%description svn
%{summary}.

%prep
# Verify GPG signatures
gpghome="$(mktemp -qd)" # Ensure we don't use any existing gpg keyrings
# Convert the ascii-armored key to binary
# (use --yes to ensure an existing dearmored key is overwritten)
gpg2 --homedir "$gpghome" --dearmor --quiet --yes %{SOURCE9}
xz -dc %{SOURCE0} | # Upstream signs the uncompressed tarballs
    gpgv2 --homedir "$gpghome" --quiet --keyring %{SOURCE9}.gpg %{SOURCE1} -
rm -rf "$gpghome" # Cleanup tmp gpg home dir

# Ensure a blank line follows autosetup, el6 chokes otherwise
# https://bugzilla.redhat.com/1310704
%autosetup -p1 -n %{name}-%{tarball_version}%{?rcrev}

# Install print-failed-test-output script
install -p -m 755 %{SOURCE99} print-failed-test-output

# Remove git-archimport from command list
sed -i '/^git-archimport/d' command-list.txt

%if %{without cvs}
# Remove git-cvs* from command list
sed -i '/^git-cvs/d' command-list.txt
%endif
# endif without cvs

%if %{without p4}
# Remove git-p4 from command list
sed -i '/^git-p4/d' command-list.txt
%endif
# endif without p4

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
cat << \EOF > config.mak
V = 1
CFLAGS = %{build_cflags}
LDFLAGS = %{build_ldflags}
NEEDS_CRYPTO_WITH_SSL = 1
USE_LIBPCRE = 1
ETC_GITCONFIG = %{_sysconfdir}/gitconfig
INSTALL_SYMLINKS = 1
GITWEB_PROJECTROOT = %{_localstatedir}/lib/git
GNU_ROFF = 1
NO_PERL_CPAN_FALLBACKS = 1
%if %{with python2}
PYTHON_PATH = %{__python2}
%else
NO_PYTHON = 1
%endif
# endif with python2
htmldir = %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
prefix = %{_prefix}
perllibdir = %{perl_vendorlib}
gitwebdir = %{_localstatedir}/www/git

# Test options
DEFAULT_TEST_TARGET = prove
GIT_PROVE_OPTS = --verbose --normalize %{?_smp_mflags} --formatter=TAP::Formatter::File
GIT_TEST_OPTS = -x --verbose-log
EOF

# Print config.mak to aid confirmation/verification of settings
cat config.mak

# Filter bogus perl requires
# packed-refs comes from a comment in contrib/hooks/update-paranoid
%if %{use_new_rpm_filters}
%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(packed-refs\\)
%if ! %{defined perl_bootstrap}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Term::ReadKey\\)
%endif
# endif ! defined perl_bootstrap
%else
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
sed -e '/perl(packed-refs)/d'
EOF

%global __perl_requires %{_builddir}/%{name}-%{version}%{?rcrev}/%{name}-req
chmod +x %{__perl_requires}
%endif
# endif use_new_rpm_filters

# Remove Git::LoadCPAN to ensure we use only system perl modules.  This also
# allows the dependencies to be automatically processed by rpm.
rm -rf perl/Git/LoadCPAN{.pm,/}
grep -rlZ '^use Git::LoadCPAN::' | xargs -r0 sed -i 's/Git::LoadCPAN:://g'

# Update gitweb default home link string
sed -i 's@"++GITWEB_HOME_LINK_STR++"@$ENV{"SERVER_NAME"} ? "git://" . $ENV{"SERVER_NAME"} : "projects"@' \
    gitweb/gitweb.perl

# Move contrib/{contacts,subtree} docs to Documentation so they build with the
# proper asciidoc/docbook/xmlto options
mv contrib/{contacts,subtree}/git-*.txt Documentation/

%build
# Improve build reproducibility
export TZ=UTC
export SOURCE_DATE_EPOCH=$(date -r version +%%s 2>/dev/null)

%make_build all %{?with_docs:doc}

%make_build -C contrib/contacts/ all

%if %{libsecret}
%make_build -C contrib/credential/libsecret/
%endif
# endif libsecret

%make_build -C contrib/diff-highlight/

%make_build -C contrib/subtree/ all

# Fix shebang in a few places to silence rpmlint complaints
%if %{with python2}
sed -i -e '1s@#! */usr/bin/env python$@#!%{__python2}@' \
    contrib/fast-import/import-zips.py \
    contrib/hg-to-git/hg-to-git.py \
    contrib/hooks/multimail/git_multimail.py \
    contrib/hooks/multimail/migrate-mailhook-config \
    contrib/hooks/multimail/post-receive.example \
    contrib/svn-fe/svnrdump_sim.py
%else
# Remove contrib/fast-import/import-zips.py, contrib/hg-to-git, and
# contrib/svn-fe which all require python2.
rm -rf contrib/fast-import/import-zips.py contrib/hg-to-git contrib/svn-fe
%endif
# endif with python2

# The multimail hook is installed with git.  Use python3 to avoid an
# unnecessary python2 dependency, if possible.
%if %{with python3}
sed -i -e '1s@#!\( */usr/bin/env python\|%{__python2}\)$@#!%{__python3}@' \
    contrib/hooks/multimail/git_multimail.py \
    contrib/hooks/multimail/migrate-mailhook-config \
    contrib/hooks/multimail/post-receive.example
%endif
# endif with python3

%install
%make_install %{?with_docs:install-doc}

%make_install -C contrib/contacts

%global elispdir %{_emacs_sitelispdir}/git
pushd contrib/emacs >/dev/null
for el in *.el ; do
    # Note: No byte-compiling is done.  These .el files are one-line stubs
    # which only serve to point users to better alternatives.
    install -Dpm 644 $el %{buildroot}%{elispdir}/$el
    rm -f $el # clean up to avoid cruft in git-core-doc
done
popd >/dev/null

%if %{libsecret}
install -pm 755 contrib/credential/libsecret/git-credential-libsecret \
    %{buildroot}%{gitexecdir}
%endif
# endif libsecret
install -pm 755 contrib/credential/netrc/git-credential-netrc \
    %{buildroot}%{gitexecdir}
# temporarily move contrib/credential/netrc aside to prevent it from being
# deleted in the docs preparation, so the tests can be run in %%check
mv contrib/credential/netrc .

%make_install -C contrib/subtree

mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -pm 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{gitweb_httpd_conf}
sed "s|@PROJECTROOT@|%{_localstatedir}/lib/git|g" \
    %{SOURCE14} > %{buildroot}%{_sysconfdir}/gitweb.conf

# install contrib/diff-highlight and clean up to avoid cruft in git-core-doc
install -Dpm 0755 contrib/diff-highlight/diff-highlight \
    %{buildroot}%{_datadir}/git-core/contrib/diff-highlight
rm -rf contrib/diff-highlight/{Makefile,diff-highlight,*.perl,t}

# Clean up contrib/subtree to avoid cruft in the git-core-doc docdir
rm -rf contrib/subtree/{INSTALL,Makefile,git-subtree*,t}

# git-archimport is not supported
find %{buildroot} Documentation -type f -name 'git-archimport*' -exec rm -f {} ';'

%if %{without cvs}
# Remove git-cvs* and gitcvs*
find %{buildroot} Documentation \( -type f -o -type l \) \
    \( -name 'git-cvs*' -o -name 'gitcvs*' \) -exec rm -f {} ';'
%endif
# endif without cvs

%if %{without p4}
# Remove git-p4* and mergetools/p4merge
find %{buildroot} Documentation -type f -name 'git-p4*' -exec rm -f {} ';'
rm -f %{buildroot}%{gitexecdir}/mergetools/p4merge
%endif
# endif without p4

# Remove unneeded git-remote-testsvn so git-svn can be noarch
rm -f %{buildroot}%{gitexecdir}/git-remote-testsvn

exclude_re="archimport|email|git-(citool|cvs|daemon|gui|instaweb|p4|subtree|svn)|gitk|gitweb|p4merge"
(find %{buildroot}{%{_bindir},%{_libexecdir}} -type f -o -type l | grep -vE "$exclude_re" | sed -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}{%{_bindir},%{_libexecdir}} -mindepth 1 -type d | grep -vE "$exclude_re" | sed -e 's@^%{buildroot}@%dir @') >> bin-man-doc-files
(find %{buildroot}%{perl_vendorlib} -type f | sed -e s@^%{buildroot}@@) > perl-git-files
(find %{buildroot}%{perl_vendorlib} -mindepth 1 -type d | sed -e 's@^%{buildroot}@%dir @') >> perl-git-files
# Split out Git::SVN files
grep Git/SVN perl-git-files > perl-git-svn-files
sed -i "/Git\/SVN/ d" perl-git-files
%if %{with docs}
(find %{buildroot}%{_mandir} -type f | grep -vE "$exclude_re|Git" | sed -e s@^%{buildroot}@@ -e 's/$/*/' ) >> bin-man-doc-files
%else
rm -rf %{buildroot}%{_mandir}
%endif
# endif with docs

mkdir -p %{buildroot}%{_localstatedir}/lib/git
%if %{use_systemd}
install -Dp -m 0644 %{SOURCE16} %{buildroot}%{_unitdir}/git.socket
perl -p \
    -e "s|\@GITEXECDIR\@|%{gitexecdir}|g;" \
    -e "s|\@BASE_PATH\@|%{_localstatedir}/lib/git|g;" \
    %{SOURCE15} > %{buildroot}%{_unitdir}/git@.service
%else
mkdir -p %{buildroot}%{_sysconfdir}/xinetd.d
perl -p \
    -e "s|\@GITEXECDIR\@|%{gitexecdir}|g;" \
    -e "s|\@BASE_PATH\@|%{_localstatedir}/lib/git|g;" \
    %{SOURCE11} > %{buildroot}%{_sysconfdir}/xinetd.d/git
%endif
# endif use_systemd

# Setup bash completion
install -Dpm 644 contrib/completion/git-completion.bash %{buildroot}%{bashcompdir}/git
ln -s git %{buildroot}%{bashcompdir}/gitk

# Install tcsh completion
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-completion.tcsh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

# Drop .py extension from git_multimail to avoid byte-compiling
mv contrib/hooks/multimail/git_multimail{.py,}

# Move contrib/hooks out of %%docdir
mkdir -p %{buildroot}%{_datadir}/git-core/contrib
mv contrib/hooks %{buildroot}%{_datadir}/git-core/contrib
pushd contrib > /dev/null
ln -s ../../../git-core/contrib/hooks
popd > /dev/null

# Install git-prompt.sh
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-prompt.sh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

# install git-gui .desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE12}

# symlink git-citool to git-gui if they are identical
pushd %{buildroot}%{gitexecdir} >/dev/null
if cmp -s git-gui git-citool 2>/dev/null; then
    ln -svf git-gui git-citool
fi
popd >/dev/null

# find translations
%find_lang %{name} %{name}.lang
cat %{name}.lang >> bin-man-doc-files

# quiet some rpmlint complaints
chmod -R g-w %{buildroot}
chmod a-x %{buildroot}%{gitexecdir}/git-mergetool--lib
# These files probably are not needed
find . -regex '.*/\.\(git\(attributes\|ignore\)\|perlcriticrc\)' -delete
chmod a-x Documentation/technical/api-index.sh
find contrib -type f -print0 | xargs -r0 chmod -x

# Split core files
not_core_re="git-(add--interactive|contacts|credential-(libsecret|netrc)|difftool|filter-branch|instaweb|request-pull|send-mail)|gitweb"
grep -vE "$not_core_re|%{_mandir}" bin-man-doc-files > bin-files-core
touch man-doc-files-core
%if %{with docs}
grep -vE "$not_core_re" bin-man-doc-files | grep "%{_mandir}" > man-doc-files-core
%endif
# endif with docs
grep -E  "$not_core_re" bin-man-doc-files > bin-man-doc-git-files

##### DOC
# place doc files into %%{_pkgdocdir} and split them into expected packages
# contrib
not_core_doc_re="(git-(cvs|gui|citool|daemon|instaweb|subtree))|p4|svn|email|gitk|gitweb"
mkdir -p %{buildroot}%{_pkgdocdir}/
cp -pr README.md Documentation/*.txt Documentation/RelNotes contrib %{buildroot}%{_pkgdocdir}/
# Remove contrib/ files/dirs which have nothing useful for documentation
rm -rf %{buildroot}%{_pkgdocdir}/contrib/{contacts,credential,svn-fe}/
cp -p gitweb/INSTALL %{buildroot}%{_pkgdocdir}/INSTALL.gitweb
cp -p gitweb/README %{buildroot}%{_pkgdocdir}/README.gitweb

%if %{with docs}
cp -pr Documentation/*.html Documentation/docbook-xsl.css %{buildroot}%{_pkgdocdir}/
cp -pr Documentation/{howto,technical} %{buildroot}%{_pkgdocdir}/
find %{buildroot}%{_pkgdocdir}/{howto,technical} -type f \
    |grep -o "%{_pkgdocdir}.*$" >> man-doc-files-core
%endif
# endif with docs

{
    find %{buildroot}%{_pkgdocdir} -type f -maxdepth 1 \
        | grep -o "%{_pkgdocdir}.*$" \
        | grep -vE "$not_core_doc_re"
    find %{buildroot}%{_pkgdocdir}/{contrib,RelNotes} -type f \
        | grep -o "%{_pkgdocdir}.*$"
    find %{buildroot}%{_pkgdocdir} -type d | grep -o "%{_pkgdocdir}.*$" \
        | sed "s/^/\%dir /"
} >> man-doc-files-core
##### #DOC

%check
%if %{without tests}
echo "*** Skipping tests"
exit 0
%endif
# endif without tests

%if %{with docs} && %{with linkcheck}
# Test links in HTML documentation
find %{buildroot}%{_pkgdocdir} -name "*.html" -print0 | xargs -r0 linkchecker
%endif
# endif with docs && with linkcheck

# Tests to skip on all releases and architectures
GIT_SKIP_TESTS=""

%ifarch aarch64 %{arm} %{power64}
# Skip tests which fail on aarch64, arm, and ppc
#
# The following 2 tests use run_with_limited_cmdline, which calls ulimit -s 128
# to limit the maximum stack size.
# t5541.34 'push 2000 tags over http'
# t5551.25 'clone the 2,000 tag repo to check OS command line overflow'
GIT_SKIP_TESTS="$GIT_SKIP_TESTS t5541.34 t5551.25"
%endif
# endif aarch64 %%{arm} %%{power64}

%ifarch %{power64}
# Skip tests which fail on ppc
#
# t9115-git-svn-dcommit-funky-renames is disabled because it frequently fails.
# The port it uses (9115) is already in use.  It is unclear if this is
# due to an issue in the test suite or a conflict with some other process on
# the build host.  It only appears to occur on ppc-arches.
GIT_SKIP_TESTS="$GIT_SKIP_TESTS t9115"
%endif
# endif %%{power64}

export GIT_SKIP_TESTS

# Set LANG so various UTF-8 tests are run
export LANG=en_US.UTF-8

# Explicitly enable tests which may be skipped opportunistically
# (Check for variables set via test_tristate in the test suite)
export GIT_SVN_TEST_HTTPD=true
export GIT_TEST_GIT_DAEMON=true
export GIT_TEST_HTTPD=true
export GIT_TEST_SVNSERVE=true

# Create tmpdir for test output and update GIT_TEST_OPTS
# Also update GIT-BUILD-OPTIONS to keep make from any needless rebuilding
testdir=$(mktemp -d -p /tmp git-t.XXXX)
sed -i "s@^GIT_TEST_OPTS = .*@& --root=$testdir@" config.mak
touch -r GIT-BUILD-OPTIONS ts
sed -i "s@\(GIT_TEST_OPTS='.*\)'@\1 --root=$testdir'@" GIT-BUILD-OPTIONS
touch -r ts GIT-BUILD-OPTIONS

# Run the tests
make test || ./print-failed-test-output

# Run contrib/credential/netrc tests
mkdir -p contrib/credential
mv netrc contrib/credential/
make -C contrib/credential/netrc/ test || \
make -C contrib/credential/netrc/ testverbose

# Clean up test dir
rmdir --ignore-fail-on-non-empty "$testdir"

%if %{use_systemd}
%post daemon
%systemd_post git@.service

%preun daemon
%systemd_preun git@.service

%postun daemon
%systemd_postun_with_restart git@.service
%endif
# endif use_systemd

%files -f bin-man-doc-git-files
%if %{emacs_filesystem}
%{elispdir}
%endif
# endif emacs_filesystem
%{_datadir}/git-core/contrib/diff-highlight
%{_datadir}/git-core/contrib/hooks/multimail
%{_datadir}/git-core/contrib/hooks/update-paranoid
%{_datadir}/git-core/contrib/hooks/setgitperms.perl
%{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%{_datadir}/git-core/templates/hooks/pre-rebase.sample
%{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample

%files all
# No files for you!

%files core -f bin-files-core
#NOTE: this is only use of the %%doc macro in this spec file and should not
#      be used elsewhere
%{!?_licensedir:%global license %doc}
%license COPYING
# exclude is best way here because of troubles with symlinks inside git-core/
%exclude %{_datadir}/git-core/contrib/diff-highlight
%exclude %{_datadir}/git-core/contrib/hooks/multimail
%exclude %{_datadir}/git-core/contrib/hooks/update-paranoid
%exclude %{_datadir}/git-core/contrib/hooks/setgitperms.perl
%exclude %{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%exclude %{_datadir}/git-core/templates/hooks/pre-rebase.sample
%exclude %{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample
%{bashcomproot}
%{_datadir}/git-core/

%files core-doc -f man-doc-files-core
%if 0%{?rhel} && 0%{?rhel} <= 7
# .py files are only bytecompiled on EL <= 7
%exclude %{_pkgdocdir}/contrib/*/*.py[co]
%endif
# endif rhel <= 7
%{_pkgdocdir}/contrib/hooks

%if %{with cvs}
%files cvs
%{_pkgdocdir}/*git-cvs*.txt
%{_bindir}/git-cvsserver
%{gitexecdir}/*cvs*
%{?with_docs:%{_mandir}/man1/*cvs*.1*}
%{?with_docs:%{_pkgdocdir}/*git-cvs*.html}
%endif
# endif with cvs

%files daemon
%{_pkgdocdir}/git-daemon*.txt
%if %{use_systemd}
%{_unitdir}/git.socket
%{_unitdir}/git@.service
%else
%config(noreplace)%{_sysconfdir}/xinetd.d/git
%endif
# endif use_systemd
%{gitexecdir}/git-daemon
%{_localstatedir}/lib/git
%{?with_docs:%{_mandir}/man1/git-daemon*.1*}
%{?with_docs:%{_pkgdocdir}/git-daemon*.html}

%if ! %{emacs_filesystem}
%files -n emacs-git
%{_pkgdocdir}/contrib/emacs/README
%{elispdir}
%endif
# endif ! emacs_filesystem

%files email
%{_pkgdocdir}/*email*.txt
%{gitexecdir}/*email*
%{?with_docs:%{_mandir}/man1/*email*.1*}
%{?with_docs:%{_pkgdocdir}/*email*.html}

%files -n gitk
%{_pkgdocdir}/*gitk*.txt
%{_bindir}/*gitk*
%{_datadir}/gitk
%{?with_docs:%{_mandir}/man1/*gitk*.1*}
%{?with_docs:%{_pkgdocdir}/*gitk*.html}

%files -n gitweb
%{_pkgdocdir}/*.gitweb
%{_pkgdocdir}/gitweb*.txt
%{?with_docs:%{_mandir}/man1/gitweb.1*}
%{?with_docs:%{_mandir}/man5/gitweb.conf.5*}
%{?with_docs:%{_pkgdocdir}/gitweb*.html}
%config(noreplace)%{_sysconfdir}/gitweb.conf
%config(noreplace)%{_sysconfdir}/httpd/conf.d/%{gitweb_httpd_conf}
%{_localstatedir}/www/git/

%files gui
%{gitexecdir}/git-gui*
%{gitexecdir}/git-citool
%{_datadir}/applications/*git-gui.desktop
%{_datadir}/git-gui/
%{_pkgdocdir}/git-gui.txt
%{_pkgdocdir}/git-citool.txt
%{?with_docs:%{_mandir}/man1/git-gui.1*}
%{?with_docs:%{_pkgdocdir}/git-gui.html}
%{?with_docs:%{_mandir}/man1/git-citool.1*}
%{?with_docs:%{_pkgdocdir}/git-citool.html}

%files instaweb
%defattr(-,root,root)
%{gitexecdir}/git-instaweb
%{_pkgdocdir}/git-instaweb.txt
%{?with_docs:%{_mandir}/man1/git-instaweb.1*}
%{?with_docs:%{_pkgdocdir}/git-instaweb.html}

%if %{with p4}
%files p4
%{gitexecdir}/*p4*
%{gitexecdir}/mergetools/p4merge
%{_pkgdocdir}/*p4*.txt
%{?with_docs:%{_mandir}/man1/*p4*.1*}
%{?with_docs:%{_pkgdocdir}/*p4*.html}
%endif
# endif with p4

%files -n perl-Git -f perl-git-files
%{?with_docs:%{_mandir}/man3/Git.3pm*}

%files -n perl-Git-SVN -f perl-git-svn-files

%files subtree
%{gitexecdir}/git-subtree
%{_pkgdocdir}/git-subtree.txt
%{?with_docs:%{_mandir}/man1/git-subtree.1*}
%{?with_docs:%{_pkgdocdir}/git-subtree.html}

%files svn
%{gitexecdir}/git-svn
%{_pkgdocdir}/git-svn.txt
%{?with_docs:%{_mandir}/man1/git-svn.1*}
%{?with_docs:%{_pkgdocdir}/git-svn.html}

%changelog
* Fri Dec 13 2019 Trinity Quirk <tquirk@amazon.com> - 2.23.1-0.amzn2.0.2
- Remove git-instaweb dependency on lighttpd

* Mon Dec  9 2019 Frederick Lefebvre <fredlef@amazon.com> - 2.23.1-0.amzn2.0.1
- Update to 2.23.1
- CVE-2019-1348, CVE-2019-1349, CVE-2019-1350, CVE-2019-1351
- CVE-2019-1352, CVE-2019-1353, CVE-2019-1354,
- CVE-2019-1387, CVE-2019-19604

* Fri Aug 16 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-1
- Update to 2.23.0

* Sun Aug 11 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-0.2.rc2
- Update to 2.23.0-rc2

* Fri Aug 02 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-0.1.rc1
- Update to 2.23.0-rc1

* Mon Jul 29 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-0.0.rc0
- Update to 2.23.0-rc0

* Thu Jul 25 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-2
- completion: do not cache if --git-completion-helper fails
- avoid trailing comments in spec file
- drop jgit on Fedora > 30

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 07 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-1
- Update to 2.22.0

* Tue Jun 04 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.22.0-0.7.rc3
- Perl 5.30 re-rebuild updated packages

* Mon Jun 03 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.6.rc3
- Update to 2.22.0-rc3

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.22.0-0.5.rc2
- Perl 5.30 re-rebuild of bootstrapped packages

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.22.0-0.4.rc2
- Perl 5.30 rebuild

* Thu May 30 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.3.rc2
- Update to 2.22.0-rc1

* Fri May 24 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.2.rc1
- Apply upstream fixes for diff-parseopt issues on s390x

* Sun May 19 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.1.rc1
- Update to 2.22.0-rc1

* Mon May 13 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.0.rc0
- Update to 2.22.0-rc0
- Ensure a consistent format for test output
- Improve JGIT test prereq (jgit on Fedora >= 30 is broken)
- Add perl(JSON::PP) BuildRequires for trace2 tests

* Sun Feb 24 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-1
- Update to 2.21.0
- Move gitweb manpages to gitweb package
- Link git-citool to git-gui if they are identical

* Tue Feb 19 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-0.2.rc2
- Update to 2.21.0.rc2

* Fri Feb 15 2019 Todd Zullinger <tmz@pobox.com>
- Set SOURCE_DATE_EPOCH and TZ to improve build reproducibility

* Wed Feb 13 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-0.1.rc1
- Update to 2.21.0.rc1

* Thu Feb 07 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-0.0.rc0
- Update to 2.21.0.rc0
- Remove %%changelog entries prior to 2017

* Thu Jan 31 2019 Todd Zullinger <tmz@pobox.com> - 2.20.1-2
- Remove extraneous pcre BuildRequires
- Add additional BuildRequires for i18n locales used in tests
- Replace gitweb home-link with inline sed
- Add gnupg2-smime and perl JSON BuildRequires for tests
- Work around gpg-agent issues in the test suite
- Drop gnupg BuildRequires on fedora >= 30
- Fix formatting of contrib/{contacts,subtree} docs
- Use %%{build_cflags} and %%{build_ldflags}
- Drop unneeded TEST_SHELL_PATH make variable

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 15 2018 Todd Zullinger <tmz@pobox.com> - 2.20.1-1
- Update to 2.20.1

* Sun Dec 09 2018 Todd Zullinger <tmz@pobox.com> - 2.20.0-1
- Update to 2.20.0

* Sat Dec 01 2018 Todd Zullinger <tmz@pobox.com> - 2.20.0-0.2.rc2
- Update to 2.20.0.rc2

* Wed Nov 21 2018 Todd Zullinger <tmz@pobox.com> - 2.20.0-0.1.rc1
- Update to 2.20.0.rc1

* Wed Nov 21 2018 Todd Zullinger <tmz@pobox.com> - 2.19.2-1
- Update to 2.19.2

* Tue Oct 23 2018 Todd Zullinger <tmz@pobox.com>
- Skip test BuildRequires when --without tests is used
- Simplify gpg verification of Source0
- Use %%{without ...} macro consistently
- Add comments to %%endif statements
- Add glibc-langpack-en BuildRequires for en_US.UTF-8 locale

* Mon Oct 22 2018 Pavel Cahyna <pcahyna@redhat.com> - 2.19.1-2
- Update condition for the t5540-http-push-webdav test for future RHEL

* Fri Oct 05 2018 Todd Zullinger <tmz@pobox.com> - 2.19.1-1
- Update to 2.19.1 (CVE-2018-17456)

* Mon Sep 10 2018 Todd Zullinger <tmz@pobox.com> - 2.19.0-1
- Update to 2.19.0

* Fri Sep 07 2018 Todd Zullinger <tmz@pobox.com> - 2.19.0-0.5.rc2
- Fix smart-http test due to changes in cookie sort order in curl-7.61.1
- Add --without tests option to skip tests

* Thu Sep 06 2018 Sebastian Kisela <skisela@redhat.com> - 2.19.0-0.4.rc2
- Move instaweb to a separate subpackage
- Fix builds without docs and without cvs and/or p4

* Tue Sep 04 2018 Todd Zullinger <tmz@pobox.com> - 2.19.0-0.3.rc2
- Update to 2.19.0.rc2
- Drop unnecessary Conflicts: when git-p4 is disabled
- Obsolete git-cvs if it's disabled
- Remove contrib/fast-import/import-zips.py, contrib/hg-to-git, and
  contrib/svn-fe which all require python2
- Drop git-gnome-keyring obsolete for fedora > 30

* Tue Sep 04 2018 Nils Philippsen <nils@redhat.com> - 2.19.0-0.2.rc1
- obsolete git-p4 if it's disabled

* Tue Aug 28 2018 Todd Zullinger <tmz@pobox.com> - 2.19.0-0.1.rc1
- Update to 2.19.0.rc1

* Mon Aug 20 2018 Todd Zullinger <tmz@pobox.com> - 2.19.0-0.0.rc0
- Update to 2.19.0.rc0

* Mon Aug 20 2018 Todd Zullinger <tmz@pobox.com> - 2.18.0-2.5
- Remove git-remote-testsvn, make git-svn noarch
- Restore fixed contrib/credential/netrc tests

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.0-2.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 2.18.0-2.3
- Perl 5.28 rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.18.0-2.2
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.18.0-2.1
- Perl 5.28 rebuild

* Mon Jun 25 2018 Pavel Cahyna <pcahyna@redhat.com> - 2.18.0-2
- Fix build --without cvs

* Wed Jun 20 2018 Todd Zullinger <tmz@pobox.com> - 2.18.0-1
- Update to 2.18.0

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.18.0-0.3.rc2
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Todd Zullinger <tmz@pobox.com> - 2.18.0-0.2.rc2
- Update to 2.18.0-rc2
- Apply upstream zlib buffer handling patch (#1582555)

* Wed Jun 06 2018 Todd Zullinger <tmz@pobox.com>
- Include git-contacts, SubmittingPatches suggests it to users
- Build git-subtree docs in %%build

* Mon Jun 04 2018 Todd Zullinger <tmz@pobox.com> - 2.18.0-0.1.rc1
- Update to 2.18.0-rc1
- Drop flaky & out-of-place netrc credential helper tests

* Fri Jun 01 2018 Todd Zullinger <tmz@pobox.com> - 2.18.0-0.0.rc0.1
- add -p: fix counting empty context lines in edited patches

* Wed May 30 2018 Todd Zullinger <tmz@pobox.com> - 2.18.0-0.0.rc0
- Update to 2.18.0-rc0
- Use new INSTALL_SYMLINKS setting

* Wed May 30 2018 Todd Zullinger <tmz@pobox.com> - 2.17.1-3
- Use %%apply_patch for aarch64 zlib patch, return to %%autosetup
- Disable jgit tests on s390x, they're unreliable
- Use %%make_build and %%make_install

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
