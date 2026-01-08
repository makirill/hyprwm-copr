Name:           hyprgraphics
Version:        0.5.0
Release:        %autorelease
Summary:        Hyprland graphics / resource utilities

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprgraphics
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libjxl_cms)
BuildRequires:  pkgconfig(libjxl_threads)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libheif)
BuildRequires:  pkgconfig(librsvg-2.0)

%description
Hyprgraphics is a small C++ library with graphics / resource related utilities used across the hypr* ecosystem.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
Development files for %{name} v%{version}.

%prep
%autosetup

%build
%cmake --no-warn-unused-cli -DCMAKE_BUILD_TYPE:STRING=Release
%cmake_build --config Release

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.3
%{_libdir}/lib%{name}.so.%{version}

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
%autochangelog

