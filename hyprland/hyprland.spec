Name:           hyprland
Version:        0.52.2
Release:        %autorelease
Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland
Source:         %{url}/releases/download/v%{version}/source-v%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  glaze-static
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig(aquamarine)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xwayland)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(aquamarine)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprcursor)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(uuid)
BUildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(hyprwayland-scanner)

Requires:       xorg-x11-server-Xwayland%{?_isa}
Requires:       aquamarine%{?_isa} >= 0.9.3
Requires:       hyprcursor%{?_isa} >= 0.1.7
Requires:       hyprgraphics%{?_isa} >= 0.1.6
Requires:       hyprlang%{?_isa} >= 0.3.2
Requires:       hyprutils%{?_isa} >= 0.8.2

#Recommends:     (qt5-qtwayland if qt5-qtbase-gui)
#Recommends:     (qt6-qtwayland if qt6-qtbase-gui)

%description
Hyprland is a dynamic tiling Wayland compositor that doesn't sacrifice
on its looks. It supports multiple layouts, fancy effects, has a
very flexible IPC model allowing for a lot of customization, a powerful
plugin system and more.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
Development files for %{name} v%{version}.


%prep
%autosetup -n hyprland-source -N

%build
%cmake --no-warn-unused-cli -DCMAKE_BUILD_TYPE:STRING=Release -DNO_TESTS=TRUE -DBUILD_TESTING=FALSE
%cmake_build --config Release

%install
%cmake_install

%files
%license LICENSE
%{_bindir}/[Hh]yprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
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

