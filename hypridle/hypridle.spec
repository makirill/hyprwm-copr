Name:           hypridle
Version:        0.1.7
Release:        %autorelease
Summary:        Hyprland's idle daemon
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hypridle
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  cmake(hyprwayland-scanner)
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

%description
%{summary}.

%prep
%autosetup

%build
%cmake --no-warn-unused-cli -DCMAKE_BUILD_TYPE:STRING=Release
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md assets/example.conf
%{_bindir}/%{name}
%{_datadir}/hypr/hypridle.conf
%{_userunitdir}/%{name}.service

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun %{name}.service

%changelog
%autochangelog

