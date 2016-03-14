############################
# Set global SPEC variables
############################
%global __python_ver 27
%global pybasever 2.7
%global pyver 2.7.6
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
Name: %{python}
Version: %{pyver}
Release: 2%{?dist}
Summary: An interpreted, interacive, object-oriented programming language
Group: Development/Languages
License: Python
URL: http://www.python.org/
Source: https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Obsoletes: python27 <= 2.7.6
Provides: python27 = 2.7.6
Provides: python(abi) = 2.7.6

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


###########################################################
# BUILD
# The build directive does initial prep for building,
# then runs the configure script and then make to compile.
# Compiled code is placed in %{buildroot}
###########################################################
%build

# Convenience variable pointing to the directory used for
# PATH's
topdir=$(pwd)

# Configuring for make, prefix sets the install to /usr/local or
# whatever the setting is.  Enable unicode enables unicode support,
# enable shared builds as a shared library instead of a static library.
# Lastly, since the lib is also installed in /usr/local, tell the
# compiler where it is.
./configure --prefix=%{prefix} \
			--enable-unicode=ucs4 \
			--enable-shared \
			LDFLAGS="-Wl,--rpath=/usr/local/lib"

# First build python
make -s %{?_smp_flags}

# Fix interpreter paths to point to '/usr/local/bin/env python2.7'
# instead of '/usr/bin/env python', then create a link called python2.7
LD_LIBRARY_PATH="$topdir" $topdir/python Tools/scripts/pathfix.py -i "%{_bindir}/env python%{pybasever}" .
ln -s python python%{pybasever}

# Build with new python. Adds the directory to the path
# before running make (-s for slient).
LD_LIBRARY_PATH="$topdir" PATH=$PATH:$topdir make -s %{?_smp_flags}


###########################################################
# INSTALL
# This directive is where the code is actually installed
# in the %{buildroot} folder in preparation for packaging.
###########################################################
%install

# set the install path for Python packages
echo '[install-scripts]' >setup.cfg
echo 'install_dir='"%{buildroot}%{bindir}" >> setup.cfg

# NOTE: Look out for umask
# Sanity check before removal of old buildroot files
[ -d "%{buildroot}" -a "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# Create lib-dynload directory, then altinstall into %{buildroot} at
# the ${prefix} (e.g., /usr/local)
mkdir -p %{buildroot}%{prefix}/lib/python%{pybasever}/lib-dynload
make altinstall DESTDIR=%{buildroot} PREFIX=%{prefix}

# Hack to remove a stray file that should not have been generated.
rm %{buildroot}%{prefix}/bin/smtpd.py~

# Install pip
# --no-check-certificate must be used because of old verison
# of wget
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
LD_LIBRARY_PATH=%{buildroot}%{prefix}/lib %{buildroot}%{bindir}/python2.7 get-pip.py
# Now virtualenv
LD_LIBRARY_PATH=%{buildroot}%{prefix}/lib %{buildroot}%{bindir}/pip2.7 install virtualenv

if [ -e %{buildroot}%{prefix}/bin/virtualenv-3.5 ]; then
  mv %{buildroot}%{prefix}/bin/virtualenv-3.5 %{buildroot}%{prefix}/bin/virtualenv-2.7
else
  cp %{buildroot}%{prefix}/bin/virtualenv %{buildroot}%{prefix}/bin/virtualenv-2.7
fi

# Fix paths in shebangs
FILES=%{buildroot}%{bindir}/*
for f in $FILES
do
	sed -i 's|'%{buildroot}'||g' $f
done

FOLDERS=%{buildroot}%{prefix}/lib/python%{pybasever}/site-packages/*.dist-info

for f in $FOLDERS
do
	sed -i 's|'%{buildroot}'||g' $f/RECORD
done

###########################################################
# CLEAN
# This directive is for cleaning up post packaging, simply
# removes the buildroot directory in this case.
###########################################################
%clean
# Sanity check before removal of old buildroot files
[ -d "%{buildroot}" -a "%{buildroot}" != "/" ] && rm -rf %{buildroot}


##############################################################
# FILES
# The files directive must list all files that were installed
# so that they can be included in the package.
##############################################################
%files
%defattr(-,root,root,-)

# Documentation
%doc LICENSE README

# Executables
%{bindir}/pydoc*
%{bindir}/python%{pybasever}
%{bindir}/python%{pybasever}-config
%{bindir}/2to3
%{bindir}/idle
%{bindir}/smtpd.py
%{bindir}/pip
%{bindir}/pip2
%{bindir}/pip2.7
%{bindir}/easy_install
%{bindir}/easy_install-2.7
%{bindir}/virtualenv
%{bindir}/virtualenv-2.7
%{bindir}/wheel

# Man files
%{prefix}/share/man/*/*

# Lib files
%{prefix}/lib/pkgconfig/python-%{pybasever}.pc
%{prefix}/lib/libpython%{pybasever}.so
%{prefix}/lib/libpython%{pybasever}.so.1.0
%{prefix}/lib/python%{pybasever}/

# .h include files
/usr/local/include/python%{pybasever}/

# This directive is for changes made post release.
%changelog
