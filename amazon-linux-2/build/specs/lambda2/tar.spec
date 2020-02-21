%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%global WITH_SELINUX 1
%endif
Summary: A GNU file archiving program
Name: tar
Epoch: 2
Version: 1.26
Release: 35%{?dist}
License: GPLv3+
Group: Applications/Archiving
URL: http://www.gnu.org/software/tar/

Source0: ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.xz
Source1: ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.xz.sig
# Manpage for tar and gtar, a bit modified help2man generated manpage
Source2: tar.1

# Stop issuing lone zero block warnings.
# ~> https://bugzilla.redhat.com/show_bug.cgi?id=135601
# ~> downstream
Patch1: tar-1.14-loneZeroWarning.patch

# Fix extracting sparse files to a file system like vfat, when ftruncate may fail
# to grow the size of a file.
# ~> #179507,
# ~> http://lists.gnu.org/archive/html/bug-tar/2006-02/msg00000.html
# ~> still downtream (do we need this now? ftruncate & vfat works is now OK)
Patch2: tar-1.15.1-vfatTruncate.patch

# Change inclusion defaults of tar to
# "--wildcards --anchored --wildcards-match-slash" for compatibility reasons.
# ~> #206841
# ~> downstream (compatibility)
Patch3: tar-1.17-wildcards.patch

# Ignore errors from setting utime() for source file on read-only file-system.
# ~> #500742
# ~> http://lists.gnu.org/archive/html/bug-tar/2009-06/msg00016.html
# ~> still downstream
Patch4: tar-1.22-atime-rofs.patch

# The --old-archive option was not working.
# ~> #594044
# ~> http://lists.gnu.org/archive/html/bug-tar/2010-05/msg00015.html
# ~> upstream (2a61a37)
Patch5: tar-1.23-oldarchive.patch

# Fix for bad cooperation of -C and -u options.
# ~> #688567
# ~> http://lists.gnu.org/archive/html/bug-tar/2012-02/msg00007.html
# ~> still downstream
Patch6: tar-1.26-update-with-change-directory.patch

# Fix rawhide build failure with undefined gets.
# ~> upstream (gnulib)
Patch7: tar-1.26-stdio.in.patch

# Fix regression with --keep-old-files option.
# ~> #799252
# ~> http://lists.gnu.org/archive/html/bug-tar/2011-11/msg00043.html
# ~> upstream (7a5a3708c)
Patch8: tar-1.26-add-skip-old-files-option.patch

# Prepare included gnulib library for SELinux support.
# -> Related to the next patch.
Patch9:  tar-1.26-selinux-gnulib.patch

# Add support for extended attributes, SELinux and POSIX ACLs.
# ~> Original implementation #200925
# ~> http://lists.gnu.org/archive/html/bug-tar/2012-08/msg00012.html
# ~> upstream (b997c90f9, 696338043, d36f5a3cc, 085cace18, up-to ~> 83701a590)
Patch10: tar-1.26-xattrs.patch

# Fix problem with bit UIDs/GIDs (> 2^21) and --posix format.
# ~> #913406
# ~> upstream (it is part of df7b55a8f6354e)
Patch11: tar-1.26-posix-biguid.patch

# Allow store sparse files of effective size >8GB into pax archives
# ~> #516309
# ~> http://lists.gnu.org/archive/html/bug-tar/2013-01/msg00001.html
# ~> already upstream (2f6c03cba)
Patch12: tar-1.26-pax-big-sparse-files.patch

# Fix: Allow extracting single volume in a multi-volume archive
# ~> #919897
# ~> http://lists.gnu.org/archive/html/bug-tar/2013-03/msg00002.html
# ~> upstream (beca89bc)
Patch13: tar-1.26-allow-extract-single-volume.patch

# Do not print xattrs/selinux/acls when --no-xattrs/--no-acls/--no-selinux
# options are used during -tvv output.  (TODO: merge this with xattrs patch
# once becomes upstream)
# ~> downstream (yet)
# ~> proposal: http://lists.gnu.org/archive/html/bug-tar/2013-05/msg00020.html
Patch14: tar-1.26-xattrs-printing.patch

# Use a birthtime instead of ctime.
# ~> upstream (189e43 & 49bd10)
# ~> http://lists.gnu.org/archive/html/bug-tar/2011-06/msg00000.html
# ~> http://lists.gnu.org/archive/html/bug-tar/2013-05/msg00022.html
Patch15: tar-1.26-fix-symlink-eating-bug.patch

# Add documentation which was not yet pushed upstream
# ~> downstream
# ~> #996753
Patch16: tar-1.26-docu-xattrs.patch

# The --xattrs-include or --xattrs-exclude options should imply --xattrs.
# ~> still downstream
#    http://lists.gnu.org/archive/html/bug-tar/2013-05/msg00020.html
# ~> #965969
Patch17: tar-1.26-xattrs-include-implies-xattrs.patch

# If the 'st_size' != 0 && count(blocks) == 0 && st_size < size(block), this
# does not necessarily must be a sparse file.
# ~> upstream (paxutils):  986382a0bb3261
# ~> #1024095, #1024268
Patch18: tar-1.27-sparse-stat-detection.patch

# Don't add "false" default acls when during extraction (#1220890)
# ~> #1220890
Patch19: tar-1.26-default-acls.patch

# Make sure getfilecon's wrapper set's freed pointer to NULL to avoid double
# free later in client code.
# ~> upstream commit (gnulib): b6b3ed1fa4c
# ~> rhbz#1347396
Patch20: tar-1.26-dont-segfault-with-disabled-selinux.patch

# Restore incremental backups correctly, files were not being removed
# ~> upstream commits: 738fb9c2f44 b6979c7278e f86e0605d0e
# ~> rhbz#1184697
Patch21: tar-1.26-restore-incremental-backups.patch

# Fix the behavior of tar when --directory option is used together with
# --remove-files.
# ~> upstream commits: e3d28d84bda b41b004638f f7077dd38b0 d3fd92c6fb2
# 	d28eee6b4f1 74ce228f6df 3125d311e17 3de5db2a151 fc58a8bd984
#	fcde08534bd e6fcc73efa7
# ~> rhbz#1319820
Patch22: tar-1.26-directory_with_remove-files.patch

# Repair the ignorance of --xattrs-exclude/include options
# ~> upstream: bb6ddd8e04c and c81a0853bb8
# ~> rhbz#1341786
Patch23: tar-1.26-xattrs-exclude-include-repair.patch

# Intorduce new option "--keep-directory-symlink", backported from version 1.27
# ~> upstream: 2c06a809180
# ~> rhbz#1350640
Patch24: tar-1.26-keep-directory-symlink.patch

# Fix non-determinism in archive-type-heuristic
# ~> upstream: 1847ec67cec + 1e8b786e651
# ~> rhbz#1437297
Patch25: tar-1.26-non-deterministic-archive-detection.patch

# Avoid tar to hang with --extract --xatrrs and --skip-old-files options
# ~> upstream: 597b0ae509 and ca9399d4e
# -> proposed: https://www.mail-archive.com/bug-tar@gnu.org/msg05229.html
# ~> rhbz#1408168
Patch26: tar-1.26-xattrs-skip-old-files-hangs.patch

# List sparse files of 8GB+ properly, without failure.
# ~> upstream: 586a6263e9d97 ec94fbdf458ad
# ~> paxutils-upstream: 45af1632aa64a 58b8ac114790e
Patch27: tar-1.26-large-sparse-file-listing.patch

# Document (and test) --keep-directory-option
# ~> upstream: d06126f814563b01e598b85a8cc233604a2948f2
# ~> rhbz#1504146
Patch28: tar-1.26-keep-directory-symlink-doc-and-test.patch

# Fix --delay-directory-restore
# ~> rhbz#1513946
# ~> upstream: d06126f814563b01e598b85a8cc233604a2948f2
Patch29: tar-1.26-delay-dir-restore.patch

# Silence gcc warnings
# ~> upstream tar: 17f99bc6f, 5bb0433
# ~> upstream paxutils: 0b3d84a0
Patch999: tar-1.26-silence-gcc.patch

BuildRequires: autoconf automake texinfo gettext libacl-devel rsh

# cover needs of tar's testsuite
BuildRequires: attr acl policycoreutils

%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif
Provides: bundled(gnulib)
Provides: /bin/tar
Provides: /bin/gtar

Prefix: %{_prefix}

%description
The GNU tar program saves many files together in one archive and can
restore individual files (or all of the files) from that archive. Tar
can also be used to add supplemental files to an archive and to update
or list files in the archive. Tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives, and the ability to perform incremental and full
backups.

If you want to use tar for remote backups, you also need to install
the rmt package on the remote box.

%prep
%setup -q
%patch1 -p1 -b .loneZeroWarning
%patch2 -p1 -b .vfatTruncate
%patch3 -p1 -b .wildcards
%patch4 -p1 -b .rofs
%patch5 -p1 -b .oldarchive
%patch6 -p1 -b .update_and_changedir
%patch7 -p1 -b .gets  %{?_rawbuild}
%patch8 -p1 -b .skip-old-files
%patch9 -p1 -b .selinux-gnulib-prep
%patch10 -p1 -b .xattrs-selinux-acls
%patch11 -p1 -b .big_uid_gid
%patch12 -p1 -b .pax-sparse-big-files
%patch13 -p1 -b .extract-single-volume
%patch14 -p1 -b .print-xattrs-fix
%patch15 -p1 -b .birthtime
%patch16 -p1 -b .xattrs-documentation
%patch17 -p1 -b .xattrs-if-xattrs-include
%patch18 -p1 -b .sparse-stat-detection
%patch19 -p1 -b .default-acls
%patch20 -p1 -b .disabled-selinux
%patch21 -p1 -b .incremental-backups
%patch22 -p1 -b .directory
%patch23 -p1 -b .xattrs-exclude-include
%patch24 -p1 -b .keep-directory-symlink
%patch25 -p1 -b .fix-archive-detection-heuristic
%patch26 -p1 -b .extract-xattrs-hangs
%patch27 -p1 -b .large-sparse-file-listing
%patch28 -p1 -b .test-and-doc-for-keep-dir-symlink
%patch29 -p1 -b .delayed-dir
%patch999 -p1 -b .silence-gcc

autoreconf -v

%build
%if ! %{WITH_SELINUX}
%global CONFIGURE_SELINUX --without-selinux
%endif

%configure %{?CONFIGURE_SELINUX} \
    DEFAULT_RMT_DIR=%{_sysconfdir} \
    RSH=%{_bindir}/ssh \
    FORCE_UNSAFE_CONFIGURE=1
make

%install
make DESTDIR=$RPM_BUILD_ROOT install

ln -s tar $RPM_BUILD_ROOT%{_bindir}/gtar

%files
%license COPYING
%{_bindir}/tar
%{_bindir}/gtar

%exclude %{_mandir}
%exclude %{_infodir}
%exclude %{_datadir}
%exclude %{_sysconfdir}

%changelog
* Fri Feb 21 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Jul 09 2018 Pavel Raiskup <praiskup@redhat.com> - 1.26-35
- fix --keep-directory-restore (rhbz#1513946)

* Thu Oct 19 2017 Pavel Raiskup <praiskup@redhat.com> - 1.26-34
- document --keep-directory-symlink in manual page (rhbz#1504146)

* Thu Sep 07 2017 Pavel Raiskup <praiskup@redhat.com> - 1.26-33
- extract: deterministic archive type detection (rhbz#1437297)
- avoid hang when extracting with --xattrs --skip-old-files (rhbz#1408168)
- fix listing of large sparse members (rhbz#1347229)

* Tue Feb 28 2017 Tomas Repik <trepik@redhat.com> - 2:1.26-32
- restore incremental backups correctly, files were not being removed (rhbz#1184697)
- fix the behavior of tar when --directory option is used together with
  --remove-files
- repair the ignorance of --xattrs-exclude/include options (rhbz#1341786)
- Intorduce new option '--keep-directory-symlink'

* Mon Jun 20 2016 Pavel Raiskup <praiskup@redhat.com> - 1.26-31
- avoid double free in selinux code (rhbz#1347396)

* Thu Jun 04 2015 Pavel Raiskup <praiskup@redhat.com> - 1.26-30
- don't mistakenly set default ACLs (#1220890)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2:1.26-29
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2:1.26-28
- Mass rebuild 2013-12-27

* Mon Nov 18 2013 Pavel Raiskup <praiskup@redhat.com> - 1.26-27
- sparse file detection based on fstat() fix (#1024268)

* Mon Sep 09 2013 Pavel Raiskup <praiskup@redhat.com> - 1.26-26
- the --xattrs-include implies --xattrs now (#965969)

* Wed Aug 14 2013 Pavel Raiskup <praiskup@redhat.com> - 1.26-26
- add documenation for xattrs-like options (#996753)

* Thu Jun 20 2013 Pavel Raiskup <praiskup@redhat.com> - 1.26-25
- the /etc/rmt seems to be the best place where to look for rmt binary (see the
  commit message in Fedora's cpio.git for more info)

* Tue Jun 04 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-24
- fix "symlink eating" bug (already fixed in upstream git)

* Thu May 30 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-23
- use /usr/bin/ssh as the default remote shell binary (#969015)
- do not verbose-print xattrs when --no-xattrs option is used
- do not override the config.{guess,sub} twice, this is already done by the
  redhat-rpm-config package (#951442)

* Tue May 28 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-22
- again search for 'rmt' binary in %%{_sbindir} on target host

* Tue Mar 26 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-21
- enable build for arm64 (#926610)
- silence gcc warnings (lint fixes without risk from upstream) for RPMDiff

* Tue Mar 19 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-20
- allow extracting single volume from multi-volume archive (#919897)
- usrmove: /bin/tar ~> /usr/bin/tar, selinux handling edit

* Fri Mar 01 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-19
- fix creating sparse pax archives containing files of effective
  size >8GB (#516309)
- silence rpmlint (fix bad dates in changelog based on git log dates)

* Wed Feb 20 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-18
- fix problems with big uids/gids and pax format (> 2^21) (#913406)

* Mon Feb 18 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-17
- add possibility to 'rpmbuild' without %%check phase
- make the autoreconf phase verbose
- re-create older patches (avoid offset warnings during patching)
- remove patches which we don't need now (xattrs - will be updated, sigpipe -
  test should work now, partial revert of *at() conversion was done because of
  incompatible xattr patch)
- add upstream up2date xattr patch

* Fri Feb 01 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-16
- make the info documentation more visible in manpage (#903666)
- sync tar.1 manpage with actual --help output (e.g. added --skip-old-files)
- add the last_help2man_run file to git repo to allow more easily find changes
  in --help in future
- make the DEFAULTS section to be more visible in man page
- verbose 'make check' only when some fail happened (append to koji build.log)

* Thu Nov 29 2012 Ondrej Vasik <ovasik@redhat.com> - 2:1.26-15
- add missing --full-time option to manpage

* Thu Oct 18 2012 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-14
- fix bad behaviour of --keep-old-files and add --skip-old-files option
  (#799252)

* Wed Oct 10 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-13
- fix badly written macro for building --without-selinux
- allow to build tar in difference CoverityScan by forcing the '.gets' patch to
  be applied even in the run without patches

* Fri Oct 05 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-12
- repair the xattr-gnulib-prepare patch to allow build tar without SELinux
  support
- fedora-review compliance -> remove trailing white-spaces, remove macro from
  comment, remove BR of gawk;coreutils;gzip that should be covered automatically
  by minimum build environment, do not `rm -rf' buildroot at the beginning of
  install phase (needed only in EPEL), remove BuildRoot definition, remove
  defattr macro, s/define/global/
- do not use ${VAR} syntax for bash variables, use just $VAR

* Wed Aug 22 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-11
- fix manpage to reflect #850291 related commit

* Tue Aug 21 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-10
- prepare Gnulib for new xattrs (#850291)
- new version of RH xattrs patch (#850291)
- enable verbose mode in testsuite to allow better debugging on error

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-8
- force the fchown() be called before xattrs_set() (#771927)

* Sat Jun 16 2012 Ondrej Vasik <ovasik@redhat.com> 2:1.26-7
- store&restore security.capability extended attributes category
  (#771927)
- fix build failure with undefined gets

* Tue May 15 2012 Ondrej Vasik <ovasik@redhat.com> 2:1.26-6
- add virtual provides for bundled(gnulib) copylib (#821790)

* Thu Apr 05 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-5
- fix for bad cooperation of the '-C' (change directory) and '-u' (update
  package) options (#688567)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  2 2011 Ville Skyttä <ville.skytta@iki.fi> - 2:1.26-3
- Man page heading formatting fixes.

* Mon Sep 26 2011 Kamil Dudka <kdudka@redhat.com> 2:1.26-2
- restore basic functionality of --acl, --selinux, and --xattr (#717684)

* Sat Mar 12 2011 Ondrej Vasik <ovasik@redhat.com> 2:1.26-1
- new upstream release 1.26
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Ondrej Vasik <ovasik@redhat.com> 2:1.25-5
- drop unnecessary hard dependency on info package(#671157)

* Mon Jan 03 2011 Ondrej Vasik <ovasik@redhat.com> 2:1.25-4
- mention that some compression options might not work if
  the external program is not available(#666755)

* Wed Dec 08 2010 Kamil Dudka <kdudka@redhat.com> 2:1.25-3
- correctly store long sparse file names in PAX archives (#656834)

* Tue Nov 23 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.25-2
- fix issue with --one-file-system and --listed-incremental
  (#654718)

* Mon Nov 08 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.25-1
- new upstream release 1.25

* Mon Oct 25 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.24-1
- new upstream release 1.24, use .xz archive

* Wed Sep 29 2010 jkeating - 2:1.23-8
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Kamil Dudka <kdudka@redhat.com> 2:1.23-7
- match non-stripped file names (#637085)

* Mon Sep 20 2010 Kamil Dudka <kdudka@redhat.com> 2:1.23-6
- fix exclusion of long file names with --xattrs (#634866)
- do not crash with --listed-incremental (#635318)

* Mon Aug 16 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-5
- add support for security.NTACL xattrs (#621215)

* Tue Jun 01 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-4
- recognize old-archive/portability options(#594044)

* Wed Apr 07 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-3
- allow storing of extended attributes for fifo and block
  or character devices files(#573147)

* Mon Mar 15 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-2
- update help2maned manpage

* Fri Mar 12 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-1
- new upstream release 1.23, remove applied patches

* Wed Mar 10 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-17
- CVE-2010-0624 tar, cpio: Heap-based buffer overflow
  by expanding a specially-crafted archive (#572149)
- realloc within check_exclusion_tags() caused invalid write
  (#570591)
- not closing file descriptors for excluded files/dirs with
  exlude-tag... options could cause descriptor exhaustion
  (#570591)

* Sat Feb 20 2010 Kamil Dudka <kdudka@redhat.com> 2:1.22-16
- support for "lustre.*" extended attributes (#561855)

* Thu Feb 04 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-15
- fix segfault with corrupted metadata in code_ns_fraction
  (#531441)

* Wed Feb 03 2010 Kamil Dudka <kdudka@redhat.com> 2:1.22-14
- allow also build with SELinux support

* Mon Feb 01 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-13
- allow build without SELinux support(#556679)

* Tue Jan 05 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-12
- do not fail with POSIX 2008 glibc futimens() (#552320)
- temporarily disable fix for #531441, causing stack smashing
  with newer glibc(#551206)

* Tue Dec 08 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-11
- fix segfault with corrupted metadata in code_ns_fraction
  (#531441)
- commented patches and sources

* Fri Nov 27 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-10
- store xattrs for symlinks (#525992) - by Kamil Dudka
- update tar(1) manpage (#539787)
- fix memory leak in xheader (#518079)

* Wed Nov 18 2009 Kamil Dudka <kdudka@redhat.com> 2:1.22-9
- store SELinux context for symlinks (#525992)

* Thu Aug 27 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-8
- provide symlink manpage for gtar

* Thu Aug 06 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-7
- do process install-info only without --excludedocs(#515923)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-5
- Fix restoring of directory default acls(#511145)
- Do not patch generated autotools files

* Thu Jun 25 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-4
- Report record size only if the archive refers to a device
  (#487760)
- Do not sigabrt with new gcc/glibc because of writing to
  struct members of gnutar header at once via strcpy

* Fri May 15 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-3
- ignore errors from setting utime() for source file
  on read-only filesystem (#500742)

* Fri Mar 06 2009 Kamil Dudka <kdudka@redhat.com> 2:1.22-2
- improve tar-1.14-loneZeroWarning.patch (#487315)

* Mon Mar 02 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-1
- New upstream release 1.22, removed applied patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 05 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.21-1
- New upstream release 1.21, removed applied patches
- add support for -I option, fix testsuite failure

* Thu Dec 11 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-6
- add BuildRequires for rsh (#475950)

* Fri Nov 21 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-5
- fix off-by-one errors in xattrs patch (#472355)

* Mon Nov 10 2008 Kamil Dudka <kdudka@redhat.com> 2:1.20-4
- fixed bug #465803: labels with --multi-volume (upstream patch)

* Fri Oct 10 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-3
- Fixed wrong documentation for xattrs options (#466517)
- fixed bug with null file terminator and change dirs
  (upstream)

* Fri Aug 29 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-2
- patch fuzz clean up

* Mon May 26 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-1
- new upstream release 1.20 (lzma support, few new options
  and bugfixes)
- heavily modified xattrs patches(as tar-1.20 now uses automake
  1.10.1)

* Tue Feb 12 2008 Radek Brich <rbrich@redhat.com> 2:1.19-3
- do not print getfilecon/setfilecon warnings when SELinux is disabled
  or SELinux data are not available (bz#431879)
- fix for GCC 4.3

* Mon Jan 21 2008 Radek Brich <rbrich@redhat.com> 2:1.19-2
- fix errors in man page
  * fix definition of --occurrence (bz#416661, patch by Jonathan Wakely)
  * update meaning of -l: it has changed from --one-filesystem
    to --check-links (bz#426717)
- update license tag, tar 1.19 is GPLv3+

* Mon Dec 17 2007 Radek Brich <rbrich@redhat.com> 2:1.19-1
- upgrade to 1.19
- updated xattrs patch, removed 3 upstream patches

* Wed Dec 12 2007 Radek Brich <rbrich@redhat.com> 2:1.17-5
- fix (non)detection of xattrs
- move configure stuff from -xattrs patch to -xattrs-conf,
  so the original patch could be easily read
- fix -xattrs patch to work with zero length files and show
  warnings when xattrs not available (fixes by James Antill)
- possible corruption (#408621) - add warning to man page
  for now, may be actually fixed later, depending on upstream

* Tue Oct 23 2007 Radek Brich <rbrich@redhat.com> 2:1.17-4
- upstream patch for CVE-2007-4476
  (tar stack crashing in safer_name_suffix)

* Tue Aug 28 2007 Radek Brich <rbrich@redhat.com> 2:1.17-3
- gawk build dependency

* Tue Aug 28 2007 Radek Brich <rbrich@redhat.com> 2:1.17-2
- updated license tag
- fixed CVE-2007-4131 tar directory traversal vulnerability (#251921)

* Thu Jun 28 2007 Radek Brich <rbrich@redhat.com> 2:1.17-1
- new upstream version
- patch for wildcards (#206841), restoring old behavior
- patch for testsuite
- update -xattrs patch
- drop 13 obsolete patches

* Tue Feb 06 2007 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-26
- fix spec file to meet Fedora standards (#226478)

* Mon Jan 22 2007 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-25
- fix non-failsafe install-info use in scriptlets (#223718)

* Wed Jan 03 2007 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-24
- supply tar man page (#219375)

* Tue Dec 12 2006 Florian La Roche <laroche@redhat.com> 2:1.15.1-23
- fix CVE-2006-6097 GNU tar directory traversal (#216937)

* Sun Dec 10 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-22
- fix some rpmlint spec file issues

* Wed Oct 25 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-21
- build with dist-tag

* Mon Oct 09 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-20
- another fix of tar-1.15.1-xattrs.patch from James Antill

* Wed Oct 04 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-19
- another fix of tar-1.15.1-xattrs.patch from James Antill

* Sun Oct 01 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-18
- fix tar-1.15.1-xattrs.patch (#208701)

* Tue Sep 19 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-17
- start new epoch, downgrade to solid stable 1.15.1-16 (#206979),
- all patches are backported

* Tue Sep 19 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.91-2
- apply patches, which were forgotten during upgrade

* Wed Sep 13 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.91-1
- upgrade, which also fix incremental backup (#206121)

* Fri Sep 08 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-7
- fix tar-debuginfo package (#205615)

* Thu Aug 10 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-6
- add xattr support (#200925), patch from james.antill@redhat.com

* Mon Jul 24 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-5
- fix incompatibilities in appending files to the end
  of an archive (#199515)

* Tue Jul 18 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-4
- fix problem with unpacking archives in a directory for which
  one has write permission but does not own (such as /tmp) (#149686)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.15.90-3.1
- rebuild

* Thu Jun 29 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-3
- fix typo in tar.1 man page

* Tue Apr 25 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-2
- exclude listed02.at from testsuite again, because it
  still fails on s390

* Tue Apr 25 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-1
- upgrade

* Mon Apr 24 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-16
- fix problem when options at the end of command line were
  not recognized (#188707)

* Thu Apr 13 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-15
- fix segmentation faul introduced with hugeSparse.patch

* Wed Mar 22 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-14
- fix problems with extracting large sparse archive members (#185460)

* Fri Feb 17 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-13
- fix heap overlfow bug CVE-2006-0300 (#181773)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.15.1-12.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.15.1-12.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-12
- fix extracting sparse files to a filesystem like vfat,
  when ftruncate may fail to grow the size of a file.(#179507)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 04 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-11
- correctly pad archive members that shrunk during archiving (#172373)

* Tue Sep 06 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-10
- provide man page (#163709, #54243, #56041)

* Mon Aug 15 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-9
- silence newer option (#164902)

* Wed Jul 27 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-8
- A file is dumpable if it is sparse and both --sparse
  and --totals are specified (#154882)

* Tue Jul 26 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-7
- exclude listed02.at from testsuite

* Fri Jul 22 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-6
- remove tar-1.14-err.patch, not needed (158743)

* Fri Apr 15 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-5
- extract sparse files even if the output fd is not seekable.(#154882)
- (sparse_scan_file): Bugfix. offset had incorrect type.

* Mon Mar 14 2005 Peter Vrabec <pvrabec@redhat.com>
- gcc4 fix (#150993) 1.15.1-4

* Mon Jan 31 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuild 1.15.1-3

* Mon Jan 17 2005 Peter Vrabec <pvrabec@redhat.com>
- fix tests/testsuite

* Fri Jan 07 2005 Peter Vrabec <pvrabec@redhat.com>
- upgrade to 1.15.1

* Mon Oct 11 2004 Peter Vrabec <pvrabec@redhat.com>
- patch to stop issuing lone zero block warnings
- rebuilt

* Mon Oct 11 2004 Peter Vrabec <pvrabec@redhat.com>
- URL added to spec file
- spec file clean up

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Jeff Johnson <jbj@jbj.org> 1.14-1
- upgrade to 1.14.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Jeff Johnson <jbj@redhat.com> 1.13.25-13
- rebuilt because of crt breakage on ppc64.
- dump automake15 requirement.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1.13.25-10
- fix broken buildrquires on autoconf253

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 1.13.25-9
- rebuild from CVS.

* Fri Aug 23 2002 Phil Knirsch <pknirsch@redhat.com> 1.13.25-8
- Included security patch from errata release.

* Mon Jul  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-7
- Fix argv NULL termination (#64869)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-4
- Fix build with autoconf253 (LIBOBJ change; autoconf252 worked)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Oct 23 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-2
- Don't include hardlinks to sockets in a tar file (#54827)

* Thu Sep 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-1
- 1.13.25

* Tue Sep 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.22-1
- Update to 1.13.22, adapt patches

* Mon Aug 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.19-6
- Fix #52084

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.19-5
- Fix build with current autoconf (stricter checking on AC_DEFINE)
- Fix segfault when tarring directories without having read permissions
  (#40802)

* Tue Mar  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't depend on librt.

* Fri Feb 23 2001 Trond Eivind Glomsröd <teg@redhat.com>
- langify

* Thu Feb 22 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up the man page (#28915)

* Wed Feb 21 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.19, nukes -I and fixes up -N
- Add -I back in as an alias to -j with a nice loud warning

* Mon Oct 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.18
- Update man page to reflect changes

* Thu Oct  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix the "ignore failed read" option (Bug #8330)

* Mon Sep 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix hang on tar tvzf - <something.tar.gz, introduced by
  exit code fix (Bug #15448), Patch from Tim Waugh <twaugh@redhat.com>

* Fri Aug 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- really fix exit code (Bug #15448)

* Mon Aug  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix exit code (Bug #15448), patch from Tim Waugh <twaugh@redhat.com>

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- fix for ia64

* Wed Feb  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix the exclude bug (#9201)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description
- fix fnmatch build problems

* Sun Jan  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.13.17
- remove dotbug patch (fixed in base)
- update download URL

* Fri Jan  7 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix a severe bug (tar xf any_package_containing_. would delete the
  current directory)

* Wed Jan  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.3.16
- unset LINGUAS before running configure

* Tue Nov  9 1999 Bernhard Rosenkränzer <bero@redhat.com>
- 1.13.14
- Update man page to know about -I / --bzip
- Remove dependancy on rmt - tar can be used for anything local
  without it.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.13.11.

* Wed Aug 18 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.9.

* Thu Aug 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.6.
- support -y --bzip2 options for bzip2 compression (#2415).

* Fri Jul 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.5.

* Tue Jul 13 1999 Bill Nottingham <notting@redhat.com>
- update to 1.13

* Sat Jun 26 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.12.64014.
- pipe patch corrected for remote tars now merged in.

* Sun Jun 20 1999 Jeff Johnson <jbj@redhat.com>
- update to tar-1.12.64013.
- subtract (and reopen #2415) bzip2 support using -y.
- move gtar to /bin.

* Tue Jun 15 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to tar-1.12.64011 to
-   add bzip2 support (#2415)
-   fix filename bug (#3479)

* Mon Mar 29 1999 Jeff Johnson <jbj@redhat.com>
- fix suspended tar with compression over pipe produces error (#390).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 8)

* Mon Mar 08 1999 Michael Maher <mike@redhat.com>
- added patch for bad name cache.
- FIXES BUG 320

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- add /usr/bin/gtar symlink (change #421)

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump.
- Turn on nls.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 1.11.8 to 1.12
- various spec file cleanups
- /sbin/install-info support

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu May 29 1997 Michael Fulbright <msf@redhat.com>
- Fixed to include rmt
