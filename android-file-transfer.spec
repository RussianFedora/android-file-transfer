Name:           android-file-transfer
Version:        3.0
Release:        1%{?dist}
Summary:        Reliable MTP client with minimalistic UI

License:        GPLv3+
URL:            https://github.com/whoozle/android-file-transfer-linux
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
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
%autosetup -n %{name}-linux-%{version}
mkdir %{_target_platform}

%build
pushd %{_target_platform}
    %cmake ..
popd
%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}

install -Dpm0644 %{name}.appdata.xml %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

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
