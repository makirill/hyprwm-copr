%global debug_package %{nil}

Name:           glaze
Version:        6.5.1
Release:        %autorelease
Summary:        Extremely fast, in memory, JSON and interface library

License:        MIT
URL:            https://github.com/stephenberry/glaze
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
One of the fastest JSON libraries in the world. Glaze reads and writes from object memory, simplifying interfaces and offering incredible performance.

%package        devel
Summary:        Development files for %{name}
BuildArch:      noarch
Provides:       %{name}-static = %{version}-%{release}
%description    devel
Development files for %{name} v%{version}.

%prep
%autosetup

%build
%cmake \
    -Dglaze_INSTALL_CMAKEDIR=%{_datadir}/cmake/%{name} \
    -Dglaze_DISABLE_SIMD_WHEN_SUPPORTED:BOOL=ON \
    -Dglaze_DEVELOPER_MODE:BOOL=OFF \
    -Dglaze_ENABLE_FUZZING:BOOL=OFF
%cmake_build

%install
%cmake_install

%files devel
%license LICENSE
%doc README.md
%{_datadir}/cmake/%{name}/
%{_includedir}/%{name}/

%changelog
%autochangelog

