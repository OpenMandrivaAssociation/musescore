%define srcname MuseScore
%define shortname mscore

Summary:    Linux MusE Score Typesetter
Name:       musescore
Version:    1.3
Release:    1
# (Fedora) rtf2html is LGPLv2+
# paper4.png paper5.png are LGPLv3
# the rest is GPLv2
License:    GPLv2 and LGPLv2+ and LGPLv3
Url:        http://musescore.org
Group:      Publishing
Source0:    http://downloads.sourceforge.net/project/mscore/mscore/%{srcname}-%{version}/%{shortname}-%{version}.tar.bz2
# (Fedora) For building the jazz font
Source1:    mscore-ConvertFont.ff
# (Fedora) For mime types
Source2:    mscore.xml
Patch0:     mscore-1.0-awl-fix-underlink.patch
Patch1:     mscore-1.0-disable-uitools.patch
# (Fedora) use the system default soundfont instead of the deleted, non-free, one 
Patch2:     mscore-use-default-soundfont.patch
# (Fedora) don't build the common files (font files, wallpapers, demo song,
# instrument list) into the binary executable to reduce its size. This is also
# useful to inform the users about the existence of different choices for common
# files. The font files need to be separated due to the font packaging guidelines.
Patch3:     mscore-separate-commonfiles.patch
# (Fedora) Split the large documentation into a separate package
Patch4:     mscore-split-doc.patch
# (Fedora) Fix DSO linking.
Patch5:     mscore-dso-linking.patch
# (Fedora) Fix some gcc warnings
Patch6:     mscore-fix-gcc-warnings.patch
# (Fedora) Use system qtsingleapplication
Patch7:	    mscore-system-qtsingleapplication.patch
BuildRequires:  cmake
BuildRequires:  libalsa-devel
BuildRequires:  jackit-devel
BuildRequires:  fluidsynth-devel
BuildRequires:  portaudio-devel
BuildRequires:  qt4-devel > 4:4.4
BuildRequires:  qt4-linguist
BuildRequires:  doxygen
BuildRequires:  texlive-mf2pt1
Requires:   qtscriptbindings
Requires:   %{name}-fonts = %{version}-%{release}
Requires:   soundfont2-default
Provides:   musescore
Obsoletes:  mscore

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
Summary:       MuseScore documentation
Group:         Development/Other
License:       CC-BY
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch
Obsoletes:     mscore-doc

%description doc
MuseScore is a free cross platform WYSIWYG music notation program.

This package contains the user manual of MuseScore in different languages.

%package fonts
Summary:       MuseScore fonts
Group:         Publishing
License:       GPL+ with exceptions and OFL
BuildArch:     noarch
BuildRequires: fontforge
BuildRequires: tetex
BuildRequires: t1utils
Obsoletes:     mscore-fonts

%description fonts
MuseScore is a free cross platform WYSIWYG music notation program.

This package contains the musical notation fonts for use of MuseScore.

%prep
%setup -q -n %{shortname}-%{version}/mscore
%patch0 -p2 -b .underlink
%patch1 -p0 -b .disable-uitools

%patch2 -p2 -b .default-soundfont
%patch3 -p2 -b .separate-commonfiles
%patch4 -p2 -b .split-doc
%patch5 -p2 -b .dso-linking
%patch6 -p2 -b .gcc-warnings
%patch7 -p2 -b .qtsingleapp

# only install .qm files
perl -pi -e 's,.*.ts\n,,g' share/locale/CMakeLists.txt

# (Fedora) Remove the precompiled binary
rm rtf2html/rtf2html

# (Fedora) Do not build the bundled qt scripting interface:
sed -i 's|scriptgen||' CMakeLists.txt

# (Fedora) Fix EOL encoding
sed 's|\r||' rtf2html/README > tmpfile
touch -r rtf2html/README tmpfile
mv -f tmpfile rtf2html/README

# (Fedora) Remove preshipped fonts. We will build them from source
rm -f %{shortname}/%{shortname}/fonts/*.ttf

# (Fedora) Disable rpath
sed -i '/rpath/d' %{shortname}/CMakeLists.txt

# (Fedora) this is non-free soundfont "Gort's Minipiano"
rm -f mscore/data/piano1.sf2

# (Fedora) Force specific compile flags:
find . -name CMakeLists.txt -exec sed -i 's|-O3|%{optflags}|' {} \;

%build
%cmake_qt4 -DUSE_GLOBAL_FLUID=ON -DBUILD_SCRIPT_INTERFACE=OFF
%make
make lupdate
make lrelease

# (Fedora) Build fonts from source:
pushd ../%{shortname}/fonts
   # adapt genFont script to mandriva's cmake build dir
   sed -i 's,../../../build/mscore/genft,../../build/mscore/genft,' genFont
   ./genFont
   fontforge %{SOURCE1} MuseJazz.sfd
popd

%install
rm -rf %{buildroot}
%{makeinstall_std} -C build

# Install fonts
mkdir -p %{buildroot}/%{_datadir}/fonts/%{shortname}
install -pm 644 %{shortname}/fonts/%{shortname}*.ttf %{buildroot}/%{_datadir}/fonts/%{shortname}

# Install Manpage
install -D -pm 644 packaging/%{shortname}.1 %{buildroot}/%{_mandir}/man1/%{shortname}.1

# Install mimetype file
install -D -pm 644 %{SOURCE2} %{buildroot}/%{_datadir}/mime/packages/%{shortname}.xml

# (Fedora) gather the doc files in one location
   cp -p rtf2html/ChangeLog        ChangeLog.rtf2html
   cp -p rtf2html/COPYING.LESSER   COPYING.LESSER.rtf2html
   cp -p rtf2html/README           README.rtf2html
   cp -p rtf2html/README.mscore    README.mscore.rtf2html
   cp -p rtf2html/README.ru        README.ru.rtf2html
   cp -p osdabzip/README           README.osdabzip
   cp -p osdabzip/README.mscore    README.mscore.osdabzip
   cp -p share/wallpaper/COPYRIGHT COPYING.wallpaper


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog* NEWS README* COPYING*
%{_bindir}/%{shortname}
%{_datadir}/%{shortname}*
%{_datadir}/applications/%{shortname}.desktop
%{_datadir}/pixmaps/%{shortname}.*
%{_datadir}/mime/packages/%{shortname}.xml
%{_datadir}/soundfonts/TimGM6mb.sf2
%{_mandir}/man1/*
%{qt4plugins}/designer/libawlplugin.so
%exclude %{_datadir}/%{shortname}-*/man/

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/%{shortname}-*/man/

%files fonts
%{_datadir}/fonts/%{shortname}


%changelog
* Mon Oct 31 2011 Thomas Spuhler <tspuhler@mandriva.org> 1.1-2mdv2012.0
+ Revision: 707958
- added %%patch9 -p2 -b .enable-portaudio-by-default for audio to play out of the box

* Sun Oct 30 2011 Thomas Spuhler <tspuhler@mandriva.org> 1.1-1
+ Revision: 707861
- removed BuildRequires:	qtsingleapplication-devel, we use system version
  added BuildRequires:  texlive-mf2pt1
  changed Provides:   mscore to musescore
- imported package musescore


