#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		neovim_gui
%define		egg_name	neovim_gui
Summary:	Python GTK GUI for neovim
Name:		python-neovim-gui
Version:	0.1.3
Release:	6
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/neovim/python-gui/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	99f03793e41150e71569c389a9256435
Patch0:		pynvim-0.3.patch
URL:		https://github.com/neovim/python-gui
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Simple nvim GUI implemented using GTK

%package -n python3-neovim-gui
Summary:	Python GTK GUI for neovim
Group:		Libraries/Python

%description -n python3-neovim-gui
Simple nvim GUI implemented using GTK

%prep
%setup -q -n python-gui-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
mv $RPM_BUILD_ROOT%{_bindir}/pynvim{,2}
%endif

%if %{with python3}
%py3_install
mv $RPM_BUILD_ROOT%{_bindir}/pynvim{,3}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/pynvim2
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/screen.so
%{py_sitedir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-neovim-gui
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/pynvim3
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}/*.py
%attr(755,root,root) %{py3_sitedir}/%{module}/screen.*.so
%{py3_sitedir}/%{egg_name}-%{version}-py*.egg-info
%endif
