# NOTE: There are no ELF objects produced by the package, so no need
# for debuginfo.
%define debug_package %{nil}

%define _catalogue /etc/X11/fontpath.d

# FIXME: The _sysfontdir stuff doesn't work yet, so don't use it.  Once
# upstream fonts have a build time configureable output directory that is
# a sane mechanism, we can rethink this.
%define _x11fontdirprefix	%{_datadir}
# NOTE: Fonts strictly intended for X core fonts, should be installed
# into _x11fontdir.
%define _x11fontdir		%{_x11fontdirprefix}/X11/fonts
%define _type1_fontdir		%{_x11fontdir}
%define _otf_fontdir		%{_x11fontdir}
%define _ttf_fontdir		%{_x11fontdir}

# Configuration section
%define with_ethiopic_fonts	1
%if %{with_ethiopic_fonts}
%define ethiopic_fonts -a35
%else
%define ethiopic_fonts ""
%endif

Summary:	X.Org X11 fonts
Name:		xorg-x11-fonts
Version:	7.5
Release:	9%{?dist}
License:	MIT and Lucida and Public Domain
Group:		User Interface/X
URL:		http://www.x.org

BuildArch:	noarch

Source0:  ftp://ftp.x.org/pub/individual/font/encodings-1.0.3.tar.bz2
Source1:  ftp://ftp.x.org/pub/individual/font/font-alias-1.0.3.tar.bz2
Source10: ftp://ftp.x.org/pub/individual/font/font-adobe-100dpi-1.0.2.tar.bz2
Source11: ftp://ftp.x.org/pub/individual/font/font-adobe-75dpi-1.0.2.tar.bz2
Source12: ftp://ftp.x.org/pub/individual/font/font-adobe-utopia-100dpi-1.0.3.tar.bz2
Source13: ftp://ftp.x.org/pub/individual/font/font-adobe-utopia-75dpi-1.0.3.tar.bz2
Source14: ftp://ftp.x.org/pub/individual/font/font-adobe-utopia-type1-1.0.3.tar.bz2
Source15: ftp://ftp.x.org/pub/individual/font/font-arabic-misc-1.0.2.tar.bz2
Source16: ftp://ftp.x.org/pub/individual/font/font-bh-100dpi-1.0.2.tar.bz2
Source17: ftp://ftp.x.org/pub/individual/font/font-bh-75dpi-1.0.2.tar.bz2
Source18: ftp://ftp.x.org/pub/individual/font/font-bh-lucidatypewriter-100dpi-1.0.2.tar.bz2
Source19: ftp://ftp.x.org/pub/individual/font/font-bh-lucidatypewriter-75dpi-1.0.2.tar.bz2
# Luxi fonts are under a bad license.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=317641
# Source20: ftp://ftp.x.org/pub/individual/font/font-bh-ttf-1.0.0.tar.bz2
# Source21: ftp://ftp.x.org/pub/individual/font/font-bh-type1-1.0.0.tar.bz2
Source22: ftp://ftp.x.org/pub/individual/font/font-bitstream-100dpi-1.0.2.tar.bz2
Source23: ftp://ftp.x.org/pub/individual/font/font-bitstream-75dpi-1.0.2.tar.bz2
Source25: ftp://ftp.x.org/pub/individual/font/font-bitstream-type1-1.0.2.tar.bz2
Source26: ftp://ftp.x.org/pub/individual/font/font-cronyx-cyrillic-1.0.2.tar.bz2
Source27: ftp://ftp.x.org/pub/individual/font/font-cursor-misc-1.0.2.tar.bz2
Source28: ftp://ftp.x.org/pub/individual/font/font-daewoo-misc-1.0.2.tar.bz2
Source29: ftp://ftp.x.org/pub/individual/font/font-dec-misc-1.0.2.tar.bz2
# Source30: ftp://ftp.x.org/pub/individual/font/font-ibm-type1-1.0.0.tar.bz2
Source31: ftp://ftp.x.org/pub/individual/font/font-isas-misc-1.0.2.tar.bz2
Source32: ftp://ftp.x.org/pub/individual/font/font-jis-misc-1.0.2.tar.bz2
Source33: ftp://ftp.x.org/pub/individual/font/font-micro-misc-1.0.2.tar.bz2
Source34: ftp://ftp.x.org/pub/individual/font/font-misc-cyrillic-1.0.2.tar.bz2
%if %{with_ethiopic_fonts}
Source35: ftp://ftp.x.org/pub/individual/font/font-misc-ethiopic-1.0.2.tar.bz2
%endif
# Source36: ftp://ftp.x.org/pub/individual/font/font-misc-meltho-1.0.0.tar.bz2
Source37: ftp://ftp.x.org/pub/individual/font/font-misc-misc-1.1.1.tar.bz2
Source38: ftp://ftp.x.org/pub/individual/font/font-mutt-misc-1.0.2.tar.bz2
Source39: ftp://ftp.x.org/pub/individual/font/font-schumacher-misc-1.1.1.tar.bz2
Source40: ftp://ftp.x.org/pub/individual/font/font-screen-cyrillic-1.0.3.tar.bz2
Source41: ftp://ftp.x.org/pub/individual/font/font-sony-misc-1.0.2.tar.bz2
Source42: ftp://ftp.x.org/pub/individual/font/font-sun-misc-1.0.2.tar.bz2
Source43: ftp://ftp.x.org/pub/individual/font/font-winitzki-cyrillic-1.0.2.tar.bz2
Source44: ftp://ftp.x.org/pub/individual/font/font-xfree86-type1-1.0.3.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-font-utils >= 7.5-3
# FIXME: fontconfig is needed only because the upstream Makefiles invoke
# fc-cache at build time.  This is totally useless, because we do not ship
# any of the resulting cache files, we generate them at install time from the
# rpm scripts.  However, it is easier to depend on fontconfig here than it is
# to patch all 40+ tarballs to stop running fc-cache.
BuildRequires: fontconfig
BuildRequires: autoconf automake libtool

BuildRequires: ucs2any, bdftruncate, bdftopcf

Conflicts: xorg-x11-server-Xorg < 1.3.0.0-10
Conflicts: xorg-x11-server-Xnest < 1.3.0.0-10
Conflicts: xorg-x11-server-Xdmx < 1.3.0.0-10
Conflicts: xorg-x11-server-Xvfb < 1.3.0.0-10
Conflicts: xorg-x11-server-Xephyr < 1.3.0.0-10
Conflicts: xorg-x11-xfs < 1.0.4-1

%description
X.Org X Window System fonts

%package misc
Summary: misc bitmap fonts for the X Window System
Group: User Interface/X
Requires(post): mkfontdir, fontconfig
Requires(postun): mkfontdir, fontconfig
Obsoletes: XFree86-base-fonts
Obsoletes: xorg-x11-base-fonts
Obsoletes: fonts-xorg-base
Obsoletes: xorg-x11-fonts-base
Provides: xorg-x11-fonts-base

%description misc
This package contains misc bitmap Chinese, Japanese, Korean, Indic, and Arabic
fonts for use with X Window System.
#--------------------------------------------------------------------------
%package Type1
Summary: Type1 fonts provided by the X Window System
Group: User Interface/X
Requires(post): mkfontdir, fontconfig, ttmkfdir
Requires(postun): mkfontdir, fontconfig, ttmkfdir
Obsoletes: XFree86-base-fonts
Obsoletes: xorg-x11-base-fonts
Obsoletes: fonts-xorg-base

%description Type1
A collection of Type1 fonts which are part of the core X Window System
distribution.
#--------------------------------------------------------------------------
%if %{with_ethiopic_fonts}
%package ethiopic
Summary: Ethiopic fonts
Group: User Interface/X
Requires(post): mkfontdir, ttmkfdir, mkfontscale, fontconfig
Requires(postun): mkfontdir, ttmkfdir, mkfontscale, fontconfig

%description ethiopic
Ethiopic fonts which are part of the core X Window System distribution.
%endif
#--------------------------------------------------------------------------
%package 75dpi
Summary: A set of 75dpi resolution fonts for the X Window System.
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-75dpi-fonts
Obsoletes: xorg-x11-75dpi-fonts
Obsoletes: fonts-xorg-75dpi

%description 75dpi
A set of 75 dpi fonts used by the X window system.
#--------------------------------------------------------------------------
%package 100dpi
Summary: A set of 100dpi resolution fonts for the X Window System.
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-100dpi-fonts
Obsoletes: xorg-x11-100dpi-fonts
Obsoletes: fonts-xorg-100dpi

%description 100dpi
A set of 100 dpi fonts used by the X window system.
#--------------------------------------------------------------------------
%package ISO8859-1-75dpi
Summary: A set of 75dpi ISO-8859-1 fonts for X.
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-75dpi-fonts
Obsoletes: xorg-x11-75dpi-fonts
# The ISO8859-1 fonts used to be coupled with the UCS fonts.
Obsoletes: fonts-xorg-75dpi
Conflicts: fonts-xorg-75dpi

%description ISO8859-1-75dpi
Contains a set of 75dpi fonts for ISO-8859-1.
#--------------------------------------------------------------------------
%package ISO8859-1-100dpi
Summary: A set of 100dpi ISO-8859-1 fonts for X.
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-100dpi-fonts
Obsoletes: xorg-x11-100dpi-fonts
# The ISO8859-1 fonts used to be coupled with the UCS fonts.
Obsoletes: fonts-xorg-100dpi
Conflicts: fonts-xorg-100dpi

%description ISO8859-1-100dpi
Contains a set of 100dpi fonts for ISO-8859-1.
#--------------------------------------------------------------------------
%package ISO8859-2-75dpi
Summary: A set of 75dpi Central European language fonts for X.
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-ISO8859-2-75dpi-fonts
Obsoletes: xorg-x11-ISO8859-2-75dpi-fonts
Obsoletes: fonts-xorg-ISO8859-2-75dpi

%description ISO8859-2-75dpi
Contains a set of 75dpi fonts for Central European languages.
#--------------------------------------------------------------------------
%package ISO8859-2-100dpi
Summary: A set of 100dpi Central European language fonts for X.
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-ISO8859-2-100dpi-fonts
Obsoletes: xorg-x11-ISO8859-2-100dpi-fonts
Obsoletes: fonts-xorg-ISO8859-2-100dpi

%description ISO8859-2-100dpi
Contains a set of 100dpi fonts for Central European languages.
#--------------------------------------------------------------------------
%package ISO8859-9-75dpi
Summary: ISO8859-9-75dpi fonts
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-ISO8859-9-75dpi-fonts
Obsoletes: xorg-x11-ISO8859-9-75dpi-fonts
Obsoletes: fonts-xorg-ISO8859-9-75dpi

%description ISO8859-9-75dpi
Contains a set of 75dpi fonts for the Turkish language.
#--------------------------------------------------------------------------
%package ISO8859-9-100dpi
Summary: ISO8859-9-100dpi fonts
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-ISO8859-9-100dpi-fonts
Obsoletes: xorg-x11-ISO8859-9-100dpi-fonts
Obsoletes: fonts-xorg-ISO8859-9-100dpi

%description ISO8859-9-100dpi
Contains a set of 100dpi fonts for the Turkish language.
#--------------------------------------------------------------------------
%package ISO8859-14-75dpi
Summary: ISO8859-14-75dpi fonts
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-ISO8859-14-75dpi-fonts
Obsoletes: xorg-x11-ISO8859-14-75dpi-fonts
Obsoletes: fonts-xorg-ISO8859-14-75dpi

%description ISO8859-14-75dpi
Contains a set of 75dpi fonts in the ISO8859-14 encoding which
provide Welsh support.
#--------------------------------------------------------------------------
%package ISO8859-14-100dpi
Summary: ISO8859-14-100dpi fonts
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-ISO8859-14-100dpi-fonts
Obsoletes: xorg-x11-ISO8859-14-100dpi-fonts
Obsoletes: fonts-xorg-ISO8859-14-100dpi

%description ISO8859-14-100dpi
Contains a set of 100dpi fonts in the ISO8859-14 encoding which
provide Welsh support.
#--------------------------------------------------------------------------
%package ISO8859-15-75dpi
Summary: ISO8859-15-75dpi fonts
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-ISO8859-15-75dpi-fonts
Obsoletes: xorg-x11-ISO8859-15-75dpi-fonts
Obsoletes: fonts-xorg-ISO8859-15-75dpi

%description ISO8859-15-75dpi
Contains a set of 75dpi fonts in the ISO8859-15 encoding which
provide Euro support.
#--------------------------------------------------------------------------
%package ISO8859-15-100dpi
Summary: ISO8859-15-100dpi fonts
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-ISO8859-15-100dpi-fonts
Obsoletes: xorg-x11-ISO8859-15-100dpi-fonts
Obsoletes: fonts-xorg-ISO8859-15-100dpi

%description ISO8859-15-100dpi
Contains a set of 100dpi fonts in the ISO8859-15 encoding which
provide Euro support.
#--------------------------------------------------------------------------
%package cyrillic
Summary: Cyrillic fonts for X.
Group: User Interface/X
Requires(post): mkfontdir
Requires(postun): mkfontdir
Obsoletes: XFree86-cyrillic-fonts
Obsoletes: xorg-x11-cyrillic-fonts
Obsoletes: fonts-xorg-cyrillic

%description cyrillic
Contains a set of Cyrillic fonts.
#--------------------------------------------------------------------------
%prep
%define setup_fonts_misc	-a15 -a27 -a28 -a29 -a31 -a32 -a33 -a37 -a38 -a39 -a41 -a42
%define setup_fonts_100dpi	-a10 -a12 -a16 -a18 -a22
%define setup_fonts_75dpi	-a11 -a13 -a17 -a19 -a23
%define setup_fonts_cyrillic	-a26 -a34 -a40 -a43
%define setup_fonts_type1	-a14 -a25 -a44
%define setup_fonts_otf		%{ethiopic_fonts}

%define setup_fonts_bitmap	%{setup_fonts_misc} %{setup_fonts_100dpi} %{setup_fonts_75dpi} %{setup_fonts_cyrillic}
%define setup_fonts_scaleable	%{setup_fonts_type1} %{setup_fonts_otf}

%define setup_font_metadata	-a1

%setup -q -c %{name}-%{version} %{setup_font_metadata} %{setup_fonts_bitmap} %{setup_fonts_scaleable}


#--------------------------------------------------------------------------
%build
pushd encodings-*
autoreconf -vif
%configure --with-fontrootdir=%{_x11fontdir}
make
popd

for dir in font-*; do
    pushd $dir
    # FIXME: do any fonts actually support the ISO8559 configure flags?
    autoreconf -vif
    %configure --with-fontrootdir=%{_x11fontdir} \
	--disable-iso8859-3 --disable-iso8859-4 --disable-iso8859-6 \
	--disable-iso8859-10 --disable-iso8859-11 --disable-iso8859-12 \
	--disable-iso8859-13 --disable-iso8859-16
    make
    popd
done

#--------------------------------------------------------------------------
%install
rm -rf $RPM_BUILD_ROOT

for dir in *; do
    make -C $dir install DESTDIR=$RPM_BUILD_ROOT
done

# Install catalogue symlinks
mkdir -p $RPM_BUILD_ROOT%{_catalogue}
for f in misc:unscaled:pri=10 75dpi:unscaled:pri=20 100dpi:unscaled:pri=30 Type1 TTF OTF cyrillic; do
    ln -fs %{_x11fontdir}/${f%%%%:*} $RPM_BUILD_ROOT%{_catalogue}/xorg-x11-fonts-$f
done

# Create fake %ghost files for file manifests.
{
    # Make ghost fonts.alias, fonts.dir, encodings.dir files
    FONTDIR=$RPM_BUILD_ROOT%{_x11fontdir}
    # Create fake %ghost fonts.alias
    for subdir in TTF OTF ; do
        touch $FONTDIR/$subdir/fonts.{alias,scale}
        chmod 0644 $FONTDIR/$subdir/fonts.{alias,scale}
    done
    # Create fake %ghost encodings.dir, fonts.dir, fonts.scale, fonts.cache-*
    for subdir in Type1 TTF OTF 100dpi 75dpi cyrillic misc ; do
        rm -f $FONTDIR/$subdir/{encodings,fonts}.dir
        touch $FONTDIR/$subdir/{encodings,fonts}.dir
        chmod 0644 $FONTDIR/$subdir/{encodings,fonts}.dir
        touch $FONTDIR/$subdir/fonts.scale
        chmod 0644 $FONTDIR/$subdir/fonts.scale

        # Create bogus fonts.cache-* files
        # Create somewhat future-proofed ghosted fonts.cache-* files so that
        # the font packages own these files.
        for fcver in $(seq 1 9) ; do
            touch $FONTDIR/$subdir/fonts.cache-$fcver
            chmod 0644 $FONTDIR/$subdir/fonts.cache-$fcver
        done
    done
}

#--------------------------------------------------------------------------
# xorg-x11-fonts-update-dirs is provided by xorg-x11-font-utils to
# deduplicate stuff run in %post

%post misc
{
# Only run fc-cache in the Type1 dir, gzipped pcf's take forever
  xorg-x11-fonts-update-dirs --skip-fontscale %{_x11fontdir}/misc
}

%postun misc
{
  # Rebuild fonts.dir when uninstalling package. (exclude the local, CID dirs)
  if [ "$1" = "0" -a -d %{_x11fontdir}/misc ]; then
    xorg-x11-fonts-update-dirs --skip-fontscale %{_x11fontdir}/misc
  fi
}

%post Type1
{
  xorg-x11-fonts-update-dirs %{_x11fontdir}/Type1
} 

%postun Type1
{
  FONTDIR=%{_type1_fontdir}/Type1
  if [ "$1" = "0" -a -d $FONTDIR ]; then
    xorg-x11-fonts-update-dirs $FONTDIR
  fi
}

%if %{with_ethiopic_fonts}
%post ethiopic
{
  xorg-x11-fonts-update-dirs --skip-fontscale --need-ttmkfdir %{_ttf_fontdir}/TTF
  xorg-x11-fonts-update-dirs %{_ttf_fontdir}/OTF
}

%postun ethiopic
{
  FONTDIR=%{_ttf_fontdir}/TTF
  if [ "$1" = "0" -a -d $FONTDIR ]; then
    xorg-x11-fonts-update-dirs --skip-fontscale --need-ttmkfdir $FONTDIR
  fi
  FONTDIR=%{_otf_fontdir}/OTF
  if [ "$1" = "0" -a -d $FONTDIR ]; then
    xorg-x11-fonts-update-dirs $FONTDIR
  fi
}
%endif

%post 75dpi
mkfontdir %{_x11fontdir}/75dpi

%post 100dpi
mkfontdir %{_x11fontdir}/100dpi

%post ISO8859-1-75dpi
mkfontdir %{_x11fontdir}/75dpi

%post ISO8859-1-100dpi
mkfontdir %{_x11fontdir}/100dpi

%post ISO8859-2-75dpi
mkfontdir %{_x11fontdir}/75dpi

%post ISO8859-2-100dpi
mkfontdir %{_x11fontdir}/100dpi

%post ISO8859-9-75dpi
mkfontdir %{_x11fontdir}/75dpi

%post ISO8859-9-100dpi
mkfontdir %{_x11fontdir}/100dpi

%post ISO8859-14-75dpi
mkfontdir %{_x11fontdir}/75dpi

%post ISO8859-14-100dpi
mkfontdir %{_x11fontdir}/100dpi

%post ISO8859-15-75dpi
mkfontdir %{_x11fontdir}/75dpi

%post ISO8859-15-100dpi
mkfontdir %{_x11fontdir}/100dpi

%post cyrillic
mkfontdir %{_x11fontdir}/cyrillic

%postun 75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun 100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun ISO8859-1-75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun ISO8859-1-100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun ISO8859-2-75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun ISO8859-2-100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi  ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun ISO8859-9-75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun ISO8859-9-100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi  ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun ISO8859-14-75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun ISO8859-14-100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi  ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun ISO8859-15-75dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/75dpi ]; then
    mkfontdir %{_x11fontdir}/75dpi
  fi
}

%postun ISO8859-15-100dpi
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/100dpi  ]; then
    mkfontdir %{_x11fontdir}/100dpi
  fi
}

%postun cyrillic
{
  if [ "$1" = "0" -a -d %{_x11fontdir}/cyrillic ]; then
    mkfontdir %{_x11fontdir}/cyrillic
  fi
}

#--------------------------------------------------------------------------
%check

#--------------------------------------------------------------------------
%clean
rm -rf $RPM_BUILD_ROOT
#--------------------------------------------------------------------------
%files misc
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-misc:unscaled:pri=10
%dir %{_x11fontdir}/misc
%{_x11fontdir}/misc/*
%dir %{_datadir}/X11/fonts/encodings
%dir %{_datadir}/X11/fonts/encodings/large
%{_datadir}/X11/fonts/encodings/*.enc.gz
%ghost %verify(not md5 size mtime) %{_datadir}/X11/fonts/encodings/encodings.dir
%{_datadir}/X11/fonts/encodings/large/*.enc.gz
%ghost %verify(not md5 size mtime) %{_datadir}/X11/fonts/encodings/large/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.alias
#%ghost %attr(644,root,root) %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.cache-*

%if %{with_ethiopic_fonts}
%files ethiopic
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-TTF
%{_catalogue}/xorg-x11-fonts-OTF
# TTF fonts
%dir %{_x11fontdir}/TTF
# font-misc-ethiopic
%{_x11fontdir}/TTF/GohaTibebZemen.ttf
%ghost %verify(not md5 size mtime) %{_x11fontdir}/TTF/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/TTF/fonts.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/TTF/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/TTF/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/TTF/fonts.cache-*
# OTF fonts
%dir %{_x11fontdir}/OTF
%{_x11fontdir}/OTF/GohaTibebZemen.otf
%ghost %verify(not md5 size mtime) %{_x11fontdir}/OTF/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/OTF/fonts.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/OTF/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/OTF/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/OTF/fonts.cache-*
%endif

%files 75dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??.pcf*
%{_x11fontdir}/75dpi/courBO??.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??.pcf*
%{_x11fontdir}/75dpi/helvBO??.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??.pcf*
%{_x11fontdir}/75dpi/ncenBI??.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??.pcf*
%{_x11fontdir}/75dpi/timBI??.pcf*
%{_x11fontdir}/75dpi/symb??.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??.pcf*
%{_x11fontdir}/75dpi/UTRG__??.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??.pcf*
%{_x11fontdir}/75dpi/lubBI??.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??.pcf*
# font-bitstream-75dpi
%{_x11fontdir}/75dpi/char[BIR]??.pcf*
%{_x11fontdir}/75dpi/charBI??.pcf*
%{_x11fontdir}/75dpi/tech14.pcf*
%{_x11fontdir}/75dpi/techB14.pcf*
%{_x11fontdir}/75dpi/term14.pcf*
%{_x11fontdir}/75dpi/termB14.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files 100dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??.pcf*
%{_x11fontdir}/100dpi/courBO??.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??.pcf*
%{_x11fontdir}/100dpi/helvBO??.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??.pcf*
%{_x11fontdir}/100dpi/ncenBI??.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??.pcf*
%{_x11fontdir}/100dpi/timBI??.pcf*
%{_x11fontdir}/100dpi/symb??.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??.pcf*
%{_x11fontdir}/100dpi/UTRG__??.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??.pcf*
%{_x11fontdir}/100dpi/lubBI??.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??.pcf*
# font-bitstream-100dpi
%{_x11fontdir}/100dpi/char[BIR]??.pcf*
%{_x11fontdir}/100dpi/charBI??.pcf*
%{_x11fontdir}/100dpi/tech14.pcf*
%{_x11fontdir}/100dpi/techB14.pcf*
%{_x11fontdir}/100dpi/term14.pcf*
%{_x11fontdir}/100dpi/termB14.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files ISO8859-1-75dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/courBO??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/helvBO??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/ncenBI??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/timBI??-ISO8859-1.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/UTRG__??-ISO8859-1.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/75dpi/lubBI??-ISO8859-1.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??-ISO8859-1.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files ISO8859-1-100dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/courBO??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/helvBO??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/ncenBI??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/timBI??-ISO8859-1.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/UTRG__??-ISO8859-1.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??-ISO8859-1.pcf*
%{_x11fontdir}/100dpi/lubBI??-ISO8859-1.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??-ISO8859-1.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files ISO8859-2-75dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/courBO??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/helvBO??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/ncenBI??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/timBI??-ISO8859-2.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/UTRG__??-ISO8859-2.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/75dpi/lubBI??-ISO8859-2.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??-ISO8859-2.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files ISO8859-2-100dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/courBO??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/helvBO??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/ncenBI??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/timBI??-ISO8859-2.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/UTRG__??-ISO8859-2.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??-ISO8859-2.pcf*
%{_x11fontdir}/100dpi/lubBI??-ISO8859-2.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??-ISO8859-2.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files ISO8859-9-75dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/courBO??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/helvBO??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/ncenBI??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/timBI??-ISO8859-9.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/UTRG__??-ISO8859-9.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/75dpi/lubBI??-ISO8859-9.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??-ISO8859-9.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files ISO8859-9-100dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/courBO??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/helvBO??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/ncenBI??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/timBI??-ISO8859-9.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/UTRG__??-ISO8859-9.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??-ISO8859-9.pcf*
%{_x11fontdir}/100dpi/lubBI??-ISO8859-9.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??-ISO8859-9.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files ISO8859-14-75dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/courBO??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/helvBO??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/ncenBI??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/timBI??-ISO8859-14.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/UTRG__??-ISO8859-14.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/75dpi/lubBI??-ISO8859-14.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??-ISO8859-14.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files ISO8859-14-100dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/courBO??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/helvBO??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/ncenBI??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/timBI??-ISO8859-14.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/UTRG__??-ISO8859-14.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??-ISO8859-14.pcf*
%{_x11fontdir}/100dpi/lubBI??-ISO8859-14.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??-ISO8859-14.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files ISO8859-15-75dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-75dpi:unscaled:pri=20
%dir %{_x11fontdir}/75dpi
# font-adobe-75dpi
%{_x11fontdir}/75dpi/cour[BOR]??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/courBO??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/helv[BOR]??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/helvBO??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/ncen[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/ncenBI??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/tim[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/timBI??-ISO8859-15.pcf*
# font-adobe-utopia-75dpi
%{_x11fontdir}/75dpi/UTBI__??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/UT[BI]___??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/UTRG__??-ISO8859-15.pcf*
# font-bh-75dpi
%{_x11fontdir}/75dpi/luBIS??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/lu[BIR]S??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/lub[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/75dpi/lubBI??-ISO8859-15.pcf*
# font-bh-lucidatypewriter-75dpi
%{_x11fontdir}/75dpi/lut[BR]S??-ISO8859-15.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/75dpi/fonts.cache-*

%files ISO8859-15-100dpi
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-100dpi:unscaled:pri=30
%dir %{_x11fontdir}/100dpi
# font-adobe-100dpi
%{_x11fontdir}/100dpi/cour[BOR]??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/courBO??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/helv[BOR]??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/helvBO??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/ncen[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/ncenBI??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/tim[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/timBI??-ISO8859-15.pcf*
# font-adobe-utopia-100dpi
%{_x11fontdir}/100dpi/UTBI__??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/UT[BI]___??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/UTRG__??-ISO8859-15.pcf*
# font-bh-100dpi
%{_x11fontdir}/100dpi/luBIS??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/lu[BIR]S??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/lub[BIR]??-ISO8859-15.pcf*
%{_x11fontdir}/100dpi/lubBI??-ISO8859-15.pcf*
# font-bh-lucidatypewriter-100dpi
%{_x11fontdir}/100dpi/lut[BR]S??-ISO8859-15.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/100dpi/fonts.cache-*

%files Type1
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-Type1
%dir %{_x11fontdir}/Type1
# font-adobe-utopia-type1
%{_x11fontdir}/Type1/UT??____.[ap]f[ma]
# font-bitstream-type1
%{_x11fontdir}/Type1/c0???bt_.[ap]f[mb]
# font-ibm-type1
# Pulled for licensing reasons (see bz 317641)
# %{_x11fontdir}/Type1/cour*.afm
# %{_x11fontdir}/Type1/cour*.pfa
#font-xfree86-type1
%{_x11fontdir}/Type1/cursor.pfa
%ghost %verify(not md5 size mtime) %{_x11fontdir}/Type1/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/Type1/fonts.dir
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/Type1/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/Type1/fonts.scale
#%ghost %verify(not md5 size mtime) %{_x11fontdir}/Type1/fonts.cache
%ghost %verify(not md5 size mtime) %{_x11fontdir}/Type1/fonts.cache-*

%files cyrillic
%defattr(-,root,root,-)
%{_catalogue}/xorg-x11-fonts-cyrillic
%dir %{_x11fontdir}/cyrillic
# font-cronyx-cyrillic
%{_x11fontdir}/cyrillic/crox[1-6]*.pcf*
%{_x11fontdir}/cyrillic/koi10x16b.pcf*
%{_x11fontdir}/cyrillic/koi10x20.pcf*
%{_x11fontdir}/cyrillic/koi6x10.pcf*
%{_x11fontdir}/cyrillic/koinil2.pcf*
# font-misc-cyrillic
%{_x11fontdir}/cyrillic/koi12x24*.pcf*
%{_x11fontdir}/cyrillic/koi6x13.pcf*
%{_x11fontdir}/cyrillic/koi6x13b.pcf*
%{_x11fontdir}/cyrillic/koi6x9.pcf*
%{_x11fontdir}/cyrillic/koi[5789]x*.pcf*
# font-screen-cyrillic
%{_x11fontdir}/cyrillic/screen8x16*.pcf*
# font-winitzki-cyrillic
%{_x11fontdir}/cyrillic/proof9x16.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/cyrillic/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/cyrillic/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/cyrillic/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/cyrillic/fonts.scale
%ghost %verify(not md5 size mtime) %{_x11fontdir}/cyrillic/fonts.cache-*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 7.5-9
- Mass rebuild 2013-12-27

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 7.5-8
- autoreconf for aarch64

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 28 2011 Matěj Cepl <mcepl@redhat.com> - 7.5-4
- Fix call of xorg-x11-fonts-update-dirs (#726267)

* Fri Nov 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-3
- Rely on a script provided in xorg-x11-font-utils for mkfontscale and
  friends (#634039)

* Fri Nov 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-2
- This time with tarballs

* Fri Nov 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.5-1
- Update fonts to latest upstream releases

* Tue Jun 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 7.2-11
- Require xorg-x11-font-utils >= 7.2-11 for font-utils 1.1.0
- Fix bashism in spec file (&>)
- Remove perl hack for DEFAULT_FONTS_DIR, fixed upstream 
- Remove perl and autoconf requirement.
- Create %ghost files {misc|705dpi|...}/fonts.scale.
- Drop fontdir alias patches
- Update a few fonts (well, all of them)
    - encodings-1.0.3
    - font-adobe-100dpi-1.0.1
    - font-adobe-75dpi-1.0.1
    - font-adobe-utopia-100dpi-1.0.2
    - font-adobe-utopia-75dpi-1.0.2
    - font-adobe-utopia-type1-1.0.2
    - font-alias-1.0.2
    - font-arabic-misc-1.0.1
    - font-bh-100dpi-1.0.1
    - font-bh-75dpi-1.0.1
    - font-bh-lucidatypewriter-100dpi-1.0.1
    - font-bh-lucidatypewriter-75dpi-1.0.1
    - font-bitstream-100dpi-1.0.1
    - font-bitstream-75dpi-1.0.1
    - font-bitstream-type1-1.0.1
    - font-cronyx-cyrillic-1.0.1
    - font-cursor-misc-1.0.1
    - font-daewoo-misc-1.0.1
    - font-dec-misc-1.0.1
    - font-isas-misc-1.0.1
    - font-jis-misc-1.0.1
    - font-micro-misc-1.0.1
    - font-misc-cyrillic-1.0.1
    - font-misc-ethiopic-1.0.1
    - font-misc-misc-1.1.0
    - font-mutt-misc-1.0.1
    - font-schumacher-misc-1.1.0
    - font-screen-cyrillic-1.0.2
    - font-sony-misc-1.0.1
    - font-sun-misc-1.0.1
    - font-winitzki-cyrillic-1.0.1
    - font-xfree86-type1-1.0.2

* Fri Mar 05 2010 Matěj Cepl <mcepl@redhat.com> - 7.2-10
- Fixed bad directory ownership of /etc//X11/fontpath.d

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Adam Jackson <ajax@redhat.com> 7.2-8
- Yet another rebuild attempt.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 7.2-6
- IBM refused to relicense ibm-type1 fonts with permission to modify,
  so they were dropped (bugzilla 317641)
- Meltho Syrian fonts (misc-meltho) have a bad license, upstream did not
  respond to request for relicensing, so they were dropped. This also
  means that the -syriac subpackage has been removed. (bugzilla 317641)

* Tue Dec 18 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 7.2-5
- Remove bh-ttf and bh-type1 (Luxi fonts) and truetype subpackage, due to 
  licensing issues (#317641)
- Correct license tag

* Mon Nov 19 2007 Kristian Høgsberg <krh@redhat.com> - 7.2-4
- Quote percentage signs in symlinking bash-magic (#390171).

* Mon Aug 27 2007 Adam Jackson <ajax@redhat.com> 7.2-3
- Fix build for F8, don't leave references to RPM_BUILD_ROOT in the
  encodings output. (#251058)

* Fri Jul 06 2007 Florian La Roche <laroche@redhat.com> - 7.2-2
- add fontconfig dep foer misc post/postun

* Fri Jun 22 2007 Kristian Høgsberg <krh@redhat.com> - 7.2-1
- Use the new catalogue font install mechanism, drop all chkfontpath dependencies.
- Unsplit base and misc subpackages, we don't require any base fonts
  now that we have built-ins.

* Fri Dec 8 2006 Adam Jackson <ajax@redhat.com> 7.1-3
- Create encodings.dir containing entries for both
  %{_datadir}/X11/fonts/encodings and
  %{_datadir}/X11/fonts/encodings/large (#209102).

* Thu Aug 31 2006 Kristian Høgsberg <krh@redhat.com> 7.1-2
- Fix postun scripts to only run if the directory is still there (#197208).

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 7.1-1
- Added "BuildRequires: autoconf" temporary dependency.
- Use Fedora Extras style BuildRoot specification.

* Fri May 26 2006 Mike A. Harris <mharris@redhat.com> 7.0-4
- Added "BuildRequires: fontconfig" for (#192038)

* Sat Mar 04 2006 Mike A. Harris <mharris@redhat.com> 7.0-3
- Ensure upgrade-only section of fonts-base rpm post script only executes on
  upgrades using -gt instead of -ge.

* Fri Feb 24 2006 Mike A. Harris <mharris@redhat.com> 7.0-2
- Generate encodings.dir files in the encodings dirs with mkfontscale from the
  base fonts package post install script, to work around bug (#173875)

* Thu Jan 26 2006 Mike A. Harris <mharris@redhat.com> 7.0-1
- Bumped artificial package version to 7.0, to indicate that the font tarballs
  are all from X11R7.0.
- Enabled the ethiopic font subpackage experimentally for bug (#176678)

* Tue Jan 17 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-3
- Added missing post/postun scripts for ISO8859-1-75dpi and ISO8859-1-100dpi
  font packages. (#174416)

* Tue Jan 10 2006 Bill Nottingham <notting@redhat.com> 1.0.0-2
- fix obsoletes (#177377)

* Thu Dec 15 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated all font packages to X11R7 RC4 versions.
- Added perl hack to build section to massage all of the configure.ac files
  to use pkgconfig to autodetect the top level X fontdir.
- Added font-alias-1.0.0-fonts-alias-fontdir-fix.patch to use pkgconfig to
  autodetect the top level X fontdir.
- Added encodings-1.0.0-encodings-fontdir-fix.patch to use pkgconfig to
  autodetect the top level X fontdir.
- Use new --disable-iso8859-* options instead of deleting unwanted encodings.
- Added dependency on font-utils 1.0.0

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-1
- Updated all font packages to X11R7 RC3 versions.

* Fri Nov 25 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-8
- Due to a bug in chkfontpath which will remove both 'misc' and 'misc:unscaled'
  from the fontpath, use sed magic to do it instead, based of xfs scripts.

* Wed Nov 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-7
- Undo the workaround implemented in build 0.99.0-5, and make the misc fonts
  directory ":unscaled" again.
- Invoke chkfontpath to remove the bare 'misc' font path without the :unscaled
  attribute from xfs config.

* Mon Nov 14 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-6
- Fixed mkfontscale invocation in Type1 font subpackage post/postun scripts
  by removing accidental -o argument that creeped in via cut and paste
  error. (#173059)

* Sun Nov 13 2005 Jeremy Katz <katzj@redhat.com> - 0.99.0-5
- don't use :unscaled for base fonts as a temporary workaround for #172997

* Wed Nov 9 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-4
- Added Obsoletes/Conflicts lines for fonts-xorg-* et al. to all subpackages,
  so that OS upgrades work properly.

* Tue Nov 8 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Split the old style 'base' fonts package up into 'base' and 'misc', where
  'base' now contains only the 'cursor' and 'fixed' fonts required by the
  X server, and 'misc' contains a variety of Asian, Arabic, Indic, and other
  fonts that can now be optionally installed or removed.
- Use globs in file manifests to reduce size of specfile.
- Add post/postun scripts for all font subpackages.
- Disable ethiopic fonts by default.

* Mon Nov 7 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Added "BuildArch: noarch" so that all fonts are noarch.

* Tue Oct 25 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial packaging.
