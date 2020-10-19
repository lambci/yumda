%define buildid 152.320

# We have to override the new %%install behavior because, well... the kernel is special.
%global __spec_install_pre %%{___build_pre}

Summary: The Linux kernel

# Amazon: Enable module signing and disable efi
%global signmodules 1
%global usingefi 0

# Save original buildid for later if it's defined
%if 0%{?buildid:1}
%global orig_buildid %{buildid}
%undefine buildid
%endif

# Tentatively set this macro to override .amzn1
%global dist .amzn2

# AMZN variables
#
# AMZN_MAJOR: generation of Amazon Linux
# AMZN_MINOR: point release of Amazon Linux
%global AMZN_MAJOR 2
%global AMZN_MINOR 0

###################################################################
# Polite request for people who spin their own kernel rpms:
# please modify the "buildid" define in a way that identifies
# that the kernel isn't the stock distribution kernel, for example,
# by setting the define to ".local" or ".bz123456". This will be
# appended to the full kernel version.
#
# (Uncomment the '#' and both spaces below to set the buildid.)
#
# %% define buildid .local
###################################################################

# The buildid can also be specified on the rpmbuild command line
# by adding --define="buildid .whatever". If both the specfile and
# the environment define a buildid they will be concatenated together.
%if 0%{?orig_buildid:1}
%if 0%{?buildid:1}
%global srpm_buildid %{buildid}
%define buildid %{srpm_buildid}%{orig_buildid}
%else
%define buildid %{orig_buildid}
%endif
%endif

# what kernel is it we are building
%global kversion 4.14.198
%define rpmversion %{kversion}

# What parts do we want to build?  We must build at least one kernel.
# These are the kernels that are built IF the architecture allows it.
# All should default to 1 (enabled) and be flipped to 0 (disabled)
# by later arch-specific checks.

# The following build options are enabled by default.
# Use either --without <opt> in your rpmbuild command or force values
# to 0 in here to disable them.
#
# standard kernel
%define with_up        %{?_without_up:        0} %{?!_without_up:        1}
# kernel-debug
%define with_debug     %{?_without_debug:     0} %{?!_without_debug:     0}
# kernel-doc
%define with_doc       %{?_without_doc:       0} %{?!_without_doc:       0}
# kernel-headers
%define with_headers   %{?_without_headers:   0} %{?!_without_headers:   1}
# perf
%define with_perf      %{?_without_perf:      0} %{?!_without_perf:      1}
# tools
%define with_tools     %{?_without_tools:     0} %{?!_without_tools:     1}
# kernel-debuginfo
%define with_debuginfo %{?_without_debuginfo: 0} %{?!_without_debuginfo: 1}
# Want to build a the vsdo directories installed
%define with_vdso_install %{?_without_vdso_install: 0} %{?!_without_vdso_install: 1}
# Use dracut instead of mkinitrd for initrd image generation
%define with_dracut       %{?_without_dracut:       0} %{?!_without_dracut:       1}
# Control whether we build the hmac for fips mode
%define with_fips      %{?_without_fips:       0} %{?!_without_fips:   1}

# Build the kernel-doc package, but don't fail the build if it botches.
# Here "true" means "continue" and "false" means "fail the build".
%define doc_build_fail true

# should we do C=1 builds with sparse
%define with_sparse	%{?_with_sparse:      1} %{?!_with_sparse:      0}

# Set debugbuildsenabled to 1 for production (build separate debug kernels)
#  and 0 for rawhide (all kernels are debug kernels).
# See also 'make debug' and 'make release'.
%define debugbuildsenabled 0

# do we want the oldconfig run over the config files (when regenerating
# configs this should be avoided in order to save duplicate work...)
%define with_oldconfig     %{?_without_oldconfig:      0} %{?!_without_oldconfig:      1}

# pkg_release is what we'll fill in for the rpm Release: field
%define pkg_release %{?buildid}%{?dist}

%define make_target bzImage

%define KVERREL %{rpmversion}-%{pkg_release}.%{_target_cpu}
%define hdrarch %_target_cpu
%define asmarch %_target_cpu

%if !%{debugbuildsenabled}
%define with_debug 0
%endif

%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
%define debuginfodir /usr/lib/debug

%define all_x86 i386 i686

%if %{with_vdso_install}
# These arches install vdso/ directories.
%define vdso_arches x86_64 aarch64
%endif

# Overrides for generic default options

# don't do debug builds on anything but i686 and x86_64
%ifnarch i686 x86_64 aarch64
%define with_debug 0
%endif

# only package docs noarch
%ifnarch noarch
%define with_doc 0
%endif

# don't build noarch kernels or headers (duh)
%ifarch noarch
%define with_up 0
%define with_headers 0
%define with_tools 0
%define with_perf 0
%define signmodules 0
%define all_arch_configs kernel-%{version}-*.config
%endif

# Per-arch tweaks

%ifarch %{all_x86}
%define asmarch x86
%define hdrarch i386
%define all_arch_configs kernel-%{version}-i?86*.config
%define image_install_path boot
%define kernel_image arch/%{asmarch}/boot/bzImage
%endif

%ifarch x86_64
%define asmarch x86
%define all_arch_configs kernel-%{version}-x86_64*.config
%define image_install_path boot
%define kernel_image arch/%{asmarch}/boot/bzImage
%endif

%ifarch aarch64
%define all_arch_configs kernel-%{version}-aarch64*.config
%define asmarch arm64
%define hdrarch arm64
%define image_install_path boot
%define make_target Image
%define kernel_image arch/%{asmarch}/boot/Image
%define with_perf 1
%endif

# amazon: don't use nonint config target - we want to know when our config files are
# not complete
%define oldconfig_target oldconfig

# To temporarily exclude an architecture from being built, add it to
# %%nobuildarches. Do _NOT_ use the ExclusiveArch: line, because if we
# don't build kernel-headers then the new build system will no longer let
# us use the previous build of that package -- it'll just be completely AWOL.
# Which is a BadThing(tm).

# We don't build a kernel on i386; we only do kernel-headers there
%define nobuildarches i386 i486 i586 i686 noarch

%ifarch %nobuildarches
%define with_up 0
%define with_debuginfo 0
%define with_perf 0
%define with_tools 0
%define _enable_debug_packages 0
%define signmodules 0
%endif

# Architectures we build tools/cpupower on
%define cpupowerarchs %{ix86} x86_64 aarch64
#define cpupowerarchs none

#
# Three sets of minimum package version requirements in the form of Conflicts:
# to versions below the minimum
#

#
# First the general kernel 2.6 required versions as per
# Documentation/Changes
#
%define kernel_dot_org_conflicts  ppp < 2.4.3-3, isdn4k-utils < 3.2-32, nfs-utils < 1.2.5-7.fc17, e2fsprogs < 1.37-4, util-linux < 2.12, jfsutils < 1.1.7-2, reiserfs-utils < 3.6.19-2, xfsprogs < 2.6.13-4, procps < 3.2.5-6.3, oprofile < 0.9.1-2, device-mapper-libs < 1.02.63-2, mdadm < 3.2.1-5

#
# Then a series of requirements that are distribution specific, either
# because we add patches for something, or the older versions have
# problems with the newer kernel or lack certain things that make
# integration in the distro harder than needed.
#
%define package_conflicts initscripts < 7.23, udev < 063-6, iptables < 1.3.2-1, selinux-policy-targeted < 1.25.3-14, squashfs-tools < 4.0

# We moved the drm include files into kernel-headers, make sure there's
# a recent enough libdrm-devel on the system that doesn't have those.
%define kernel_headers_conflicts libdrm-devel < 2.4.0-0.15

#
# Packages that need to be installed before the kernel is, because the %%post
# scripts use them.
#
%define kernel_prereq  fileutils, module-init-tools, initscripts >= 8.11.1-1, grubby >= 7.0.15-2.5
%if %{with_dracut}
%define initrd_prereq  dracut >= 004-336.27, grubby >= 7.0.10-1
%else
%define initrd_prereq  mkinitrd >= 6.0.91
%endif
# XXX: fedora16 has a prereq grubby >= 8.3-1

#
# This macro does requires, provides, conflicts, obsoletes for a kernel package.
#	%%kernel_reqprovconf <subpackage>
# It uses any kernel_<subpackage>_conflicts and kernel_<subpackage>_obsoletes
# macros defined above.
#
%define kernel_reqprovconf \
Provides: kernel = %{rpmversion}-%{pkg_release}\
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{pkg_release}%{?1:.%{1}}\
Provides: kernel-drm = 4.3.0\
Provides: kernel-drm-nouveau = 16\
Provides: kernel-modeset = 1\
Provides: kernel-uname-r = %{KVERREL}%{?1:.%{1}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): %{initrd_prereq}\
Requires(post): %{_sbindir}/new-kernel-pkg\
Requires(preun): %{_sbindir}/new-kernel-pkg\
Conflicts: %{kernel_dot_org_conflicts}\
Conflicts: %{package_conflicts}\
%{expand:%%{?kernel%{?1:_%{1}}_conflicts:Conflicts: %%{kernel%{?1:_%{1}}_conflicts}}}\
%{expand:%%{?kernel%{?1:_%{1}}_obsoletes:Obsoletes: %%{kernel%{?1:_%{1}}_obsoletes}}}\
%{expand:%%{?kernel%{?1:_%{1}}_provides:Provides: %%{kernel%{?1:_%{1}}_provides}}}\
# We can't let RPM do the dependencies automatic because it'll then pick up\
# a correct but undesirable perl dependency from the module headers which\
# isn't required for the kernel proper to function\
AutoReq: no\
AutoProv: yes\
%{nil}

Name: kernel%{?variant}
Group: System Environment/Kernel
License: GPLv2 and Redistributable, no modification permitted
URL: http://www.kernel.org/
Version: %{rpmversion}
Release: %{pkg_release}
# DO NOT CHANGE THE 'ExclusiveArch' LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %%nobuildarches (ABOVE) INSTEAD
ExclusiveArch: noarch i686 x86_64 aarch64
ExclusiveOS: Linux

%kernel_reqprovconf
%ifarch x86_64
Requires(pre): microcode_ctl >= 2:2.1-47.amzn2.0.4
%endif

%ifarch x86_64
Obsoletes: kernel-smp
%endif

Provides: kmod-lustre-client = 2.10.5

#
# List the packages used during the kernel build
#
BuildRequires: kmod >= 14, patch >= 2.5.4, bash >= 2.03, sh-utils, tar
BuildRequires: bzip2, findutils, gzip, m4, perl, make >= 3.78, diffutils, gawk
BuildRequires: gcc >= 7.2.1, hostname, openssl
# Required for kernel documentation build
%if %{with_doc}
BuildRequires: python-virtualenv, python-sphinx, ImageMagick-perl
%endif
#defines based on the compiler version we need to use
%global _gcc gcc
%global _gxx g++
%global _gccver %(eval %{_gcc} -dumpfullversion 2>/dev/null || :)
%if "%{_gccver}" > "7"
Provides: buildrequires(gcc) = %{_gccver}
%endif
BuildRequires: binutils >= 2.12
BuildRequires: system-rpm-config, gdb, bc
BuildRequires: net-tools
BuildRequires: xmlto, asciidoc
BuildRequires: openssl-devel
%if %{with_sparse}
BuildRequires: sparse >= 0.4.1
%endif
%if %{with_perf}
BuildRequires: elfutils-devel zlib-devel binutils-devel newt-devel python-devel perl(ExtUtils::Embed) bison
BuildRequires: audit-libs-devel
BuildRequires: numactl-devel

%endif
%if %{with_tools}
BuildRequires: pciutils-devel gettext
%endif # tools
BuildConflicts: rhbuildsys(DiskFree) < 3000Mb

%if %{with_debuginfo}
BuildRequires: rpm-build >= 4.11.3-40.amzn2.0.4, elfutils
# Most of these should be enabled after more investigation
%undefine _include_minidebuginfo
%undefine _find_debuginfo_dwz_opts
%undefine _debuginfo_subpackages
%global _find_debuginfo_opts -r
%global _missing_build_ids_terminate_build 1
%global _no_recompute_build_ids 1
%endif

%if %{signmodules}
BuildRequires: pesign >= 0.10-4
%endif

%if %{with_fips}
BuildRequires: hmaccalc
%endif

Source0: linux-4.14.198.tar
Source1: linux-4.14.198-patches.tar

# this is for %{signmodules}
Source11: x509.genkey

Source15: kconfig.py
Source16: mod-extra.list
Source17: mod-extra.sh
Source18: mod-extra-sign.sh
%define modsign_cmd %{SOURCE18}

Source19: Makefile.config
Source20: config-x86_64
Source30: config-aarch64
Source50: split-man.pl
%define split_man_cmd %{SOURCE50}

# Sources for kernel-tools
Source2000: cpupower.init
Source2001: cpupower.config

# __PATCHFILE_TEMPLATE__
Patch0001: 0001-scsi-sd_revalidate_disk-prevent-NULL-ptr-deref.patch
Patch0002: 0002-bump-the-default-TTL-to-255.patch
Patch0003: 0003-bump-default-tcp_wmem-from-16KB-to-20KB.patch
Patch0004: 0004-force-perf-to-use-usr-bin-python-instead-of-usr-bin-.patch
Patch0005: 0005-nvme-update-timeout-module-parameter-type.patch
Patch0006: 0006-not-for-upstream-testmgr-config-changes-to-enable-FI.patch
Patch0007: 0007-drivers-introduce-AMAZON_DRIVER_UPDATES.patch
Patch0008: 0008-drivers-amazon-add-network-device-drivers-support.patch
Patch0009: 0009-drivers-amazon-introduce-AMAZON_ENA_ETHERNET.patch
Patch0010: 0010-Importing-Amazon-ENA-driver-1.5.0-into-amazon-4.14.y.patch
Patch0011: 0011-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
Patch0012: 0012-xen-manage-introduce-helper-function-to-know-the-on-.patch
Patch0013: 0013-xenbus-add-freeze-thaw-restore-callbacks-support.patch
Patch0014: 0014-x86-xen-Introduce-new-function-to-map-HYPERVISOR_sha.patch
Patch0015: 0015-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
Patch0016: 0016-xen-blkfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch0017: 0017-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch0018: 0018-xen-time-introduce-xen_-save-restore-_steal_clock.patch
Patch0019: 0019-x86-xen-save-and-restore-steal-clock.patch
Patch0020: 0020-xen-events-add-xen_shutdown_pirqs-helper-function.patch
Patch0021: 0021-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
Patch0022: 0022-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
Patch0023: 0023-Not-for-upstream-PM-hibernate-Speed-up-hibernation-b.patch
Patch0024: 0024-xen-blkfront-resurrect-request-based-mode.patch
Patch0025: 0025-xen-blkfront-add-persistent_grants-parameter.patch
Patch0026: 0026-ACPI-SPCR-Make-SPCR-available-to-x86.patch
Patch0027: 0027-Revert-xen-dont-fiddle-with-event-channel-masking-in.patch
Patch0028: 0028-locking-paravirt-Use-new-static-key-for-controlling-.patch
Patch0029: 0029-KVM-Introduce-paravirtualization-hints-and-KVM_HINTS.patch
Patch0030: 0030-KVM-X86-Choose-qspinlock-when-dedicated-physical-CPU.patch
Patch0031: 0031-x86-paravirt-Set-up-the-virt_spin_lock_key-after-sta.patch
Patch0032: 0032-KVM-X86-Fix-setup-the-virt_spin_lock_key-before-stat.patch
Patch0033: 0033-xen-blkfront-Fixed-blkfront_restore-to-remove-a-call.patch
Patch0034: 0034-x86-tsc-avoid-system-instability-in-hibernation.patch
Patch0035: 0035-blk-mq-simplify-queue-mapping-schedule-with-each-pos.patch
Patch0036: 0036-blk-wbt-Avoid-lock-contention-and-thundering-herd-is.patch
Patch0037: 0037-x86-MCE-AMD-Read-MCx_MISC-block-addresses-on-any-CPU.patch
Patch0038: 0038-x86-CPU-Rename-intel_cacheinfo.c-to-cacheinfo.c.patch
Patch0039: 0039-x86-CPU-AMD-Calculate-last-level-cache-ID-from-numbe.patch
Patch0040: 0040-x86-CPU-AMD-Fix-LLC-ID-bit-shift-calculation.patch
Patch0041: 0041-sched-topology-Introduce-NUMA-identity-node-sched-do.patch
Patch0042: 0042-x86-CPU-AMD-Derive-CPU-topology-from-CPUID-function-.patch
Patch0043: 0043-vmxnet3-increase-default-rx-ring-sizes.patch
Patch0044: 0044-block-xen-blkfront-consider-new-dom0-features-on-res.patch
Patch0045: 0045-ACPICA-Enable-sleep-button-on-ACPI-legacy-wake.patch
Patch0046: 0046-xen-restore-pirqs-on-resume-from-hibernation.patch
Patch0047: 0047-xen-Only-restore-the-ACPI-SCI-interrupt-in-xen_resto.patch
Patch0048: 0048-net-ena-Import-the-ENA-v2-driver-2.0.2g.patch
Patch0049: 0049-arm64-export-memblock_reserve-d-regions-via-proc-iom.patch
Patch0050: 0050-arm64-Fix-proc-iomem-for-reserved-but-not-memory-reg.patch
Patch0051: 0051-efi-arm64-Check-whether-x18-is-preserved-by-runtime-.patch
Patch0052: 0052-arm64-kexec-always-reset-to-EL2-if-present.patch
Patch0053: 0053-arm64-acpi-fix-alignment-fault-in-accessing-ACPI.patch
Patch0054: 0054-ACPICA-ACPI-6.2-Additional-PPTT-flags.patch
Patch0055: 0055-drivers-base-cacheinfo-move-cache_setup_of_node.patch
Patch0056: 0056-drivers-base-cacheinfo-setup-DT-cache-properties-ear.patch
Patch0057: 0057-cacheinfo-rename-of_node-to-fw_token.patch
Patch0058: 0058-arm64-acpi-Create-arch-specific-cpu-to-acpi-id-helpe.patch
Patch0059: 0059-ACPI-PPTT-Add-Processor-Properties-Topology-Table-pa.patch
Patch0060: 0060-ACPI-Enable-PPTT-support-on-ARM64.patch
Patch0061: 0061-drivers-base-cacheinfo-Add-support-for-ACPI-based-fi.patch
Patch0062: 0062-arm64-Add-support-for-ACPI-based-firmware-tables.patch
Patch0063: 0063-arm64-topology-rename-cluster_id.patch
Patch0064: 0064-arm64-topology-enable-ACPI-PPTT-based-CPU-topology.patch
Patch0065: 0065-ACPI-Add-PPTT-to-injectable-table-list.patch
Patch0066: 0066-arm64-topology-divorce-MC-scheduling-domain-from-cor.patch
Patch0067: 0067-ACPI-PPTT-use-ACPI-ID-whenever-ACPI_PPTT_ACPI_PROCES.patch
Patch0068: 0068-ACPI-PPTT-fix-build-when-CONFIG_ACPI_PPTT-is-not-ena.patch
Patch0069: 0069-ACPI-PPTT-Handle-architecturally-unknown-cache-types.patch
Patch0070: 0070-xen-netfront-call-netif_device_attach-on-resume.patch
Patch0071: 0071-xfs-refactor-superblock-verifiers.patch
Patch0072: 0072-libxfs-add-more-bounds-checking-to-sb-sanity-checks.patch
Patch0073: 0073-xfs-only-validate-summary-counts-on-primary-superblo.patch
Patch0074: 0074-xfs-iomap-define-and-use-the-IOMAP_F_DIRTY-flag-in-x.patch
Patch0075: 0075-iomap-add-a-swapfile-activation-function.patch
Patch0076: 0076-iomap-provide-more-useful-errors-for-invalid-swap-fi.patch
Patch0077: 0077-iomap-don-t-allow-holes-in-swapfiles.patch
Patch0078: 0078-iomap-inline-data-should-be-an-iomap-type-not-a-flag.patch
Patch0079: 0079-iomap-fsync-swap-files-before-iterating-mappings.patch
Patch0080: 0080-Import-lustre-client-2.10.5.patch
Patch0081: 0081-Config-glue-for-lustre-client.patch
Patch0082: 0082-net-allow-per-netns-sysctl_rmem-and-sysctl_wmem-for-.patch
Patch0083: 0083-tcp-Namespace-ify-sysctl_tcp_rmem-and-sysctl_tcp_wme.patch
Patch0084: 0084-Add-new-config-CONFIG_MICROVM-to-enable-microvm-opti.patch
Patch0085: 0085-x86-stacktrace-Do-not-unwind-after-user-regs.patch
Patch0086: 0086-x86-stacktrace-Remove-STACKTRACE_DUMP_ONCE.patch
Patch0087: 0087-x86-stacktrace-Clarify-the-reliable-success-paths.patch
Patch0088: 0088-x86-stacktrace-Do-not-fail-for-ORC-with-regs-on-stac.patch
Patch0089: 0089-x86-unwind-orc-Detect-the-end-of-the-stack.patch
Patch0090: 0090-x86-stacktrace-Enable-HAVE_RELIABLE_STACKTRACE-for-t.patch
Patch0091: 0091-lustre-fix-ACL-handling.patch
Patch0092: 0092-irqchip-gic-v2m-invoke-from-gic-v3-initialization-an.patch
Patch0093: 0093-PCI-al-Add-Amazon-Annapurna-Labs-PCIe-host-controlle.patch
Patch0094: 0094-arm64-acpi-pci-invoke-_DSM-whether-to-preserve-firmw.patch
Patch0095: 0095-NFS-Remove-redundant-semicolon.patch
Patch0096: 0096-Fix-microvm-config-dependency-in-Kconfig.patch
Patch0097: 0097-microvm-enable-debug-in-case-of-tcp-out-of-memory.patch
Patch0098: 0098-linux-ena-update-ENA-linux-driver-to-version-2.1.1.patch
Patch0099: 0099-PCI-Add-Amazon-s-Annapurna-Labs-vendor-ID.patch
Patch0100: 0100-PCI-Add-ACS-quirk-for-Amazon-Annapurna-Labs-root-por.patch
Patch0101: 0101-Partially-revert-cc946adcb9e983ad9fe56ebe35f1292e111.patch
Patch0102: 0102-livepatch-introduce-shadow-variable-API.patch
Patch0103: 0103-livepatch-__klp_shadow_get_or_alloc-is-local-to-shad.patch
Patch0104: 0104-livepatch-add-un-patch-callbacks.patch
Patch0105: 0105-livepatch-move-transition-complete-notice-into-klp_c.patch
Patch0106: 0106-livepatch-add-transition-notices.patch
Patch0107: 0107-livepatch-Correctly-call-klp_post_unpatch_callback-i.patch
Patch0108: 0108-livepatch-__klp_disable_patch-should-never-be-called.patch
Patch0109: 0109-livepatch-send-a-fake-signal-to-all-blocking-tasks.patch
Patch0110: 0110-livepatch-force-transition-to-finish.patch
Patch0111: 0111-livepatch-Remove-immediate-feature.patch
Patch0112: 0112-livepatch-add-locking-to-force-and-signal-functions.patch
Patch0113: 0113-livepatch-Initialize-shadow-variables-safely-by-a-cu.patch
Patch0114: 0114-livepatch-Allow-to-call-a-custom-callback-when-freei.patch
Patch0115: 0115-livepatch-Remove-reliable-stacktrace-check-in-klp_tr.patch
Patch0116: 0116-livepatch-Replace-synchronize_sched-with-synchronize.patch
Patch0117: 0117-livepatch-Change-unsigned-long-old_addr-void-old_fun.patch
Patch0118: 0118-xen-Restore-xen-pirqs-on-resume-from-hibernation.patch
Patch0119: 0119-block-add-io-timeout-to-sysfs.patch
Patch0120: 0120-block-don-t-show-io_timeout-if-driver-has-no-timeout.patch
Patch0121: 0121-Add-Amazon-EFA-driver-version-1.4.patch
Patch0122: 0122-percpu-refcount-Introduce-percpu_ref_resurrect.patch
Patch0123: 0123-block-Allow-unfreezing-of-a-queue-while-requests-are.patch
Patch0124: 0124-nvme-change-namespaces_mutext-to-namespaces_rwsem.patch
Patch0125: 0125-blk-mq-fix-hang-caused-by-freeze-unfreeze-sequence.patch
Patch0126: 0126-nvme-move-the-dying-queue-check-from-cancel-to-compl.patch
Patch0127: 0127-nvme-pci-Better-support-for-disabling-controller.patch
Patch0128: 0128-nvme-host-core-Allow-overriding-of-wait_ready-timeou.patch
Patch0129: 0129-nvme-host-pci-Fix-a-race-in-controller-removal.patch
Patch0130: 0130-nvme-pci-move-cq_vector-1-check-outside-of-q_lock.patch
Patch0131: 0131-irqchip-gic-v3-its-Pass-its_node-pointer-to-each-com.patch
Patch0132: 0132-irqchip-gic-v3-its-Only-emit-SYNC-if-targetting-a-va.patch
Patch0133: 0133-irqchip-gic-v3-its-Only-emit-VSYNC-if-targetting-a-v.patch
Patch0134: 0134-irqchip-gic-v3-its-Refactor-LPI-allocator.patch
Patch0135: 0135-irqchip-gic-v3-its-Use-full-range-of-LPIs.patch
Patch0136: 0136-irqchip-gic-v3-its-Move-minimum-LPI-requirements-to-.patch
Patch0137: 0137-irqchip-gic-v3-its-Drop-chunk-allocation-compatibili.patch
Patch0138: 0138-irqchip-gic-v3-Expose-GICD_TYPER-in-the-rdist-struct.patch
Patch0139: 0139-irqchip-gic-v3-its-Honor-hypervisor-enforced-LPI-ran.patch
Patch0140: 0140-irqchip-gic-v3-its-Reduce-minimum-LPI-allocation-to-.patch
Patch0141: 0141-irqchip-gic-v3-its-Cap-lpi_id_bits-to-reduce-memory-.patch
Patch0142: 0142-irqchip-gic-v3-its-Gracefully-fail-on-LPI-exhaustion.patch
Patch0143: 0143-irqchip-gic-v3-its-Fix-comparison-logic-in-lpi_range.patch
Patch0144: 0144-iommu-io-pgtable-arm-Convert-to-IOMMU-API-TLB-sync.patch
Patch0145: 0145-iommu-io-pgtable-arm-v7s-Convert-to-IOMMU-API-TLB-sy.patch
Patch0146: 0146-iommu-arm-smmu-v3-Implement-flush_iotlb_all-hook.patch
Patch0147: 0147-iommu-dma-Add-support-for-non-strict-mode.patch
Patch0148: 0148-iommu-Add-iommu.strict-command-line-option.patch
Patch0149: 0149-iommu-io-pgtable-arm-Add-support-for-non-strict-mode.patch
Patch0150: 0150-iommu-arm-smmu-v3-Add-support-for-non-strict-mode.patch
Patch0151: 0151-iommu-io-pgtable-arm-v7s-Add-support-for-non-strict-.patch
Patch0152: 0152-iommu-arm-smmu-Support-non-strict-mode.patch
Patch0153: 0153-iommu-use-config-option-to-specify-if-iommu-mode-sho.patch
Patch0154: 0154-locking-atomic-Add-atomic_cond_read_acquire.patch
Patch0155: 0155-locking-barriers-Introduce-smp_cond_load_relaxed-and.patch
Patch0156: 0156-locking-qspinlock-Use-atomic_cond_read_acquire.patch
Patch0157: 0157-locking-mcs-Use-smp_cond_load_acquire-in-MCS-spin-lo.patch
Patch0158: 0158-locking-qspinlock-Use-smp_cond_load_relaxed-to-wait-.patch
Patch0159: 0159-locking-qspinlock-Use-smp_store_release-in-queued_sp.patch
Patch0160: 0160-locking-qspinlock-Elide-back-to-back-RELEASE-operati.patch
Patch0161: 0161-locking-qspinlock-Use-try_cmpxchg-instead-of-cmpxchg.patch
Patch0162: 0162-MAINTAINERS-Add-myself-as-a-co-maintainer-for-the-lo.patch
Patch0163: 0163-arm64-barrier-Implement-smp_cond_load_relaxed.patch
Patch0164: 0164-arm64-locking-Replace-ticket-lock-implementation-wit.patch
Patch0165: 0165-arm64-kconfig-Ensure-spinlock-fastpaths-are-inlined-.patch
Patch0166: 0166-arm64-pull-in-upstream-erratum-workarounds.patch
Patch0167: 0167-arm64-Avoid-flush_icache_range-in-alternatives-patch.patch
Patch0168: 0168-update-ena-driver-to-version-2.1.3.patch
Patch0169: 0169-Revert-nvme-pci-Better-support-for-disabling-control.patch
Patch0170: 0170-nvme-pci-introduce-RECONNECTING-state-to-mark-initia.patch
Patch0171: 0171-nvme-allow-controller-RESETTING-to-RECONNECTING-tran.patch
Patch0172: 0172-nvme-rename-NVME_CTRL_RECONNECTING-state-to-NVME_CTR.patch
Patch0173: 0173-nvme-pci-Fix-timeouts-in-connecting-state.patch
Patch0174: 0174-nvme-pci-shutdown-on-timeout-during-deletion.patch
Patch0175: 0175-nvme-pci-Unblock-reset_work-on-IO-failure.patch
Patch0176: 0176-nvme-pci-Don-t-disable-on-timeout-in-reset-state.patch
Patch0177: 0177-nvme-pci-use-atomic-bitops-to-mark-a-queue-enabled.patch
Patch0178: 0178-arm64-fix-merge-error-in-errata-changes.patch
Patch0179: 0179-lustre-hold-lock-while-walking-changelog-dev-list.patch
Patch0180: 0180-Revert-Fix-the-locking-in-dcache_readdir-and-friends.patch
Patch0181: 0181-drivers-amazon-efa-update-to-1.5.0.patch
Patch0182: 0182-SMB3-Backup-intent-flag-missing-from-compounded-ops.patch
Patch0183: 0183-Add-support-for-setting-owner-info-dos-attributes-an.patch
Patch0184: 0184-update-ENA-linux-driver-to-version-2.2.1.patch
Patch0185: 0185-Revert-update-ENA-linux-driver-to-version-2.2.1.patch
Patch0186: 0186-kunit-test-add-KUnit-test-runner-core.patch
Patch0187: 0187-kunit-test-add-test-resource-management-API.patch
Patch0188: 0188-kunit-test-add-string_stream-a-std-stream-like-strin.patch
Patch0189: 0189-kunit-test-add-assertion-printing-library.patch
Patch0190: 0190-kunit-test-add-the-concept-of-expectations.patch
Patch0191: 0191-lib-enable-building-KUnit-in-lib.patch
Patch0192: 0192-kunit-test-add-initial-tests.patch
Patch0193: 0193-kunit-test-add-support-for-test-abort.patch
Patch0194: 0194-kunit-test-add-tests-for-kunit-test-abort.patch
Patch0195: 0195-kunit-test-add-the-concept-of-assertions.patch
Patch0196: 0196-kunit-test-add-tests-for-KUnit-managed-resources.patch
Patch0197: 0197-kunit-fix-failure-to-build-without-printk.patch
Patch0198: 0198-kunit-tool-add-Python-wrappers-for-running-KUnit-tes.patch
Patch0199: 0199-kunit-defconfig-add-defconfigs-for-building-KUnit-te.patch
Patch0200: 0200-kunit-Fix-build_dir-option.patch
Patch0201: 0201-Documentation-kunit-add-documentation-for-KUnit.patch
Patch0202: 0202-Documentation-kunit-Fix-verification-command.patch
Patch0203: 0203-lib-list-test-add-a-test-for-the-list-doubly-linked-.patch
Patch0204: 0204-cifs-Fix-slab-out-of-bounds-in-send_set_info-on-SMB2.patch
Patch0205: 0205-CIFS-don-t-log-STATUS_NOT_FOUND-errors-for-DFS.patch
Patch0206: 0206-Don-t-log-expected-error-on-DFS-referral-request.patch
Patch0207: 0207-Don-t-log-confusing-message-on-reconnect-by-default.patch
Patch0208: 0208-genirq-export-irq_get_percpu_devid_partition-to-modu.patch
Patch0209: 0209-perf-core-Export-AUX-buffer-helpers-to-modules.patch
Patch0210: 0210-perf-core-Add-PERF_AUX_FLAG_COLLISION-to-report-coll.patch
Patch0211: 0211-arm64-sysreg-Move-SPE-registers-and-PSB-into-common-.patch
Patch0212: 0212-arm64-head-Init-PMSCR_EL2.-PA-PCT-when-entered-at-EL.patch
Patch0213: 0213-dt-bindings-Document-devicetree-binding-for-ARM-SPE.patch
Patch0214: 0214-drivers-perf-Add-support-for-ARMv8.2-Statistical-Pro.patch
Patch0215: 0215-perf-tools-Add-ARM-Statistical-Profiling-Extensions-.patch
Patch0216: 0216-perf-arm-spe-Fix-uninitialized-record-error-variable.patch
Patch0217: 0217-ACPICA-ACPI-6.3-MADT-add-support-for-statistical-pro.patch
Patch0218: 0218-ACPICA-ACPI-6.3-PPTT-add-additional-fields-in-Proces.patch
Patch0219: 0219-ACPI-PPTT-Modify-node-flag-detection-to-find-last-ID.patch
Patch0220: 0220-ACPI-PPTT-Add-function-to-return-ACPI-6.3-Identical-.patch
Patch0221: 0221-arm_pmu-acpi-spe-Add-initial-MADT-SPE-probing.patch
Patch0222: 0222-perf-arm_spe-Enable-ACPI-Platform-automatic-module-l.patch
Patch0223: 0223-ena-update-to-2.2.3.patch
Patch0224: 0224-random-try-to-actively-add-entropy-rather-than-passi.patch
Patch0225: 0225-random-introduce-RANDOM_WAIT_JITTER-config-option.patch
Patch0226: 0226-lustre-update-to-AmazonFSxLustreClient-v2.10.8-1.patch
Patch0227: 0227-Revert-ena-update-to-2.2.3.patch
Patch0228: 0228-kernel-sched-fair.c-Fix-divide-by-zero.patch
Patch0229: 0229-efi-honour-memory-reservations-passed-via-a-linux-sp.patch
Patch0230: 0230-efi-arm-libstub-add-a-root-memreserve-config-table.patch
Patch0231: 0231-efi-add-API-to-reserve-memory-persistently-across-ke.patch
Patch0232: 0232-efi-Permit-calling-efi_mem_reserve_persistent-from-a.patch
Patch0233: 0233-efi-Prevent-GICv3-WARN-by-mapping-the-memreserve-tab.patch
Patch0234: 0234-efi-Permit-multiple-entries-in-persistent-memreserve.patch
Patch0235: 0235-efi-Reduce-the-amount-of-memblock-reservations-for-p.patch
Patch0236: 0236-efi-memreserve-deal-with-memreserve-entries-in-unmap.patch
Patch0237: 0237-efi-memreserve-Register-reservations-as-reserved-in-.patch
Patch0238: 0238-irqchip-gic-v3-Ensure-GICR_CTLR.EnableLPI-0-is-obser.patch
Patch0239: 0239-irqchip-gic-v3-its-Change-initialization-ordering-fo.patch
Patch0240: 0240-irqchip-gic-v3-its-Simplify-LPI_PENDBASE_SZ-usage.patch
Patch0241: 0241-irqchip-gic-v3-its-Split-property-table-clearing-fro.patch
Patch0242: 0242-irqchip-gic-v3-its-Move-pending-table-allocation-to-.patch
Patch0243: 0243-irqchip-gic-v3-its-Keep-track-of-property-table-s-PA.patch
Patch0244: 0244-irqchip-gic-v3-its-Allow-use-of-pre-programmed-LPI-t.patch
Patch0245: 0245-irqchip-gic-v3-its-Use-pre-programmed-redistributor-.patch
Patch0246: 0246-irqchip-gic-v3-its-Check-that-all-RDs-have-the-same-.patch
Patch0247: 0247-irqchip-gic-v3-its-Register-LPI-tables-with-EFI-conf.patch
Patch0248: 0248-irqchip-gic-v3-its-Allow-use-of-LPI-tables-in-reserv.patch
Patch0249: 0249-iommu-arm-smmu-v3-Prevent-any-devices-access-to-memo.patch
Patch0250: 0250-iommu-arm-smmu-v3-Abort-all-transactions-if-SMMU-is-.patch
Patch0251: 0251-iommu-arm-smmu-v3-Don-t-disable-SMMU-in-kdump-kernel.patch
Patch0252: 0252-xen-blkfront-Delay-flush-till-queue-lock-dropped.patch
Patch0253: 0253-Upgrade-to-ena-2.2.8.patch
Patch0254: 0254-Fix-a-build-issue-caused-by-45b2013293a2a.patch
Patch0255: 0255-NFSv4.1-fix-incorrect-return-value-in-copy_file_rang.patch
Patch0256: 0256-lustre-restore-mgc-binding-for-sptlrpc.patch
Patch0257: 0257-Update-lustrefsx-to-v2.10.8-5.patch
Patch0258: 0258-printk-Move-console-matching-logic-into-a-separate-f.patch
Patch0259: 0259-printk-Fix-preferred-console-selection-with-multiple.patch
Patch0260: 0260-printk-Correctly-set-CON_CONSDEV-even-when-preferred.patch
Patch0261: 0261-KVM-arm-arm64-Factor-out-hypercall-handling-from-PSC.patch
Patch0262: 0262-KVM-arm64-Implement-PV_TIME_FEATURES-call.patch
Patch0263: 0263-KVM-Implement-kvm_put_guest.patch
Patch0264: 0264-KVM-arm64-Support-stolen-time-reporting-via-shared-s.patch
Patch0265: 0265-KVM-Allow-kvm_device_ops-to-be-const.patch
Patch0266: 0266-KVM-arm64-Provide-VCPU-attributes-for-stolen-time.patch
Patch0267: 0267-arm-arm64-smccc-psci-add-arm_smccc_1_1_get_conduit.patch
Patch0268: 0268-arm-arm64-Provide-a-wrapper-for-SMCCC-1.1-calls.patch
Patch0269: 0269-arm-arm64-Make-use-of-the-SMCCC-1.1-wrapper.patch
Patch0270: 0270-arm64-Retrieve-stolen-time-as-paravirtualized-guest.patch
Patch0271: 0271-Makefile-Add-AMZN-specific-variables.patch
Patch0272: 0272-ena-Update-to-2.2.10.patch
Patch0273: 0273-fs-copy-BTRFS_IOC_-SG-ET_FSLABEL-to-vfs.patch
Patch0274: 0274-xfs-one-shot-cached-buffers.patch
Patch0275: 0275-xfs-add-prerequisite-for-online-labeling.patch
Patch0276: 0276-xfs-implement-online-get-set-fs-label.patch
Patch0277: 0277-xfs-fix-string-handling-in-label-get-set-functions.patch
Patch0278: 0278-xfs-fall-back-to-native-ioctls-for-unhandled-compat-.patch
Patch0279: 0279-mm-rid-swapoff-of-quadratic-complexity.patch
Patch0280: 0280-mm-swapoff-shmem_unuse-stop-eviction-without-igrab.patch
Patch0281: 0281-sched-wait-Introduce-wait_var_event.patch
Patch0282: 0282-UBUNTU-SAUCE-aws-mm-aggressive-swapoff.patch
Patch0283: 0283-UBUNTU-SAUCE-aws-mm-swap-improve-swap-readahead-heur.patch
Patch0284: 0284-block-genhd-Notify-udev-about-capacity-change.patch
Patch0285: 0285-drivers-block-virtio_blk.c-Convert-to-use-set_capaci.patch
Patch0286: 0286-drivers-block-xen-blkfront.c-Convert-to-use-set_capa.patch
Patch0287: 0287-drivers-nvme-host-core.c-Convert-to-use-set_capacity.patch
Patch0288: 0288-drivers-scsi-sd.c-Convert-to-use-set_capacity_revali.patch
Patch0289: 0289-CIFS-make-IPC-a-regular-tcon.patch
Patch0290: 0290-CIFS-use-tcon_ipc-instead-of-use_ipc-parameter-of-SM.patch
Patch0291: 0291-drivers-amazon-efa-update-to-1.9.0.patch
Patch0292: 0292-Remove-unused-variables-in-the-nvme-disk-resize-patc.patch
Patch0293: 0293-net-packet-fix-overflow-in-tpacket_rcv.patch
Patch0294: 0294-cpu-hotplug-Add-new-add-remove-_cpu-functions.patch
Patch0295: 0295-define-__poll_t-annotate-constants.patch
Patch0296: 0296-Partial-backport-of-mm-introduce-page_size.patch
Patch0297: 0297-nitro_enclaves-Add-ioctl-interface-definition.patch
Patch0298: 0298-nitro_enclaves-Define-the-PCI-device-interface.patch
Patch0299: 0299-nitro_enclaves-Define-enclave-info-for-internal-book.patch
Patch0300: 0300-nitro_enclaves-Init-PCI-device-driver.patch
Patch0301: 0301-nitro_enclaves-Handle-PCI-device-command-requests.patch
Patch0302: 0302-nitro_enclaves-Handle-out-of-band-PCI-device-events.patch
Patch0303: 0303-nitro_enclaves-Init-misc-device-providing-the-ioctl-.patch
Patch0304: 0304-nitro_enclaves-Add-logic-for-creating-an-enclave-VM.patch
Patch0305: 0305-nitro_enclaves-Add-logic-for-setting-an-enclave-vCPU.patch
Patch0306: 0306-nitro_enclaves-Add-logic-for-getting-the-enclave-ima.patch
Patch0307: 0307-nitro_enclaves-Add-logic-for-setting-an-enclave-memo.patch
Patch0308: 0308-nitro_enclaves-Add-logic-for-starting-an-enclave.patch
Patch0309: 0309-nitro_enclaves-Add-logic-for-terminating-an-enclave.patch
Patch0310: 0310-nitro_enclaves-Add-Kconfig-for-the-Nitro-Enclaves-dr.patch
Patch0311: 0311-enclaves-Define-PCI_VENDOR_ID_AMAZON.patch
Patch0312: 0312-nitro_enclaves-Add-Makefile-for-the-Nitro-Enclaves-d.patch
Patch0313: 0313-nitro_enclaves-Add-sample-for-ioctl-interface-usage.patch
Patch0314: 0314-nitro_enclaves-Add-overview-documentation.patch
Patch0315: 0315-MAINTAINERS-Add-entry-for-the-Nitro-Enclaves-driver.patch
Patch0316: 0316-arm64-Enable-PCI-write-combine-resources-under-sysfs.patch
Patch0317: 0317-nfs-optimise-readdir-cache-page-invalidation.patch
Patch0318: 0318-nfs-Fix-security-label-length-not-being-reset.patch
Patch0319: 0319-netfilter-ctnetlink-add-a-range-check-for-l3-l4-prot.patch

BuildRoot: %{_tmppath}/kernel-%{KVERREL}-root

%description
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.


%package doc
Summary: Various documentation bits found in the kernel source
Group: Documentation
%description doc
This package contains documentation files from the kernel
source. Various bits of information about the Linux kernel and the
device drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to Linux kernel modules at load time.


%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: glibc-kernheaders
Provides: glibc-kernheaders = 3.0-46
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package debuginfo-common-%{_target_cpu}
Summary: Kernel source files used by %{name}-debuginfo packages
Group: Development/Debug
%description debuginfo-common-%{_target_cpu}
This package is required by %{name}-debuginfo subpackages.
It provides the kernel source files common to all builds.

%if %{with_perf}
%package -n perf
Summary: Performance monitoring for the Linux kernel
Group: Development/System
License: GPLv2
%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.

%package -n perf-debuginfo
Summary: Debug information for package perf
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n perf-debuginfo
This package provides debug information for the perf package.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_bindir}/perf(\.debug)?|.*%%{_libexecdir}/perf-core/.*|.*%%{_libdir}/traceevent/plugins/.*|XXX' -o perf-debuginfo.list}

%package -n python-perf
Summary: Python bindings for apps which will manipulate perf events
Group: Development/Libraries
%description -n python-perf
The python-perf package contains a module that permits applications
written in the Python programming language to use the interface
to manipulate perf events.

%package -n python-perf-debuginfo
Summary: Debug information for package perf python bindings
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n python-perf-debuginfo
This package provides debug information for the perf python bindings.

%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{python_sitearch}/perf.so(\.debug)?|XXX' -o python-perf-debuginfo.list}

%endif #perf

%if %{with_tools}
%package tools
Summary: Assortment of tools for the Linux kernel
Group: Development/System
License: GPLv2
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:1.5-16

%description tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.

%package tools-devel
Summary: Assortment of tools for the Linux kernel
Group: Development/System
License: GPLv2
Requires: kernel-tools = %{version}-%{release}
%ifarch %{cpupowerarchs}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
%endif # cpupower

%description tools-devel
This package contains the development files for the tools/ directory from
the kernel source.

%package tools-debuginfo
Summary: Debug information for package kernel-tools
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description tools-debuginfo
This package provides debug information for package kernel-tools.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_bindir}/centrino-decode(\.debug)?|.*%%{_bindir}/powernow-k8-decode(\.debug)?|.*%%{_bindir}/cpupower(\.debug)?|.*%%{_libdir}/libcpupower.*|XXX' -o kernel-tools-debuginfo.list}
%endif

#
# This macro creates a kernel-<subpackage>-debuginfo package.
#	%%kernel_debuginfo_package <subpackage>
#
%define kernel_debuginfo_package() \
%package %{?1:%{1}-}debuginfo\
Summary: Debug information for package %{name}%{?1:-%{1}}\
Group: Development/Debug\
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}\
Provides: %{name}%{?1:-%{1}}-debuginfo-%{_target_cpu} = %{version}-%{release}\
AutoReqProv: no\
%description -n %{name}%{?1:-%{1}}-debuginfo\
This package provides debug information for package %{name}%{?1:-%{1}}.\
This is required to use SystemTap with %{name}%{?1:-%{1}}-%{KVERREL}.\
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '/.*/%%{KVERREL}%{?1:\.%{1}}/.*|/.*%%{KVERREL}%{?1:\.%{1}}(\.debug)?' -o debuginfo%{?1}.list}\
%{nil}

#
# This macro creates a kernel-<subpackage>-devel package.
#	%%kernel_devel_package <subpackage> <pretty-name>
#
%define kernel_devel_package() \
%package %{?1:%{1}-}devel\
Summary: Development package for building kernel modules to match the %{?2:%{2} }kernel\
Group: System Environment/Kernel\
Provides: kernel%{?1:-%{1}}-devel-%{_target_cpu} = %{version}-%{release}\
Provides: kernel-devel-%{_target_cpu} = %{version}-%{release}%{?1:.%{1}}\
Provides: kernel-devel = %{version}-%{release}%{?1:.%{1}}\
Provides: kernel-devel-uname-r = %{KVERREL}%{?1:.%{1}}\
AutoReqProv: no\
Requires(pre): %{_bindir}/find\
Requires(post): %{_sbindir}/hardlink\
Requires: perl\
Requires: elfutils-libelf-devel\
Requires: gcc >= 7.2.1\
%if  "%{_gccver}" > "7"\
Provides: buildrequires(gcc) = %{_gccver}\
%endif\
%description -n kernel%{?variant}%{?1:-%{1}}-devel\
This package provides kernel headers and makefiles sufficient to build modules\
against the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage> and its -devel and -debuginfo too.
#	%%define variant_summary The Linux kernel compiled for <configuration>
#	%%kernel_variant_package [-n <pretty-name>] <subpackage>
#
%define kernel_variant_package(n:) \
%package %1\
Summary: %{variant_summary}\
Group: System Environment/Kernel\
%kernel_reqprovconf\
%{expand:%%kernel_devel_package %1 %{!?-n:%1}%{?-n:%{-n*}}}\
%{expand:%%kernel_debuginfo_package %1}\
%{nil}


# First the auxiliary packages of the main kernel package.
%kernel_devel_package
%kernel_debuginfo_package


# Now, each variant package.

%define variant_summary The Linux kernel compiled with extra debugging enabled
%kernel_variant_package debug
%description debug
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.


%prep
# more sanity checking; do it quietly
if [ "%{patches}" != "%%{patches}" ] ; then
  for patch in %{patches} ; do
    if [ ! -f $patch ] ; then
      echo "ERROR: Patch  ${patch##/*/}  listed in specfile but is missing"
      exit 1
    fi
  done
fi 2>/dev/null

patch_command='patch -p1 -F1 -s'

ApplyNoCheckPatch()
{
  local patch=$1
  shift
  case "$patch" in
    *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
    *.gz) gunzip < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
    *) $patch_command ${1+"$@"} < $patch ;;
  esac
}

ApplyPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  if ! grep -E "^Patch[0-9]+: $patch\$" %{_specdir}/${RPM_PACKAGE_NAME%%%%%{?variant}}.spec ; then
    if [ "${patch:0:8}" != "patch-3." ] ; then
      echo "ERROR: Patch  $patch  not listed as a source patch in specfile"
      exit 1
    fi
  fi 2>/dev/null
  case "$patch" in
  *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.gz) gunzip < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *) $patch_command ${1+"$@"} < "$RPM_SOURCE_DIR/$patch" ;;
  esac
}

# don't apply patch if it's empty
ApplyOptionalPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  local C=$(wc -l $RPM_SOURCE_DIR/$patch | awk '{print $1}')
  if [ "$C" -gt 9 ]; then
    ApplyPatch $patch ${1+"$@"}
  fi
}

# First we unpack the kernel tarball.
# If this isn't the first make prep, we use links to the existing clean tarball
# which speeds things up quite a bit.

# Update to latest upstream.
%define vanillaversion %{kversion}

# %%{vanillaversion} : the full version name, e.g. 2.6.35-rc6-git3
# %%{kversion}       : the base version, e.g. 2.6.34

# Use kernel-%%{kversion}%%{?dist} as the top-level directory name
# so we can prep different trees within a single git directory.

%setup -q -n kernel-%{kversion}%{?dist} -c
mv linux-%{vanillaversion} vanilla-%{vanillaversion}

%if "%{kversion}" != "%{vanillaversion}"
# Need to apply patches to the base vanilla version.
pushd vanilla-%{vanillaversion} && popd

%endif

# Now build the fedora kernel tree.
if [ -d linux-%{KVERREL} ]; then
  # Just in case we ctrl-c'd a prep already
  rm -rf deleteme.%{_target_cpu}
  # Move away the stale away, and delete in background.
  mv linux-%{KVERREL} deleteme.%{_target_cpu}
  rm -rf deleteme.%{_target_cpu} &
fi

cp -rl vanilla-%{vanillaversion} linux-%{KVERREL}

cd linux-%{KVERREL}
tar xf %{SOURCE1}

# Drop some necessary files from the source dir into the buildroot
cp $RPM_SOURCE_DIR/config-* .
cp %{SOURCE15} .

%ifnarch %nobuildarches
# Dynamically generate kernel .config files from config-* files
make -f %{SOURCE19} VERSION=%{version} config
%endif

# apply the patches we had included in the -patches tarball. We use the
# linux-KVER-patches.list hardcoded apply log filename
patch_list=linux-%{kversion}-patches.list
if [ ! -f ${patch_list} ] ; then
    echo "ERROR: patch file apply log is missing: ${patch_list} not found"
    exit -1
fi
for p in `cat $patch_list` ; do
  ApplyNoCheckPatch ${p}
done

# __APPLYFILE_TEMPLATE__
ApplyPatch 0001-scsi-sd_revalidate_disk-prevent-NULL-ptr-deref.patch
ApplyPatch 0002-bump-the-default-TTL-to-255.patch
ApplyPatch 0003-bump-default-tcp_wmem-from-16KB-to-20KB.patch
ApplyPatch 0004-force-perf-to-use-usr-bin-python-instead-of-usr-bin-.patch
ApplyPatch 0005-nvme-update-timeout-module-parameter-type.patch
ApplyPatch 0006-not-for-upstream-testmgr-config-changes-to-enable-FI.patch
ApplyPatch 0007-drivers-introduce-AMAZON_DRIVER_UPDATES.patch
ApplyPatch 0008-drivers-amazon-add-network-device-drivers-support.patch
ApplyPatch 0009-drivers-amazon-introduce-AMAZON_ENA_ETHERNET.patch
ApplyPatch 0010-Importing-Amazon-ENA-driver-1.5.0-into-amazon-4.14.y.patch
ApplyPatch 0011-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
ApplyPatch 0012-xen-manage-introduce-helper-function-to-know-the-on-.patch
ApplyPatch 0013-xenbus-add-freeze-thaw-restore-callbacks-support.patch
ApplyPatch 0014-x86-xen-Introduce-new-function-to-map-HYPERVISOR_sha.patch
ApplyPatch 0015-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
ApplyPatch 0016-xen-blkfront-add-callbacks-for-PM-suspend-and-hibern.patch
ApplyPatch 0017-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
ApplyPatch 0018-xen-time-introduce-xen_-save-restore-_steal_clock.patch
ApplyPatch 0019-x86-xen-save-and-restore-steal-clock.patch
ApplyPatch 0020-xen-events-add-xen_shutdown_pirqs-helper-function.patch
ApplyPatch 0021-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
ApplyPatch 0022-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
ApplyPatch 0023-Not-for-upstream-PM-hibernate-Speed-up-hibernation-b.patch
ApplyPatch 0024-xen-blkfront-resurrect-request-based-mode.patch
ApplyPatch 0025-xen-blkfront-add-persistent_grants-parameter.patch
ApplyPatch 0026-ACPI-SPCR-Make-SPCR-available-to-x86.patch
ApplyPatch 0027-Revert-xen-dont-fiddle-with-event-channel-masking-in.patch
ApplyPatch 0028-locking-paravirt-Use-new-static-key-for-controlling-.patch
ApplyPatch 0029-KVM-Introduce-paravirtualization-hints-and-KVM_HINTS.patch
ApplyPatch 0030-KVM-X86-Choose-qspinlock-when-dedicated-physical-CPU.patch
ApplyPatch 0031-x86-paravirt-Set-up-the-virt_spin_lock_key-after-sta.patch
ApplyPatch 0032-KVM-X86-Fix-setup-the-virt_spin_lock_key-before-stat.patch
ApplyPatch 0033-xen-blkfront-Fixed-blkfront_restore-to-remove-a-call.patch
ApplyPatch 0034-x86-tsc-avoid-system-instability-in-hibernation.patch
ApplyPatch 0035-blk-mq-simplify-queue-mapping-schedule-with-each-pos.patch
ApplyPatch 0036-blk-wbt-Avoid-lock-contention-and-thundering-herd-is.patch
ApplyPatch 0037-x86-MCE-AMD-Read-MCx_MISC-block-addresses-on-any-CPU.patch
ApplyPatch 0038-x86-CPU-Rename-intel_cacheinfo.c-to-cacheinfo.c.patch
ApplyPatch 0039-x86-CPU-AMD-Calculate-last-level-cache-ID-from-numbe.patch
ApplyPatch 0040-x86-CPU-AMD-Fix-LLC-ID-bit-shift-calculation.patch
ApplyPatch 0041-sched-topology-Introduce-NUMA-identity-node-sched-do.patch
ApplyPatch 0042-x86-CPU-AMD-Derive-CPU-topology-from-CPUID-function-.patch
ApplyPatch 0043-vmxnet3-increase-default-rx-ring-sizes.patch
ApplyPatch 0044-block-xen-blkfront-consider-new-dom0-features-on-res.patch
ApplyPatch 0045-ACPICA-Enable-sleep-button-on-ACPI-legacy-wake.patch
ApplyPatch 0046-xen-restore-pirqs-on-resume-from-hibernation.patch
ApplyPatch 0047-xen-Only-restore-the-ACPI-SCI-interrupt-in-xen_resto.patch
ApplyPatch 0048-net-ena-Import-the-ENA-v2-driver-2.0.2g.patch
ApplyPatch 0049-arm64-export-memblock_reserve-d-regions-via-proc-iom.patch
ApplyPatch 0050-arm64-Fix-proc-iomem-for-reserved-but-not-memory-reg.patch
ApplyPatch 0051-efi-arm64-Check-whether-x18-is-preserved-by-runtime-.patch
ApplyPatch 0052-arm64-kexec-always-reset-to-EL2-if-present.patch
ApplyPatch 0053-arm64-acpi-fix-alignment-fault-in-accessing-ACPI.patch
ApplyPatch 0054-ACPICA-ACPI-6.2-Additional-PPTT-flags.patch
ApplyPatch 0055-drivers-base-cacheinfo-move-cache_setup_of_node.patch
ApplyPatch 0056-drivers-base-cacheinfo-setup-DT-cache-properties-ear.patch
ApplyPatch 0057-cacheinfo-rename-of_node-to-fw_token.patch
ApplyPatch 0058-arm64-acpi-Create-arch-specific-cpu-to-acpi-id-helpe.patch
ApplyPatch 0059-ACPI-PPTT-Add-Processor-Properties-Topology-Table-pa.patch
ApplyPatch 0060-ACPI-Enable-PPTT-support-on-ARM64.patch
ApplyPatch 0061-drivers-base-cacheinfo-Add-support-for-ACPI-based-fi.patch
ApplyPatch 0062-arm64-Add-support-for-ACPI-based-firmware-tables.patch
ApplyPatch 0063-arm64-topology-rename-cluster_id.patch
ApplyPatch 0064-arm64-topology-enable-ACPI-PPTT-based-CPU-topology.patch
ApplyPatch 0065-ACPI-Add-PPTT-to-injectable-table-list.patch
ApplyPatch 0066-arm64-topology-divorce-MC-scheduling-domain-from-cor.patch
ApplyPatch 0067-ACPI-PPTT-use-ACPI-ID-whenever-ACPI_PPTT_ACPI_PROCES.patch
ApplyPatch 0068-ACPI-PPTT-fix-build-when-CONFIG_ACPI_PPTT-is-not-ena.patch
ApplyPatch 0069-ACPI-PPTT-Handle-architecturally-unknown-cache-types.patch
ApplyPatch 0070-xen-netfront-call-netif_device_attach-on-resume.patch
ApplyPatch 0071-xfs-refactor-superblock-verifiers.patch
ApplyPatch 0072-libxfs-add-more-bounds-checking-to-sb-sanity-checks.patch
ApplyPatch 0073-xfs-only-validate-summary-counts-on-primary-superblo.patch
ApplyPatch 0074-xfs-iomap-define-and-use-the-IOMAP_F_DIRTY-flag-in-x.patch
ApplyPatch 0075-iomap-add-a-swapfile-activation-function.patch
ApplyPatch 0076-iomap-provide-more-useful-errors-for-invalid-swap-fi.patch
ApplyPatch 0077-iomap-don-t-allow-holes-in-swapfiles.patch
ApplyPatch 0078-iomap-inline-data-should-be-an-iomap-type-not-a-flag.patch
ApplyPatch 0079-iomap-fsync-swap-files-before-iterating-mappings.patch
ApplyPatch 0080-Import-lustre-client-2.10.5.patch
ApplyPatch 0081-Config-glue-for-lustre-client.patch
ApplyPatch 0082-net-allow-per-netns-sysctl_rmem-and-sysctl_wmem-for-.patch
ApplyPatch 0083-tcp-Namespace-ify-sysctl_tcp_rmem-and-sysctl_tcp_wme.patch
ApplyPatch 0084-Add-new-config-CONFIG_MICROVM-to-enable-microvm-opti.patch
ApplyPatch 0085-x86-stacktrace-Do-not-unwind-after-user-regs.patch
ApplyPatch 0086-x86-stacktrace-Remove-STACKTRACE_DUMP_ONCE.patch
ApplyPatch 0087-x86-stacktrace-Clarify-the-reliable-success-paths.patch
ApplyPatch 0088-x86-stacktrace-Do-not-fail-for-ORC-with-regs-on-stac.patch
ApplyPatch 0089-x86-unwind-orc-Detect-the-end-of-the-stack.patch
ApplyPatch 0090-x86-stacktrace-Enable-HAVE_RELIABLE_STACKTRACE-for-t.patch
ApplyPatch 0091-lustre-fix-ACL-handling.patch
ApplyPatch 0092-irqchip-gic-v2m-invoke-from-gic-v3-initialization-an.patch
ApplyPatch 0093-PCI-al-Add-Amazon-Annapurna-Labs-PCIe-host-controlle.patch
ApplyPatch 0094-arm64-acpi-pci-invoke-_DSM-whether-to-preserve-firmw.patch
ApplyPatch 0095-NFS-Remove-redundant-semicolon.patch
ApplyPatch 0096-Fix-microvm-config-dependency-in-Kconfig.patch
ApplyPatch 0097-microvm-enable-debug-in-case-of-tcp-out-of-memory.patch
ApplyPatch 0098-linux-ena-update-ENA-linux-driver-to-version-2.1.1.patch
ApplyPatch 0099-PCI-Add-Amazon-s-Annapurna-Labs-vendor-ID.patch
ApplyPatch 0100-PCI-Add-ACS-quirk-for-Amazon-Annapurna-Labs-root-por.patch
ApplyPatch 0101-Partially-revert-cc946adcb9e983ad9fe56ebe35f1292e111.patch
ApplyPatch 0102-livepatch-introduce-shadow-variable-API.patch
ApplyPatch 0103-livepatch-__klp_shadow_get_or_alloc-is-local-to-shad.patch
ApplyPatch 0104-livepatch-add-un-patch-callbacks.patch
ApplyPatch 0105-livepatch-move-transition-complete-notice-into-klp_c.patch
ApplyPatch 0106-livepatch-add-transition-notices.patch
ApplyPatch 0107-livepatch-Correctly-call-klp_post_unpatch_callback-i.patch
ApplyPatch 0108-livepatch-__klp_disable_patch-should-never-be-called.patch
ApplyPatch 0109-livepatch-send-a-fake-signal-to-all-blocking-tasks.patch
ApplyPatch 0110-livepatch-force-transition-to-finish.patch
ApplyPatch 0111-livepatch-Remove-immediate-feature.patch
ApplyPatch 0112-livepatch-add-locking-to-force-and-signal-functions.patch
ApplyPatch 0113-livepatch-Initialize-shadow-variables-safely-by-a-cu.patch
ApplyPatch 0114-livepatch-Allow-to-call-a-custom-callback-when-freei.patch
ApplyPatch 0115-livepatch-Remove-reliable-stacktrace-check-in-klp_tr.patch
ApplyPatch 0116-livepatch-Replace-synchronize_sched-with-synchronize.patch
ApplyPatch 0117-livepatch-Change-unsigned-long-old_addr-void-old_fun.patch
ApplyPatch 0118-xen-Restore-xen-pirqs-on-resume-from-hibernation.patch
ApplyPatch 0119-block-add-io-timeout-to-sysfs.patch
ApplyPatch 0120-block-don-t-show-io_timeout-if-driver-has-no-timeout.patch
ApplyPatch 0121-Add-Amazon-EFA-driver-version-1.4.patch
ApplyPatch 0122-percpu-refcount-Introduce-percpu_ref_resurrect.patch
ApplyPatch 0123-block-Allow-unfreezing-of-a-queue-while-requests-are.patch
ApplyPatch 0124-nvme-change-namespaces_mutext-to-namespaces_rwsem.patch
ApplyPatch 0125-blk-mq-fix-hang-caused-by-freeze-unfreeze-sequence.patch
ApplyPatch 0126-nvme-move-the-dying-queue-check-from-cancel-to-compl.patch
ApplyPatch 0127-nvme-pci-Better-support-for-disabling-controller.patch
ApplyPatch 0128-nvme-host-core-Allow-overriding-of-wait_ready-timeou.patch
ApplyPatch 0129-nvme-host-pci-Fix-a-race-in-controller-removal.patch
ApplyPatch 0130-nvme-pci-move-cq_vector-1-check-outside-of-q_lock.patch
ApplyPatch 0131-irqchip-gic-v3-its-Pass-its_node-pointer-to-each-com.patch
ApplyPatch 0132-irqchip-gic-v3-its-Only-emit-SYNC-if-targetting-a-va.patch
ApplyPatch 0133-irqchip-gic-v3-its-Only-emit-VSYNC-if-targetting-a-v.patch
ApplyPatch 0134-irqchip-gic-v3-its-Refactor-LPI-allocator.patch
ApplyPatch 0135-irqchip-gic-v3-its-Use-full-range-of-LPIs.patch
ApplyPatch 0136-irqchip-gic-v3-its-Move-minimum-LPI-requirements-to-.patch
ApplyPatch 0137-irqchip-gic-v3-its-Drop-chunk-allocation-compatibili.patch
ApplyPatch 0138-irqchip-gic-v3-Expose-GICD_TYPER-in-the-rdist-struct.patch
ApplyPatch 0139-irqchip-gic-v3-its-Honor-hypervisor-enforced-LPI-ran.patch
ApplyPatch 0140-irqchip-gic-v3-its-Reduce-minimum-LPI-allocation-to-.patch
ApplyPatch 0141-irqchip-gic-v3-its-Cap-lpi_id_bits-to-reduce-memory-.patch
ApplyPatch 0142-irqchip-gic-v3-its-Gracefully-fail-on-LPI-exhaustion.patch
ApplyPatch 0143-irqchip-gic-v3-its-Fix-comparison-logic-in-lpi_range.patch
ApplyPatch 0144-iommu-io-pgtable-arm-Convert-to-IOMMU-API-TLB-sync.patch
ApplyPatch 0145-iommu-io-pgtable-arm-v7s-Convert-to-IOMMU-API-TLB-sy.patch
ApplyPatch 0146-iommu-arm-smmu-v3-Implement-flush_iotlb_all-hook.patch
ApplyPatch 0147-iommu-dma-Add-support-for-non-strict-mode.patch
ApplyPatch 0148-iommu-Add-iommu.strict-command-line-option.patch
ApplyPatch 0149-iommu-io-pgtable-arm-Add-support-for-non-strict-mode.patch
ApplyPatch 0150-iommu-arm-smmu-v3-Add-support-for-non-strict-mode.patch
ApplyPatch 0151-iommu-io-pgtable-arm-v7s-Add-support-for-non-strict-.patch
ApplyPatch 0152-iommu-arm-smmu-Support-non-strict-mode.patch
ApplyPatch 0153-iommu-use-config-option-to-specify-if-iommu-mode-sho.patch
ApplyPatch 0154-locking-atomic-Add-atomic_cond_read_acquire.patch
ApplyPatch 0155-locking-barriers-Introduce-smp_cond_load_relaxed-and.patch
ApplyPatch 0156-locking-qspinlock-Use-atomic_cond_read_acquire.patch
ApplyPatch 0157-locking-mcs-Use-smp_cond_load_acquire-in-MCS-spin-lo.patch
ApplyPatch 0158-locking-qspinlock-Use-smp_cond_load_relaxed-to-wait-.patch
ApplyPatch 0159-locking-qspinlock-Use-smp_store_release-in-queued_sp.patch
ApplyPatch 0160-locking-qspinlock-Elide-back-to-back-RELEASE-operati.patch
ApplyPatch 0161-locking-qspinlock-Use-try_cmpxchg-instead-of-cmpxchg.patch
ApplyPatch 0162-MAINTAINERS-Add-myself-as-a-co-maintainer-for-the-lo.patch
ApplyPatch 0163-arm64-barrier-Implement-smp_cond_load_relaxed.patch
ApplyPatch 0164-arm64-locking-Replace-ticket-lock-implementation-wit.patch
ApplyPatch 0165-arm64-kconfig-Ensure-spinlock-fastpaths-are-inlined-.patch
ApplyPatch 0166-arm64-pull-in-upstream-erratum-workarounds.patch
ApplyPatch 0167-arm64-Avoid-flush_icache_range-in-alternatives-patch.patch
ApplyPatch 0168-update-ena-driver-to-version-2.1.3.patch
ApplyPatch 0169-Revert-nvme-pci-Better-support-for-disabling-control.patch
ApplyPatch 0170-nvme-pci-introduce-RECONNECTING-state-to-mark-initia.patch
ApplyPatch 0171-nvme-allow-controller-RESETTING-to-RECONNECTING-tran.patch
ApplyPatch 0172-nvme-rename-NVME_CTRL_RECONNECTING-state-to-NVME_CTR.patch
ApplyPatch 0173-nvme-pci-Fix-timeouts-in-connecting-state.patch
ApplyPatch 0174-nvme-pci-shutdown-on-timeout-during-deletion.patch
ApplyPatch 0175-nvme-pci-Unblock-reset_work-on-IO-failure.patch
ApplyPatch 0176-nvme-pci-Don-t-disable-on-timeout-in-reset-state.patch
ApplyPatch 0177-nvme-pci-use-atomic-bitops-to-mark-a-queue-enabled.patch
ApplyPatch 0178-arm64-fix-merge-error-in-errata-changes.patch
ApplyPatch 0179-lustre-hold-lock-while-walking-changelog-dev-list.patch
ApplyPatch 0180-Revert-Fix-the-locking-in-dcache_readdir-and-friends.patch
ApplyPatch 0181-drivers-amazon-efa-update-to-1.5.0.patch
ApplyPatch 0182-SMB3-Backup-intent-flag-missing-from-compounded-ops.patch
ApplyPatch 0183-Add-support-for-setting-owner-info-dos-attributes-an.patch
ApplyPatch 0184-update-ENA-linux-driver-to-version-2.2.1.patch
ApplyPatch 0185-Revert-update-ENA-linux-driver-to-version-2.2.1.patch
ApplyPatch 0186-kunit-test-add-KUnit-test-runner-core.patch
ApplyPatch 0187-kunit-test-add-test-resource-management-API.patch
ApplyPatch 0188-kunit-test-add-string_stream-a-std-stream-like-strin.patch
ApplyPatch 0189-kunit-test-add-assertion-printing-library.patch
ApplyPatch 0190-kunit-test-add-the-concept-of-expectations.patch
ApplyPatch 0191-lib-enable-building-KUnit-in-lib.patch
ApplyPatch 0192-kunit-test-add-initial-tests.patch
ApplyPatch 0193-kunit-test-add-support-for-test-abort.patch
ApplyPatch 0194-kunit-test-add-tests-for-kunit-test-abort.patch
ApplyPatch 0195-kunit-test-add-the-concept-of-assertions.patch
ApplyPatch 0196-kunit-test-add-tests-for-KUnit-managed-resources.patch
ApplyPatch 0197-kunit-fix-failure-to-build-without-printk.patch
ApplyPatch 0198-kunit-tool-add-Python-wrappers-for-running-KUnit-tes.patch
ApplyPatch 0199-kunit-defconfig-add-defconfigs-for-building-KUnit-te.patch
ApplyPatch 0200-kunit-Fix-build_dir-option.patch
ApplyPatch 0201-Documentation-kunit-add-documentation-for-KUnit.patch
ApplyPatch 0202-Documentation-kunit-Fix-verification-command.patch
ApplyPatch 0203-lib-list-test-add-a-test-for-the-list-doubly-linked-.patch
ApplyPatch 0204-cifs-Fix-slab-out-of-bounds-in-send_set_info-on-SMB2.patch
ApplyPatch 0205-CIFS-don-t-log-STATUS_NOT_FOUND-errors-for-DFS.patch
ApplyPatch 0206-Don-t-log-expected-error-on-DFS-referral-request.patch
ApplyPatch 0207-Don-t-log-confusing-message-on-reconnect-by-default.patch
ApplyPatch 0208-genirq-export-irq_get_percpu_devid_partition-to-modu.patch
ApplyPatch 0209-perf-core-Export-AUX-buffer-helpers-to-modules.patch
ApplyPatch 0210-perf-core-Add-PERF_AUX_FLAG_COLLISION-to-report-coll.patch
ApplyPatch 0211-arm64-sysreg-Move-SPE-registers-and-PSB-into-common-.patch
ApplyPatch 0212-arm64-head-Init-PMSCR_EL2.-PA-PCT-when-entered-at-EL.patch
ApplyPatch 0213-dt-bindings-Document-devicetree-binding-for-ARM-SPE.patch
ApplyPatch 0214-drivers-perf-Add-support-for-ARMv8.2-Statistical-Pro.patch
ApplyPatch 0215-perf-tools-Add-ARM-Statistical-Profiling-Extensions-.patch
ApplyPatch 0216-perf-arm-spe-Fix-uninitialized-record-error-variable.patch
ApplyPatch 0217-ACPICA-ACPI-6.3-MADT-add-support-for-statistical-pro.patch
ApplyPatch 0218-ACPICA-ACPI-6.3-PPTT-add-additional-fields-in-Proces.patch
ApplyPatch 0219-ACPI-PPTT-Modify-node-flag-detection-to-find-last-ID.patch
ApplyPatch 0220-ACPI-PPTT-Add-function-to-return-ACPI-6.3-Identical-.patch
ApplyPatch 0221-arm_pmu-acpi-spe-Add-initial-MADT-SPE-probing.patch
ApplyPatch 0222-perf-arm_spe-Enable-ACPI-Platform-automatic-module-l.patch
ApplyPatch 0223-ena-update-to-2.2.3.patch
ApplyPatch 0224-random-try-to-actively-add-entropy-rather-than-passi.patch
ApplyPatch 0225-random-introduce-RANDOM_WAIT_JITTER-config-option.patch
ApplyPatch 0226-lustre-update-to-AmazonFSxLustreClient-v2.10.8-1.patch
ApplyPatch 0227-Revert-ena-update-to-2.2.3.patch
ApplyPatch 0228-kernel-sched-fair.c-Fix-divide-by-zero.patch
ApplyPatch 0229-efi-honour-memory-reservations-passed-via-a-linux-sp.patch
ApplyPatch 0230-efi-arm-libstub-add-a-root-memreserve-config-table.patch
ApplyPatch 0231-efi-add-API-to-reserve-memory-persistently-across-ke.patch
ApplyPatch 0232-efi-Permit-calling-efi_mem_reserve_persistent-from-a.patch
ApplyPatch 0233-efi-Prevent-GICv3-WARN-by-mapping-the-memreserve-tab.patch
ApplyPatch 0234-efi-Permit-multiple-entries-in-persistent-memreserve.patch
ApplyPatch 0235-efi-Reduce-the-amount-of-memblock-reservations-for-p.patch
ApplyPatch 0236-efi-memreserve-deal-with-memreserve-entries-in-unmap.patch
ApplyPatch 0237-efi-memreserve-Register-reservations-as-reserved-in-.patch
ApplyPatch 0238-irqchip-gic-v3-Ensure-GICR_CTLR.EnableLPI-0-is-obser.patch
ApplyPatch 0239-irqchip-gic-v3-its-Change-initialization-ordering-fo.patch
ApplyPatch 0240-irqchip-gic-v3-its-Simplify-LPI_PENDBASE_SZ-usage.patch
ApplyPatch 0241-irqchip-gic-v3-its-Split-property-table-clearing-fro.patch
ApplyPatch 0242-irqchip-gic-v3-its-Move-pending-table-allocation-to-.patch
ApplyPatch 0243-irqchip-gic-v3-its-Keep-track-of-property-table-s-PA.patch
ApplyPatch 0244-irqchip-gic-v3-its-Allow-use-of-pre-programmed-LPI-t.patch
ApplyPatch 0245-irqchip-gic-v3-its-Use-pre-programmed-redistributor-.patch
ApplyPatch 0246-irqchip-gic-v3-its-Check-that-all-RDs-have-the-same-.patch
ApplyPatch 0247-irqchip-gic-v3-its-Register-LPI-tables-with-EFI-conf.patch
ApplyPatch 0248-irqchip-gic-v3-its-Allow-use-of-LPI-tables-in-reserv.patch
ApplyPatch 0249-iommu-arm-smmu-v3-Prevent-any-devices-access-to-memo.patch
ApplyPatch 0250-iommu-arm-smmu-v3-Abort-all-transactions-if-SMMU-is-.patch
ApplyPatch 0251-iommu-arm-smmu-v3-Don-t-disable-SMMU-in-kdump-kernel.patch
ApplyPatch 0252-xen-blkfront-Delay-flush-till-queue-lock-dropped.patch
ApplyPatch 0253-Upgrade-to-ena-2.2.8.patch
ApplyPatch 0254-Fix-a-build-issue-caused-by-45b2013293a2a.patch
ApplyPatch 0255-NFSv4.1-fix-incorrect-return-value-in-copy_file_rang.patch
ApplyPatch 0256-lustre-restore-mgc-binding-for-sptlrpc.patch
ApplyPatch 0257-Update-lustrefsx-to-v2.10.8-5.patch
ApplyPatch 0258-printk-Move-console-matching-logic-into-a-separate-f.patch
ApplyPatch 0259-printk-Fix-preferred-console-selection-with-multiple.patch
ApplyPatch 0260-printk-Correctly-set-CON_CONSDEV-even-when-preferred.patch
ApplyPatch 0261-KVM-arm-arm64-Factor-out-hypercall-handling-from-PSC.patch
ApplyPatch 0262-KVM-arm64-Implement-PV_TIME_FEATURES-call.patch
ApplyPatch 0263-KVM-Implement-kvm_put_guest.patch
ApplyPatch 0264-KVM-arm64-Support-stolen-time-reporting-via-shared-s.patch
ApplyPatch 0265-KVM-Allow-kvm_device_ops-to-be-const.patch
ApplyPatch 0266-KVM-arm64-Provide-VCPU-attributes-for-stolen-time.patch
ApplyPatch 0267-arm-arm64-smccc-psci-add-arm_smccc_1_1_get_conduit.patch
ApplyPatch 0268-arm-arm64-Provide-a-wrapper-for-SMCCC-1.1-calls.patch
ApplyPatch 0269-arm-arm64-Make-use-of-the-SMCCC-1.1-wrapper.patch
ApplyPatch 0270-arm64-Retrieve-stolen-time-as-paravirtualized-guest.patch
ApplyPatch 0271-Makefile-Add-AMZN-specific-variables.patch
ApplyPatch 0272-ena-Update-to-2.2.10.patch
ApplyPatch 0273-fs-copy-BTRFS_IOC_-SG-ET_FSLABEL-to-vfs.patch
ApplyPatch 0274-xfs-one-shot-cached-buffers.patch
ApplyPatch 0275-xfs-add-prerequisite-for-online-labeling.patch
ApplyPatch 0276-xfs-implement-online-get-set-fs-label.patch
ApplyPatch 0277-xfs-fix-string-handling-in-label-get-set-functions.patch
ApplyPatch 0278-xfs-fall-back-to-native-ioctls-for-unhandled-compat-.patch
ApplyPatch 0279-mm-rid-swapoff-of-quadratic-complexity.patch
ApplyPatch 0280-mm-swapoff-shmem_unuse-stop-eviction-without-igrab.patch
ApplyPatch 0281-sched-wait-Introduce-wait_var_event.patch
ApplyPatch 0282-UBUNTU-SAUCE-aws-mm-aggressive-swapoff.patch
ApplyPatch 0283-UBUNTU-SAUCE-aws-mm-swap-improve-swap-readahead-heur.patch
ApplyPatch 0284-block-genhd-Notify-udev-about-capacity-change.patch
ApplyPatch 0285-drivers-block-virtio_blk.c-Convert-to-use-set_capaci.patch
ApplyPatch 0286-drivers-block-xen-blkfront.c-Convert-to-use-set_capa.patch
ApplyPatch 0287-drivers-nvme-host-core.c-Convert-to-use-set_capacity.patch
ApplyPatch 0288-drivers-scsi-sd.c-Convert-to-use-set_capacity_revali.patch
ApplyPatch 0289-CIFS-make-IPC-a-regular-tcon.patch
ApplyPatch 0290-CIFS-use-tcon_ipc-instead-of-use_ipc-parameter-of-SM.patch
ApplyPatch 0291-drivers-amazon-efa-update-to-1.9.0.patch
ApplyPatch 0292-Remove-unused-variables-in-the-nvme-disk-resize-patc.patch
ApplyPatch 0293-net-packet-fix-overflow-in-tpacket_rcv.patch
ApplyPatch 0294-cpu-hotplug-Add-new-add-remove-_cpu-functions.patch
ApplyPatch 0295-define-__poll_t-annotate-constants.patch
ApplyPatch 0296-Partial-backport-of-mm-introduce-page_size.patch
ApplyPatch 0297-nitro_enclaves-Add-ioctl-interface-definition.patch
ApplyPatch 0298-nitro_enclaves-Define-the-PCI-device-interface.patch
ApplyPatch 0299-nitro_enclaves-Define-enclave-info-for-internal-book.patch
ApplyPatch 0300-nitro_enclaves-Init-PCI-device-driver.patch
ApplyPatch 0301-nitro_enclaves-Handle-PCI-device-command-requests.patch
ApplyPatch 0302-nitro_enclaves-Handle-out-of-band-PCI-device-events.patch
ApplyPatch 0303-nitro_enclaves-Init-misc-device-providing-the-ioctl-.patch
ApplyPatch 0304-nitro_enclaves-Add-logic-for-creating-an-enclave-VM.patch
ApplyPatch 0305-nitro_enclaves-Add-logic-for-setting-an-enclave-vCPU.patch
ApplyPatch 0306-nitro_enclaves-Add-logic-for-getting-the-enclave-ima.patch
ApplyPatch 0307-nitro_enclaves-Add-logic-for-setting-an-enclave-memo.patch
ApplyPatch 0308-nitro_enclaves-Add-logic-for-starting-an-enclave.patch
ApplyPatch 0309-nitro_enclaves-Add-logic-for-terminating-an-enclave.patch
ApplyPatch 0310-nitro_enclaves-Add-Kconfig-for-the-Nitro-Enclaves-dr.patch
ApplyPatch 0311-enclaves-Define-PCI_VENDOR_ID_AMAZON.patch
ApplyPatch 0312-nitro_enclaves-Add-Makefile-for-the-Nitro-Enclaves-d.patch
ApplyPatch 0313-nitro_enclaves-Add-sample-for-ioctl-interface-usage.patch
ApplyPatch 0314-nitro_enclaves-Add-overview-documentation.patch
ApplyPatch 0315-MAINTAINERS-Add-entry-for-the-Nitro-Enclaves-driver.patch
ApplyPatch 0316-arm64-Enable-PCI-write-combine-resources-under-sysfs.patch
ApplyPatch 0317-nfs-optimise-readdir-cache-page-invalidation.patch
ApplyPatch 0318-nfs-Fix-security-label-length-not-being-reset.patch
ApplyPatch 0319-netfilter-ctnetlink-add-a-range-check-for-l3-l4-prot.patch

# Any further pre-build tree manipulations happen here.

chmod +x scripts/checkpatch.pl

touch .scmversion

# only deal with configs if we are going to build for the arch
%ifnarch %nobuildarches

mkdir configs

# Remove configs not for the buildarch
for cfg in kernel-%{version}-*.config; do
  if [ `echo %{all_arch_configs} | grep -c $cfg` -eq 0 ]; then
    rm -f $cfg
  fi
done

%if !%{debugbuildsenabled}
rm -f kernel-%{version}-*debug.config
%endif

# now run oldconfig over all the config files
for i in *.config
do
  mv $i .config
  Arch=`head -1 .config | cut -b 3-`
%if %{with_oldconfig}
  make ARCH=$Arch %{oldconfig_target}
%endif
  echo "# $Arch" > configs/$i
  cat .config >> configs/$i
done
# end of kernel config
%endif

# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -exec rm -f {} \; >/dev/null

cd ..

###
### build
###
%build

%if %{with_sparse}
%define sparse_mflags	C=1
%endif

cp_vmlinux()
{
  eu-strip --remove-comment -o "$2" "$1"
}

export CC=%{?_gcc}%{?!_gcc:gcc}
export HOSTCC=%{?_gcc}%{?!_gcc:gcc}
export HOSTCXX=%{?_gxx}%{?!_gxx:g++}

%global make_defines CC=gcc HOSTCC=gcc HOSTCXX=g++

export KBUILD_BUILD_HOST=$(hostname --short)

BuildKernel() {
    MakeTarget=$1
    KernelImage=$2
    Flavour=$3
    Flav=${Flavour:+.${Flavour}}
    InstallName=${4:-vmlinuz}

    # Pick the right config file for the kernel we're building
    Config=kernel-%{version}-%{_target_cpu}${Flavour:+-${Flavour}}.config
    DevelDir=/usr/src/kernels/%{KVERREL}${Flav}

    # When the bootable image is just the ELF kernel, strip it.
    # We already copy the unstripped file into the debuginfo package.
    if [ "$KernelImage" = vmlinux ]; then
      CopyKernel=cp_vmlinux
    else
      CopyKernel=cp
    fi

    KernelVer=%{version}-%{release}.%{_target_cpu}${Flav}
    echo BUILDING A KERNEL FOR ${Flavour} %{_target_cpu}...

    # make sure EXTRAVERSION says what we want it to say
    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}.%{_target_cpu}${Flav}/" Makefile

    # set AMZN_MAJOR and AMZN_MINOR
    perl -p -i -e "s/^AMZN_MAJOR.*/AMZN_MAJOR = %{AMZN_MAJOR}/" Makefile
    perl -p -i -e "s/^AMZN_MINOR.*/AMZN_MINOR = %{AMZN_MINOR}/" Makefile

    # and now to start the build process

    make -s mrproper
    cp configs/$Config .config

%if %{signmodules}
    cp %{SOURCE11} .
%endif

    Arch=`head -1 .config | cut -b 3-`
    echo USING ARCH=$Arch

    make -s ARCH=$Arch %{oldconfig_target} %{?make_defines} > /dev/null
    make -s ARCH=$Arch V=1 %{?_smp_mflags} $MakeTarget %{?sparse_mflags} %{?make_defines}
    make -s ARCH=$Arch V=1 %{?_smp_mflags} modules %{?sparse_mflags} %{?make_defines} || exit 1

    # Start installing the results
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/boot
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer

%if %{with_dracut}
    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-$KernelVer.img bs=1M count=20
%else
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initrd-$KernelVer.img bs=1M count=5
%endif

    if [ -f arch/$Arch/boot/zImage.stub ]; then
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
    fi
    %if %{signmodules}
        %if %{usingefi}
        # Sign the image if we're using EFI
        %pesign -s -i $KernelImage -o vmlinuz.signed
        if [ ! -s vmlinuz.signed ]; then
            echo "pesigning failed"
            exit 1
        fi
        mv vmlinuz.signed $KernelImage
        %endif
    %endif
    $CopyKernel $KernelImage \
    		$RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    chmod 755 $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer

%if %{with_fips}
    #hmac sign the kernel for FIPS
    echo "Creating hmac file: $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac"
    ls -l $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    sha512hmac $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer | sed -e "s,$RPM_BUILD_ROOT,," >  $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac
%endif
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
    # Override $(mod-fw) because we don't want it to install any firmware
    # we'll get it from the linux-firmware package and we don't want conflicts
    make -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=$KernelVer mod-fw=

%ifarch %{vdso_arches}
    make -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=$KernelVer
    if grep '^CONFIG_XEN=y$' .config >/dev/null ; then
        echo > ldconfig-kernel.conf "\
# This directive teaches ldconfig to search in nosegneg subdirectories
# and cache the DSOs there with extra bit 0 set in their hwcap match
# fields.  In Xen guest kernels, the vDSO tells the dynamic linker to
# search in nosegneg subdirectories and to match this extra hwcap bit
# in the ld.so.cache file.
hwcap 1 nosegneg"
    fi
    if [ ! -s ldconfig-kernel.conf ]; then
      echo > ldconfig-kernel.conf "\
# Placeholder file, no vDSO hwcap entries used in this kernel."
    fi
    %{__install} -D -m 444 ldconfig-kernel.conf \
        $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-$KernelVer.conf
%endif

    # And save the headers/makefiles etc for building modules against
    #
    # This all looks scary, but the end result is supposed to be:
    # * all arch relevant include/ files
    # * all Makefile/Kconfig files
    # * all script/ files

    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    (cd $RPM_BUILD_ROOT/lib/modules/$KernelVer ; ln -s build source)
    # dirs for additional modules per module-init-tools, kbuild/modules.txt
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/extra
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/weak-updates
    # first copy everything
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp Module.symvers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    gzip -c9 Module.symvers >  $RPM_BUILD_ROOT/boot/symvers-$KernelVer.gz
    cp System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -s Module.markers ]; then
      cp Module.markers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi
    # then drop all but the needed Makefiles/Kconfig files
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Documentation
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -f tools/objtool/objtool ]; then
      cp -a tools/objtool/objtool $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/objtool/ || :
    fi
    cp -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -d arch/$Arch/scripts ]; then
      cp -a arch/$Arch/scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch} || :
    fi
    if [ -f arch/$Arch/*lds ]; then
      cp -a arch/$Arch/*lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch}/ || :
    fi
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*.o
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*/*.o
    if [ -d arch/%{asmarch}/include ]; then
      cp -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    cp -a include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include

    # newer kernels relocate these from under include/linux to
    # include/generated.... Maintain compatibility with old(er) code looking
    # for former files in the formerly valid location
    pushd  $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/linux
    test -s utsrelease.h        || ln -sf ../generated/utsrelease.h .
    test -s autoconf.h          || ln -sf ../generated/autoconf.h .
    popd
    # Make sure the Makefile and version.h have a matching timestamp so that
    # external modules can be built
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/uapi/linux/version.h
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/linux/autoconf.h
    # Copy .config to include/config/auto.conf so "make prepare" is unnecessary.
    cp -a $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf

%if %{with_debuginfo}
    eu-readelf -n vmlinux | grep "Build ID" | awk '{print $NF}' > vmlinux.id
    cp vmlinux.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.id
    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    #
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    cp vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
%endif #debuginfo

    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # mark modules executable so that strip-to-file can strip them
    xargs --no-run-if-empty chmod u+x < modnames

    # Generate a list of modules for block and networking.

    grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
    sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
      sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
      LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
    }

    collect_modules_list networking \
                        'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt(l_|2x00)(pci|usb)_probe|register_netdevice'
    collect_modules_list block \
                        'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size'
    collect_modules_list drm \
                        'drm_open|drm_init'
    collect_modules_list modesetting \
                        'drm_crtc_init'

    # detect missing or incorrect license tags
    rm -f modinfo
    while read i
    do
      echo -n "${i#$RPM_BUILD_ROOT/lib/modules/$KernelVer/} " >> modinfo
      %{_sbindir}/modinfo -l $i >> modinfo
    done < modnames

    grep -E -v \
    	  'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' \
	  modinfo && exit 1

    rm -f modinfo modnames

    # Call the modules-extra script to move things around
    %{SOURCE17} $RPM_BUILD_ROOT/lib/modules/$KernelVer %{SOURCE16}

%if %{signmodules}
    # Save off the .tmp_versions/ directory.  We'll use it in the
    # __debug_install_post macro below to sign the right things
    # Also save the signing keys so we actually sign the modules with the
    # right key.
    cp -r .tmp_versions .tmp_versions.sign${Flavour:+.${Flavour}}
    cp certs/signing_key.pem signing_key.pem.sign${Flavour:+.${Flavour}}
    cp certs/signing_key.x509 signing_key.x509.sign${Flavour:+.${Flavour}}
%endif

    # remove files that will be auto generated by depmod at rpm -i time
    for i in alias alias.bin builtin.bin ccwmap dep dep.bin ieee1394map inputmap isapnpmap ofmap pcimap seriomap symbols symbols.bin usbmap devname softdep
    do
      rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$i
    done

    # Move the devel headers out of the root file system
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir
    ln -sf $DevelDir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    # prune junk from kernel-devel
    find $RPM_BUILD_ROOT/usr/src/kernels -name ".*.cmd" -exec rm -f {} \;
}

###
# DO it...
###

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}

cd linux-%{KVERREL}

%if %{with_debug}
BuildKernel %make_target %kernel_image debug
%endif

%if %{with_up}
BuildKernel %make_target %kernel_image
%endif

# perf
%global perf_make \
  make %{?_smp_mflags} -C tools/perf -s V=1 EXTRA_CFLAGS="-Wno-error=array-bounds" HAVE_CPLUS_DEMANGLE=1 NO_LIBUNWIND=1 NO_GTK2=1 NO_LIBNUMA=1 NO_STRLCPY=1 prefix=%{_prefix} lib=%{_lib} PYTHON=%{__python}
%if %{with_perf}
%{perf_make} all
%{perf_make} man || %{doc_build_fail}
%endif

%if %{with_tools}
%ifarch %{cpupowerarchs}
# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
make %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif # ix86
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif # x86_64
%ifarch %{ix86} x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   make
   popd
   pushd tools/power/x86/turbostat
   make
   popd
%endif #turbostat/x86_energy_perf_policy
%endif # cpupowerarchs
%endif # tools

%if %{with_doc}
#
# Make the HTML documents.
# Newer kernel versions use ReST markups for documentation which
# needs to be built using Sphinx. Sphinx toolchain is fragile and any
# upgrade to its toolchain or dependent python package can cause
# documentation build to fail. To avoid this problem, documentation
# build uses one particular version of Sphinx. To build document,
# we create a virtual environment and install the required version
# of Sphinx inside it.
# Refer to $SRC/Documentation/sphinx/requirements.txt for more
# information related to package and version dependency.
#
virtualenv doc_build_env
source ./doc_build_env/bin/activate
pip install -r Documentation/sphinx/requirements.txt
make htmldocs || %{doc_build_fail}
deactivate
rm -rf doc_build_env

# Build man pages for the kernel API (section 9)
scripts/kernel-doc -man $(find . -name '*.[ch]') | %{split_man_cmd} Documentation/output/man
pushd Documentation/output/man
gzip *.9
popd

# sometimes non-world-readable files sneak into the kernel source tree
chmod -R a=rX Documentation
find Documentation -type d | xargs chmod u+w

# switch absolute symlinks to relative ones
find . -lname "$(pwd)*" -exec sh -c 'ln -snvf $(python -c "from os.path import *; print relpath(\"$(readlink {})\",dirname(\"{}\"))") {}' \;
%endif # with_doc

# In the modsign case, we do 3 things.  1) We check the "flavour" and hard
# code the value in the following invocations.  This is somewhat sub-optimal
# but we're doing this inside of an RPM macro and it isn't as easy as it
# could be because of that.  2) We restore the .tmp_versions/ directory from
# the one we saved off in BuildKernel above.  This is to make sure we're
# signing the modules we actually built/installed in that flavour.  3) We
# grab the arch and invoke mod-sign.sh command to actually sign the modules.
#
# We have to do all of those things _after_ find-debuginfo runs, otherwise
# that will strip the signature off of the modules.
%define __modsign_install_post \
  if [ "%{signmodules}" == "1" ]; then \
    if [ "%{with_debug}" != "0" ]; \
    then \
      Arch=`head -1 configs/kernel-%{rpmversion}-%{_target_cpu}-debug.config | cut -b 3-` \
      rm -rf .tmp_versions \
      mv .tmp_versions.sign.debug .tmp_versions \
      mv signing_key.pem.sign.debug signing_key.pem \
      mv signing_key.x509.sign.debug signing_key.x509 \
      make -s ARCH=$Arch V=1 INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_sign KERNELRELEASE=%{KVERREL}.debug \
      %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}.debug/extra/ \
    else \
      Arch=`head -1 configs/kernel-%{rpmversion}-%{_target_cpu}.config | cut -b 3-` \
      rm -rf .tmp_versions \
      mv signing_key.pem.sign signing_key.pem \
      mv signing_key.x509.sign signing_key.x509 \
      %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/ \
      %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/extra/ \
    fi \
  fi \
%{nil}

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
%define debug_package %{nil}

%if %{with_debuginfo}

%ifnarch noarch
%global __debug_package 1
%files -f debugfiles.list debuginfo-common-%{_target_cpu}
%defattr(-,root,root)
%endif # noarch

%endif # debuginfo

#
# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__modsign_install_post}

###
### install
###

%install

cd linux-%{KVERREL}

%if %{with_doc}
docdir=$RPM_BUILD_ROOT%{_datadir}/doc/kernel-doc-%{rpmversion}
man9dir=$RPM_BUILD_ROOT%{_datadir}/man/man9

# copy the source over
mkdir -p $docdir
tar -f - --exclude=man --exclude='.*' -c Documentation | tar xf - -C $docdir

# Install man pages for the kernel API.
mkdir -p $man9dir
pushd Documentation/output/man
find -type f -name '*.9.gz' -print0 |
xargs -0 --no-run-if-empty %{__install} -m 444 -t $man9dir $m
popd
ls $man9dir | grep -q '' || > $man9dir/BROKEN
%endif # with_doc

# We have to do the headers install before the tools install because the
# kernel headers_install will remove any header files in /usr/include that
# it doesn't install itself.

%if %{with_headers}
# Install kernel headers
make -s ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

# Do headers_check but don't die if it fails.
make -s ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_check \
     > hdrwarnings.txt || :
if grep -q exist hdrwarnings.txt; then
   sed s:^$RPM_BUILD_ROOT/usr/include/:: hdrwarnings.txt
   # Temporarily cause a build failure if header inconsistencies.
   # exit 1
fi

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
     	-name ..install.cmd -o -name ..check.cmd \) | xargs rm -f

# glibc provides scsi headers for itself, for now
rm -rf $RPM_BUILD_ROOT/usr/include/scsi
rm -f $RPM_BUILD_ROOT/usr/include/asm*/atomic.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/io.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/irq.h
%endif

%if %{with_perf}
# perf tool binary and supporting scripts/binaries
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install
# python-perf extension
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-python_ext
# perf man pages (note: implicit rpm magic compresses them later)
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-man || %{doc_build_fail}
# clean up files we don't use
rm -f $RPM_BUILD_ROOT/etc/bash_completion.d/perf
%endif

%if %{with_tools}
%ifarch %{cpupowerarchs}
make -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
rm -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower
mv cpupower.lang ../
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
%ifarch %{ix86} x86_64
   mkdir -p %{buildroot}%{_mandir}/man8
   pushd tools/power/x86/x86_energy_perf_policy
   make DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   make DESTDIR=%{buildroot} install
   popd
%endif #turbostat/x86_energy_perf_policy
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
mkdir -p %{buildroot}%{_initddir} %{buildroot}%{_sysconfdir}/sysconfig
#install -m644 %{SOURCE2000} %{buildroot}%{_initddir}/cpupower
install -m644 %{SOURCE2001} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
%endif # cpupowerarchs
# just in case so the files list won't croak
touch ../cpupower.lang
%endif # tools


###
### clean
###

%clean
rm -rf $RPM_BUILD_ROOT

###
### scripts
###

%if %{with_tools}
%post tools
%{_sbindir}/ldconfig

%postun tools
%{_sbindir}/ldconfig
%endif

#
# This macro defines a %%post script for a kernel*-devel package.
#	%%kernel_devel_post [<subpackage>]
#
%define kernel_devel_post() \
%{expand:%%post %{?1:%{1}-}devel}\
if [ -f /etc/sysconfig/kernel ]\
then\
    . /etc/sysconfig/kernel || exit $?\
fi\
if [ "$HARDLINK" != "no" -a -x %{_sbindir}/hardlink ]\
then\
    (cd /usr/src/kernels/%{KVERREL}%{?1:.%{1}} &&\
     %{_bindir}/find . -type f | while read f; do\
       %{_sbindir}/hardlink -c /usr/src/kernels/*.%{dist}.*/$f $f\
     done)\
fi\
%{nil}

# This macro defines a %%posttrans script for a kernel package.
#	%%kernel_variant_posttrans [<subpackage>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_posttrans() \
%{expand:%%posttrans %{?1}}\
%{expand:\
%if %{with_dracut}\
%{_sbindir}/new-kernel-pkg --package kernel%{?1:-%{1}} --mkinitrd --make-default --dracut --depmod --install %{KVERREL}%{?1:-%{1}} || exit $?\
%else\
%{_sbindir}/new-kernel-pkg --package kernel%{?1:-%{1}} --mkinitrd --make-default --depmod --install %{KVERREL}%{?1:-%{1}} || exit $?\
%endif\
}\
%{_sbindir}/new-kernel-pkg --package kernel%{?1:-%{1}} --rpmposttrans %{KVERREL}%{?1:.%{1}} || exit $?\
%{nil}

#
# This macro defines a %%post script for a kernel package and its devel package.
#	%%kernel_variant_post [-v <subpackage>] [-r <replace>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_post(v:r:) \
%{expand:%%kernel_devel_post %{?-v*}}\
%{expand:%%kernel_variant_posttrans %{?-v*}}\
%{expand:%%post %{?-v*}}\
%{-r:\
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&\
   [ -f /etc/sysconfig/kernel ]; then\
  %{_bindir}/sed -r -i -e 's/^DEFAULTKERNEL=%{-r*}$/DEFAULTKERNEL=kernel%{?-v:-%{-v*}}/' /etc/sysconfig/kernel || exit $?\
fi}\
%{nil}

#
# This macro defines a %%preun script for a kernel package.
#	%%kernel_variant_preun <subpackage>
#
%define kernel_variant_preun() \
%{expand:%%preun %{?1}}\
%{_sbindir}/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL}%{?1:.%{1}} || exit $?\
%{nil}

%kernel_variant_preun
%kernel_variant_post

%kernel_variant_preun debug
%kernel_variant_post -v debug

if [ -x %{_sbindir}/ldconfig ]
then
    %{_sbindir}/ldconfig -X || exit $?
fi

###
### file lists
###

%if %{with_headers}
%files headers
%defattr(-,root,root)
/usr/include/*
%endif

# only some architecture builds need kernel-doc
%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/kernel-doc-%{rpmversion}/Documentation/*
%dir %{_datadir}/doc/kernel-doc-%{rpmversion}/Documentation
%dir %{_datadir}/doc/kernel-doc-%{rpmversion}
%{_datadir}/man/man9/*
%endif

%if %{with_perf}
%files -n perf
%defattr(-,root,root)
%{_bindir}/perf
%{_bindir}/trace
%dir %{_libexecdir}/perf-core
%{_libexecdir}/perf-core/*
%{_datadir}/perf-core/*
%{_datadir}/doc/perf*/*
%dir %{_libdir}/traceevent/plugins
%{_libdir}/traceevent/plugins/*
%{_mandir}/man[1-8]/perf*
%doc linux-%{KVERREL}/tools/perf/Documentation/examples.txt

%files -n python-perf
%defattr(-,root,root)
%{python_sitearch}/*

%if %{with_debuginfo}
%files -f perf-debuginfo.list -n perf-debuginfo
%defattr(-,root,root)

%files -f python-perf-debuginfo.list -n python-perf-debuginfo
%defattr(-,root,root)
%endif # with_debuginfo
%endif # with_perf

%if %{with_tools}
%files tools -f cpupower.lang
%defattr(-,root,root)
%{_mandir}/man[1-8]/cpupower*
%{_bindir}/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*
%endif
%{_libdir}/libcpupower.so.0
%{_libdir}/libcpupower.so.0.0.1
#%{_initddir}/cpupower
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower

%if %{with_debuginfo}
%files tools-debuginfo -f kernel-tools-debuginfo.list
%defattr(-,root,root)
%endif

%ifarch %{cpupowerarchs}
%files tools-devel
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%endif
%endif # with_tools

# This is %%{image_install_path} on an arch where that includes ELF files,
# or empty otherwise.
%define elf_image_install_path %{?kernel_image_elf:%{image_install_path}}

#
# This macro defines the %%files sections for a kernel package
# and its devel and debuginfo packages.
#	%%kernel_variant_files [-k vmlinux] <condition> <subpackage>
#
%define kernel_variant_files(k:) \
%if %{1}\
%{expand:%%files %{?2}}\
%defattr(-,root,root)\
/%{image_install_path}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-%{KVERREL}%{?2:.%{2}}\
%attr(600,root,root) /boot/System.map-%{KVERREL}%{?2:.%{2}}\
%if %{with_fips} \
/%{image_install_path}/.vmlinuz-%{KVERREL}%{?2:.%{2}}.hmac \
%endif \
/boot/symvers-%{KVERREL}%{?2:.%{2}}.gz\
/boot/config-%{KVERREL}%{?2:.%{2}}\
%dir /lib/modules/%{KVERREL}%{?2:.%{2}}\
/lib/modules/%{KVERREL}%{?2:.%{2}}/kernel\
/lib/modules/%{KVERREL}%{?2:.%{2}}/build\
/lib/modules/%{KVERREL}%{?2:.%{2}}/source\
/lib/modules/%{KVERREL}%{?2:.%{2}}/extra\
/lib/modules/%{KVERREL}%{?2:.%{2}}/updates\
/lib/modules/%{KVERREL}%{?2:.%{2}}/weak-updates\
%ifarch %{vdso_arches}\
/lib/modules/%{KVERREL}%{?2:.%{2}}/vdso\
/etc/ld.so.conf.d/kernel-%{KVERREL}%{?2:.%{2}}.conf\
%endif\
/lib/modules/%{KVERREL}%{?2:.%{2}}/modules.*\
%if %{with_dracut}\
%ghost /boot/initramfs-%{KVERREL}%{?2:.%{2}}.img\
%else\
%ghost /boot/initrd-%{KVERREL}%{?2:.%{2}}.img\
%endif\
%{expand:%%files %{?2:%{2}-}devel}\
%defattr(-,root,root)\
%verify(not mtime) /usr/src/kernels/%{KVERREL}%{?2:.%{2}}\
%dir /usr/src/kernels\
%if %{with_debuginfo}\
%ifnarch noarch\
%{expand:%%files -f debuginfo%{?2}.list %{?2:%{2}-}debuginfo}\
%defattr(-,root,root)\
%endif\
%endif\
%endif\
%{nil}

%kernel_variant_files %{with_up}
%kernel_variant_files %{with_debug} debug

#
# Finally kernel-livepatch as it has it's own version/release
# NOTE: Don't move this anywhere else, otherwise it'll need
# it's own Name: and that affects all the packages that
# follow. Aslo having a Version, Release affects other subpackages
# so safely tuck this to the end.
# Other Caveats: This spec file uses a special hack for __spec_install_post
# Hence, all operations in __spec_install_post should not refer to
# either %%{version} or %%{release}
#
%ifarch x86_64
%package -n kernel-livepatch-%{rpmversion}-%{buildid}
Summary: Livepatches for the Linux Kernel
Version: 1.0
Release: 0%{?dist}
Requires: kpatch
%systemd_requires

%description -n kernel-livepatch-%{rpmversion}-%{buildid}
This package contains the live patch modules for bug fixes
against the version of the kernel. This package contains
version 0 (no real livepatches) and helps subscribe to
the kernel livepatch updates for the kernel.

%files -n kernel-livepatch-%{rpmversion}-%{buildid}
%defattr(-,root,root)
%{nil}
%endif

%changelog
* Wed Sep 23 2020 Builder <builder@amazon.com>
- builder/572453a4a8730efd79668a45d410bee66fd45eda last changes:

- linux/23e03786c673356c346b92b870b850f45ffa22ff last changes:
  + [23e0378] [2020-08-24] netfilter: ctnetlink: add a range check for l3/l4 protonum (willmcvicker@google.com)
  + [f517cbc] [2020-09-15] nfs: Fix security label length not being reset (jeffrey.mitchell@starlab.io)
  + [9fb69ea] [2020-01-22] nfs: optimise readdir cache page invalidation (dai.ngo@oracle.com)
  + [9aac8b1] [2020-09-18] arm64: Enable PCI write-combine resources under sysfs (csbisa@amazon.com)
  + [f33cb06] [2020-04-17] MAINTAINERS: Add entry for the Nitro Enclaves driver (andraprs@amazon.com)
  + [b524a70] [2020-05-18] nitro_enclaves: Add overview documentation (andraprs@amazon.com)
  + [672ae64] [2020-05-18] nitro_enclaves: Add sample for ioctl interface usage (andraprs@amazon.com)
  + [eebacda8] [2020-02-05] nitro_enclaves: Add Makefile for the Nitro Enclaves driver (andraprs@amazon.com)
  + [dcaf450] [2020-09-17] enclaves: Define PCI_VENDOR_ID_AMAZON (samjonas@amazon.com)
  + [662ccad] [2020-02-05] nitro_enclaves: Add Kconfig for the Nitro Enclaves driver (andraprs@amazon.com)
  + [6730e57] [2020-03-09] nitro_enclaves: Add logic for terminating an enclave (andraprs@amazon.com)
  + [53bf6b7] [2020-03-09] nitro_enclaves: Add logic for starting an enclave (andraprs@amazon.com)
  + [7e209b9] [2020-03-09] nitro_enclaves: Add logic for setting an enclave memory region (andraprs@amazon.com)
  + [2716260] [2020-05-21] nitro_enclaves: Add logic for getting the enclave image load info (andraprs@amazon.com)
  + [450e9c0] [2020-03-09] nitro_enclaves: Add logic for setting an enclave vCPU (andraprs@amazon.com)
  + [5392f42] [2020-03-09] nitro_enclaves: Add logic for creating an enclave VM (andraprs@amazon.com)
  + [acc7e60] [2020-03-09] nitro_enclaves: Init misc device providing the ioctl interface (andraprs@amazon.com)
  + [b5e4b5f] [2020-03-09] nitro_enclaves: Handle out-of-band PCI device events (andraprs@amazon.com)
  + [ca4b376] [2020-03-09] nitro_enclaves: Handle PCI device command requests (andraprs@amazon.com)
  + [b62d48f] [2020-03-09] nitro_enclaves: Init PCI device driver (andraprs@amazon.com)
  + [ecebbf69] [2020-03-10] nitro_enclaves: Define enclave info for internal bookkeeping (andraprs@amazon.com)
  + [5d83280] [2020-02-05] nitro_enclaves: Define the PCI device interface (andraprs@amazon.com)
  + [604874a] [2020-02-05] nitro_enclaves: Add ioctl interface definition (andraprs@amazon.com)
  + [7f9040b] [2020-09-17] Partial backport of "mm: introduce page_size()" (samjonas@amazon.com)
  + [39d6b61] [2017-07-02] define __poll_t, annotate constants (viro@zeniv.linux.org.uk)
  + [94d61fd] [2020-03-23] cpu/hotplug: Add new {add,remove}_cpu() functions (qais.yousef@arm.com)
  + [3c1e521] [2020-08-30] net/packet: fix overflow in tpacket_rcv (orcohen@paloaltonetworks.com)
  + [3a2079c] [2020-09-01] Remove unused variables in the nvme disk resize patches (yishache@amazon.com)
  + [192270b] [2020-08-27] drivers/amazon: efa: update to 1.9.0 (yishache@amazon.com)
  + [32d4226] [2018-01-24] CIFS: use tcon_ipc instead of use_ipc parameter of SMB2_ioctl (aaptel@suse.com)
  + [d6f73ee] [2018-01-24] CIFS: make IPC a regular tcon (aaptel@suse.com)
  + [6cd06c9] [2020-02-25] drivers/scsi/sd.c: Convert to use set_capacity_revalidate_and_notify (sblbir@amazon.com)
  + [022c2a2] [2020-02-25] drivers/nvme/host/core.c: Convert to use set_capacity_revalidate_and_notify (sblbir@amazon.com)
  + [daad991] [2020-02-25] drivers/block/xen-blkfront.c: Convert to use set_capacity_revalidate_and_notify (sblbir@amazon.com)
  + [e85eb06] [2020-02-25] drivers/block/virtio_blk.c: Convert to use set_capacity_revalidate_and_notify (sblbir@amazon.com)
  + [3fffe85] [2020-02-25] block/genhd: Notify udev about capacity change (sblbir@amazon.com)
  + [ae4d0e3] [2019-12-17] UBUNTU SAUCE [aws]: mm: swap: improve swap readahead heuristic (andrea.righi@canonical.com)
  + [2e3fc43] [2019-05-10] UBUNTU SAUCE [aws]: mm: aggressive swapoff (andrea.righi@canonical.com)
  + [b8d2425] [2019-05-10] sched/wait: Introduce wait_var_event() (peterz@infradead.org)
  + [02eb694] [2019-05-10] mm: swapoff: shmem_unuse() stop eviction without igrab() (hughd@google.com)
  + [df0dff4] [2019-05-10] mm: rid swapoff of quadratic complexity (vpillai@digitalocean.com)
  + [88c1d85] [2019-08-15] xfs: fall back to native ioctls for unhandled compat ones (hch@lst.de)
  + [6071293] [2018-06-05] xfs: fix string handling in label get/set functions (arnd@arndb.de)
  + [013e171] [2018-05-15] xfs: implement online get/set fs label (sandeen@sandeen.net)
  + [67a37ce] [2020-07-08] xfs: add prerequisite for online labeling (astroh@amazon.com)
  + [9afbd87] [2018-05-13] xfs: one-shot cached buffers (dchinner@redhat.com)
  + [26c2e66] [2018-05-15] fs: copy BTRFS_IOC_[SG]ET_FSLABEL to vfs (sandeen@redhat.com)
  + [3a424688] [2020-07-13] ena: Update to 2.2.10 (surajjs@amazon.com)
  + [9d1e57a] [2019-12-09] Makefile: Add AMZN specific variables (luqia@amazon.com)
  + [997abc4] [2019-10-21] arm64: Retrieve stolen time as paravirtualized guest (steven.price@arm.com)
  + [b6e2fe6] [2019-10-21] arm/arm64: Make use of the SMCCC 1.1 wrapper (steven.price@arm.com)
  + [fb17076] [2019-10-21] arm/arm64: Provide a wrapper for SMCCC 1.1 calls (steven.price@arm.com)
  + [d8df501] [2019-08-09] arm/arm64: smccc/psci: add arm_smccc_1_1_get_conduit() (mark.rutland@arm.com)
  + [693593c] [2019-10-21] KVM: arm64: Provide VCPU attributes for stolen time (steven.price@arm.com)
  + [48d49d6] [2019-10-21] KVM: Allow kvm_device_ops to be const (steven.price@arm.com)
  + [e6754bd] [2019-10-21] KVM: arm64: Support stolen time reporting via shared structure (steven.price@arm.com)
  + [bdfcf10] [2019-10-21] KVM: Implement kvm_put_guest() (steven.price@arm.com)
  + [67c23bd] [2019-10-21] KVM: arm64: Implement PV_TIME_FEATURES call (steven.price@arm.com)
  + [b5b2230] [2019-10-21] KVM: arm/arm64: Factor out hypercall handling from PSCI code (christoffer.dall@arm.com)
  + [6e96670] [2020-02-13] printk: Correctly set CON_CONSDEV even when preferred console was not registered (benh@kernel.crashing.org)
  + [6057a42] [2020-02-13] printk: Fix preferred console selection with multiple matches (benh@kernel.crashing.org)
  + [f032887] [2020-02-13] printk: Move console matching logic into a separate function (benh@kernel.crashing.org)
  + [5b47f89] [2020-06-18] Update lustrefsx to v2.10.8-5 (astroh@amazon.com)
  + [e1b5128] [2020-05-27] lustre: restore mgc binding for sptlrpc (astroh@amazon.com)
  + [f4da32d] [2019-04-11] NFSv4.1 fix incorrect return value in copy_file_range (kolga@netapp.com)
  + [4b126dc] [2020-05-27] Fix a build issue caused by 45b2013293a2a (sblbir@amazon.com)
  + [d37ce8e] [2020-05-26] Upgrade to ena 2.2.8 (sblbir@amazon.com)
  + [738cb4a] [2020-04-13] xen-blkfront: Delay flush till queue lock dropped (samjonas@amazon.com)
  + [0d7c20f] [2019-04-23] iommu/arm-smmu-v3: Don't disable SMMU in kdump kernel (will.deacon@arm.com)
  + [2077655] [2018-07-25] iommu/arm-smmu-v3: Abort all transactions if SMMU is enabled in kdump kernel (will.deacon@arm.com)
  + [ffb335e] [2018-07-12] iommu/arm-smmu-v3: Prevent any devices access to memory without registration (thunder.leizhen@huawei.com)
  + [2fe33f2] [2018-07-27] irqchip/gic-v3-its: Allow use of LPI tables in reserved memory (marc.zyngier@arm.com)
  + [a70d9d0] [2018-07-27] irqchip/gic-v3-its: Register LPI tables with EFI config table (marc.zyngier@arm.com)
  + [04f89d2] [2018-07-27] irqchip/gic-v3-its: Check that all RDs have the same property table (marc.zyngier@arm.com)
  + [cc4eae9] [2018-06-26] irqchip/gic-v3-its: Use pre-programmed redistributor tables with kdump kernels (marc.zyngier@arm.com)
  + [33576f2] [2018-07-27] irqchip/gic-v3-its: Allow use of pre-programmed LPI tables (marc.zyngier@arm.com)
  + [68a3726] [2018-07-27] irqchip/gic-v3-its: Keep track of property table's PA and VA (marc.zyngier@arm.com)
  + [a8c3be8] [2018-07-27] irqchip/gic-v3-its: Move pending table allocation to init time (marc.zyngier@arm.com)
  + [3e15e2c] [2018-07-27] irqchip/gic-v3-its: Split property table clearing from allocation (marc.zyngier@arm.com)
  + [d3950de] [2018-07-17] irqchip/gic-v3-its: Simplify LPI_PENDBASE_SZ usage (marc.zyngier@arm.com)
  + [9fb44d4] [2018-07-27] irqchip/gic-v3-its: Change initialization ordering for LPIs (marc.zyngier@arm.com)
  + [703d0a9] [2018-03-21] irqchip/gic-v3: Ensure GICR_CTLR.EnableLPI=0 is observed before enabling (shankerd@codeaurora.org)
  + [c125f11] [2019-12-06] efi/memreserve: Register reservations as 'reserved' in /proc/iomem (ardb@kernel.org)
  + [3b187be] [2019-06-09] efi/memreserve: deal with memreserve entries in unmapped memory (ard.biesheuvel@linaro.org)
  + [6f1e642] [2018-11-29] efi: Reduce the amount of memblock reservations for persistent allocations (ard.biesheuvel@linaro.org)
  + [14e5029] [2018-11-29] efi: Permit multiple entries in persistent memreserve data structure (ard.biesheuvel@linaro.org)
  + [afb69bf] [2018-11-23] efi: Prevent GICv3 WARN() by mapping the memreserve table before first use (ard.biesheuvel@linaro.org)
  + [744c02d] [2018-11-14] efi: Permit calling efi_mem_reserve_persistent() from atomic context (ard.biesheuvel@linaro.org)
  + [401ce76] [2018-09-21] efi: add API to reserve memory persistently across kexec reboot (ard.biesheuvel@linaro.org)
  + [2a47c49] [2018-09-21] efi/arm: libstub: add a root memreserve config table (ard.biesheuvel@linaro.org)
  + [658a89a] [2018-09-21] efi: honour memory reservations passed via a linux specific config table (ard.biesheuvel@linaro.org)
  + [1489ab2] [2020-04-07] kernel/sched/fair.c: Fix divide by zero (sblbir@amazon.com)
  + [fbb6ae8] [2020-04-01] Revert "ena: update to 2.2.3" (yishache@amazon.com)
  + [7dd292c] [2020-03-08] lustre: update to AmazonFSxLustreClient v2.10.8-1 (astroh@amazon.com)
  + [587ce2f] [2020-01-29] random: introduce RANDOM_WAIT_JITTER config option (fllinden@amazon.com)
  + [17c8c0c] [2019-09-28] random: try to actively add entropy rather than passively wait for it (torvalds@linux-foundation.org)
  + [7d192e9] [2020-02-26] ena: update to 2.2.3 (fllinden@amazon.com)
  + [4e6ec2e] [2019-06-26] perf: arm_spe: Enable ACPI/Platform automatic module loading (jeremy.linton@arm.com)
  + [a76d8fd] [2019-06-26] arm_pmu: acpi: spe: Add initial MADT/SPE probing (jeremy.linton@arm.com)
  + [1f7007e] [2019-06-26] ACPI/PPTT: Add function to return ACPI 6.3 Identical tokens (jeremy.linton@arm.com)
  + [0f2f2ee] [2019-06-26] ACPI/PPTT: Modify node flag detection to find last IDENTICAL (jeremy.linton@arm.com)
  + [d2710e1] [2020-01-29] ACPICA: ACPI 6.3: PPTT add additional fields in Processor Structure Flags (erik.schmauss@intel.com)
  + [29ca3d5] [2020-01-28] ACPICA: ACPI 6.3: MADT: add support for statistical profiling in GICC (erik.schmauss@intel.com)
  + [68926d3] [2018-08-10] perf arm spe: Fix uninitialized record error variable (kim.phillips@arm.com)
  + [b4242e2] [2018-01-14] perf tools: Add ARM Statistical Profiling Extensions (SPE) support (kim.phillips@arm.com)
  + [9fcddbd] [2016-09-22] drivers/perf: Add support for ARMv8.2 Statistical Profiling Extension (will.deacon@arm.com)
  + [e0acb9f] [2016-09-22] dt-bindings: Document devicetree binding for ARM SPE (will.deacon@arm.com)
  + [b529256] [2017-07-07] arm64: head: Init PMSCR_EL2.{PA,PCT} when entered at EL2 without VHE (will.deacon@arm.com)
  + [c8fad27] [2017-09-20] arm64: sysreg: Move SPE registers and PSB into common header files (will.deacon@arm.com)
  + [e7f9cb6] [2016-09-23] perf/core: Add PERF_AUX_FLAG_COLLISION to report colliding samples (will.deacon@arm.com)
  + [65fcd1b] [2016-08-16] perf/core: Export AUX buffer helpers to modules (will.deacon@arm.com)
  + [72502a5] [2016-07-25] genirq: export irq_get_percpu_devid_partition to modules (will.deacon@arm.com)
  + [0875024] [2018-03-29] Don't log confusing message on reconnect by default (stfrench@microsoft.com)
  + [b32871e] [2018-03-21] Don't log expected error on DFS referral request (smfrench@gmail.com)
  + [dfe9ff4] [2017-11-21] CIFS: don't log STATUS_NOT_FOUND errors for DFS (aaptel@suse.com)
  + [bc70e6a] [2018-07-05] cifs: Fix slab-out-of-bounds in send_set_info() on SMB2 ACE setting (sbrivio@redhat.com)
  + [ef599b6] [2019-12-31] lib/list-test: add a test for the 'list' doubly linked list (davidgow@google.com)
  + [35edeee] [2019-09-08] Documentation: kunit: Fix verification command (sj38.park@gmail.com)
  + [c2f68fd] [2019-09-23] Documentation: kunit: add documentation for KUnit (brendanhiggins@google.com)
  + [011f001] [2019-09-07] kunit: Fix '--build_dir' option (sj38.park@gmail.com)
  + [47087f8] [2019-09-23] kunit: defconfig: add defconfigs for building KUnit tests (brendanhiggins@google.com)
  + [c3e85b6] [2019-09-23] kunit: tool: add Python wrappers for running KUnit tests (felixguoxiuping@gmail.com)
  + [fe4274d] [2019-09-23] kunit: fix failure to build without printk (brendanhiggins@google.com)
  + [55db339] [2019-09-23] kunit: test: add tests for KUnit managed resources (akndr41@gmail.com)
  + [2b12280] [2019-09-23] kunit: test: add the concept of assertions (brendanhiggins@google.com)
  + [d9ad584] [2019-09-23] kunit: test: add tests for kunit test abort (brendanhiggins@google.com)
  + [6cc2c73] [2019-09-23] kunit: test: add support for test abort (brendanhiggins@google.com)
  + [0c4ff43] [2019-09-23] kunit: test: add initial tests (brendanhiggins@google.com)
  + [7cb1707] [2019-12-31] lib: enable building KUnit in lib/ (brendanhiggins@google.com)
  + [529b0ec] [2019-09-23] kunit: test: add the concept of expectations (brendanhiggins@google.com)
  + [446c7f9] [2019-09-23] kunit: test: add assertion printing library (brendanhiggins@google.com)
  + [edaaf3f] [2019-09-23] kunit: test: add string_stream a std::stream like string builder (brendanhiggins@google.com)
  + [cc1e670] [2019-09-23] kunit: test: add test resource management API (brendanhiggins@google.com)
  + [bedc955] [2019-09-23] kunit: test: add KUnit test runner core (brendanhiggins@google.com)
  + [457c10a] [2020-02-03] Revert "update ENA linux driver to version 2.2.1" (anchalag@amazon.com)
  + [0aa7171] [2020-01-20] update ENA linux driver to version 2.2.1 (anchalag@amazon.com)
  + [d407856] [2019-12-18] Add support for setting owner info, dos attributes, and create time (bprotopopov@hotmail.com)
  + [0260201] [2018-08-28] SMB3: Backup intent flag missing from compounded ops (stfrench@microsoft.com)
  + [fe7e763] [2019-12-19] drivers/amazon: efa: update to 1.5.0 (luqia@amazon.com)
  + [fc30262] [2019-12-16] Revert "Fix the locking in dcache_readdir() and friends". (fllinden@amazon.com)
  + [0e3b139] [2019-12-04] lustre: hold lock while walking changelog dev list (astroh@amazon.com)
  + [b83b6bd] [2019-11-15] arm64: fix merge error in errata changes (fllinden@amazon.com)
  + [a1b387b] [2019-11-12] nvme-pci: use atomic bitops to mark a queue enabled (hch@lst.de)
  + [0014344] [2019-11-11] nvme-pci: Don't disable on timeout in reset state (keith.busch@intel.com)
  + [bfb0bfe] [2019-11-11] nvme-pci: Unblock reset_work on IO failure (keith.busch@intel.com)
  + [175a844] [2019-11-11] nvme-pci: shutdown on timeout during deletion (keith.busch@intel.com)
  + [df59830] [2018-02-08] nvme-pci: Fix timeouts in connecting state (keith.busch@intel.com)
  + [050829d] [2019-11-11] nvme: rename NVME_CTRL_RECONNECTING state to NVME_CTRL_CONNECTING (maxg@mellanox.com)
  + [d3d9f7e] [2017-10-25] nvme: allow controller RESETTING to RECONNECTING transition (jsmart2021@gmail.com)
  + [ad172c6] [2019-11-11] nvme-pci: introduce RECONNECTING state to mark initializing procedure (jianchao.w.wang@oracle.com)
  + [871fcc5] [2019-11-11] Revert "nvme/pci: Better support for disabling controller" (sblbir@amazon.com)
  + [f565e33] [2019-11-04] update ena driver to version 2.1.3 (alakeshh@amazon.com)
  + [deb9f00] [2018-06-22] arm64: Avoid flush_icache_range() in alternatives patching code (will.deacon@arm.com)
  + [bd8df3e] [2018-09-27] arm64: pull in upstream erratum workarounds (fllinden@amazon.com)
  + [d853311] [2018-03-13] arm64: kconfig: Ensure spinlock fastpaths are inlined if !PREEMPT (will.deacon@arm.com)
  + [d1fcb19] [2018-03-13] arm64: locking: Replace ticket lock implementation with qspinlock (will.deacon@arm.com)
  + [62f85a7] [2018-01-31] arm64: barrier: Implement smp_cond_load_relaxed (will.deacon@arm.com)
  + [5ffadf9] [2018-04-26] MAINTAINERS: Add myself as a co-maintainer for the locking subsystem (will.deacon@arm.com)
  + [6ca840d] [2018-04-26] locking/qspinlock: Use try_cmpxchg() instead of cmpxchg() when locking (will.deacon@arm.com)
  + [bb1ea1c] [2018-04-26] locking/qspinlock: Elide back-to-back RELEASE operations with smp_wmb() (will.deacon@arm.com)
  + [522b12b] [2018-04-26] locking/qspinlock: Use smp_store_release() in queued_spin_unlock() (will.deacon@arm.com)
  + [c059389] [2018-04-26] locking/qspinlock: Use smp_cond_load_relaxed() to wait for next node (will.deacon@arm.com)
  + [f731040] [2018-04-26] locking/mcs: Use smp_cond_load_acquire() in MCS spin loop (jason.low2@hp.com)
  + [4c84595] [2018-04-26] locking/qspinlock: Use atomic_cond_read_acquire() (will.deacon@arm.com)
  + [90d6875] [2018-04-26] locking/barriers: Introduce smp_cond_load_relaxed() and atomic_cond_read_relaxed() (will.deacon@arm.com)
  + [8620c1d] [2017-10-12] locking/atomic: Add atomic_cond_read_acquire() (will.deacon@arm.com)
  + [136b844] [2019-08-29] iommu: use config option to specify if iommu mode should be strict (fllinden@amazon.com)
  + [fab8ce0f] [2018-09-20] iommu/arm-smmu: Support non-strict mode (robin.murphy@arm.com)
  + [624e04c] [2018-09-20] iommu/io-pgtable-arm-v7s: Add support for non-strict mode (robin.murphy@arm.com)
  + [2d07d34] [2018-09-20] iommu/arm-smmu-v3: Add support for non-strict mode (thunder.leizhen@huawei.com)
  + [bb17e75] [2018-09-20] iommu/io-pgtable-arm: Add support for non-strict mode (thunder.leizhen@huawei.com)
  + [1b6eff8] [2018-09-20] iommu: Add "iommu.strict" command line option (thunder.leizhen@huawei.com)
  + [ddfa706] [2018-09-20] iommu/dma: Add support for non-strict mode (thunder.leizhen@huawei.com)
  + [e866055] [2018-09-20] iommu/arm-smmu-v3: Implement flush_iotlb_all hook (thunder.leizhen@huawei.com)
  + [27d6fb1] [2017-09-28] iommu/io-pgtable-arm-v7s: Convert to IOMMU API TLB sync (robin.murphy@arm.com)
  + [747b417] [2017-09-28] iommu/io-pgtable-arm: Convert to IOMMU API TLB sync (robin.murphy@arm.com)
  + [61abebd] [2019-03-12] irqchip/gic-v3-its: Fix comparison logic in lpi_range_cmp (linux@rasmusvillemoes.dk)
  + [0f52b46] [2019-01-29] irqchip/gic-v3-its: Gracefully fail on LPI exhaustion (marc.zyngier@arm.com)
  + [63c1170] [2018-08-28] irqchip/gic-v3-its: Cap lpi_id_bits to reduce memory footprint (jia.he@hxt-semitech.com)
  + [0a0facf] [2018-05-31] irqchip/gic-v3-its: Reduce minimum LPI allocation to 1 for PCI devices (marc.zyngier@arm.com)
  + [eafeffc] [2018-05-31] irqchip/gic-v3-its: Honor hypervisor enforced LPI range (marc.zyngier@arm.com)
  + [e5eb66d] [2018-05-30] irqchip/gic-v3: Expose GICD_TYPER in the rdist structure (marc.zyngier@arm.com)
  + [57b3626] [2018-05-27] irqchip/gic-v3-its: Drop chunk allocation compatibility (marc.zyngier@arm.com)
  + [cbce75c] [2018-05-27] irqchip/gic-v3-its: Move minimum LPI requirements to individual busses (marc.zyngier@arm.com)
  + [22e8569] [2018-05-27] irqchip/gic-v3-its: Use full range of LPIs (marc.zyngier@arm.com)
  + [e3f5a71] [2018-05-27] irqchip/gic-v3-its: Refactor LPI allocator (marc.zyngier@arm.com)
  + [3e17ea1] [2018-06-22] irqchip/gic-v3-its: Only emit VSYNC if targetting a valid collection (marc.zyngier@arm.com)
  + [e1cfea5] [2018-06-22] irqchip/gic-v3-its: Only emit SYNC if targetting a valid collection (marc.zyngier@arm.com)
  + [a88a5e0] [2017-07-28] irqchip/gic-v3-its: Pass its_node pointer to each command builder (marc.zyngier@arm.com)
  + [762b7d3] [2018-05-17] nvme-pci: move ->cq_vector == -1 check outside of ->q_lock (axboe@kernel.dk)
  + [1aa9c00] [2019-09-13] nvme/host/pci: Fix a race in controller removal (sblbir@amzn.com)
  + [b08ceff] [2019-09-13] nvme/host/core: Allow overriding of wait_ready timeout (sblbir@amzn.com)
  + [6c3b1e0] [2019-09-10] nvme/pci: Better support for disabling controller (sblbir@amzn.com)
  + [61ff698] [2017-11-02] nvme: move the dying queue check from cancel to completion (hch@lst.de)
  + [24f72ee] [2019-08-28] blk-mq: fix hang caused by freeze/unfreeze sequence (bob.liu@oracle.com)
  + [7bed381] [2019-08-16] nvme: change namespaces_mutext to namespaces_rwsem (jianchao.w.wang@oracle.com)
  + [559fd44] [2018-09-26] block: Allow unfreezing of a queue while requests are in progress (bvanassche@acm.org)
  + [3d3c1b8] [2019-08-16] percpu-refcount: Introduce percpu_ref_resurrect() (bvanassche@acm.org)
  + [35924bb] [2019-09-05] Add Amazon EFA driver version 1.4 (alakeshh@amazon.com)
  + [907a019] [2019-04-02] block: don't show io_timeout if driver has no timeout handler (zhangweiping@didiglobal.com)
  + [99c8539] [2018-11-29] block: add io timeout to sysfs (zhangweiping@didiglobal.com)
  + [59b3151] [2019-08-15] xen: Restore xen-pirqs on resume from hibernation (anchalag@amazon.com)
  + [fcca54e] [2019-01-09] livepatch: Change unsigned long old_addr -> void *old_func in struct klp_func (pmladek@suse.com)
  + [254edd0] [2018-11-07] livepatch: Replace synchronize_sched() with synchronize_rcu() (paulmck@linux.ibm.com)
  + [d36d5af] [2018-07-12] livepatch: Remove reliable stacktrace check in klp_try_switch_task() (kamalesh@linux.vnet.ibm.com)
  + [ae68957] [2018-04-16] livepatch: Allow to call a custom callback when freeing shadow variables (pmladek@suse.com)
  + [ae48af4] [2018-04-16] livepatch: Initialize shadow variables safely by a custom callback (pmladek@suse.com)
  + [8b6312c] [2017-12-21] livepatch: add locking to force and signal functions (mbenes@suse.cz)
  + [e03db4e] [2018-01-10] livepatch: Remove immediate feature (mbenes@suse.cz)
  + [5fabc02] [2017-11-22] livepatch: force transition to finish (mbenes@suse.cz)
  + [630a9a4] [2017-11-15] livepatch: send a fake signal to all blocking tasks (mbenes@suse.cz)
  + [d8edcc7] [2017-10-20] livepatch: __klp_disable_patch() should never be called for disabled patches (pmladek@suse.com)
  + [43f6ec1] [2017-10-20] livepatch: Correctly call klp_post_unpatch_callback() in error paths (pmladek@suse.com)
  + [f47c18f] [2017-10-13] livepatch: add transition notices (joe.lawrence@redhat.com)
  + [e9abf2a] [2017-10-13] livepatch: move transition "complete" notice into klp_complete_transition() (joe.lawrence@redhat.com)
  + [afa70df] [2017-10-13] livepatch: add (un)patch callbacks (joe.lawrence@redhat.com)
  + [4751042] [2017-09-14] livepatch: __klp_shadow_get_or_alloc() is local to shadow.c (jkosina@suse.cz)
  + [dad9e74] [2017-08-31] livepatch: introduce shadow variable API (joe.lawrence@redhat.com)
  + [a4726ae] [2019-08-15] Partially revert cc946adcb9e983ad9fe56ebe35f1292e111ff10e (sblbir@amzn.com)
  + [cd2f3fb] [2019-07-11] PCI: Add ACS quirk for Amazon Annapurna Labs root ports (alisaidi@amazon.com)
  + [8aa1e39] [2019-07-11] PCI: Add Amazon's Annapurna Labs vendor ID (jonnyc@amazon.com)
  + [451f028] [2019-06-24] linux/ena: update ENA linux driver to version 2.1.1 (fllinden@amazon.com)
  + [aa2c82d] [2019-07-02] microvm: enable debug in case of tcp out of memory (alakeshh@amazon.com)
  + [ba0a1ec] [2019-07-03] Fix microvm config dependency in Kconfig (alakeshh@amazon.com)
  + [e678d8a] [2019-02-12] NFS: Remove redundant semicolon (zhangliguang@linux.alibaba.com)
  + [15c487a] [2019-05-31] arm64: acpi/pci: invoke _DSM whether to preserve firmware PCI setup (fllinden@amazon.com)
  + [c059b6c] [2019-03-28] PCI: al: Add Amazon Annapurna Labs PCIe host controller driver (jonnyc@amazon.com)
  + [4f2d6e7] [2019-04-24] irqchip/gic-v2m: invoke from gic-v3 initialization and add acpi quirk flow (zeev@amazon.com)
  + [7c63cfa] [2019-04-03] lustre: fix ACL handling (fllinden@amazon.com)
  + [5b2545e] [2018-05-18] x86/stacktrace: Enable HAVE_RELIABLE_STACKTRACE for the ORC unwinder (jslaby@suse.cz)
  + [b61518f] [2018-05-18] x86/unwind/orc: Detect the end of the stack (jpoimboe@redhat.com)
  + [fd90ff7] [2018-05-18] x86/stacktrace: Do not fail for ORC with regs on stack (jslaby@suse.cz)
  + [fab2700] [2018-05-18] x86/stacktrace: Clarify the reliable success paths (jslaby@suse.cz)
  + [4e23f71] [2018-05-18] x86/stacktrace: Remove STACKTRACE_DUMP_ONCE (jslaby@suse.cz)
  + [9ae8895] [2018-05-18] x86/stacktrace: Do not unwind after user regs (jslaby@suse.cz)
  + [981f226] [2019-03-12] Add new config CONFIG_MICROVM to enable microvm optimized kernel (alakeshh@amazon.com)
  + [fd86549] [2019-02-19] tcp: Namespace-ify sysctl_tcp_rmem and sysctl_tcp_wmem (edumazet@google.com)
  + [4503898] [2017-11-07] net: allow per netns sysctl_rmem and sysctl_wmem for protos (edumazet@google.com)
  + [ce10d90] [2019-03-01] Config glue for lustre client. (fllinden@amazon.com)
  + [fa6dfcb] [2019-03-01] Import lustre client 2.10.5 (fllinden@amazon.com)
  + [bf3f27c] [2018-06-05] iomap: fsync swap files before iterating mappings (darrick.wong@oracle.com)
  + [d0898ab] [2018-06-01] iomap: inline data should be an iomap type, not a flag (hch@lst.de)
  + [2d2e771] [2018-05-16] iomap: don't allow holes in swapfiles (osandov@fb.com)
  + [9f947b9] [2018-05-16] iomap: provide more useful errors for invalid swap files (osandov@fb.com)
  + [5556ee1] [2018-05-10] iomap: add a swapfile activation function (darrick.wong@oracle.com)
  + [e503ac8] [2019-01-30] xfs, iomap: define and use the IOMAP_F_DIRTY flag in xfs (fllinden@amazon.com)
  + [8654022] [2018-08-01] xfs: only validate summary counts on primary superblock (darrick.wong@oracle.com)
  + [d785740] [2018-07-26] libxfs: add more bounds checking to sb sanity checks (billodo@redhat.com)
  + [99a96e5] [2018-07-29] xfs: refactor superblock verifiers (darrick.wong@oracle.com)
  + [3ad5dbc] [2019-01-31] xen-netfront: call netif_device_attach on resume (fllinden@amazon.com)
  + [242ea87] [2018-10-04] ACPI/PPTT: Handle architecturally unknown cache types (jhugo@codeaurora.org)
  + [f0bfc0c] [2018-06-05] ACPI / PPTT: fix build when CONFIG_ACPI_PPTT is not enabled (sudeep.holla@arm.com)
  + [929dfff] [2018-06-29] ACPI / PPTT: use ACPI ID whenever ACPI_PPTT_ACPI_PROCESSOR_ID_VALID is set (Sudeep.Holla@arm.com)
  + [af7071f] [2018-05-11] arm64: topology: divorce MC scheduling domain from core_siblings (jeremy.linton@arm.com)
  + [b4e8e11] [2018-05-11] ACPI: Add PPTT to injectable table list (jeremy.linton@arm.com)
  + [9e59f97] [2018-05-11] arm64: topology: enable ACPI/PPTT based CPU topology (jeremy.linton@arm.com)
  + [6079b3b] [2018-05-11] arm64: topology: rename cluster_id (jeremy.linton@arm.com)
  + [f57def6] [2018-05-11] arm64: Add support for ACPI based firmware tables (jeremy.linton@arm.com)
  + [e284e27] [2018-05-11] drivers: base cacheinfo: Add support for ACPI based firmware tables (jeremy.linton@arm.com)
  + [841e33a] [2018-05-11] ACPI: Enable PPTT support on ARM64 (jeremy.linton@arm.com)
  + [6eeb1ad] [2018-05-11] ACPI/PPTT: Add Processor Properties Topology Table parsing (jeremy.linton@arm.com)
  + [4331055] [2018-05-11] arm64/acpi: Create arch specific cpu to acpi id helper (jeremy.linton@arm.com)
  + [3db2106] [2018-05-11] cacheinfo: rename of_node to fw_token (jeremy.linton@arm.com)
  + [1a0cf0c] [2018-05-11] drivers: base: cacheinfo: setup DT cache properties early (jeremy.linton@arm.com)
  + [80dfe2c] [2018-05-11] drivers: base: cacheinfo: move cache_setup_of_node() (jeremy.linton@arm.com)
  + [c1537a0] [2017-11-17] ACPICA: ACPI 6.2: Additional PPTT flags (jeremy.linton@arm.com)
  + [d094777] [2018-07-23] arm64: acpi: fix alignment fault in accessing ACPI (takahiro.akashi@linaro.org)
  + [a323f6c] [2018-07-02] arm64: kexec: always reset to EL2 if present (mark.rutland@arm.com)
  + [0919298] [2018-03-08] efi/arm64: Check whether x18 is preserved by runtime services calls (ard.biesheuvel@linaro.org)
  + [ce58bdd] [2018-10-11] arm64: Fix /proc/iomem for reserved but not memory regions (will.deacon@arm.com)
  + [9c0b4dd] [2018-07-23] arm64: export memblock_reserve()d regions via /proc/iomem (james.morse@arm.com)
  + [f056d61] [2018-11-10] net: ena: Import the ENA v2 driver (2.0.2g) (alakeshh@amazon.com)
  + [6c7ba10] [2018-11-10] xen: Only restore the ACPI SCI interrupt in xen_restore_pirqs. (fllinden@amazon.com)
  + [efff305] [2018-10-26] xen: restore pirqs on resume from hibernation. (fllinden@amazon.com)
  + [2617da2] [2018-10-29] ACPICA: Enable sleep button on ACPI legacy wake (anchalag@amazon.com)
  + [354fc8e] [2018-10-18] block: xen-blkfront: consider new dom0 features on restore (eduval@amazon.com)
  + [fe49c77] [2017-11-30] vmxnet3: increase default rx ring sizes (skhare@vmware.com)
  + [62d16f4] [2018-04-27] x86/CPU/AMD: Derive CPU topology from CPUID function 0xB when available (suravee.suthikulpanit@amd.com)
  + [b003d07] [2017-09-07] sched/topology: Introduce NUMA identity node sched domain (suravee.suthikulpanit@amd.com)
  + [b906446] [2018-06-13] x86/CPU/AMD: Fix LLC ID bit-shift calculation (suravee.suthikulpanit@amd.com)
  + [f4fea16] [2018-04-27] x86/CPU/AMD: Calculate last level cache ID from number of sharing threads (suravee.suthikulpanit@amd.com)
  + [9eef55e] [2018-04-27] x86/CPU: Rename intel_cacheinfo.c to cacheinfo.c (bp@suse.de)
  + [5d555a8] [2018-05-17] x86/MCE/AMD: Read MCx_MISC block addresses on any CPU (bp@suse.de)
  + [ea79913] [2018-08-15] blk-wbt: Avoid lock contention and thundering herd issue in wbt_wait (anchalag@amazon.com)
  + [6e9c039] [2018-01-12] blk-mq: simplify queue mapping & schedule with each possisble CPU (hch@lst.de)
  + [da89adf] [2018-04-09] x86: tsc: avoid system instability in hibernation (eduval@amazon.com)
  + [263b8b27] [2018-06-05] xen-blkfront: Fixed blkfront_restore to remove a call to negotiate_mq (anchalag@amazon.com)
  + [c115864] [2018-03-24] KVM: X86: Fix setup the virt_spin_lock_key before static key get initialized (wanpengli@tencent.com)
  + [846e503] [2017-10-28] x86/paravirt: Set up the virt_spin_lock_key after static keys get initialized (douly.fnst@cn.fujitsu.com)
  + [57bb90c] [2018-02-13] KVM: X86: Choose qspinlock when dedicated physical CPUs are available (wanpengli@tencent.com)
  + [cb8f7ed2] [2018-02-13] KVM: Introduce paravirtualization hints and KVM_HINTS_DEDICATED (wanpengli@tencent.com)
  + [8d404e9] [2017-09-06] locking/paravirt: Use new static key for controlling call of virt_spin_lock() (jgross@suse.com)
  + [0eac561] [2018-03-27] Revert "xen: dont fiddle with event channel masking in suspend/resume" (anchalag@amazon.com)
  + [ec4540c] [2018-01-18] ACPI: SPCR: Make SPCR available to x86 (prarit@redhat.com)
  + [189857f] [2016-04-26] xen-blkfront: add 'persistent_grants' parameter (aliguori@amazon.com)
  + [3d3331a] [2017-03-10] xen-blkfront: resurrect request-based mode (kamatam@amazon.com)
  + [799722d] [2017-11-02] Not-for-upstream: PM / hibernate: Speed up hibernation by batching requests (cyberax@amazon.com)
  + [5052f90] [2017-10-27] PM / hibernate: update the resume offset on SNAPSHOT_SET_SWAP_AREA (cyberax@amazon.com)
  + [c1cdead] [2017-08-24] x86/xen: close event channels for PIRQs in system core suspend callback (kamatam@amazon.com)
  + [c33cc65] [2017-08-24] xen/events: add xen_shutdown_pirqs helper function (kamatam@amazon.com)
  + [3363e01] [2017-07-21] x86/xen: save and restore steal clock (kamatam@amazon.com)
  + [f434dd7] [2017-07-13] xen/time: introduce xen_{save,restore}_steal_clock (kamatam@amazon.com)
  + [cf90d13] [2017-01-09] xen-netfront: add callbacks for PM suspend and hibernation support (kamatam@amazon.com)
  + [54a3a09] [2017-06-08] xen-blkfront: add callbacks for PM suspend and hibernation (kamatam@amazon.com)
  + [0e96577] [2017-02-11] x86/xen: add system core suspend and resume callbacks (kamatam@amazon.com)
  + [0479afb] [2018-02-22] x86/xen: Introduce new function to map HYPERVISOR_shared_info on Resume (anchalag@amazon.com)
  + [0f5c87a] [2017-07-13] xenbus: add freeze/thaw/restore callbacks support (kamatam@amazon.com)
  + [67197f6] [2017-07-13] xen/manage: introduce helper function to know the on-going suspend mode (kamatam@amazon.com)
  + [27e8079] [2017-07-12] xen/manage: keep track of the on-going suspend mode (kamatam@amazon.com)
  + [72b2bd2] [2018-02-27] Importing Amazon ENA driver 1.5.0 into amazon-4.14.y/master. (vallish@amazon.com)
  + [98969f4] [2018-02-12] drivers/amazon: introduce AMAZON_ENA_ETHERNET (vallish@amazon.com)
  + [42dfb63] [2018-02-12] drivers/amazon: add network device drivers support (vallish@amazon.com)
  + [ac80923] [2018-02-12] drivers: introduce AMAZON_DRIVER_UPDATES (vallish@amazon.com)
  + [a3636c1] [2017-10-27] not-for-upstream: testmgr config changes to enable FIPS boot (alakeshh@amazon.com)
  + [e9cdd26] [2017-09-19] nvme: update timeout module parameter type (vallish@amazon.com)
  + [62e0f30] [2015-12-08] force perf to use /usr/bin/python instead of /usr/bin/python2 (kamatam@amazon.com)
  + [d2e272c] [2013-02-13] bump default tcp_wmem from 16KB to 20KB (gafton@amazon.com)
  + [a71dd3f] [2016-01-26] bump the default TTL to 255 (kamatam@amazon.com)
  + [ac2f321] [2012-02-10] scsi: sd_revalidate_disk prevent NULL ptr deref (kernel-team@fedoraproject.org)


