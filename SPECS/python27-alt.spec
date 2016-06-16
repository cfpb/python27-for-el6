############################
# Set global SPEC variables
############################
%global __python_ver 27
%global pybasever 2.7
%global pyver 2.7.11
%global python python%{__python_ver}
%global __python %{python}

%global prefix /usr/local
%global bindir %{prefix}/bin
%global pylibdir %{prefix}/lib/python%{pybasever}
%global dynload_dir %{pylibdir}/lib-dynload
%global site_packages %{pylibdir}/site-packages

###############
# Set metadata
###############
Name:		%{python}
Version:   	%{pyver}
Release: 	2%{?dist}
Summary: 	An interpreted, interacive, object-oriented programming language
Group: 		Development/Languages
License: 	Python
URL: 		http://www.python.org/
Source: 	https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Obsoletes: 	python27 <= 2.7.6
Provides: 	python27 = 2.7.11
Provides: 	python(abi) = 2.7.11

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need
a programmable interface.

This package is a custom deploy of Python 2.7 used by the
Consumer Financial Protection Bureau.

Note that documentation for Python is provided in the python-docs
package.

#####################
# Build requirements
#####################
BuildRoot: %(mktemp -ud %{_tmppath}/build/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: gcc make autoconf
BuildRequires: zlib-devel bzip2-devel openssl-devel sqlite-devel
AutoReq: no


########################################################
# PREP and SETUP
# The prep directive removes existing build directory
# and extracts source code so we have a fresh
# code base.  -n defines the name of the directory
# to be Python-2.7 instead of the default, python27-alt
########################################################

%prep
%setup -n Python-%{version}


%build
%configure
make %{?_smp_mflags}


%install
%make_install



%files
/usr/bin
/usr/include/python2.7/
/usr/lib/python2.7/
/usr/lib64/pkgconfig/
/usr/lib64/python2.7/
/usr/share/man/man1/
/usr/lib64/libpython2.7.a

%doc



%changelog

