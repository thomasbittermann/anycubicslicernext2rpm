#!/bin/bash
set -euo pipefail

# Configuration
REPO_URL="https://cdn-universe-slicer.anycubic.com/prod"
DIST_NAME="noble"  # i.e. noble (24.04), jammy (22.04)
ARCH="amd64"
COMP="main"
PKG_URL="${REPO_URL}/dists/${DIST_NAME}/${COMP}/binary-${ARCH}/Packages"

# Check for required tools
for tool in curl wget ar tar perl; do
    if ! command -v "$tool" &> /dev/null; then
        printf "Error: %s is not installed.\n" "$tool" >&2
        exit 1
    fi
done

FILE_URI=$(curl -s "$PKG_URL" | grep "^Filename:" | awk '{print $2}')
FILE_NAME=$(echo "$FILE_URI" | perl -pe 's;.*/([^/]+);$1;')
PKG_VERSION_FILE="./usr/share/AnycubicSlicerNext/resources/build-version.txt"
SCRIPT_DIR=$(dirname $(readlink -m "${BASH_SOURCE[0]}"))
SPEC_FILE="$SCRIPT_DIR/anycubicslicernext.spec"

BUILD_SOURCES="$HOME/rpmbuild/SOURCES"
BUILD_SPECS="$HOME/rpmbuild/SPECS"
mkdir -p "$BUILD_SOURCES" "$BUILD_SPECS"

# Copy spec file to rpmbuild/SPECS
cp "$SPEC_FILE" "$BUILD_SPECS/"
TARGET_SPEC="$BUILD_SPECS/$(basename "$SPEC_FILE")"

pushd "$BUILD_SOURCES" > /dev/null

if [[ -f "$FILE_NAME" ]]; then
    printf "already downloaded %s\n" "$FILE_NAME"
fi

wget -nc "$REPO_URL/$FILE_URI"

# We use a fixed temporary directory for extraction
TMP_DIR="anycubicslicernext-tmp"
rm -rf "$TMP_DIR"
mkdir "$TMP_DIR"

# Cleanup on exit
trap 'rm -rf "$TMP_DIR"' EXIT

cd "$TMP_DIR"

ar x "../$FILE_NAME"
tar xzf data.tar.gz

# Detect version from extracted files
if [[ ! -f "$PKG_VERSION_FILE" ]]; then
    printf "Error: Version file %s not found in package.\n" "$PKG_VERSION_FILE" >&2
    exit 1
fi
PKG_VERSION=$(tr -d '\r' < "$PKG_VERSION_FILE")

if [[ -z "$PKG_VERSION" ]]; then
    printf "Error: Could not determine PKG_VERSION from %s\n" "$PKG_VERSION_FILE" >&2
    exit 1
fi

printf "Found version: %s\n" "$PKG_VERSION"

if [[ -f "$TARGET_SPEC" ]]; then
    CURRENT_SPEC_VERSION=$(grep "^Version:" "$TARGET_SPEC" | awk '{print $2}')
    if [[ "$CURRENT_SPEC_VERSION" != "$PKG_VERSION" ]]; then
        printf "Updating spec file: %s -> %s\n" "$CURRENT_SPEC_VERSION" "$PKG_VERSION"
        sed -i "s/^Version:.*/Version: $PKG_VERSION/" "$TARGET_SPEC"
        sed -i "s/^Release:.*/Release: 1/" "$TARGET_SPEC"

        # Add changelog entry
        DATE_STR=$(LC_ALL=C date "+%a %b %d %Y")
        USER_NAME=$(git config user.name || echo "Automated Build")
        USER_EMAIL=$(git config user.email || echo "automated@build.local")
        DEB_VERSION=$(echo "$FILE_NAME" | perl -pe 's/.*?-(.*)-Ubuntu.*/$1/')
        CHANGELOG_ENTRY="* $DATE_STR $USER_NAME <$USER_EMAIL> - $PKG_VERSION-1\n- Updated to version $PKG_VERSION\n- converted from $DEB_VERSION deb packages"
        sed -i "/%changelog/a $CHANGELOG_ENTRY\n" "$TARGET_SPEC"

        # Copy the updated spec file back as the new template
        cp "$TARGET_SPEC" "$SPEC_FILE"
        printf "Updated template: %s\n" "$SPEC_FILE"
    fi
fi

TARBALL="anycubicslicernext-$PKG_VERSION.tar.bz2"

if [[ -f "../$TARBALL" ]]; then
    printf "Tarball %s already exists, skipping...\n" "$TARBALL"
    exit 0
fi

# Perform remaining adjustments
rm -v *.gz debian-binary usr/LICENSE.txt
mv -v usr/lib{,64}

cd ..
SRC_DIR="anycubicslicernext-$PKG_VERSION"
rm -rf "$SRC_DIR"
mv "$TMP_DIR" "$SRC_DIR"

tar cjf "$SRC_DIR.tar.bz2" "$SRC_DIR"

# Disable trap since we moved the directory
trap - EXIT
rm -rf "$SRC_DIR"

popd > /dev/null

printf "\nSuccess! To build the RPM, run:\n"
printf "rpmbuild -ba %s\n" "$TARGET_SPEC"
