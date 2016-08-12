Name:           android-file-transfer
Version:        3.0
Release:        1%{?dist}
Summary:        Reliable MTP client with minimalistic UI

License:        GPLv3+
URL:            https://github.com/whoozle/android-file-transfer-linux
Source0:        https://github.com/whoozle/android-file-transfer-linux/archive/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(fuse)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  file-devel
BuildRequires:  readline-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib


%description
Android File Transfer for Linux — reliable MTP client with minimalistic UI
similar to Android File Transfer for Mac.

%prep
%setup -q -n %{name}-linux-%{version}


%build
mkdir build
pushd build
    %cmake ..
    %make_build
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd build
    %make_install
popd

install -dm 755 %{buildroot}%{_datadir}/appdata/
install -m 644 -p %{name}.appdata.xml %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE
%doc FAQ.md README.md
%{_bindir}/*
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/*.png


%changelog
* Fri Aug 12 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 3.0-1
- Initial release for fedora
