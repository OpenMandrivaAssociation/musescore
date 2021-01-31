%define srcname MuseScore
%define shortname mscore
%define fontfamilyname %{shortname}
%define shortver 3.0

#define beta beta

Summary:	Linux MusE Score Typesetter
Name:		musescore
Version:	3.6.1
Release:	%{?beta:0.%{beta}.}1
# (Fedora) rtf2html is LGPLv2+
# paper4.png paper5.png are LGPLv3
# the rest is GPLv2
License:	GPLv2 and LGPLv2+ and LGPLv3
Url:		http://musescore.org
Group:		Publishing
Source0:	https://github.com/musescore/MuseScore/archive/v%{version}%{?beta:%{beta}}.tar.gz
# For mime types
Source2:	https://github.com/musescore/MuseScore/raw/master/build/mscore.xml
Patch2:		musescore-3.0.2-dont-copy-qtwebengine.patch
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
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(Qt5Designer)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5UiTools)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(poppler)
BuildRequires:	pkgconfig(poppler-qt5)
BuildRequires:	pkgconfig(vorbisfile)
BuildRequires:	qt5-assistant
BuildRequires:	qt5-designer
BuildRequires:	qt5-devel >= 5.3
BuildRequires:	qt5-linguist
BuildRequires:	qt5-linguist-tools
BuildRequires:	qt5-qtquick1
Requires:	%{name}-fonts = %{version}-%{release}
Requires:	fonts-ttf-freefont
Requires:	soundfont2-default
Provides:	musescore
Obsoletes:	mscore

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

# (Fedora) Disable rpath
sed -i '/rpath/d' %{shortname}/CMakeLists.txt

# (Fedora) Force specific compile flags:
find . -name CMakeLists.txt -exec sed -i -e 's|-m32|%{optflags}|' -e 's|-O3|%{optflags}|' {} \;

%cmake_qt5 \
	-DOMR:BOOL=ON \
	-DOCR:BOOL=ON \
	-DUSE_SYSTEM_FREETYPE:BOOL=ON \
	-DUSE_SYSTEM_POPPLER:BOOL=ON \
	-DBUILD_PORTMIDI:BOOL=OFF \
	-DDOWNLOAD_SOUNDFONT:BOOL=OFF

%build
%make lrelease -C build
%make -C build
%make referenceDocumentation -C build

%install
%make_install -C build

mkdir -p %{buildroot}/%{_datadir}/applications
cp -a build/%{shortname}.desktop %{buildroot}/%{_datadir}/applications

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
install -D -p share/templates/*.mscz %{buildroot}/%{_datadir}/%{shortname}-%{shortver}/demos/

pushd %{buildroot}/%{_xfontdir}/TTF
cd bravura
ln -s ../Bravura.otf .
ln -s ../BravuraText.otf .
cd ../gootville
ln -s ../Gootville.otf .
ln -s ../GootvilleText.otf .
cd ..
popd

# Mime type
mkdir -p %{buildroot}/%{_datadir}/mime/packages
install -pm 644 %{SOURCE2} %{buildroot}/%{_datadir}/mime/packages/

# Desktop file
desktop-file-install \
   --dir=%{buildroot}/%{_datadir}/applications \
   --add-category="X-Notation" \
   --remove-category="Sequencer" \
   --remove-category="AudioVideoEditing" \
   --remove-key="Version" \
   --add-mime-type="audio/midi" \
   --add-mime-type="text/x-lilypond" \
   --add-mime-type="application/xml" \
   %{buildroot}/%{_datadir}/applications/%{shortname}.desktop

# Move images to the freedesktop location
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/{32x32,64x64}/apps/
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/{32x32,64x64}/mimetypes/

# Manpage
mkdir -p %{buildroot}/%{_mandir}/man1
install -pm 644 build/%{shortname}.1 %{buildroot}/%{_mandir}/man1/

%files
%doc README*
%{_bindir}/%{shortname}
%{_bindir}/%{name}
%{_datadir}/%{shortname}*
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/applications/%{shortname}.desktop
%{_datadir}/mime/packages/%{shortname}.xml
%{_datadir}/mime/packages/%{name}.xml
%{_mandir}/man1/*
%{_datadir}/metainfo/org.musescore.MuseScore.appdata.xml

%files doc
%defattr(-,root,root,-)

%files fonts
%{_datadir}/fonts/TTF/*
