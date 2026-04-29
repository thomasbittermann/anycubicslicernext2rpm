# anycubicslicernext2rpm

This project provides tools to convert the Anycubic Slicer Next Debian package (for Ubuntu/Debian) into an RPM package suitable for distributions like Fedora, RHEL, or AlmaLinux.

## Overview

The conversion process consists of two main parts:
1. **Source Preparation**: A script that downloads the latest `.deb` package from Anycubic's CDN, extracts its contents, and repacks them into a source tarball.
2. **RPM Building**: An RPM spec file that defines how to install the files from the source tarball into an RPM package.

## Prerequisites

To use these tools, you need the following installed on your system:
- `bash`
- `curl`
- `wget`
- `binutils` (for the `ar` command)
- `tar`
- `perl`
- `rpm-build`

## Usage

### 1. Prepare the Source Tarball

Run the provided shell script to download and prepare the source files. The script targets the "noble" (Ubuntu 24.04) distribution by default and places the resulting tarball in `~/rpmbuild/SOURCES/`.

```bash
./anycubicslicernext2rpm.sh
```

*Note: You may need to adjust the `DIST_NAME` or `ARCH` variables inside the script if you wish to target a different base.*

### 2. Build the RPM

Once the source preparation is complete, use `rpmbuild` to create the package:

```bash
rpmbuild -ba ~/rpmbuild/SPECS/anycubicslicernext.spec
```

The resulting RPM package will be located in `~/rpmbuild/RPMS/x86_64/`.

## Files

- `anycubicslicernext2rpm.sh`: Automates fetching and repacking the Debian package.
- `anycubicslicernext.spec`: The RPM specification file.
- `README.md`: This documentation.

## Acknowledgments

- Originally based on conversions performed via `alien`, then manually refined for better compatibility with modern RPM-based distributions.
