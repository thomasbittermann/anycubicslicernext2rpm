# anycubicslicernext2rpm

This project provides tools to convert the Anycubic Slicer Next Debian package (for Ubuntu/Debian) into an RPM package suitable for RPM-based distributions such as Fedora. It was developed and tested on Fedora 44.

## Overview

The conversion process consists of two main parts:
1. **Source Preparation**: A script that downloads the latest `.deb` package from Anycubic's CDN, verifies its checksum, extracts its contents, and repacks them into a source tarball.
2. **RPM Building**: An RPM spec file that installs the prebuilt files from the source tarball into an RPM package.

The `.deb` contains prebuilt binaries, so nothing is compiled. The spec only repackages them and maps the dependencies to Fedora package names.

## Prerequisites

- `bash`
- `curl`
- `binutils` (for the `ar` command)
- `tar`
- `coreutils` (`sha256sum`), `sed`, `awk`
- `rpm-build`
- `openssl` (only needed if the TLS workaround is triggered, see below)

## Usage

### 1. Prepare the Source Tarball

Run the script to download and prepare the source files. It targets the "noble" (Ubuntu 24.04) repository by default and places the resulting tarball in `~/rpmbuild/SOURCES/`.

```bash
./anycubicslicernext2rpm.sh
```

The script:
- reads the package index and finds the current `.deb`
- downloads it (resumable) and verifies the SHA256 from the index
- extracts it and reads the version from `build-version.txt`
- updates `Version:`, `Release:` and `%changelog` in the spec if the upstream version changed, and copies the spec to `~/rpmbuild/SPECS/`
- creates `~/rpmbuild/SOURCES/anycubicslicernext-<version>.tar.bz2`

*Note: Adjust `DIST_NAME` or `ARCH` in the script if you want to target a different base.*

### 2. Build the RPM

```bash
rpmbuild -ba ~/rpmbuild/SPECS/anycubicslicernext.spec
```

The resulting RPM is in `~/rpmbuild/RPMS/x86_64/`. Install it with:

```bash
sudo dnf install ~/rpmbuild/RPMS/x86_64/anycubicslicernext-*.rpm
```

## Updating to a new upstream version

Run the script again, then `rpmbuild -ba`. When upstream bumps the version, the script sets `Version:`, resets `Release:` to 1 and adds a changelog entry. For packaging-only changes (same upstream version), bump `Release:` and add a `%changelog` entry by hand.

Edit the spec template in this repository, not the copy in `~/rpmbuild/SPECS/`, which the script overwrites on every run.

## TLS certificate workaround

The Anycubic CDN serves an incomplete certificate chain (the intermediate certificate is missing). Browsers hide this by fetching the intermediate themselves, but `curl` and OpenSSL fail with "unable to get local issuer certificate".

If the first request fails, the script:
1. fetches the intermediate from the `CA Issuers` URL in the server certificate
2. checks that the server certificate verifies through it against the system CA store
3. uses the extended bundle for this run only

Nothing is installed into the system trust store, and the script aborts instead of falling back to insecure mode if the check fails. If Anycubic fixes their server, the workaround is skipped automatically.

## Spec file notes

- `%files` lists directories rather than individual files, so upstream adding or removing files doesn't break the build.
- The bundled private libraries are excluded from the generated `Provides` and `Requires`, since no distribution package provides them. If a new upstream release adds a private library that leaks into `rpm -qpR`, add it to `__requires_exclude`.
- Static libraries, headers and CMake files are removed in `%install`, as they are not needed at runtime.
- Strip, build-id links, rpath checks and shebang mangling are disabled because the binaries are prebuilt.
- Runtime dependencies use Fedora names: `webkit2gtk4.1`, `gtk3`, `mesa-libGLU`, `dbus-libs` and `gstreamer1-plugin-libav` (upstream depends on libav for video).
- The binaries are built on Ubuntu 24.04 and need glibc 2.38 or newer.

After a build, check the dependencies with:

```bash
rpm -qpR ~/rpmbuild/RPMS/x86_64/anycubicslicernext-*.rpm
```

Only system libraries should appear.

## Troubleshooting

- **Blank window under Wayland:** try `WEBKIT_DISABLE_DMABUF_RENDERER=1 AnycubicSlicerNext`.
- **"Installed (but unpackaged) file(s) found":** upstream added files outside the packaged paths. Add them to `%files` or remove them in `%install`.
- **Unresolvable dependency on install:** a private library probably leaked into `Requires`. Extend `__requires_exclude` in the spec.

## Files

- `anycubicslicernext2rpm.sh`: Automates fetching, verifying and repacking the Debian package.
- `anycubicslicernext.spec`: The RPM specification file (template).
- `README.md`: This documentation.

## Disclaimer

This is an unofficial repackaging and is not affiliated with Anycubic. The package contains Anycubic's prebuilt binaries; see the license shipped with the upstream package.

## Acknowledgments

- Originally based on conversions performed via `alien`, then manually refined for better compatibility with modern RPM-based distributions.
