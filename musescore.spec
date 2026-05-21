# https://bugreports.qt.io/browse/QTBUG-73834
%global	_disable_lto 1

%define		srcname MuseScore
%define		shortname mscore
%define		fontfamilyname %{shortname}
%define		shortver %(echo %{version}|cut -d. -f1-2)

#define beta beta

Summary:	Linux MusE Score Typesetter
Name:		musescore
Version:		4.7.1
Release:	%{?beta:0.%{beta}.}1
# rtf2html is LGPLv2+
# paper4.png paper5.png are LGPLv3
# the rest is GPLv2
License:	GPLv2 and LGPLv2+ and LGPLv3
Url:		https://musescore.org
Group:		Publishing
Source0:	https://github.com/musescore/MuseScore/archive/%{srcname}-%{version}%{?beta:%{beta}}.tar.gz
Patch0:		musescore-4.7.1-dont-use-gtk-platform-theme.patch
BuildRequires:		cmake >= 3.22
BuildRequires:		ninja
BuildRequires:		qmake-qt6
BuildRequires:		xxd
BuildRequires:		pkgconfig(alsa)
# This is in Restricted
#BuildRequires:	pkgconfig(fdk-aac)
BuildRequires:		pkgconfig(flac)
BuildRequires:		pkgconfig(flac++)
BuildRequires:		pkgconfig(fluidsynth)
BuildRequires:		pkgconfig(freetype2)
BuildRequires:		pkgconfig(harfbuzz)
BuildRequires:		pkgconfig(jack)
BuildRequires:		pkgconfig(lame)
BuildRequires:		pkgconfig(libavcodec)
BuildRequires:		pkgconfig(libavdevice)
BuildRequires:		pkgconfig(libavfilter)
BuildRequires:		pkgconfig(libavformat)
BuildRequires:		pkgconfig(libavutil)
BuildRequires:		pkgconfig(libopusenc)
BuildRequires:		pkgconfig(libpulse)
BuildRequires:		pkgconfig(libswscale)
BuildRequires:		pkgconfig(libswresample)
BuildRequires:		pkgconfig(opus)
BuildRequires:		pkgconfig(poppler)
BuildRequires:		pkgconfig(poppler-qt6)
BuildRequires:		pkgconfig(portaudio-2.0)
BuildRequires:		pkgconfig(Qt6Concurrent)
BuildRequires:		pkgconfig(Qt6Core)
BuildRequires:		pkgconfig(Qt6Core5Compat)
BuildRequires:		pkgconfig(Qt6Designer)
BuildRequires:		pkgconfig(Qt6Gui)
BuildRequires:		pkgconfig(Qt6Help)
BuildRequires:		pkgconfig(Qt6NetworkAuth)
BuildRequires:		pkgconfig(Qt6QuickControls2)
BuildRequires:		pkgconfig(Qt6QuickTemplates2)
BuildRequires:		pkgconfig(Qt6QuickWidgets)
BuildRequires:		pkgconfig(Qt6ShaderTools)
BuildRequires:		pkgconfig(Qt6StateMachine)
BuildRequires:		pkgconfig(Qt6Svg)
BuildRequires:		pkgconfig(Qt6Test)
BuildRequires:		pkgconfig(Qt6UiTools)
BuildRequires:		pkgconfig(Qt6WebEngineCore)
BuildRequires:		pkgconfig(Qt6WebEngineWidgets)
BuildRequires:		pkgconfig(Qt6Widgets)
BuildRequires:		pkgconfig(Qt6Xml)
BuildRequires:		pkgconfig(sndfile)
BuildRequires:		pkgconfig(tinyxml2)
BuildRequires:		pkgconfig(vorbisfile)
BuildRequires:		pkgconfig(xkbcommon)
Requires:	%{name}-fonts = %{version}-%{release}
Requires:	fonts-ttf-freefont
Requires:	soundfont2-default
Provides:	%{name} = %{EVRD}
%rename	%{shortname}

%description
MuseScore stands for Linux MusE Score Typesetter.
Features:
	- WYSIWYG design, notes are entered on a "virtual notepaper".
	- TrueType font(s) for printing & display allows for high quality scaling
	to all sizes.
	- Easy & fast note entry.
	- Many editing functions.
	- MusicXML import/export.
	- Midi (SMF) import/export.
	- MuseData import.
	- Midi input for note entry.
	- Integrated sequencer and software synthesizer to play the score.
	- Print or create pdf files.

%files
%doc README*
%{_bindir}/%{shortname}
%{_datadir}/%{shortname}*
%{_datadir}/applications/org.%{name}.%{srcname}.desktop
%{_datadir}/metainfo/org.%{name}.%{srcname}.appdata.xml
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/icons/hicolor/*x*/apps/%{shortname}.png
%{_datadir}/icons/hicolor/512x512/mimetypes/*.png
%{_datadir}/icons/hicolor/scalable/mimetypes/*.svg
%{_mandir}/man1/%{shortname}.1*


#-----------------------------------------------------------------------------

%package doc
Summary:    MuseScore documentation
Group:      Development/Other
License:    CC-BY
Requires:   %{name} = %{version}-%{release}
%rename	mscore-doc
BuildArch:		noarch

%description doc
MuseScore Studio is a free cross platform WYSIWYG music notation program.
This package contains the reference manual of MuseScore.

%files doc
# FIXME: find and install some updated docs
# Old stuff but better than nothing
%doc share/manual/reference-en.pdf

#-----------------------------------------------------------------------------

%package fonts
Summary:	MuseScore fonts
Group:		Publishing
License:		GPL+ with exceptions and OFL
BuildRequires:		fontforge
BuildRequires:		t1utils
BuildRequires:		tetex
%rename	mscore-fonts
BuildArch:		noarch

%description fonts
MuseScore Studio is a free cross platform WYSIWYG music notation program.
This package contains the musical notation fonts for use of MuseScore.

%files fonts
%{_datadir}/fonts/TTF/*

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{srcname}-%{version}%{?beta:%{beta}}

%cmake -G Ninja \
	-DMUSE_APP_BUILD_MODE=release \
	-DMUE_COMPILE_USE_SYSTEM_FREETYPE:BOOL=ON \
	-DMUE_COMPILE_USE_SYSTEM_HARFBUZZ:BOOL=ON \
	-DMUE_COMPILE_USE_SYSTEM_OPUSENC:BOOL=ON \
	-DMUE_COMPILE_USE_SYSTEM_FLAC:BOOL=ON \
	-DMUE_DOWNLOAD_SOUNDFONT:BOOL=OFF \
	-DMUE_BUILD_IMPEXP_MNX_MODULE:BOOL=OFF \
	-DBUILD_PORTMIDI:BOOL=OFF \
	-DBUILD_CRASHPAD_CLIENT:BOOL=OFF


%build
%ninja_build -C build


%install
%ninja_install -C build

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

pushd %{buildroot}/%{_xfontdir}/TTF
	cd bravura
	ln -s ../Bravura.otf .
	ln -s ../BravuraText.otf .
	cd ../gootville
	ln -s ../Gootville.otf .
	ln -s ../GootvilleText.otf .
	cd ..
popd

# These are packaged separately
rm -f %{buildroot}/%{_xfontdir}/TTF/Free*

# Install demo files
mkdir -p %{buildroot}%{_datadir}/%{shortname}-%{shortver}/demos
install -D -p demos/*.mscz %{buildroot}/%{_datadir}/%{shortname}-%{shortver}/demos/

# No point in packaging dupes or headers for internal libraries
cd %{buildroot}
rm -rf \
	.%{_bindir}/crashpad_handler \
	.%{_includedir}/gmock \
	.%{_includedir}/gtest \
	.%{_includedir}/opus \
	.%{_includedir}/kddockwidgets-qt6 \
	.%{_libdir}/cmake/GTest \
	.%{_libdir}/cmake/KDDockWidgets-qt6 \
	.%{_libdir}/cmake/Opus \
	.%{_libdir}/*.a \
	.%{_libdir}/pkgconfig
