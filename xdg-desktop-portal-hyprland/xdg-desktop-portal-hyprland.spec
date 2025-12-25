Name:           xdg-desktop-portal-hyprland
Epoch:          1
Version:        1.3.11
Release:        %autorelease
Summary:        xdg-desktop-portal backend for hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/xdg-desktop-portal-hyprland
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

# required for Screenshot portal implementation
Requires:       grim
Requires:       xdg-desktop-portal
# required for hyprland-share-picker
Requires:       slurp
Requires:       qt6-qtwayland

%description
%{summary}.

%prep
%autosetup

%build
%cmake --no-warn-unused-cli -DCMAKE_BUILD_TYPE:STRING=Release
%cmake_build

%install
%cmake_install

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/hyprland-share-picker
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_libexecdir}/%{name}
%{_userunitdir}/%{name}.service

%changelog
%autochangelog

