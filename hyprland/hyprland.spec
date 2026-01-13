Name:           hyprland
Version:        0.53.1
Release:        11%{?dist}
Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland
Source:         %{url}/releases/download/v%{version}/source-v%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  glaze-devel >= 6.0.0
BuildRequires:  mesa-libGL-devel

BuildRequires:  pkgconfig(aquamarine) >= 0.9.3
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(hyprcursor)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(hyprwire)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(muparser)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  udis86-devel

%description
Hyprland is a dynamic tiling Wayland compositor that doesn't sacrifice
on its looks. It supports multiple layouts, fancy effects, has a
very flexible IPC model allowing for a lot of customization, a powerful
plugin system and more.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake
Requires:       gcc-c++
Requires:       pkgconfig(gbm)
Requires:       meson
Requires:       pkgconfig(hyprwayland-scanner)
Requires:       pkgconfig(hyprwire)
Requires:       pkgconfig(muparser)
Requires:       pkgconfig(pangocairo)
Requires:       pkgconfig(re2)
Requires:       pkgconfig(tomlplusplus)
Requires:       pkgconfig(uuid)
Requires:       pkgconfig(wayland-protocols) >= 1.45
Requires:       pkgconfig(xcursor)
Requires:       udis86-devel
%description    devel
Development files for %{name} v%{version}. Hyprland plugins are build for specific setup,
so this package is an mandatory requirement for plugins.


%prep
%autosetup -n hyprland-source -N


%build
%cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=FALSE
%cmake_build


%install
%cmake_install

%files
%license LICENSE
%{_bindir}/[Hh]yprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_bindir}/start-hyprland
%{_datadir}/hypr/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/wayland-sessions/hyprland-uwsm.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_mandir}/man1/hyprctl.1*
%{_mandir}/man1/Hyprland.1*
%{bash_completions_dir}/hypr*
%{fish_completions_dir}/hypr*.fish
%{zsh_completions_dir}/_hypr*


%files devel
%{_datadir}/pkgconfig/hyprland.pc
%{_includedir}/hyprland/


%changelog
%autochangelog

