%define _trivial .0
%define _buildid .6

# Do we want SELinux & Audit
%if 0%{?!noselinux:1}
%define WITH_SELINUX 1
%else
%define WITH_SELINUX 0
%endif

# OpenSSH privilege separation requires a user & group ID
%define sshd_uid    74
%define sshd_gid    74

# Do we want libedit support
%define libedit 0

# Do we want LDAP support
%define ldap 0

# Do not forget to bump pam_ssh_agent_auth release if you rewind the main package release to 1
%define openssh_ver 7.4p1
%define openssh_rel 16
%define pam_ssh_agent_ver 0.10.3
%define pam_ssh_agent_rel 2

Summary: An open source implementation of SSH protocol versions 1 and 2
Name: openssh
Version: %{openssh_ver}
Release: %{openssh_rel}%{?dist}%{?rescue_rel}%{?_trivial}%{?_buildid}
URL: http://www.openssh.com/portable.html
#URL1: http://pamsshagentauth.sourceforge.net
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
#Source1: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz.asc
Source2: sshd.pam
Source3: sshd.init
Source4: http://prdownloads.sourceforge.net/pamsshagentauth/pam_ssh_agent_auth/pam_ssh_agent_auth-%{pam_ssh_agent_ver}.tar.bz2
Source5: pam_ssh_agent-rmheaders
Source6: ssh-keycat.pam
Source7: sshd.sysconfig
Source9: sshd@.service
Source10: sshd.socket
Source11: sshd.service
Source12: sshd-keygen.service
Source13: sshd-keygen

# Internal debug
Patch0: openssh-5.9p1-wIm.patch

#?
Patch100: openssh-7.4p1-coverity.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1889
Patch103: openssh-5.8p1-packet.patch

#https://bugzilla.mindrot.org/show_bug.cgi?id=1402
# https://bugzilla.redhat.com/show_bug.cgi?id=1171248
# record pfs= field in CRYPTO_SESSION audit event
Patch200: openssh-7.4p1-audit.patch
# Do not write to one socket from more processes (#1310684)
Patch202: openssh-6.6p1-audit-race-condition.patch

# --- pam_ssh-agent ---
# make it build reusing the openssh sources
Patch300: pam_ssh_agent_auth-0.10.3-build.patch
# check return value of seteuid()
Patch301: pam_ssh_agent_auth-0.10.3-seteuid.patch
# explicitly make pam callbacks visible
Patch302: pam_ssh_agent_auth-0.9.2-visibility.patch
# don't use xfree (#1024965)
Patch303: pam_ssh_agent_auth-0.10.3-no-xfree.patch
# update to current version of agent structure
Patch304: pam_ssh_agent_auth-0.10.3-agent_structure.patch
# do not directly dereference return value of getpwuid()
Patch305: pam_ssh_agent_auth-0.10.3-dereference.patch
# Use hardcoded date -- getting it from file is broken on i386
Patch306: pam_ssh_agent_auth-0.10.3-man-date.patch

#https://bugzilla.mindrot.org/show_bug.cgi?id=1641 (WONTFIX)
Patch400: openssh-7.4p1-role-mls.patch
#https://bugzilla.redhat.com/show_bug.cgi?id=781634
Patch404: openssh-6.6p1-privsep-selinux.patch

#?-- unwanted child :(
Patch501: openssh-6.6p1-ldap.patch
#?
Patch502: openssh-6.6p1-keycat.patch

#http6://bugzilla.mindrot.org/show_bug.cgi?id=1644
Patch601: openssh-6.6p1-allow-ip-opts.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1893
Patch604: openssh-6.6p1-keyperm.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1925
Patch606: openssh-5.9p1-ipv6man.patch
#?
Patch607: openssh-5.8p2-sigpipe.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1789
Patch609: openssh-5.5p1-x11.patch

#?
Patch700: openssh-7.4p1-fips.patch
#?
# drop? Patch701: openssh-5.6p1-exit-deadlock.patch
#?
Patch702: openssh-5.1p1-askpass-progress.patch
#?
Patch703: openssh-4.3p2-askpass-grab-info.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=205842
# drop? Patch704: openssh-5.9p1-edns.patch
#?
Patch706: openssh-6.6.1p1-localdomain.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1635 (WONTFIX)
Patch707: openssh-6.6p1-redhat.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1890 (WONTFIX) need integration to prng helper which is discontinued :)
Patch708: openssh-6.6p1-entropy.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1640 (WONTFIX)
Patch709: openssh-6.2p1-vendor.patch
# warn users for unsupported UsePAM=no (#757545)
Patch711: openssh-6.6p1-log-usepam-no.patch
# make aes-ctr ciphers use EVP engines such as AES-NI from OpenSSL
Patch712: openssh-6.3p1-ctr-evp-fast.patch
# add cavs test binary for the aes-ctr
Patch713: openssh-7.4p1-ctr-cavstest.patch
# add SSH KDF CAVS test driver
Patch714: openssh-7.4p1-kdf-cavs.patch


#http://www.sxw.org.uk/computing/patches/openssh.html
#changed cache storage type - #848228
Patch800: openssh-7.4p1-gsskex.patch
#http://www.mail-archive.com/kerberos@mit.edu/msg17591.html
Patch801: openssh-6.6p1-force_krb.patch
# add new option GSSAPIEnablek5users and disable using ~/.k5users by default (#1169843)
# CVE-2014-9278
Patch802: openssh-6.6p1-GSSAPIEnablek5users.patch
# Respect k5login_directory option in krk5.conf (#1328243)
Patch803: openssh-6.6p1-k5login_directory.patch
Patch900: openssh-6.1p1-gssapi-canohost.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1780
Patch901: openssh-7.4p1-kuserok.patch
# use default_ccache_name from /etc/krb5.conf (#991186)
Patch902: openssh-6.3p1-krb5-use-default_ccache_name.patch
# Change GSSAPIStrictAcceptor to yes as it ever was (#1488982)
Patch903: openssh-7.4p1-gss-strict-acceptor.patch

# Run ssh-copy-id in the legacy mode when SSH_COPY_ID_LEGACY variable is set (#969375
Patch905: openssh-7.4p1-legacy-ssh-copy-id.patch
# Use tty allocation for a remote scp (#985650)
Patch906: openssh-6.4p1-fromto-remote.patch
# log when a client requests an interactive session and only sftp is allowed (#1130198)
Patch914: openssh-6.6.1p1-log-sftp-only-connections.patch
# log via monitor in chroots without /dev/log (#1083482)
Patch918: openssh-7.4p1-log-in-chroot.patch
# MLS labeling according to chosen sensitivity (#1202843)
Patch919: openssh-6.6.1p1-mls-fix-labeling.patch
# sshd test mode show all config values (#1187597)
Patch920: openssh-6.6p1-test-mode-all-values.patch
# Add sftp option to force mode of created files (#1191055)
Patch921: openssh-6.6p1-sftp-force-permission.patch
# fix memory problem (#1223218)
Patch924: openssh-6.6p1-memory-problems.patch
# Enhance AllowGroups documentation in man page (#1150007)
Patch925: openssh-6.6p1-allowGroups-documentation.patch
# provide option GssKexAlgorithms to disable vulnerable groun1 kex
Patch928: openssh-7.4p1-gssKexAlgorithms.patch
# make s390 use /dev/ crypto devices -- ignore closefrom (#1318760)
Patch935: openssh-6.6p1-s390-closefrom.patch
# expose more information to PAM (#1312304)
Patch938: openssh-7.4p1-expose-pam.patch
# Move MAX_DISPLAYS to a configuration option (#1341302)
Patch939: openssh-6.6p1-x11-max-displays.patch
# Add systemd stuff so it can track running service (#1381997)
Patch942: openssh-6.6p1-systemd.patch
# Permit root login to preserve backward compatibility
Patch943: openssh-7.4p1-permit-root-login.patch
# Restore TCP wrappers support
Patch944: openssh-7.4p1-debian-restore-tcp-wrappers.patch
# Set sane whitelist for PKCS#11 modules in ssh-agent
Patch945: openssh-7.4p1-pkcs11-whitelist.patch
# Allow legacy algorithms and formats for key exchange after rebase
Patch946: openssh-7.4p1-legacy-algorithms.patch
# Show more fingerprints
Patch947: openssh-7.4p1-show-more-fingerprints.patch
# Fix newline in the end of server ident banner (upstream 5b9070)
Patch948: openssh-7.4p1-newline-banner.patch
# Do not utilize SHA1 by default for digital signatures (#1322911)
Patch949: openssh-7.4p1-sha2-signatures.patch
# Canonize pkcs11 provider path when removing smartcard (#2682)
Patch950: openssh-7.4p1-canonize-pkcs11-provider.patch
# Do not segfault sshd if it loads RSA1 keys (#2686)
Patch951: openssh-7.4p1-rsa1-segfault.patch
# OpenSSH 7.5 fixes CBC cipher weakness
Patch952: openssh-7.4p1-cbc-weakness.patch
# sandbox-seccomp filter is not denying socketcall() on ppc64le (#1443916)
Patch953: openssh-7.4p1-sandbox-ppc64le.patch
# ControlPath too long should not be fatal (#1447561)
Patch954: openssh-7.4p1-ControlPath_too_long.patch
# sandbox-seccomp for ibmca engine from upstream (#1451809)
Patch955: openssh-7.4p1-sandbox-ibmca.patch
# Back to UseDNS=yes by default (#1478175)
Patch956: openssh-7.4p1-usedns-yes.patch
# Clatch between ClientAlive timeouts and rekeying (#1480510)
Patch957: openssh-7.4p1-rekeying-timeouts.patch
# WinSCP 5.10+ compatibility (#1496808)
Patch958: openssh-7.4p1-winscp-compat.patch
# SSH AuthorizedKeysCommand hangs when output is too large (#1496467)
Patch959: openssh-7.4p1-authorized_keys_command.patch
# Fix for CVE-2017-15906 (#1517226)
Patch960: openssh-7.5p1-sftp-empty-files.patch

## AMZN2 Patches
# Fix for CVE-2018-15473
Patch5000: AMZN2-0001-CVE-2018-15473-delay-bailout-for-invalid-user.patch  
Patch5001: CVE-2018-20685.patch
Patch5002: CVE-2019-6109a.patch
Patch5003: CVE-2019-6109b.patch
Patch5004: CVE-2019-6111.patch

License: BSD
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{ldap}
BuildRequires: openldap-devel
%endif
BuildRequires: autoconf, automake, perl, zlib-devel
BuildRequires: audit-libs-devel >= 2.0.5
BuildRequires: util-linux, groff
BuildRequires: pam-devel
BuildRequires: tcp_wrappers-devel
BuildRequires: fipscheck-devel >= 1.3.0
BuildRequires: openssl-devel >= 0.9.8j
BuildRequires: perl-podlators
BuildRequires: systemd-devel

BuildRequires: krb5-devel

%if %{libedit}
BuildRequires: libedit-devel ncurses-devel
%endif

%if %{WITH_SELINUX}
Conflicts: selinux-policy < 3.13.1-92
Requires: libselinux >= 1.27.7
BuildRequires: libselinux-devel >= 1.27.7
Requires: audit-libs >= 1.0.8
BuildRequires: audit-libs >= 1.0.8
%endif

BuildRequires: xauth

Prefix: %{_prefix}

%package clients
Summary: An open source SSH client applications
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Requires: fipscheck-lib%{_isa} >= 1.3.0
Prefix: %{_prefix}

%package server
Summary: An open source SSH server daemon
Group: System Environment/Daemons
Requires: openssh = %{version}-%{release}
Requires: pam >= 1.0.1-3
Requires: fipscheck-lib%{_isa} >= 1.3.0
Prefix: %{_prefix}

%if %{ldap}
%package ldap
Summary: A LDAP support for open source SSH server daemon
Requires: openssh = %{version}-%{release}
Group: System Environment/Daemons
Prefix: %{_prefix}
%endif

%package keycat
Summary: A mls keycat backend for openssh
Requires: openssh = %{version}-%{release}
Group: System Environment/Daemons
Prefix: %{_prefix}

%package cavs
Summary: CAVS tests for FIPS validation
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Prefix: %{_prefix}

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features.

This package includes the core files necessary for both the OpenSSH
client and server. To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package includes
the clients necessary to make encrypted connections to SSH servers.

%description server
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
the secure shell daemon (sshd). The sshd daemon allows SSH clients to
securely connect to your SSH server.

%if %{ldap}
%description ldap
OpenSSH LDAP backend is a way how to distribute the authorized tokens
among the servers in the network.
%endif

%description keycat
OpenSSH mls keycat is backend for using the authorized keys in the
openssh in the mls mode.

%description cavs
This package contains test binaries and scripts to make FIPS validation
easier. Now contains CTR and KDF CAVS test driver.

%prep
%setup -q -a 4
#Do not enable by default
%if 0
%patch0 -p1 -b .wIm
%endif

%patch103 -p1 -b .packet

pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
%patch300 -p2 -b .psaa-build
%patch301 -p2 -b .psaa-seteuid
%patch302 -p1 -b .psaa-visibility
%patch303 -p2 -b .psaa-xfree
%patch304 -p2 -b .psaa-agent
%patch305 -p2 -b .psaa-dereference
%patch306 -p2 -b .psaa-pod
# Remove duplicate headers
rm -f $(cat %{SOURCE5})
popd

%if %{WITH_SELINUX}
%patch400 -p1 -b .role-mls
%patch404 -p1 -b .privsep-selinux
%endif

%patch501 -p1 -b .ldap
%patch502 -p1 -b .keycat

%patch601 -p1 -b .ip-opts
%patch604 -p1 -b .keyperm
%patch606 -p1 -b .ipv6man
%patch607 -p1 -b .sigpipe
%patch609 -p1 -b .x11
# 
# drop? %patch701 -p1 -b .exit-deadlock
%patch702 -p1 -b .progress
%patch703 -p1 -b .grab-info
# investigate - https://bugzilla.redhat.com/show_bug.cgi?id=205842
# probably not needed anymore %patch704 -p1 -b .edns
%patch706 -p1 -b .localdomain
%patch707 -p1 -b .redhat
%patch708 -p1 -b .entropy
%patch709 -p1 -b .vendor
%patch711 -p1 -b .log-usepam-no
%patch712 -p1 -b .evp-ctr
%patch713 -p1 -b .ctr-cavs
%patch714 -p1 -b .kdf-cavs
# 
%patch800 -p1 -b .gsskex
%patch801 -p1 -b .force_krb
# 
%patch900 -p1 -b .canohost
%patch901 -p1 -b .kuserok
%patch902 -p1 -b .ccache_name
%patch903 -p1 -b .gss-strict

%patch905 -p1 -b .legacy-ssh-copy-id
%patch906 -p1 -b .fromto-remote
%patch914 -p1 -b .log-sftp-only
%patch918 -p1 -b .log-in-chroot
%patch919 -p1 -b .mls-labels
%patch802 -p1 -b .GSSAPIEnablek5users
%patch803 -p1 -b .k5login
%patch920 -p1 -b .sshd-t
%patch921 -p1 -b .sftp-force-mode
%patch924 -p1 -b .memory-problems
%patch925 -p1 -b .allowGroups
%patch928 -p1 -b .gsskexalg
%patch935 -p1 -b .s390
%patch938 -p1 -b .expose-pam
%patch939 -p1 -b .x11max
%patch942 -p1 -b .patch
%patch943 -p1 -b .permit-root
%patch944 -p1 -b .tcp_wrappers
%patch945 -p1 -b .pkcs11-whitelist
%patch946 -p1 -b .legacy
%patch947 -p1 -b .fingerprint
%patch948 -p1 -b .newline-banner
%patch949 -p1 -b .sha2
%patch950 -p1 -b .smartcard
%patch951 -p1 -b .rsa1
%patch952 -p1 -b .cbc
%patch953 -p1 -b .seccomp
%patch954 -p1 -b .ControlPath
%patch955 -p1 -b .ibmca
%patch956 -p1 -b .usedns
%patch957 -p1 -b .rekey-timeout
%patch958 -p1 -b .winscp
%patch959 -p1 -b .large-command
%patch960 -p1 -b .sftp-empty

%patch200 -p1 -b .audit
%patch202 -p1 -b .audit-race
%patch700 -p1 -b .fips

%patch100 -p1 -b .coverity

%patch5000 -p1
%patch5001 -p1
%patch5002 -p1
%patch5003 -p1
%patch5004 -p1

%if ! %{ldap}
echo 'int main(void) {}' > ldap-helper.c
> ldapconf.c
> ldapbody.c
> ldapmisc.c
%endif

# Disable PRIV_END errors for Lambda
patch sshconnect.h <<\EOF
diff -ru openssh-6.6p1/sshconnect.h openssh-6.6p2/sshconnect.h
--- openssh-6.6p1/sshconnect.h	2017-11-03 21:22:19.136394554 +0000
+++ openssh-6.6p2/sshconnect.h	2017-11-03 21:45:14.652319846 +0000
@@ -69,7 +69,7 @@
 #define PRIV_END do {					\
 	int save_errno = errno;				\
 	if (seteuid(original_real_uid) != 0)		\
-		fatal("PRIV_END: seteuid: %s",		\
-		    strerror(errno));			\
+		/*fatal("PRIV_END: seteuid: %s",		\
+		    strerror(errno))*/;			\
 	errno = save_errno;				\
 } while (0)
EOF

autoreconf

%build
# the -fvisibility=hidden is needed for clean build of the pam_ssh_agent_auth
# and it makes the ssh build more clean and even optimized better
CFLAGS="$RPM_OPT_FLAGS -fvisibility=hidden"; export CFLAGS
CFLAGS="$CFLAGS -fpic"
SAVE_LDFLAGS="$LDFLAGS"
LDFLAGS="$LDFLAGS -pie -z relro -z now"

export CFLAGS
export LDFLAGS

if test -r /etc/profile.d/krb5-devel.sh ; then
        source /etc/profile.d/krb5-devel.sh
fi
krb5_prefix=`krb5-config --prefix`
if test "$krb5_prefix" != "%{_prefix}" ; then
	CPPFLAGS="$CPPFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"
	LDFLAGS="$LDFLAGS -L${krb5_prefix}/%{_lib}"; export LDFLAGS
else
	krb5_prefix=
	CPPFLAGS="-I%{_includedir}/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I%{_includedir}/gssapi"
fi

	# --with-default-path=/usr/local/bin:/usr/bin \
	# --with-superuser-path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin \
%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--datadir=%{_datadir}/openssh \
	--with-tcp-wrappers \
  --with-privsep-path=%{_var}/empty/sshd \
	--enable-vendor-patchlevel="RHEL7-%{openssh_ver}-%{openssh_rel}" \
	--disable-strip \
	--without-zlib-version-check \
	--with-ssl-engine \
	--with-ipaddr-display \
	--with-pie=no \
	--without-systemd \
	--with-ssh1 \
%if %{ldap}
	--with-ldap \
%endif
	--with-pam \
%if %{WITH_SELINUX}
	--with-selinux --with-audit=linux \
	--with-sandbox=seccomp_filter \
%endif
	--with-kerberos5${krb5_prefix:+=${krb5_prefix}} \
%if %{libedit}
	--with-libedit
%else
	--without-libedit
%endif

# make libssh.a

make

# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    fipshmac -d $RPM_BUILD_ROOT%{_libdir}/fipscheck $RPM_BUILD_ROOT%{_bindir}/ssh $RPM_BUILD_ROOT%{_sbindir}/sshd \
%{nil}

%install
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ldap.conf

install -d $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
install -d $RPM_BUILD_ROOT%{_libdir}/fipscheck
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/sshd
install -m644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/ssh-keycat
install -m644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/sshd
install -m755 %{SOURCE13} $RPM_BUILD_ROOT/%{_sbindir}/sshd-keygen
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/

#restore slogin symlink
pushd $RPM_BUILD_ROOT%{_bindir}
ln -s ./ssh slogin
popd

%files
%defattr(-,root,root)
%license LICENCE
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%attr(0511,root,root) %{_libexecdir}/openssh/ssh-keysign
%attr(0755,root,root) %{_libexecdir}/openssh/ctr-cavstest

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/ssh
%attr(0644,root,root) %{_libdir}/fipscheck/ssh.hmac
%attr(0755,root,root) %{_bindir}/scp
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0755,root,root) %{_bindir}/slogin
%attr(0511,root,nobody) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_bindir}/sftp
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-pkcs11-helper

%files server
%defattr(-,root,root)
%dir %attr(0711,root,root) %{_var}/empty/sshd
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_sbindir}/sshd-keygen
%attr(0644,root,root) %{_libdir}/fipscheck/sshd.hmac
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/sshd
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/sshd

%if %{ldap}
%files ldap
%defattr(-,root,root)
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-ldap-helper
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-ldap-wrapper
%endif

%files keycat
%defattr(-,root,root)
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-keycat
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/ssh-keycat

%files cavs
%attr(0755,root,root) %{_libexecdir}/openssh/ctr-cavstest
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-cavs
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-cavs_driver.pl

%exclude %{_mandir}

%changelog
* Sun Jul 07 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon May 20 2019 Frederick Lefebvre <fredlef@amzn.com> - 7.4p1-16.amzn2.0.6 
- Address CVE-2018-20685, CVE-2019-6109 and CVE-2019-6111

* Fri Nov 24 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-16 + 0.10.3-2
- Fix for CVE-2017-15906 (#1517226)

* Mon Nov 06 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-15 + 0.10.3-2
- Do not hang if SSH AuthorizedKeysCommand output is too large (#1496467)
- Do not segfault pam_ssh_agent_auth if keyfile is missing (#1494268)
- Do not segfault in audit code during cleanup (#1488083)
- Add WinSCP 5.10+ compatibility (#1496808)
- Clatch between ClientAlive and rekeying timeouts (#1480510)
- Exclude dsa and ed25519 from default proposed keys in FIPS mode (#1456853)
- Add enablement for openssl-ibmca and openssl-ibmpkcs11 (#1478035)

* Fri Nov  3 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 7.4p1-14 + 0.10.3-2
- Rebuilt for RHEL-7.5

* Wed Sep 13 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-13 + 0.10.3-1
- Revert default of GSSAPIStrictAcceptorCheck=no back to yes (#1488982)

* Mon Aug 07 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-12 + 0.10.3-1
- Revert upstream change to UseDNS=no back to yes (#1478175)

* Mon May 22 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-11 + 0.10.3-1
- Compiler warnings (#1341754)

* Mon May 22 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-10 + 0.10.3-1
- Add missing messages in FIPS mode (#1341754)

* Fri May 19 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-9 + 0.10.3-1
- Allow harmless syscalls for s390 crypto modules (#1451809)

* Mon May 15 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-8 + 0.10.3-1
- Fix multilib issue in documentation (#1450361)

* Thu May 04 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-6 + 0.10.3-1
- ControlPath too long should not be a fatal error (#1447561)

* Wed Apr 26 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-5 + 0.10.3-1
- Fix the default key exchange proposal in FIPS mode (#1438414)
- Remove another wrong coverity chunk to unbreak gsskex (#1438414)

* Mon Apr 24 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-4 + 0.10.3-1
- Update seccomp filter to work on ppc64le (#1443916)

* Wed Apr 05 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-3 + 0.10.3-1
- Do not completely disable SHA-1 key exchange methods in FIPS (#1324493)
- Remove wrong coverity patches

* Thu Mar 23 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-2 + 0.10.3-1
- Fix coverity scan results
- Adjust FIPS algorithms list (#1420910)
- Revert problematic feature for chroot(#1418062)
- Fix CBC weakness in released OpenSSH 7.5

* Wed Mar 01 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-1 + 0.10.3-1
- Rebase to openssh 7.4 and pam_ssh_agent_auth 0.10.3 (#1341754)
- detach -cavs subpackage
- enable seccomp filter for sandboxed child

* Wed Mar 01 2017 Jakub Jelen <jjelen@redhat.com> - 6.6.1p1-35 + 0.9.3-9
- Do not send SD_NOTIFY from forked childern (#1381997)

* Fri Feb 24 2017 Jakub Jelen <jjelen@redhat.com> - 6.6.1p1-34 + 0.9.3-9
- Add SD_NOTIFY code to help systemd to track running service (#1381997)

* Mon Dec 19 2016 Jakub Jelen <jjelen@redhat.com> - 6.6.1p1-33 + 0.9.3-9
- Restore login with large MOTD (#1404018)

* Tue Nov 29 2016 Jakub Jelen <jjelen@redhat.com> - 6.6.1p1-32 + 0.9.3-9
- Restore funcionality of chrooted envirotments (#1398569)

* Tue Sep 06 2016 Jakub Jelen <jjelen@redhat.com> - 6.6.1p1-31 + 0.9.3-9
- Do not depend on selinux-policy (#1373297)

* Fri Jul 29 2016 Jakub Jelen <jjelen@redhat.com> - 6.6.1p1-30 + 0.9.3-9
- Drop dependency on libcap-ng for ssh-keycat (#1357859)

* Thu Jul 28 2016 Jakub Jelen <jjelen@redhat.com> - 6.6.1p1-29 + 0.9.3-9
- Rework SELinux context handling with chroot using libcap-ng (#1357859)

* Fri Jul 01 2016 Jakub Jelen <jjelen@redhat.com> - 6.6.1p1-28 + 0.9.3-9
- SFTP force permission collision with umask (#1344614)
- Make closefrom() ignore FD's to /dev/ devices on s390 (#1318760)
- Create a default value for AuthenticationMethods any (#1237129)
- Fix ssh-copy-id with LogLevel=quiet (#1349556)
- Expose more information to PAM (#1312304)
- Move MAX_DISPLAYS to a configuration option (#1341302)
- Add a wildcard option to PermitOpen directive (host) (#1344106)

* Tue May 31 2016 Jakub Jelen <jjelen@redhat.com> - 6.6.1p1-27 + 0.9.3-9
- Coverity and RPMDiff build issues (#1334326)
- CVE-2015-8325: privilege escalation via user's PAM environment and UseLogin=yes (#1329191)
- Check for real location of .k5login file (#1328243)
- close ControlPersist background process stderr (#1335540)

* Fri Apr 01 2016 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-26 + 0.9.3-9
- Drop glob patch for sftp client preventing listing many files (#1310303)
- Fix race condition between audit messages from different processes (#1310684)
- Make systemd service forking to properly report state (#1291172)
- Get rid of rpm triggers for openssh-5.x (#1312013)
- Generate the host keys when the key files are empty (#1266043)
- pam_ssh_agent_auth: authorized_keys_command option (#1317858)
- Don't use MD5 digest from pam_ssh_agent_auth in FIPS mode (#1317952)

* Wed Mar 16 2016 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-25 + 0.9.3-9
- CVE-2016-1908: possible fallback from untrusted to trusted X11 forwarding (#1298741)

* Tue Mar 15 2016 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-24 + 0.9.3-9
- CVE-2016-3115: missing sanitisation of input for X11 forwarding (#1317819)

* Wed Jan 13 2016 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-23 + 0.9.3-9
- Disable undocumented feauture Roaming for good (#1298218)
- prevents CVE-2016-0777 and CVE-2016-0778

* Fri Sep 25 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-22 + 0.9.3-9
- Use the correct constant for glob limits (#1160377)

* Thu Sep 24 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-21 + 0.9.3-9
- Extend memory limit for remote glob in sftp acc. to stat limit (#1160377)

* Thu Sep 24 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-20 + 0.9.3-9
- Fix vulnerabilities published with openssh-7.0 (#1265807)
 - Privilege separation weakness related to PAM support
 - Use-after-free bug related to PAM support

* Thu Sep 24 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-19 + 0.9.3-9
- Increase limit of files for glob match in sftp to 8192 (#1160377)

* Tue Aug 18 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-18 + 0.9.3-9
- Add GSSAPIKexAlgorithms option for server and client application (#1253062)

* Wed Jul 29 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-17 + 0.9.3-9
- Security fixes released with openssh-6.9 (CVE-2015-5352) (#1247864)
 - XSECURITY restrictions bypass under certain conditions in ssh(1) (#1238231)
 - weakness of agent locking (ssh-add -x) to password guessing (#1238238)

* Mon Jul 27 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-16 + 0.9.3-9
- only query each keyboard-interactive device once (CVE-2015-5600) (#1245971)

* Wed Jul 15 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-15 + 0.9.3-9
- One more typo in manual page documenting TERM variable (#1162683)
- Fix race condition with auditing messages answers (#1240613)

* Mon Jun 15 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-14 + 0.9.3-9
- Fix ldif schema to have correct spacing on newlines (#1184938)
- Add missing values for sshd test mode (#1187597)
- ssh-copy-id: tcsh doesnt work with multiline strings (#1201758)
- Fix memory problems with newkeys and array transfers (#1223218)
- Enhance AllowGroups documentation in man page (#1150007)

* Mon May 11 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-13 + 0.9.3-9
- Increase limit of files for glob match in sftp (#1160377)
- Add pam_reauthorize.so to /etc/pam.d/sshd (#1204233)
- Show all config values in sshd test mode (#1187597)
- Document required selinux boolean for working ssh-ldap-helper (#1178116)
- Consistent usage of pam_namespace in sshd (#1125110)
- Fix auditing when using combination of ForcedCommand and PTY (#1199112)
- Add sftp option to force mode of created files (#1197989)
- Ability to specify an arbitrary LDAP filter in ldap.conf for ssh-ldap-helper (#1201753)
- Provide documentation line for systemd service and socket (#1181591)
- Provide LDIF version of LPK schema (#1184938)
- Document TERM environment variable (#1162683)
- Fix ssh-copy-id on non-sh remote shells (#1201758)
- Do not read RSA1 hostkeys for HostBased authentication in FIPS (#1197666)

* Thu Mar 19 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-12 + 0.9.3-9
- Fix labeling in MLS according to selected sensitivity (#1202843)

* Fri Jan 16 2015 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-11 + 0.9.3-9
- fix direction in CRYPTO_SESSION audit message (#1171248)

* Wed Jan 14 2015 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-10 + 0.9.3-9
- add new option GSSAPIEnablek5users and disable using ~/.k5users by default CVE-2014-9278
  (#1169843)

* Fri Dec 19 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-9 + 0.9.3-9
- log via monitor in chroots without /dev/log (#1083482)

* Mon Dec 15 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-8 + 0.9.3-9
- increase size of AUDIT_LOG_SIZE to 256 (#1171163)
- record pfs= field in CRYPTO_SESSION audit event (#1171248)

* Thu Nov 13 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-7 + 0.9.3-9
- fix gsskex patch to correctly handle MONITOR_REQ_GSSSIGN request (#1118005)

* Fri Nov 07 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-6 + 0.9.3-9
- correct the calculation of bytes for authctxt->krb5_ccname <ams@corefiling.com> (#1161073)

* Tue Nov 04 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-5 + 0.9.3-9
- change audit trail for unknown users (#1158521)

* Sun Oct 26 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-4 + 0.9.3-9
- revert the default of KerberosUseKuserok back to yes
- fix kuserok patch which checked for the existence of .k5login unconditionally
  and hence prevented other mechanisms to be used properly

* Mon Sep 29 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-3 + 0.9.3-9
- fix parsing empty options in sshd_conf
- ignore SIGXFSZ in postauth monitor

* Tue Sep 23 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-2 + 0.9.3-9
- slightly change systemd units logic - use sshd-keygen.service (#1066615)
- log when a client requests an interactive session and only sftp is allowed (#1130198)
- sshd-keygen - don't generate DSA and ED25519 host keys in FIPS mode (#1143867)

* Mon Sep 08 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-1 + 0.9.3-9
- new upstream release (#1059667)
- prevent a server from skipping SSHFP lookup - CVE-2014-2653 (#1081338)
- make /etc/ssh/moduli file public (#1134448)
- test existence of /etc/ssh/ssh_host_ecdsa_key in sshd-keygen.service
- don't clean up gssapi credentials by default (#1134447)
- ssh-agent - try CLOCK_BOOTTIME with fallback (#1134449)
- disable the curve25519 KEX when speaking to OpenSSH 6.5 or 6.6
- add support for ED25519 keys to sshd-keygen and sshd.sysconfig
- standardise on NI_MAXHOST for gethostname() string lengths (#1097665)
- set a client's address right after a connection is set (mindrot#2257) (#912792)
- apply RFC3454 stringprep to banners when possible (mindrot#2058) (#1104662)
- don't consider a partial success as a failure (mindrot#2270) (#1112972)

* Wed Mar 19 2014 Petr Lautrbach <plautrba@redhat.com> 6.4p1-8 + 0.9.3-8
- ignore environment variables with embedded '=' or '\0' characters (#1077843)

* Tue Jan 28 2014 Petr Lautrbach <plautrba@redhat.com> 6.4p1-7 + 0.9.3-8
- log fipscheck verification message into syslog authpriv
- ssh-keygen - relative-specified certificate expiry time should be relative
  to current time and not the validity start time (#1058234)
- use the size of security of 3des for DH (#1053107)
- ssh-copy-id.1 man page fix (#1058792)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 6.4p1-6
- Mass rebuild 2014-01-24

* Mon Jan 20 2014 Petr Lautrbach <plautrba@redhat.com> 6.4p1-5 + 0.9.3-8
- use tty allocation for a remote scp (#985650)
- run ssh-copy-id in the legacy mode when SSH_COPY_ID_LEGACY variable is set (#969375)
- FIPS mode - adjust the key echange DH groups and ssh-keygen according toSP800-131A (#1001748)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 6.4p1-4
- Mass rebuild 2013-12-27

* Wed Dec 11 2013 Petr Lautrbach <plautrba@redhat.com> 6.4p1-3 + 0.9.3-8
- sshd-keygen - use correct permissions on ecdsa host key (#1023945)
- use only rsa and ecdsa host keys by default

* Tue Nov 26 2013 Petr Lautrbach <plautrba@redhat.com> 6.4p1-2 + 0.9.3-1
- fix fatal() cleanup in the audit patch (#1029074)
- fix parsing logic of ldap.conf file (#1033662)

* Fri Nov 08 2013 Petr Lautrbach <plautrba@redhat.com> 6.4p1-1 + 0.9.3-1
- new upstream release

* Fri Nov 01 2013 Petr Lautrbach <plautrba@redhat.com> 6.3p1-4 + 0.9.3-7
- adjust gss kex mechanism to the upstream changes (#1024004)
- don't use xfree in pam_ssh_agent_auth sources <geertj@gmail.com> (#1024965)

* Thu Oct 24 2013 Petr Lautrbach <plautrba@redhat.com> 6.3p1-3 + 0.9.3-6
- don't use SSH_FP_MD5 for fingerprints in FIPS mode (#1020948)

* Wed Oct 23 2013 Petr Lautrbach <plautrba@redhat.com> 6.3p1-2 + 0.9.3-6
- use default_ccache_name from /etc/krb5.conf for a kerberos cache (#991186)
- increase the size of the Diffie-Hellman groups (#1010607)
- sshd-keygen to generate ECDSA keys <i.grok@comcast.net> (#1019222)

* Mon Oct 14 2013 Petr Lautrbach <plautrba@redhat.com> 6.3p1-1 + 0.9.3-6
- new upstream release (#1013635)

* Tue Oct 08 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-9 + 0.9.3-5
- use dracut-fips package to determine if a FIPS module is installed (#1001566)
- revert -fips subpackages and hmac files suffixes

* Wed Sep 25 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-8 + 0.9.3-5
- sshd-keygen: generate only RSA keys by default (#1010361)
- use dist tag in suffixes for hmac checksum files

* Wed Sep 11 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-7 + 0.9.3-5
- use hmac_suffix for ssh{,d} hmac checksums
- bump the minimum value of SSH_USE_STRONG_RNG to 14 according to SP800-131A
- automatically restart sshd.service on-failure after 42s interval

* Thu Aug 29 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-6.1 + 0.9.3-5
- add -fips subpackages that contains the FIPS module files

* Wed Jul 31 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-5 + 0.9.3-5
- gssapi credentials need to be stored before a pam session opened (#987792)

* Tue Jul 23 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-4 + 0.9.3-5
- don't show Success for EAI_SYSTEM (#985964)
- make sftp's libedit interface marginally multibyte aware (#841771)

* Mon Jun 17 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-3 + 0.9.3-5
- move default gssapi cache to /run/user/<uid> (#848228)

* Tue May 21 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-2 + 0.9.3-5
- add socket activated sshd units to the package (#963268)
- fix the example in the HOWTO.ldap-keys

* Mon May 20 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-1 + 0.9.3-5
- new upstream release (#963582)

* Wed Apr 17 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p1-4 + 0.9.3-4
- don't use export in sysconfig file (#953111)

* Tue Apr 16 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p1-3 + 0.9.3-4
- sshd.service: use KillMode=process (#890376)
- add latest config.{sub,guess} to support aarch64 (#926284)

* Tue Apr 09 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p1-2 + 0.9.3-4
- keep track of which IndentityFile options were manually supplied and
  which were default options, and don't warn if the latter are missing.
  (mindrot#2084)

* Tue Apr 09 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p1-1 + 0.9.3-4
- new upstream release (#924727)

* Wed Mar 06 2013 Petr Lautrbach <plautrba@redhat.com> 6.1p1-7 + 0.9.3-3
- use SELinux type sshd_net_t for [net] childs (#915085)

* Thu Feb 14 2013 Petr Lautrbach <plautrba@redhat.com> 6.1p1-6 + 0.9.3-3
- fix AuthorizedKeysCommand option

* Fri Feb 08 2013 Petr Lautrbach <plautrba@redhat.com> 6.1p1-5 + 0.9.3-3
- change default value of MaxStartups - CVE-2010-5107 (#908707)

* Mon Dec 03 2012 Petr Lautrbach <plautrba@redhat.com> 6.1p1-4 + 0.9.3-3
- fix segfault in openssh-5.8p2-force_krb.patch (#882541)

* Mon Dec 03 2012 Petr Lautrbach <plautrba@redhat.com> 6.1p1-3 + 0.9.3-3
- replace RequiredAuthentications2 with AuthenticationMethods based on upstream
- obsolete RequiredAuthentications[12] options
- fix openssh-6.1p1-privsep-selinux.patch

* Fri Oct 26 2012 Petr Lautrbach <plautrba@redhat.com> 6.1p1-2
- add SELinux comment to /etc/ssh/sshd_config about SELinux command to modify port (#861400)
- drop required chkconfig (#865498)
- drop openssh-5.9p1-sftp-chroot.patch (#830237)

* Sat Sep 15 2012 Petr Lautrbach <plautrba@redhat.com> 6.1p1-1 + 0.9.3-3
- new upstream release (#852651)
- use DIR: kerberos type cache (#848228)
- don't use chroot_user_t for chrooted users (#830237)
- replace scriptlets with systemd macros (#850249)
- don't use /bin and /sbin paths (#856590)

* Mon Aug 06 2012 Petr Lautrbach <plautrba@redhat.com> 6.0p1-1 + 0.9.3-2
- new upstream release

* Mon Aug 06 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-26 + 0.9.3-1
- change SELinux context also for root user (#827109)

* Fri Jul 27 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-25 + 0.9.3-1
- fix various issues in openssh-5.9p1-required-authentications.patch

* Tue Jul 17 2012 Tomas Mraz <tmraz@redhat.com> 5.9p1-24 + 0.9.3-1
- allow sha256 and sha512 hmacs in the FIPS mode

* Fri Jun 22 2012 Tomas Mraz <tmraz@redhat.com> 5.9p1-23 + 0.9.3-1
- fix segfault in su when pam_ssh_agent_auth is used and the ssh-agent
  is not running, most probably not exploitable
- update pam_ssh_agent_auth to 0.9.3 upstream version

* Fri Apr 06 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-22 + 0.9.2-32
- don't create RSA1 key in FIPS mode
- don't install sshd-keygen.service (#810419)

* Fri Mar 30 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-21 + 0.9.2-32
- fix various issues in openssh-5.9p1-required-authentications.patch

* Wed Mar 21 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-20 + 0.9.2-32
- Fix dependencies in systemd units, don't enable sshd-keygen.service (#805338)

* Wed Feb 22 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-19 + 0.9.2-32
- Look for x11 forward sockets with AI_ADDRCONFIG flag getaddrinfo (#735889)

* Mon Feb 06 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-18 + 0.9.2-32
- replace TwoFactorAuth with RequiredAuthentications[12]
  https://bugzilla.mindrot.org/show_bug.cgi?id=983

* Tue Jan 31 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-17 + 0.9.2-32
- run privsep slave process as the users SELinux context (#781634)

* Tue Dec 13 2011 Tomas Mraz <tmraz@redhat.com> 5.9p1-16 + 0.9.2-32
- add CAVS test driver for the aes-ctr ciphers

* Sun Dec 11 2011 Tomas Mraz <tmraz@redhat.com> 5.9p1-15 + 0.9.2-32
- enable aes-ctr ciphers use the EVP engines from OpenSSL such as the AES-NI

* Tue Dec 06 2011 Petr Lautrbach <plautrba@redhat.com> 5.9p1-14 + 0.9.2-32
- warn about unsupported option UsePAM=no (#757545)

* Mon Nov 21 2011 Tomas Mraz <tmraz@redhat.com> - 5.9p1-13 + 0.9.2-32
- add back the restorecon call to ssh-copy-id - it might be needed on older
  distributions (#739989)

* Fri Nov 18 2011 Tomas Mraz <tmraz@redhat.com> - 5.9p1-12 + 0.9.2-32
- still support /etc/sysconfig/sshd loading in sshd service (#754732)
- fix incorrect key permissions generated by sshd-keygen script (#754779)

* Fri Oct 14 2011 Tomas Mraz <tmraz@redhat.com> - 5.9p1-11 + 0.9.2-32
- remove unnecessary requires on initscripts
- set VerifyHostKeyDNS to ask in the default configuration (#739856)

* Mon Sep 19 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-10 + 0.9.2-32
- selinux sandbox rewrite
- two factor authentication tweaking

* Wed Sep 14 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-9 + 0.9.2-32
- coverity upgrade
- wipe off nonfunctional nss
- selinux sandbox tweaking

* Tue Sep 13 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-8 + 0.9.2-32
- coverity upgrade
- experimental selinux sandbox

* Tue Sep 13 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-7 + 0.9.2-32
- fully reanable auditing

* Mon Sep 12 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-6 + 0.9.2-32
- repair signedness in akc patch

* Mon Sep 12 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-5 + 0.9.2-32
- temporarily disable part of audit4 patch

* Fri Sep  9 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-3 + 0.9.2-32
- Coverity second pass
- Reenable akc patch

* Thu Sep  8 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-2 + 0.9.2-32
- Coverity first pass

* Wed Sep  7 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-1 + 0.9.2-32
- Rebase to 5.9p1
- Add chroot sftp patch
- Add two factor auth patch

* Tue Aug 23 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-21 + 0.9.2-31
- ignore SIGPIPE in ssh keyscan

* Tue Aug  9 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-20 + 0.9.2-31
- save ssh-askpass's debuginfo

* Mon Aug  8 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-19 + 0.9.2-31
- compile ssh-askpass with corect CFLAGS

* Mon Aug  8 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-18 + 0.9.2-31
- improve selinux's change context log 

* Mon Aug  8 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-17 + 0.9.2-31
- repair broken man pages

* Mon Jul 25 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-16 + 0.9.2-31
- rebuild due to broken rpmbiild

* Thu Jul 21 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-15 + 0.9.2-31
- Do not change context when run under unconfined_t

* Thu Jul 14 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-14 + 0.9.2-31
- Add postlogin to pam. (#718807)

* Tue Jun 28 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-12 + 0.9.2-31
- Systemd compatibility according to Mathieu Bridon <bochecha@fedoraproject.org>
- Split out the host keygen into their own command, to ease future migration
  to systemd. Compatitbility with the init script was kept.
- Migrate the package to full native systemd unit files, according to the Fedora
  packaging guidelines.
- Prepate the unit files for running an ondemand server. (do not add it actually)

* Tue Jun 21 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-10 + 0.9.2-31
- Mention IPv6 usage in man pages

* Mon Jun 20 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-9 + 0.9.2-31
- Improve init script

* Thu Jun 16 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-7 + 0.9.2-31
- Add possibility to compile openssh without downstream patches

* Thu Jun  9 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-6 + 0.9.2-31
- remove stale control sockets (#706396)

* Tue May 31 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-5 + 0.9.2-31
- improove entropy manuals

* Fri May 27 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-4 + 0.9.2-31
- improove entropy handling
- concat ldap patches

* Tue May 24 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-3 + 0.9.2-31
- improove ldap manuals

* Mon May 23 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-2 + 0.9.2-31
- add gssapi forced command

* Tue May  3 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-1 + 0.9.2-31
- update the openssh version

* Thu Apr 28 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-34 + 0.9.2-30
- temporarily disabling systemd units

* Wed Apr 27 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-33 + 0.9.2-30
- add flags AI_V4MAPPED and AI_ADDRCONFIG to getaddrinfo

* Tue Apr 26 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-32 + 0.9.2-30
- update scriptlets

* Fri Apr 22 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-30 + 0.9.2-30
- add systemd units

* Fri Apr 22 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-28 + 0.9.2-30
- improving sshd -> passwd transation
- add template for .local domain to sshd_config

* Thu Apr 21 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-27 + 0.9.2-30
- the private keys may be 640 root:ssh_keys ssh_keysign is sgid

* Wed Apr 20 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-26 + 0.9.2-30
- improving sshd -> passwd transation

* Tue Apr  5 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-25 + 0.9.2-30
- the intermediate context is set to sshd_sftpd_t
- do not crash in packet.c if no connection

* Thu Mar 31 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-24 + 0.9.2-30
- resolve warnings in port_linux.c

* Tue Mar 29 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-23 + 0.9.2-30
- add /etc/sysconfig/sshd

* Mon Mar 28 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-22 + 0.9.2-30
- improve reseeding and seed source (documentation)

* Tue Mar 22 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-20 + 0.9.2-30
- use /dev/random or /dev/urandom for seeding prng
- improve periodical reseeding of random generator

* Thu Mar 17 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-18 + 0.9.2-30
- add periodical reseeding of random generator 
- change selinux contex for internal sftp in do_usercontext
- exit(0) after sigterm

* Thu Mar 10 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-17 + 0.9.2-30
- improove ssh-ldap (documentation)

* Tue Mar  8 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-16 + 0.9.2-30
- improve session keys audit

* Mon Mar  7 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-15 + 0.9.2-30
- CVE-2010-4755

* Fri Mar  4 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-14 + 0.9.2-30
- improove ssh-keycat (documentation)

* Thu Mar  3 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-13 + 0.9.2-30
- improve audit of logins and auths

* Tue Mar  1 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-12 + 0.9.2-30
- improove ssk-keycat

* Mon Feb 28 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-11 + 0.9.2-30
- add ssk-keycat

* Fri Feb 25 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-10 + 0.9.2-30
- reenable auth-keys ldap backend

* Fri Feb 25 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-9 + 0.9.2-30
- another audit improovements

* Thu Feb 24 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-8 + 0.9.2-30
- another audit improovements
- switchable fingerprint mode

* Thu Feb 17 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-4 + 0.9.2-30
- improve audit of server key management

* Wed Feb 16 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-3 + 0.9.2-30
- improve audit of logins and auths

* Mon Feb 14 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-1 + 0.9.2-30
- bump openssh version to 5.8p1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6p1-30.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-30 + 0.9.2-29
- clean the data structures in the non privileged process
- clean the data structures when roaming

* Wed Feb  2 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-28 + 0.9.2-29
- clean the data structures in the privileged process

* Tue Jan 25 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-25 + 0.9.2-29
- clean the data structures before exit net process

* Mon Jan 17 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-24 + 0.9.2-29
- make audit compatible with the fips mode

* Fri Jan 14 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-23 + 0.9.2-29
- add audit of destruction the server keys

* Wed Jan 12 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-22 + 0.9.2-29
- add audit of destruction the session keys

* Fri Dec 10 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-21 + 0.9.2-29
- reenable run sshd as non root user
- renable rekeying

* Wed Nov 24 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-20 + 0.9.2-29
- reapair clientloop crash (#627332)
- properly restore euid in case connect to the ssh-agent socket fails

* Mon Nov 22 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-19 + 0.9.2-28
- striped read permissions from suid and sgid binaries

* Mon Nov 15 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-18 + 0.9.2-27
- used upstream version of the biguid patch

* Mon Nov 15 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-17 + 0.9.2-27
- improoved kuserok patch

* Fri Nov  5 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-16 + 0.9.2-27
- add auditing the host based key ussage
- repait X11 abstract layer socket (#648896)

* Wed Nov  3 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-15 + 0.9.2-27
- add auditing the kex result

* Tue Nov  2 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-14 + 0.9.2-27
- add auditing the key ussage

* Wed Oct 20 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-12 + 0.9.2-27
- update gsskex patch (#645389)

* Wed Oct 20 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-11 + 0.9.2-27
- rebase linux audit according to upstream

* Fri Oct  1 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-10 + 0.9.2-27
- add missing headers to linux audit

* Wed Sep 29 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-9 + 0.9.2-27
- audit module now uses openssh audit framevork

* Wed Sep 15 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-8 + 0.9.2-27
- Add the GSSAPI kuserok switch to the kuserok patch

* Wed Sep 15 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-7 + 0.9.2-27
- Repaired the kuserok patch

* Mon Sep 13 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-6 + 0.9.2-27
- Repaired the problem with puting entries with very big uid into lastlog

* Mon Sep 13 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-5 + 0.9.2-27
- Merging selabel patch with the upstream version. (#632914)

* Mon Sep 13 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-4 + 0.9.2-27
- Tweaking selabel patch to work properly without selinux rules loaded. (#632914)

* Wed Sep  8 2010 Tomas Mraz <tmraz@redhat.com> - 5.6p1-3 + 0.9.2-27
- Make fipscheck hmacs compliant with FHS - requires new fipscheck

* Fri Sep  3 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-2 + 0.9.2-27
- Added -z relro -z now to LDFLAGS

* Fri Sep  3 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-1 + 0.9.2-27
- Rebased to openssh5.6p1

* Wed Jul  7 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-18 + 0.9.2-26
- merged with newer bugzilla's version of authorized keys command patch

* Wed Jun 30 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-17 + 0.9.2-26
- improved the x11 patch according to upstream (#598671)

* Fri Jun 25 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-16 + 0.9.2-26
- improved the x11 patch (#598671)

* Thu Jun 24 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-15 + 0.9.2-26
- changed _PATH_UNIX_X to unexistent file name (#598671)

* Wed Jun 23 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-14 + 0.9.2-26
- sftp works in deviceless chroot again (broken from 5.5p1-3)

* Tue Jun  8 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-13 + 0.9.2-26
- add option to switch out krb5_kuserok

* Fri May 21 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-12 + 0.9.2-26
- synchronize uid and gid for the user sshd

* Thu May 20 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-11 + 0.9.2-26
- Typo in ssh-ldap.conf(5) and ssh-ladap-helper(8)

* Fri May 14 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-10 + 0.9.2-26
- Repair the reference in man ssh-ldap-helper(8)
- Repair the PubkeyAgent section in sshd_config(5)
- Provide example ldap.conf

* Thu May 13 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-9 + 0.9.2-26
- Make the Ldap configuration widely compatible
- create the aditional docs for LDAP support.

* Thu May  6 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-8 + 0.9.2-26
- Make LDAP config elements TLS_CACERT and TLS_REQCERT compatiple with pam_ldap (#589360)

* Thu May  6 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-7 + 0.9.2-26
- Make LDAP config element tls_checkpeer compatiple with nss_ldap (#589360)

* Tue May  4 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-6 + 0.9.2-26
- Comment spec.file
- Sync patches from upstream

* Mon May  3 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-5 + 0.9.2-26
- Create separate ldap package
- Tweak the ldap patch
- Rename stderr patch properly

* Thu Apr 29 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-4 + 0.9.2-26
- Added LDAP support

* Mon Apr 26 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-3 + 0.9.2-26
- Ignore .bashrc output to stderr in the subsystems

* Tue Apr 20 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-2 + 0.9.2-26
- Drop dependency on man

* Fri Apr 16 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-1 + 0.9.2-26
- Update to 5.5p1

* Fri Mar 12 2010 Jan F. Chadima <jchadima@redhat.com> - 5.4p1-3 + 0.9.2-25
- repair configure script of pam_ssh_agent
- repair error mesage in ssh-keygen

* Fri Mar 12 2010 Jan F. Chadima <jchadima@redhat.com> - 5.4p1-2
- source krb5-devel profile script only if exists

* Tue Mar  9 2010 Jan F. Chadima <jchadima@redhat.com> - 5.4p1-1
- Update to 5.4p1
- discontinued support for nss-keys
- discontinued support for scard

* Wed Mar  3 2010 Jan F. Chadima <jchadima@redhat.com> - 5.4p1-0.snap20100302.1
- Prepare update to 5.4p1

* Mon Feb 15 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-22
- ImplicitDSOLinking (#564824)

* Fri Jan 29 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-21
- Allow to use hardware crypto if awailable (#559555)

* Mon Jan 25 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-20
- optimized FD_CLOEXEC on accept socket (#541809)

* Mon Jan 25 2010 Tomas Mraz <tmraz@redhat.com> - 5.3p1-19
- updated pam_ssh_agent_auth to new version from upstream (just
  a licence change)

* Thu Jan 21 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-18
- optimized RAND_cleanup patch (#557166)

* Wed Jan 20 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-17
- add RAND_cleanup at the exit of each program using RAND (#557166)

* Tue Jan 19 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-16
- set FD_CLOEXEC on accepted socket (#541809)

* Fri Jan  8 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-15
- replaced define by global in macros

* Tue Jan  5 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-14
- Update the pka patch

* Mon Dec 21 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-13
- Update the audit patch

* Fri Dec  4 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-12
- Add possibility to autocreate only RSA key into initscript (#533339)

* Fri Nov 27 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-11
- Prepare NSS key patch for future SEC_ERROR_LOCKED_PASSWORD (#537411)

* Tue Nov 24 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-10
- Update NSS key patch (#537411, #356451)

* Fri Nov 20 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-9
- Add gssapi key exchange patch (#455351)

* Fri Nov 20 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-8
- Add public key agent patch (#455350)

* Mon Nov  2 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-7
- Repair canohost patch to allow gssapi to work when host is acessed via pipe proxy (#531849)

* Thu Oct 29 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-6
- Modify the init script to prevent it to hang during generating the keys (#515145)

* Tue Oct 27 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-5
- Add README.nss

* Mon Oct 19 2009 Tomas Mraz <tmraz@redhat.com> - 5.3p1-4
- Add pam_ssh_agent_auth module to a subpackage.

* Fri Oct 16 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-3
- Reenable audit.

* Fri Oct  2 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-2
- Upgrade to new wersion 5.3p1

* Tue Sep 29 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-29
- Resolve locking in ssh-add (#491312)

* Thu Sep 24 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-28
- Repair initscript to be acord to guidelines (#521860)
- Add bugzilla# to application of edns and xmodifiers patch

* Wed Sep 16 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-26
- Changed pam stack to password-auth

* Fri Sep 11 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-25
- Dropped homechroot patch

* Mon Sep  7 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-24
- Add check for nosuid, nodev in homechroot

* Tue Sep  1 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-23
- add correct patch for ip-opts

* Tue Sep  1 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-22
- replace ip-opts patch by an upstream candidate version

* Mon Aug 31 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-21
- rearange selinux patch to be acceptable for upstream
- replace seftp patch by an upstream version

* Fri Aug 28 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-20
- merged xmodifiers to redhat patch
- merged gssapi-role to selinux patch
- merged cve-2007_3102 to audit patch
- sesftp patch only with WITH_SELINUX flag
- rearange sesftp patch according to upstream request

* Wed Aug 26 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-19
- minor change in sesftp patch

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 5.2p1-18
- rebuilt with new openssl

* Thu Jul 30 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-17
- Added dnssec support. (#205842)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2p1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-15
- only INTERNAL_SFTP can be home-chrooted
- save _u and _r parts of context changing to sftpd_t

* Fri Jul 17 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-14
- changed internal-sftp context to sftpd_t

* Fri Jul  3 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-13
- changed home length path patch to upstream version

* Tue Jun 30 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-12
- create '~/.ssh/known_hosts' within proper context

* Mon Jun 29 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-11
- length of home path in ssh now limited by PATH_MAX
- correct timezone with daylight processing

* Sat Jun 27 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-10
- final version chroot %%h (sftp only)

* Tue Jun 23 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-9
- repair broken ls in chroot %%h

* Fri Jun 12 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-8
- add XMODIFIERS to exported environment (#495690)

* Fri May 15 2009 Tomas Mraz <tmraz@redhat.com> - 5.2p1-6
- allow only protocol 2 in the FIPS mode

* Thu Apr 30 2009 Tomas Mraz <tmraz@redhat.com> - 5.2p1-5
- do integrity verification only on binaries which are part
  of the OpenSSH FIPS modules

* Mon Apr 20 2009 Tomas Mraz <tmraz@redhat.com> - 5.2p1-4
- log if FIPS mode is initialized
- make aes-ctr cipher modes work in the FIPS mode

* Fri Apr  3 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-3
- fix logging after chroot
- enable non root users to use chroot %%h in internal-sftp

* Fri Mar 13 2009 Tomas Mraz <tmraz@redhat.com> - 5.2p1-2
- add AES-CTR ciphers to the FIPS mode proposal

* Mon Mar  9 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-1
- upgrade to new upstream release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1p1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Tomas Mraz <tmraz@redhat.com> - 5.1p1-7
- drop obsolete triggers
- add testing FIPS mode support
- LSBize the initscript (#247014)

* Fri Jan 30 2009 Tomas Mraz <tmraz@redhat.com> - 5.1p1-6
- enable use of ssl engines (#481100)

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 5.1p1-5
- remove obsolete --with-rsh (#478298)
- add pam_sepermit to allow blocking confined users in permissive mode
  (#471746)
- move system-auth after pam_selinux in the session stack

* Thu Dec 11 2008 Tomas Mraz <tmraz@redhat.com> - 5.1p1-4
- set FD_CLOEXEC on channel sockets (#475866)
- adjust summary
- adjust nss-keys patch so it is applicable without selinux patches (#470859)

* Fri Oct 17 2008 Tomas Mraz <tmraz@redhat.com> - 5.1p1-3
- fix compatibility with some servers (#466818)

* Thu Jul 31 2008 Tomas Mraz <tmraz@redhat.com> - 5.1p1-2
- fixed zero length banner problem (#457326)

* Wed Jul 23 2008 Tomas Mraz <tmraz@redhat.com> - 5.1p1-1
- upgrade to new upstream release
- fixed a problem with public key authentication and explicitely
  specified SELinux role

* Wed May 21 2008 Tomas Mraz <tmraz@redhat.com> - 5.0p1-3
- pass the connection socket to ssh-keysign (#447680)

* Mon May 19 2008 Tomas Mraz <tmraz@redhat.com> - 5.0p1-2
- add LANGUAGE to accepted/sent environment variables (#443231)
- use pam_selinux to obtain the user context instead of doing it itself
- unbreak server keep alive settings (patch from upstream)
- small addition to scp manpage

* Mon Apr  7 2008 Tomas Mraz <tmraz@redhat.com> - 5.0p1-1
- upgrade to new upstream (#441066)
- prevent initscript from killing itself on halt with upstart (#438449)
- initscript status should show that the daemon is running
  only when the main daemon is still alive (#430882)

* Thu Mar  6 2008 Tomas Mraz <tmraz@redhat.com> - 4.7p1-10
- fix race on control master and cleanup stale control socket (#436311)
  patches by David Woodhouse

* Fri Feb 29 2008 Tomas Mraz <tmraz@redhat.com> - 4.7p1-9
- set FD_CLOEXEC on client socket
- apply real fix for window size problem (#286181) from upstream
- apply fix for the spurious failed bind from upstream
- apply open handle leak in sftp fix from upstream

* Tue Feb 12 2008 Dennis Gilmore <dennis@ausil.us> - 4.7p1-8
- we build for sparcv9 now  and it needs -fPIE

* Thu Jan  3 2008 Tomas Mraz <tmraz@redhat.com> - 4.7p1-7
- fix gssapi auth with explicit selinux role requested (#427303) - patch
  by Nalin Dahyabhai

* Tue Dec  4 2007 Tomas Mraz <tmraz@redhat.com> - 4.7p1-6
- explicitly source krb5-devel profile script

* Tue Dec 04 2007 Release Engineering <rel-eng at fedoraproject dot org> - 4.7p1-5
- Rebuild for openssl bump

* Tue Nov 20 2007 Tomas Mraz <tmraz@redhat.com> - 4.7p1-4
- do not copy /etc/localtime into the chroot as it is not
  necessary anymore (#193184)
- call setkeycreatecon when selinux context is established
- test for NULL privk when freeing key (#391871) - patch by
  Pierre Ossman

* Mon Sep 17 2007 Tomas Mraz <tmraz@redhat.com> - 4.7p1-2
- revert default window size adjustments (#286181)

* Thu Sep  6 2007 Tomas Mraz <tmraz@redhat.com> - 4.7p1-1
- upgrade to latest upstream
- use libedit in sftp (#203009)
- fixed audit log injection problem (CVE-2007-3102)

* Thu Aug  9 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-8
- fix sftp client problems on write error (#247802)
- allow disabling autocreation of server keys (#235466)

* Wed Jun 20 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-7
- experimental NSS keys support
- correctly setup context when empty level requested (#234951)

* Tue Mar 20 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-6
- mls level check must be done with default role same as requested

* Mon Mar 19 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-5
- make profile.d/gnome-ssh-askpass.* regular files (#226218)

* Tue Feb 27 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-4
- reject connection if requested mls range is not obtained (#229278)

* Thu Feb 22 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-3
- improve Buildroot
- remove duplicate /etc/ssh from files

* Tue Jan 16 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-2
- support mls on labeled networks (#220487)
- support mls level selection on unlabeled networks
- allow / in usernames in scp (only beginning /, ./, and ../ is special) 

* Thu Dec 21 2006 Tomas Mraz <tmraz@redhat.com> - 4.5p1-1
- update to 4.5p1 (#212606)

* Thu Nov 30 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-14
- fix gssapi with DNS loadbalanced clusters (#216857)

* Tue Nov 28 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-13
- improved pam_session patch so it doesn't regress, the patch is necessary
  for the pam_session_close to be called correctly as uid 0

* Fri Nov 10 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-12
- CVE-2006-5794 - properly detect failed key verify in monitor (#214641)

* Thu Nov  2 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-11
- merge sshd initscript patches
- kill all ssh sessions when stop is called in halt or reboot runlevel
- remove -TERM option from killproc so we don't race on sshd restart

* Mon Oct  2 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-10
- improve gssapi-no-spnego patch (#208102)
- CVE-2006-4924 - prevent DoS on deattack detector (#207957)
- CVE-2006-5051 - don't call cleanups from signal handler (#208459)

* Wed Aug 23 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-9
- don't report duplicate syslog messages, use correct local time (#189158)
- don't allow spnego as gssapi mechanism (from upstream)
- fixed memleaks found by Coverity (from upstream)
- allow ip options except source routing (#202856) (patch by HP)

* Tue Aug  8 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-8
- drop the pam-session patch from the previous build (#201341)
- don't set IPV6_V6ONLY sock opt when listening on wildcard addr (#201594)

* Thu Jul 20 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-7
- dropped old ssh obsoletes
- call the pam_session_open/close from the monitor when privsep is
  enabled so it is always called as root (patch by Darren Tucker)

* Mon Jul 17 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-6
- improve selinux patch (by Jan Kiszka)
- upstream patch for buffer append space error (#191940)
- fixed typo in configure.ac (#198986)
- added pam_keyinit to pam configuration (#198628)
- improved error message when askpass dialog cannot grab
  keyboard input (#198332)
- buildrequires xauth instead of xorg-x11-xauth
- fixed a few rpmlint warnings

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.3p2-5.1
- rebuild

* Fri Apr 14 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-5
- don't request pseudoterminal allocation if stdin is not tty (#188983)

* Thu Mar  2 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-4
- allow access if audit is not compiled in kernel (#183243)

* Fri Feb 24 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-3
- enable the subprocess in chroot to send messages to system log
- sshd should prevent login if audit call fails

* Tue Feb 21 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-2
- print error from scp if not remote (patch by Bjorn Augustsson #178923)

* Mon Feb 13 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-1
- new version

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.3p1-2.1
- bump again for double-long bug on ppc(64)

* Mon Feb  6 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p1-2
- fixed another place where syslog was called in signal handler
- pass locale environment variables to server, accept them there (#179851)

* Wed Feb  1 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p1-1
- new version, dropped obsolete patches

* Tue Dec 20 2005 Tomas Mraz <tmraz@redhat.com> - 4.2p1-10
- hopefully make the askpass dialog less confusing (#174765)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 22 2005 Tomas Mraz <tmraz@redhat.com> - 4.2p1-9
- drop x11-ssh-askpass from the package
- drop old build_6x ifs from spec file
- improve gnome-ssh-askpass so it doesn't reveal number of passphrase 
  characters to person looking at the display
- less hackish fix for the __USE_GNU problem

* Fri Nov 18 2005 Nalin Dahyabhai <nalin@redhat.com> - 4.2p1-8
- work around missing gccmakedep by wrapping makedepend in a local script
- remove now-obsolete build dependency on "xauth"

* Thu Nov 17 2005 Warren Togami <wtogami@redhat.com> - 4.2p1-7
- xorg-x11-devel -> libXt-devel
- rebuild for new xauth location so X forwarding works
- buildreq audit-libs-devel
- buildreq automake for aclocal
- buildreq imake for xmkmf
-  -D_GNU_SOURCE in flags in order to get it to build
   Ugly hack to workaround openssh defining __USE_GNU which is
   not allowed and causes problems according to Ulrich Drepper
   fix this the correct way after FC5test1

* Wed Nov  9 2005 Jeremy Katz <katzj@redhat.com> - 4.2p1-6
- rebuild against new openssl

* Fri Oct 28 2005 Tomas Mraz <tmraz@redhat.com> 4.2p1-5
- put back the possibility to skip SELinux patch
- add patch for user login auditing by Steve Grubb

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 4.2p1-4
- Change selinux patch to use get_default_context_with_rolelevel in libselinux.

* Thu Oct 13 2005 Tomas Mraz <tmraz@redhat.com> 4.2p1-3
- Update selinux patch to use getseuserbyname

* Fri Oct  7 2005 Tomas Mraz <tmraz@redhat.com> 4.2p1-2
- use include instead of pam_stack in pam config
- use fork+exec instead of system in scp - CVE-2006-0225 (#168167)
- upstream patch for displaying authentication errors

* Tue Sep 06 2005 Tomas Mraz <tmraz@redhat.com> 4.2p1-1
- upgrade to a new upstream version

* Tue Aug 16 2005 Tomas Mraz <tmraz@redhat.com> 4.1p1-5
- use x11-ssh-askpass if openssh-askpass-gnome is not installed (#165207)
- install ssh-copy-id from contrib (#88707)

* Wed Jul 27 2005 Tomas Mraz <tmraz@redhat.com> 4.1p1-4
- don't deadlock on exit with multiple X forwarded channels (#152432)
- don't use X11 port which can't be bound on all IP families (#163732)

* Wed Jun 29 2005 Tomas Mraz <tmraz@redhat.com> 4.1p1-3
- fix small regression caused by the nologin patch (#161956)
- fix race in getpeername error checking (mindrot #1054)

* Thu Jun  9 2005 Tomas Mraz <tmraz@redhat.com> 4.1p1-2
- use only pam_nologin for nologin testing

* Mon Jun  6 2005 Tomas Mraz <tmraz@redhat.com> 4.1p1-1
- upgrade to a new upstream version
- call pam_loginuid as a pam session module

* Mon May 16 2005 Tomas Mraz <tmraz@redhat.com> 4.0p1-3
- link libselinux only to sshd (#157678)

* Mon Apr  4 2005 Tomas Mraz <tmraz@redhat.com> 4.0p1-2
- fixed Local/RemoteForward in ssh_config.5 manpage
- fix fatal when Local/RemoteForward is used and scp run (#153258)
- don't leak user validity when using krb5 authentication

* Thu Mar 24 2005 Tomas Mraz <tmraz@redhat.com> 4.0p1-1
- upgrade to 4.0p1
- remove obsolete groups patch

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 28 2005 Nalin Dahyabhai <nalin@redhat.com> 3.9p1-12
- rebuild so that configure can detect that krb5_init_ets is gone now

* Mon Feb 21 2005 Tomas Mraz <tmraz@redhat.com> 3.9p1-11
- don't call syslog in signal handler
- allow password authentication when copying from remote
  to remote machine (#103364)

* Wed Feb  9 2005 Tomas Mraz <tmraz@redhat.com>
- add spaces to messages in initscript (#138508)

* Tue Feb  8 2005 Tomas Mraz <tmraz@redhat.com> 3.9p1-10
- enable trusted forwarding by default if X11 forwarding is 
  required by user (#137685 and duplicates)
- disable protocol 1 support by default in sshd server config (#88329)
- keep the gnome-askpass dialog above others (#69131)

* Fri Feb  4 2005 Tomas Mraz <tmraz@redhat.com>
- change permissions on pam.d/sshd to 0644 (#64697)
- patch initscript so it doesn't kill opened sessions if
  the sshd daemon isn't running anymore (#67624)

* Mon Jan  3 2005 Bill Nottingham <notting@redhat.com> 3.9p1-9
- don't use initlog

* Mon Nov 29 2004 Thomas Woerner <twoerner@redhat.com> 3.9p1-8.1
- fixed PIE build for all architectures

* Mon Oct  4 2004 Nalin Dahyabhai <nalin@redhat.com> 3.9p1-8
- add a --enable-vendor-patchlevel option which allows a ShowPatchLevel option
  to enable display of a vendor patch level during version exchange (#120285)
- configure with --disable-strip to build useful debuginfo subpackages

* Mon Sep 20 2004 Bill Nottingham <notting@redhat.com> 3.9p1-7
- when using gtk2 for askpass, don't buildprereq gnome-libs-devel

* Tue Sep 14 2004 Nalin Dahyabhai <nalin@redhat.com> 3.9p1-6
- build

* Mon Sep 13 2004 Nalin Dahyabhai <nalin@redhat.com>
- disable ACSS support

* Thu Sep 2 2004 Daniel Walsh <dwalsh@redhat.com> 3.9p1-5
- Change selinux patch to use get_default_context_with_role in libselinux.

* Thu Sep 2 2004 Daniel Walsh <dwalsh@redhat.com> 3.9p1-4
- Fix patch
	* Bad debug statement.
	* Handle root/sysadm_r:kerberos

* Thu Sep 2 2004 Daniel Walsh <dwalsh@redhat.com> 3.9p1-3
- Modify Colin Walter's patch to allow specifying rule during connection

* Tue Aug 31 2004 Daniel Walsh <dwalsh@redhat.com> 3.9p1-2
- Fix TTY handling for SELinux

* Tue Aug 24 2004 Daniel Walsh <dwalsh@redhat.com> 3.9p1-1
- Update to upstream

* Sun Aug 1 2004 Alan Cox <alan@redhat.com> 3.8.1p1-5
- Apply buildreq fixup patch (#125296)

* Tue Jun 15 2004 Daniel Walsh <dwalsh@redhat.com> 3.8.1p1-4
- Clean up patch for upstream submission.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 9 2004 Daniel Walsh <dwalsh@redhat.com> 3.8.1p1-2
- Remove use of pam_selinux and patch selinux in directly.  

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> 3.8.1p1-1
- request gssapi-with-mic by default but not delegation (flag day for anyone
  who used previous gssapi patches)
- no longer request x11 forwarding by default

* Thu Jun 3 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-36
- Change pam file to use open and close with pam_selinux

* Tue Jun  1 2004 Nalin Dahyabhai <nalin@redhat.com> 3.8.1p1-0
- update to 3.8.1p1
- add workaround from CVS to reintroduce passwordauth using pam

* Tue Jun 1 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-35
- Remove CLOSEXEC on STDERR

* Tue Mar 16 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-34

* Wed Mar 03 2004 Phil Knirsch <pknirsch@redhat.com> 3.6.1p2-33.30.1
- Built RHLE3 U2 update package.

* Wed Mar 3 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-33
- Close file descriptors on exec 

* Mon Mar  1 2004 Thomas Woerner <twoerner@redhat.com> 3.6.1p2-32
- fixed pie build

* Thu Feb 26 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-31
- Add restorecon to startup scripts

* Thu Feb 26 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-30
- Add multiple qualified to openssh

* Mon Feb 23 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-29
- Eliminate selinux code and use pam_selinux

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-27
- turn off pie on ppc

* Mon Jan 26 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-26
- fix is_selinux_enabled

* Wed Jan 14 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-25
- Rebuild to grab shared libselinux

* Wed Dec 3 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-24
- turn on selinux

* Tue Nov 18 2003 Nalin Dahyabhai <nalin@redhat.com>
- un#ifdef out code for reporting password expiration in non-privsep
  mode (#83585)

* Mon Nov 10 2003 Nalin Dahyabhai <nalin@redhat.com>
- add machinery to build with/without -fpie/-pie, default to doing so

* Thu Nov 06 2003 David Woodhouse <dwmw2@redhat.com> 3.6.1p2-23
- Don't whinge about getsockopt failing (#109161)

* Fri Oct 24 2003 Nalin Dahyabhai <nalin@redhat.com>
- add missing buildprereq on zlib-devel (#104558)

* Mon Oct 13 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-22
- turn selinux off

* Mon Oct 13 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-21.sel
- turn selinux on

* Fri Sep 19 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-21
- turn selinux off

* Fri Sep 19 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-20.sel
- turn selinux on

* Fri Sep 19 2003 Nalin Dahyabhai <nalin@redhat.com>
- additional fix for apparently-never-happens double-free in buffer_free()
- extend fix for #103998 to cover SSH1

* Wed Sep 17 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-19
- rebuild

* Wed Sep 17 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-18
- additional buffer manipulation cleanups from Solar Designer

* Wed Sep 17 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-17
- turn selinux off

* Wed Sep 17 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-16.sel
- turn selinux on

* Tue Sep 16 2003 Bill Nottingham <notting@redhat.com> 3.6.1p2-15
- rebuild

* Tue Sep 16 2003 Bill Nottingham <notting@redhat.com> 3.6.1p2-14
- additional buffer manipulation fixes (CAN-2003-0695)

* Tue Sep 16 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-13.sel
- turn selinux on

* Tue Sep 16 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-12
- rebuild

* Tue Sep 16 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-11
- apply patch to store the correct buffer size in allocated buffers
  (CAN-2003-0693)
- skip the initial PAM authentication attempt with an empty password if
  empty passwords are not permitted in our configuration (#103998)

* Fri Sep 5 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-10
- turn selinux off

* Fri Sep 5 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-9.sel
- turn selinux on

* Tue Aug 26 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-8
- Add BuildPreReq gtk2-devel if gtk2

* Tue Aug 12 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-7
- rebuild

* Tue Aug 12 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-6
- modify patch which clears the supplemental group list at startup to only
  complain if setgroups() fails if sshd has euid == 0
- handle krb5 installed in %%{_prefix} or elsewhere by using krb5-config

* Mon Jul 28 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-5
- Add SELinux patch

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-4
- rebuild

* Wed Jul 16 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-3
- rebuild

* Wed Jul 16 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-2
- rebuild

* Thu Jun  5 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-1
- update to 3.6.1p2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
6 rebuilt

* Mon Mar 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch for getsockopt() call to work on bigendian 64bit archs

* Fri Feb 14 2003 Nalin Dahyabhai <nalin@redhat.com> 3.5p1-6
- move scp to the -clients subpackage, because it directly depends on ssh
  which is also in -clients (#84329)

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 3.5p1-5
- rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 3.5p1-3
- rebuild

* Tue Nov 12 2002 Nalin Dahyabhai <nalin@redhat.com> 3.5p1-2
- patch PAM configuration to use relative path names for the modules, allowing
  us to not worry about which arch the modules are built for on multilib systems

* Tue Oct 15 2002 Nalin Dahyabhai <nalin@redhat.com> 3.5p1-1
- update to 3.5p1, merging in filelist/perm changes from the upstream spec

* Fri Oct  4 2002 Nalin Dahyabhai <nalin@redhat.com> 3.4p1-3
- merge

* Thu Sep 12 2002  Than Ngo <than@redhat.com> 3.4p1-2.1
- fix to build on multilib systems

* Thu Aug 29 2002 Curtis Zinzilieta <curtisz@redhat.com> 3.4p1-2gss
- added gssapi patches and uncommented patch here

* Wed Aug 14 2002 Nalin Dahyabhai <nalin@redhat.com> 3.4p1-2
- pull patch from CVS to fix too-early free in ssh-keysign (#70009)

* Thu Jun 27 2002 Nalin Dahyabhai <nalin@redhat.com> 3.4p1-1
- 3.4p1
- drop anon mmap patch

* Tue Jun 25 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3p1-2
- rework the close-on-exit docs
- include configuration file man pages
- make use of nologin as the privsep shell optional

* Mon Jun 24 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3p1-1
- update to 3.3p1
- merge in spec file changes from upstream (remove setuid from ssh, ssh-keysign)
- disable gtk2 askpass
- require pam-devel by filename rather than by package for erratum
- include patch from Solar Designer to work around anonymous mmap failures

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2.3p1-3
- don't require autoconf any more

* Fri May 31 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2.3p1-2
- build gnome-ssh-askpass with gtk2

* Tue May 28 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2.3p1-1
- update to 3.2.3p1
- merge in spec file changes from upstream

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2.2p1-1
- update to 3.2.2p1

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-4
- drop buildreq on db1-devel
- require pam-devel by package name
- require autoconf instead of autoconf253 again

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-3
- pull patch from CVS to avoid printing error messages when some of the
  default keys aren't available when running ssh-add
- refresh to current revisions of Simon's patches
 
* Thu Mar 21 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-2gss
- reintroduce Simon's gssapi patches
- add buildprereq for autoconf253, which is needed to regenerate configure
  after applying the gssapi patches
- refresh to the latest version of Markus's patch to build properly with
  older versions of OpenSSL

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-2
- bump and grind (through the build system)

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-1
- require sharutils for building (mindrot #137)
- require db1-devel only when building for 6.x (#55105), which probably won't
  work anyway (3.1 requires OpenSSL 0.9.6 to build), but what the heck
- require pam-devel by file (not by package name) again
- add Markus's patch to compile with OpenSSL 0.9.5a (from
  http://bugzilla.mindrot.org/show_bug.cgi?id=141) and apply it if we're
  building for 6.x

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-0
- update to 3.1p1

* Tue Mar  5 2002 Nalin Dahyabhai <nalin@redhat.com> SNAP-20020305
- update to SNAP-20020305
- drop debug patch, fixed upstream

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> SNAP-20020220
- update to SNAP-20020220 for testing purposes (you've been warned, if there's
  anything to be warned about, gss patches won't apply, I don't mind)

* Wed Feb 13 2002 Nalin Dahyabhai <nalin@redhat.com> 3.0.2p1-3
- add patches from Simon Wilkinson and Nicolas Williams for GSSAPI key
  exchange, authentication, and named key support

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 3.0.2p1-2
- remove dependency on db1-devel, which has just been swallowed up whole
  by gnome-libs-devel

* Sat Dec 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- adjust build dependencies so that build6x actually works right (fix
  from Hugo van der Kooij)

* Tue Dec  4 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0.2p1-1
- update to 3.0.2p1

* Fri Nov 16 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0.1p1-1
- update to 3.0.1p1

* Tue Nov 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to current CVS (not for use in distribution)

* Thu Nov  8 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0p1-1
- merge some of Damien Miller <djm@mindrot.org> changes from the upstream
  3.0p1 spec file and init script

* Wed Nov  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.0p1
- update to x11-ssh-askpass 1.2.4.1
- change build dependency on a file from pam-devel to the pam-devel package
- replace primes with moduli

* Thu Sep 27 2001 Nalin Dahyabhai <nalin@redhat.com> 2.9p2-9
- incorporate fix from Markus Friedl's advisory for IP-based authorization bugs

* Thu Sep 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.9p2-8
- Merge changes to rescue build from current sysadmin survival cd

* Thu Sep  6 2001 Nalin Dahyabhai <nalin@redhat.com> 2.9p2-7
- fix scp's server's reporting of file sizes, and build with the proper
  preprocessor define to get large-file capable open(), stat(), etc.
  (sftp has been doing this correctly all along) (#51827)
- configure without --with-ipv4-default on RHL 7.x and newer (#45987,#52247)
- pull cvs patch to fix support for /etc/nologin for non-PAM logins (#47298)
- mark profile.d scriptlets as config files (#42337)
- refer to Jason Stone's mail for zsh workaround for exit-hanging quasi-bug
- change a couple of log() statements to debug() statements (#50751)
- pull cvs patch to add -t flag to sshd (#28611)
- clear fd_sets correctly (one bit per FD, not one byte per FD) (#43221)

* Mon Aug 20 2001 Nalin Dahyabhai <nalin@redhat.com> 2.9p2-6
- add db1-devel as a BuildPrerequisite (noted by Hans Ecke)

* Thu Aug 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- pull cvs patch to fix remote port forwarding with protocol 2

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- pull cvs patch to add session initialization to no-pty sessions
- pull cvs patch to not cut off challengeresponse auth needlessly
- refuse to do X11 forwarding if xauth isn't there, handy if you enable
  it by default on a system that doesn't have X installed (#49263)

* Wed Aug  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't apply patches to code we don't intend to build (spotted by Matt Galgoci)

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- pass OPTIONS correctly to initlog (#50151)

* Wed Jul 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- switch to x11-ssh-askpass 1.2.2

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- disable the gssapi patch

* Mon Jun 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.9p2
- refresh to a new version of the gssapi patch

* Thu Jun  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- change Copyright: BSD to License: BSD
- add Markus Friedl's unverified patch for the cookie file deletion problem
  so that we can verify it
- drop patch to check if xauth is present (was folded into cookie patch)
- don't apply gssapi patches for the errata candidate
- clear supplemental groups list at startup

* Fri May 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix an error parsing the new default sshd_config
- add a fix from Markus Friedl (via openssh-unix-dev) for ssh-keygen not
  dealing with comments right

* Thu May 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- add in Simon Wilkinson's GSSAPI patch to give it some testing in-house,
  to be removed before the next beta cycle because it's a big departure
  from the upstream version

* Thu May  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish marking strings in the init script for translation
- modify init script to source /etc/sysconfig/sshd and pass $OPTIONS to sshd
  at startup (change merged from openssh.com init script, originally by
  Pekka Savola)
- refuse to do X11 forwarding if xauth isn't there, handy if you enable
  it by default on a system that doesn't have X installed

* Wed May  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.9
- drop various patches that came from or went upstream or to or from CVS

* Wed Apr 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- only require initscripts 5.00 on 6.2 (reported by Peter Bieringer)

* Sun Apr  8 2001 Preston Brown <pbrown@redhat.com>
- remove explicit openssl requirement, fixes builddistro issue
- make initscript stop() function wait until sshd really dead to avoid 
  races in condrestart

* Mon Apr  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- mention that challengereponse supports PAM, so disabling password doesn't
  limit users to pubkey and rsa auth (#34378)
- bypass the daemon() function in the init script and call initlog directly,
  because daemon() won't start a daemon it detects is already running (like
  open connections)
- require the version of openssl we had when we were built

* Fri Mar 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- make do_pam_setcred() smart enough to know when to establish creds and
  when to reinitialize them
- add in a couple of other fixes from Damien for inclusion in the errata

* Thu Mar 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.5.2p2
- call setcred() again after initgroups, because the "creds" could actually
  be group memberships

* Tue Mar 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.5.2p1 (includes endianness fixes in the rijndael implementation)
- don't enable challenge-response by default until we find a way to not
  have too many userauth requests (we may make up to six pubkey and up to
  three password attempts as it is)
- remove build dependency on rsh to match openssh.com's packages more closely

* Sat Mar  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove dependency on openssl -- would need to be too precise

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Mon Feb 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- Revert the patch to move pam_open_session.
- Init script and spec file changes from Pekka Savola. (#28750)
- Patch sftp to recognize '-o protocol' arguments. (#29540)

* Thu Feb 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- Chuck the closing patch.
- Add a trigger to add host keys for protocol 2 to the config file, now that
  configuration file syntax requires us to specify it with HostKey if we
  specify any other HostKey values, which we do.

* Tue Feb 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- Redo patch to move pam_open_session after the server setuid()s to the user.
- Rework the nopam patch to use be picked up by autoconf.

* Mon Feb 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- Update for 2.5.1p1.
- Add init script mods from Pekka Savola.
- Tweak the init script to match the CVS contrib script more closely.
- Redo patch to ssh-add to try to adding both identity and id_dsa to also try
  adding id_rsa.

* Fri Feb 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- Update for 2.5.0p1.
- Use $RPM_OPT_FLAGS instead of -O when building gnome-ssh-askpass
- Resync with parts of Damien Miller's openssh.spec from CVS, including
  update of x11 askpass to 1.2.0.
- Only require openssl (don't prereq) because we generate keys in the init
  script now.

* Tue Feb 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- Don't open a PAM session until we've forked and become the user (#25690).
- Apply Andrew Bartlett's patch for letting pam_authenticate() know which
  host the user is attempting a login from.
- Resync with parts of Damien Miller's openssh.spec from CVS.
- Don't expose KbdInt responses in debug messages (from CVS).
- Detect and handle errors in rsa_{public,private}_decrypt (from CVS).

* Wed Feb  7 2001 Trond Eivind Glomsrxd <teg@redhat.com>
- i18n-tweak to initscript.

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- More gettextizing.
- Close all files after going into daemon mode (needs more testing).
- Extract patch from CVS to handle auth banners (in the client).
- Extract patch from CVS to handle compat weirdness.

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- Finish with the gettextizing.

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- Fix a bug in auth2-pam.c (#23877)
- Gettextize the init script.

* Wed Dec 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- Incorporate a switch for using PAM configs for 6.x, just in case.

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Incorporate Bero's changes for a build specifically for rescue CDs.

* Wed Nov 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Don't treat pam_setcred() failure as fatal unless pam_authenticate() has
  succeeded, to allow public-key authentication after a failure with "none"
  authentication.  (#21268)

* Tue Nov 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to x11-askpass 1.1.1. (#21301)
- Don't second-guess fixpaths, which causes paths to get fixed twice. (#21290)

* Mon Nov 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- Merge multiple PAM text messages into subsequent prompts when possible when
  doing keyboard-interactive authentication.

* Sun Nov 26 2000 Nalin Dahyabhai <nalin@redhat.com>
- Disable the built-in MD5 password support.  We're using PAM.
- Take a crack at doing keyboard-interactive authentication with PAM, and
  enable use of it in the default client configuration so that the client
  will try it when the server disallows password authentication.
- Build with debugging flags.  Build root policies strip all binaries anyway.

* Tue Nov 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- Use DESTDIR instead of %%makeinstall.
- Remove /usr/X11R6/bin from the path-fixing patch.

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add the primes file from the latest snapshot to the main package (#20884).
- Add the dev package to the prereq list (#19984).
- Remove the default path and mimic login's behavior in the server itself.

* Fri Nov 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- Resync with conditional options in Damien Miller's .spec file for an errata.
- Change libexecdir from %%{_libexecdir}/ssh to %%{_libexecdir}/openssh.

* Tue Nov  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to OpenSSH 2.3.0p1.
- Update to x11-askpass 1.1.0.
- Enable keyboard-interactive authentication.

* Mon Oct 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to ssh-askpass-x11 1.0.3.
- Change authentication related messages to be private (#19966).

* Tue Oct 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- Patch ssh-keygen to be able to list signatures for DSA public key files
  it generates.

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add BuildPreReq on /usr/include/security/pam_appl.h to be sure we always
  build PAM authentication in.
- Try setting SSH_ASKPASS if gnome-ssh-askpass is installed.
- Clean out no-longer-used patches.
- Patch ssh-add to try to add both identity and id_dsa, and to error only
  when neither exists.

* Mon Oct  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update x11-askpass to 1.0.2. (#17835)
- Add BuildPreReqs for /bin/login and /usr/bin/rsh so that configure will
  always find them in the right place. (#17909)
- Set the default path to be the same as the one supplied by /bin/login, but
  add /usr/X11R6/bin. (#17909)
- Try to handle obsoletion of ssh-server more cleanly.  Package names
  are different, but init script name isn't. (#17865)

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.2.0p1. (#17835)
- Tweak the init script to allow proper restarting. (#18023)

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 20000823 snapshot.
- Change subpackage requirements from %%{version} to %%{version}-%%{release}
- Back out the pipe patch.

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p4, which includes fixes for config file parsing problems.
- Move the init script back.
- Add Damien's quick fix for wackiness.

* Wed Jul 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p3, which includes fixes for X11 forwarding and strtok().

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- Move condrestart to server postun.
- Move key generation to init script.
- Actually use the right patch for moving the key generation to the init script.
- Clean up the init script a bit.

* Wed Jul  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Fix X11 forwarding, from mail post by Chan Shih-Ping Richard.

* Sun Jul  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p2.
- Use of strtok() considered harmful.

* Sat Jul  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- Get the build root out of the man pages.

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add and use condrestart support in the init script.
- Add newer initscripts as a prereq.

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- Build in new environment (release 2)
- Move -clients subpackage to Applications/Internet group

* Fri Jun  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.2.1p1

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- Patch to build with neither RSA nor RSAref.
- Miscellaneous FHS-compliance tweaks.
- Fix for possibly-compressed man pages.

* Wed Mar 15 2000 Damien Miller <djm@ibs.com.au>
- Updated for new location
- Updated for new gnome-ssh-askpass build

* Sun Dec 26 1999 Damien Miller <djm@mindrot.org>
- Added Jim Knoble's <jmknoble@pobox.com> askpass

* Mon Nov 15 1999 Damien Miller <djm@mindrot.org>
- Split subpackages further based on patch from jim knoble <jmknoble@pobox.com>

* Sat Nov 13 1999 Damien Miller <djm@mindrot.org>
- Added 'Obsoletes' directives

* Tue Nov 09 1999 Damien Miller <djm@ibs.com.au>
- Use make install
- Subpackages

* Mon Nov 08 1999 Damien Miller <djm@ibs.com.au>
- Added links for slogin
- Fixed perms on manpages

* Sat Oct 30 1999 Damien Miller <djm@ibs.com.au>
- Renamed init script

* Fri Oct 29 1999 Damien Miller <djm@ibs.com.au>
- Back to old binary names

* Thu Oct 28 1999 Damien Miller <djm@ibs.com.au>
- Use autoconf
- New binary names

* Wed Oct 27 1999 Damien Miller <djm@ibs.com.au>
- Initial RPMification, based on Jan "Yenya" Kasprzak's <kas@fi.muni.cz> spec.
