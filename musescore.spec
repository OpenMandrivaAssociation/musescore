# https://bugreports.qt.io/browse/QTBUG-73834
%define _disable_lto 1

%define srcname MuseScore
%define shortname mscore
%define fontfamilyname %{shortname}
%define shortver %(echo %{version}|cut -d. -f1-2)

#define beta beta

Summary:	Linux MusE Score Typesetter
Name:		musescore
Version:	4.3.2
Release:	%{?beta:0.%{beta}.}2
# rtf2html is LGPLv2+
# paper4.png paper5.png are LGPLv3
# the rest is GPLv2
License:	GPLv2 and LGPLv2+ and LGPLv3
Url:		http://musescore.org
Group:		Publishing
Source0:	https://github.com/musescore/MuseScore/archive/v%{version}%{?beta:%{beta}}.tar.gz
Patch0:		mscore-4.2.1-dont-use-gtk-platformtheme.patch
Patch1:		musescore-4.2.1-ffmpeg7.patch
# FIXME this shouldn't be a strict requirement, but musescore
# crashes when opening a file dialog (open/save) if the qt5
# version of plasma-integration is missing
Requires:	plasma-integration
BuildRequires:	cmake
BuildRequires:	pkgconfig(alsa)
BuildRequires:	jackit-devel
BuildRequires:	pkgconfig(fluidsynth)
BuildRequires:	portaudio-devel
BuildRequires:	lame-devel
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(Qt5XmlPatterns)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5WebEngine)
BuildRequires:	pkgconfig(Qt5WebEngineCore)
BuildRequires:	pkgconfig(Qt5WebEngineWidgets)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5QuickControls2)
BuildRequires:	pkgconfig(Qt5QuickTemplates2)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(Qt5Designer)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5UiTools)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(Qt5NetworkAuth)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(poppler)
BuildRequires:	pkgconfig(poppler-qt5)
BuildRequires:	pkgconfig(vorbisfile)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavdevice)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libavfilter)
BuildRequires:	pkgconfig(libswscale)
BuildRequires:	pkgconfig(libpostproc)
BuildRequires:	pkgconfig(libswresample)
BuildRequires:	qt5-assistant
BuildRequires:	qt5-devel >= 5.3
BuildRequires:	qt5-designer
BuildRequires:	qt5-linguist
BuildRequires:	qt5-linguist-tools
Requires:	%{name}-fonts = %{version}-%{release}
Requires:	fonts-ttf-freefont
Requires:	soundfont2-default
Provides:	musescore
Obsoletes:	mscore
Requires:	qt5-qtquickcontrols
Requires:	qt5-qtquickcontrols2

%description
MuseScore stands for Linux MusE Score Typesetter.

Features:
      - WYSIWYG design, notes are entered on a "virtual notepaper"
      - TrueType font(s) for printing & display allows for high quality
        scaling to all sizes
      - easy & fast note entry
      - many editing functions
      - MusicXML import/export
      - Midi (SMF) import/export
      - MuseData import
      - Midi input for note entry
      - integrated sequencer and software synthesizer to
        play the score
      - print or create pdf files

%package doc
Summary:    MuseScore documentation
Group:      Development/Other
License:    CC-BY
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch
Obsoletes:  mscore-doc

%description doc
MuseScore is a free cross platform WYSIWYG music notation program.

This package contains the user manual of MuseScore in different languages.

%package fonts
Summary:	MuseScore fonts
Group:		Publishing
License:	GPL+ with exceptions and OFL
BuildArch:	noarch
BuildRequires:	fontforge
BuildRequires:	tetex
BuildRequires:	t1utils
Obsoletes:		mscore-fonts

%description fonts
MuseScore is a free cross platform WYSIWYG music notation program.

This package contains the musical notation fonts for use of MuseScore.

%prep
%autosetup -p1 -n MuseScore-%{version}%{?beta:%{beta}}

# (Fedora) Do not build the bundled qt scripting interface:
sed -i 's|BUILD_SCRIPTGEN TRUE|BUILD_SCRIPTGEN FALSE|' CMakeLists.txt

# (Fedora) Force specific compile flags:
find . -name CMakeLists.txt -exec sed -i -e 's|-m32|%{optflags}|' -e 's|-O3|%{optflags}|' {} \;

%cmake_qt5 \
	-DOMR:BOOL=ON \
	-DOCR:BOOL=ON \
	-DUSE_SYSTEM_FREETYPE:BOOL=ON \
	-DUSE_SYSTEM_POPPLER:BOOL=ON \
	-DBUILD_PORTMIDI:BOOL=OFF \
	-DBUILD_CRASHPAD_CLIENT:BOOL=OFF \
	-DTRY_USE_CCACHE:BOOL=OFF \
	-DDOWNLOAD_SOUNDFONT:BOOL=OFF \
	-DMUE_BUILD_UPDATE_MODULE:BOOL=OFF \
	-DMUE_BUILD_VIDEOEXPORT_MODULE:BOOL=ON

%build
%make lrelease -C build
%make -C build

%install
%make_install -C build

# Install fonts
mkdir -p %{buildroot}/%{_xfontdir}/TTF
mkdir -p %{buildroot}/%{_xfontdir}/TTF/bravura
mkdir -p %{buildroot}/%{_xfontdir}/TTF/gootville
install -pm 644 fonts/*.ttf %{buildroot}/%{_xfontdir}/TTF
install -pm 644 fonts/bravura/*.?tf %{buildroot}/%{_xfontdir}/TTF
install -pm 644 fonts/bravura/*.json %{buildroot}/%{_xfontdir}/TTF/bravura
install -pm 644 fonts/gootville/*.?tf %{buildroot}/%{_xfontdir}/TTF
install -pm 644 fonts/gootville/*.json %{buildroot}/%{_xfontdir}/TTF/gootville
install -pm 644 fonts/mscore/*.?tf %{buildroot}/%{_xfontdir}/TTF
install -pm 644 fonts/mscore/*.json %{buildroot}/%{_xfontdir}/TTF
install -pm 644 fonts/*.xml %{buildroot}/%{_xfontdir}/TTF

# these are packaged separately
rm -f %{buildroot}/%{_xfontdir}/TTF/Free*

# mscz
mkdir -p %{buildroot}%{_datadir}/%{shortname}-%{shortver}/demos
install -D -p demos/*.mscz %{buildroot}/%{_datadir}/%{shortname}-%{shortver}/demos/

# No point in packaging dupes
cd %{buildroot}
rm -rf \
	.%{_bindir}/crashpad_handler \
	.%{_includedir}/gmock \
	.%{_includedir}/gtest \
	.%{_includedir}/opus \
	.%{_libdir}/cmake/GTest \
	.%{_libdir}/*.a \
	.%{_libdir}/pkgconfig

# ... or headers for internal libraries
rm -rf \
	.%{_includedir}/kddockwidgets \
	.%{_libdir}/cmake/KDDockWidgets

pushd %{buildroot}/%{_xfontdir}/TTF
cd bravura
ln -s ../Bravura.otf .
ln -s ../BravuraText.otf .
cd ../gootville
ln -s ../Gootville.otf .
ln -s ../GootvilleText.otf .
cd ..
popd

%files
%doc README*
%{_bindir}/%{shortname}
%{_datadir}/%{shortname}*
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*.xml
%{_mandir}/man1/*.1*
%{_datadir}/metainfo/org.musescore.MuseScore.appdata.xml

%files doc
%defattr(-,root,root,-)

%files fonts
%{_datadir}/fonts/TTF/*
