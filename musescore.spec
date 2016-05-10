%define srcname MuseScore
%define shortname mscore
%define fontfamilyname %{shortname}
%define shortver 2.0

Summary:	Linux MusE Score Typesetter
Name:		musescore
Version:	2.0.3
Release:	0.1
# (Fedora) rtf2html is LGPLv2+
# paper4.png paper5.png are LGPLv3
# the rest is GPLv2
License:	GPLv2 and LGPLv2+ and LGPLv3
Url:		http://musescore.org
Group:		Publishing
Source0:	http://downloads.sourceforge.net/project/mscore/mscore/%{srcname}-%{version}/%{srcname}-%{version}.zip
# (Fedora) For mime types
Source2:	mscore.xml
BuildRequires:	cmake
BuildRequires:	pkgconfig(alsa)
BuildRequires:	jackit-devel
BuildRequires:	pkgconfig(fluidsynth)
BuildRequires:	portaudio-devel
BuildRequires:	pkgconfig(Qt5XmlPatterns)
BuildRequires:    pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(QtWebKit)
BuildRequires:    pkgconfig(Qt5WebKitWidgets)
BuildRequires:	qt5-assistant
BuildRequires:	qt5-designer
BuildRequires:	qt5-devel >= 5.3
BuildRequires:	qt5-linguist
BuildRequires:	qt5-linguist-tools
%if %mdvver >= 201500
BuildRequires:	qt5-qtquick1
%else
BuildRequires:  qt5-tools
%endif
Requires:		qtscriptbindings
Requires:		%{name}-fonts = %{version}-%{release}
Requires:		fonts-ttf-freefont
Requires:		soundfont2-default
Provides:		musescore
Obsoletes:		mscore

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
%setup -q -n %{srcname}-%{version}
%apply_patches

# Remove the precompiled binary
rm thirdparty/rtf2html/rtf2html

# (Fedora) Do not build the bundled qt scripting interface:
sed -i 's|BUILD_SCRIPTGEN TRUE|BUILD_SCRIPTGEN FALSE|' CMakeLists.txt

# (Fedora) Disable rpath
sed -i '/rpath/d' %{shortname}/CMakeLists.txt

# (Fedora) Force specific compile flags:
find . -name CMakeLists.txt -exec sed -i -e 's|-m32|%{optflags}|' -e 's|-O3|%{optflags}|' {} \;

%build
export CC=gcc
export CXX=g++
%cmake -DUSE_GLOBAL_FLUID=ON -DBUILD_SCRIPT_INTERFACE=OFF -DCMAKE_BUILD_TYPE=RELEASE -DBUILD_LAME="OFF"
%make PREFIX=/usr lrelease
%make PREFIX=/usr 
pushd rdoc
  make PREFIX=/usr
popd

%install
%{makeinstall_std} -C build
%{makeinstall_std} -C build/rdoc

mkdir -p %{buildroot}/%{_datadir}/applications
cp -a build/%{shortname}.desktop %{buildroot}/%{_datadir}/applications

# Install fonts
mkdir -p %{buildroot}/%{_xfontdir}/TTF
mkdir -p %{buildroot}/%{_xfontdir}/TTF/bravura
mkdir -p %{buildroot}/%{_xfontdir}/TTF/gootville
install -pm 644 fonts/*.ttf %{buildroot}/%{_xfontdir}/TTF
install -pm 644 fonts/bravura/*.otf %{buildroot}/%{_xfontdir}/TTF
install -pm 644 fonts/bravura/*.json %{buildroot}/%{_xfontdir}/TTF/bravura
install -pm 644 fonts/gootville/*.otf %{buildroot}/%{_xfontdir}/TTF
install -pm 644 fonts/gootville/*.json %{buildroot}/%{_xfontdir}/TTF/gootville
install -pm 644 fonts/mscore/*.ttf fonts/mscore/*.otf %{buildroot}/%{_xfontdir}/TTF
install -pm 644 fonts/mscore/*.json %{buildroot}/%{_xfontdir}/TTF
install -pm 644 fonts/*.xml %{buildroot}/%{_xfontdir}/TTF

# these are packaged separately
rm -f %{buildroot}/%{_xfontdir}/TTF/Free*

# mscz
install -p share/templates/*.mscz %{buildroot}/%{_datadir}/%{shortname}-%{shortver}/demos/
# symlinks to be safe
pushd %{buildroot}/%{_datadir}/%{shortname}-%{shortver}/demos/
for i in *.mcsz; do
  ln -s $i ../templates/$i
done
popd

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
cp -a mscore/data/mscore.xpm \
   %{buildroot}/%{_datadir}/icons/hicolor/32x32/mimetypes/application-x-musescore.xpm
cp -a mscore/data/mscore.xpm \
   %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/
cp -a mscore/data/mscore.png \
   %{buildroot}/%{_datadir}/icons/hicolor/64x64/mimetypes/application-x-musescore.png
cp -a mscore/data/mscore.png \
   %{buildroot}/%{_datadir}/icons/hicolor/64x64/apps/

# Manpage
mkdir -p %{buildroot}/%{_mandir}/man1
install -pm 644 build/%{shortname}.1 %{buildroot}/%{_mandir}/man1/

%files
%doc README*
%{_bindir}/%{shortname}
%{_datadir}/%{shortname}*
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/applications/%{shortname}.desktop
%{_datadir}/pixmaps/%{shortname}.*
%{_datadir}/mime/packages/%{shortname}.xml
%{_mandir}/man1/*
%exclude %{_datadir}/%{shortname}-*/manual/

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/%{shortname}-*/manual/

%files fonts
%{_datadir}/fonts/TTF/*
