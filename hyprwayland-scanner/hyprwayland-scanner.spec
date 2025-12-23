Name:           hyprwayland-scanner
Version:        0.4.5
Release:        %autorelease
Summary:        A Hyprland implementation of wayland-scanner, in and for C++

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwayland-scanner
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  cmake(pugixml)
BuildRequires:  gcc-c++

%description
A Hyprland implementation of wayland-scanner, in and for C++.

hw-s automatically generates properly RAII-ready, modern C++ bindings for Wayland protocols, for either servers or clients.

%package        devel
Summary:        A Hyprland implementation of wayland-scanner, in and for C++
%description    devel
Development libraries and header files for the hyprwayland-scunner v%{version}.

%prep
%autosetup

%build
%cmake
%cmake_build

%install
%cmake_install

%files devel
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

%changelog
%autochangelog
