Name:           hyprland-guiutils
Version:        0.2.1
Release:        1%{?dist}
Summary:        Hyprland GUI utilities

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-guiutils
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprtoolkit)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libdrm)

%description
%{summary}.

%prep
%autosetup


%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build


%install
%cmake_install


%files
%license LICENSE
%doc README.md
%{_bindir}/hyprland-dialog
%{_bindir}/hyprland-donate-screen
%{_bindir}/hyprland-run
%{_bindir}/hyprland-update-screen
%{_bindir}/hyprland-welcome

%changelog
%autochangelog

