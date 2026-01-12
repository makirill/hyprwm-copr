Name:           hyprpaper
Version:        0.8.1
Release:        1%{?dist}
Summary:        Hyprpaper is a wayland wallpaper utility with IPC controls.

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpaper
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros


BUildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprtoolkit)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(hyprwire)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)


%description
Hyprpaper is a simple and fast wallpaper utility for Hyprland with the ability to dynamically change wallpapers through sockets.


%prep
%autosetup


%build
%cmake -DCMAKE_BUILD_TYPE=Release
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
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service


%changelog
%autochangelog

