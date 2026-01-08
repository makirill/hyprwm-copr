Name:           hyprlang
Version:        0.6.8
Release:        %autorelease
Summary:        The official implementation library for the hypr config language

License:        LGPL-3.0-only
URL:            https://github.com/hyprwm/hyprlang
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprutils)

%description
The hypr configuration language is an extremely efficient, yet easy to work with, configuration language for linux applications.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
Development files for %{name}.

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
%{_libdir}/libhyprlang.so.2
%{_libdir}/libhyprlang.so.%{version}

%files devel
%{_includedir}/hyprlang.hpp
%{_libdir}/libhyprlang.so
%{_libdir}/pkgconfig/hyprlang.pc

%changelog
%autochangelog
