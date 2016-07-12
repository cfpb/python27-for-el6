# Python 2.7 RPM built for RHEL 6.5

**Description**:  

    RHEL 6.5 comes with Python 2.6 installed.  This project contains a SPEC file for building an RPM that compiles Python 2.7 and installs pip and virtualenv.
    Note that it improves upon the 2.7.6 rpm that was previously available.
    

## Dependencies

Currently, only RHEL and CentOS 6.5 have been tested.  Other dependencies are installed
via the boostrap.sh script.

## Installation

### Build the RPM using Vagrant

1. Once the repo has been cloned, run "vagrant up" to create the bulid VM
2. Run "vagrant ssh" to connect
3. CD to ~/rpmbuild
4. Run "rpmbuild -ba SPECS/python27-alt.spec"

### Build the RPM on a server
1. Once the repo has been cloned, run "sh ./bootstrap.sh"
2. CD to ~/rpmbuild
3. Run "rpmbuild -ba SPECS/python27-alt.spec"

### Install the RPM

Install the built RPM by running "sudo yum install RPMS/x86_64/python27-2.7.11-1.el6.x86_64.rpm"

## Configuration

Edit the SPEC file to make changes to the build configuration.

## Usage

1. Run /usr/local/bin/virtualenv ~/.virtualenvs/{ your_venv }
2. Activate using "source ~/.virtualenvs/{ your_venv }/bin/activate"
3. python -V should return 2.7.11
4. Install packages using pip, and code!

## Known issues

    Build process kept failing at the install section: the work-around to that was adding the -i option to the make command as seen in the spec file
    Also, be sure to remove any the previous python installs that you have on your system as this might have conflicts with the new build that you are making.
## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Getting involved

To contribute, please see [CONTRIBUTING](CONTRIBUTING.md).

----

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

----
