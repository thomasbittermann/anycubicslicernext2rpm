#!/bin/bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_URL="https://cdn-universe-slicer.anycubic.com/prod"
DIST_NAME="noble"
ARCH="amd64"
COMP="main"
PKG_URL="${REPO_URL}/dists/${DIST_NAME}/${COMP}/binary-${ARCH}/Packages"

PKG_VERSION_FILE="./usr/share/AnycubicSlicerNext/resources/build-version.txt"
SCRIPT_DIR=$(dirname $(readlink -m "${BASH_SOURCE[0]}"))
SPEC_FILE="$SCRIPT_DIR/anycubicslicernext.spec"

BUILD_SOURCES="$HOME/rpmbuild/SOURCES"
BUILD_SPECS="$HOME/rpmbuild/SPECS"
TMP_DIR="$BUILD_SOURCES/anycubicslicernext-tmp"   # absolute, so cleanup works from anywhere
TLS_TMP=""
CURL_OPTS=()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
die() { printf "Error: %s\n" "$*" >&2; exit 1; }

cleanup() {
    [[ -n "$TLS_TMP" ]] && rm -rf "$TLS_TMP"
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# The server sends a broken chain (no usable intermediate), which makes curl/OpenSSL
# fail with "unable to get local issuer certificate". Browsers hide this by fetching
# the intermediate themselves. We do the same, but only trust the intermediate if the
# served leaf cert verifies through it against the system CA store.
setup_tls() {
    if curl -fsS -o /dev/null "${CURL_OPTS[@]}" "$PKG_URL" 2>/dev/null; then
        return 0
    fi

    printf "TLS verification failed, trying to fetch the missing intermediate...\n" >&2
    command -v openssl &>/dev/null || die "openssl is required for the certificate workaround"

    local host=${REPO_URL#https://}
    host=${host%%/*}

    local sysbundle=""
    local candidate
    for candidate in /etc/pki/tls/certs/ca-bundle.crt /etc/ssl/certs/ca-certificates.crt; do
        if [[ -r "$candidate" ]]; then sysbundle=$candidate; break; fi
    done
    [[ -n "$sysbundle" ]] || die "no system CA bundle found"

    TLS_TMP=$(mktemp -d)

    # Leaf certificate as served
    local sclient
    sclient=$(openssl s_client -connect "$host:443" -servername "$host" </dev/null 2>/dev/null || true)
    sed -n '/BEGIN CERTIFICATE/,/END CERTIFICATE/{p;/END CERTIFICATE/q;}' <<<"$sclient" > "$TLS_TMP/leaf.pem"
    [[ -s "$TLS_TMP/leaf.pem" ]] || die "could not retrieve the server certificate from $host"

    # Where does the issuer certificate live?
    local aia
    aia=$(openssl x509 -in "$TLS_TMP/leaf.pem" -noout -text \
          | sed -n 's/.*CA Issuers - URI:\(.*\)/\1/p' | sed -n 1p)
    [[ -n "$aia" ]] || die "leaf certificate has no CA Issuers URL; ask Anycubic to fix their chain"

    printf "Fetching intermediate from %s\n" "$aia" >&2
    curl -fsSL "$aia" -o "$TLS_TMP/inter.raw" || die "could not download intermediate"
    if ! openssl x509 -inform DER -in "$TLS_TMP/inter.raw" -out "$TLS_TMP/inter.pem" 2>/dev/null; then
        openssl x509 -in "$TLS_TMP/inter.raw" -out "$TLS_TMP/inter.pem" 2>/dev/null \
            || die "intermediate is neither DER nor PEM"
    fi

    # Only continue if the leaf really chains to a public root via this intermediate
    if ! openssl verify -CAfile "$sysbundle" -untrusted "$TLS_TMP/inter.pem" "$TLS_TMP/leaf.pem" >/dev/null 2>&1; then
        die "leaf does not verify through the downloaded intermediate; refusing to trust it"
    fi

    cat "$sysbundle" "$TLS_TMP/inter.pem" > "$TLS_TMP/bundle.pem"
    CURL_OPTS=(--cacert "$TLS_TMP/bundle.pem")

    curl -fsS -o /dev/null "${CURL_OPTS[@]}" "$PKG_URL" \
        || die "still cannot reach $PKG_URL after adding the intermediate"
    printf "Intermediate verified and used for this run only.\n" >&2
}

# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------
for tool in curl ar tar sha256sum sed awk; do
    command -v "$tool" &>/dev/null || die "$tool is not installed."
done
[[ -f "$SPEC_FILE" ]] || die "spec file not found: $SPEC_FILE"

setup_tls

# ---------------------------------------------------------------------------
# Locate and download the package
# ---------------------------------------------------------------------------
PACKAGES=$(curl -fsS "${CURL_OPTS[@]}" "$PKG_URL")
FILE_URI=$(awk '/^Filename:/ {print $2; exit}' <<<"$PACKAGES")
EXPECTED_SHA256=$(awk '/^SHA256:/ {print $2; exit}' <<<"$PACKAGES")
[[ -n "$FILE_URI" ]] || die "no Filename entry in Packages"
FILE_NAME=${FILE_URI##*/}

mkdir -p "$BUILD_SOURCES" "$BUILD_SPECS"
cp "$SPEC_FILE" "$BUILD_SPECS/"
TARGET_SPEC="$BUILD_SPECS/$(basename "$SPEC_FILE")"

cd "$BUILD_SOURCES"

if [[ -f "$FILE_NAME" ]]; then
    printf "Already downloaded %s\n" "$FILE_NAME"
else
    curl -fL -C - "${CURL_OPTS[@]}" -o "$FILE_NAME.part" "$REPO_URL/$FILE_URI"
    mv "$FILE_NAME.part" "$FILE_NAME"
fi

if [[ -n "$EXPECTED_SHA256" ]]; then
    echo "$EXPECTED_SHA256  $FILE_NAME" | sha256sum -c - \
        || { rm -f "$FILE_NAME"; die "checksum mismatch, removed $FILE_NAME"; }
else
    printf "Warning: no SHA256 in Packages, skipping verification\n" >&2
fi

# ---------------------------------------------------------------------------
# Extract and detect version
# ---------------------------------------------------------------------------
rm -rf "$TMP_DIR"
mkdir "$TMP_DIR"
cd "$TMP_DIR"

ar x "../$FILE_NAME"
tar xf data.tar.*

[[ -f "$PKG_VERSION_FILE" ]] || die "$PKG_VERSION_FILE not found in package."
PKG_VERSION=$(tr -d '\r\n[:space:]' < "$PKG_VERSION_FILE")
[[ -n "$PKG_VERSION" ]] || die "empty version in $PKG_VERSION_FILE"
PKG_VERSION=${PKG_VERSION//-/.}          # RPM forbids '-' in Version
printf "Found version: %s\n" "$PKG_VERSION"

# ---------------------------------------------------------------------------
# Update spec if the version changed
# ---------------------------------------------------------------------------
CURRENT_SPEC_VERSION=$(awk '/^Version:/ {print $2; exit}' "$TARGET_SPEC")
if [[ "$CURRENT_SPEC_VERSION" != "$PKG_VERSION" ]]; then
    printf "Updating spec file: %s -> %s\n" "$CURRENT_SPEC_VERSION" "$PKG_VERSION"
    sed -i "s/^Version:.*/Version:        $PKG_VERSION/; s/^Release:.*/Release:        1/" "$TARGET_SPEC"

    DATE_STR=$(LC_ALL=C date "+%a %b %d %Y")
    USER_NAME=$(git config user.name 2>/dev/null || echo "Automated Build")
    USER_EMAIL=$(git config user.email 2>/dev/null || echo "automated@build.local")
    CHANGELOG_ENTRY="* $DATE_STR $USER_NAME <$USER_EMAIL> - $PKG_VERSION-1\n- Updated to version $PKG_VERSION\n- converted from $FILE_NAME"
    sed -i "/^%changelog/a $CHANGELOG_ENTRY\n" "$TARGET_SPEC"

    cp "$TARGET_SPEC" "$SPEC_FILE"
    printf "Updated template: %s\n" "$SPEC_FILE"
fi

# ---------------------------------------------------------------------------
# Build the source tarball
# ---------------------------------------------------------------------------
TARBALL="anycubicslicernext-$PKG_VERSION.tar.bz2"
if [[ -f "$BUILD_SOURCES/$TARBALL" ]]; then
    printf "Tarball %s already exists, skipping...\n" "$TARBALL"
    printf "To build the RPM, run:\nrpmbuild -ba %s\n" "$TARGET_SPEC"
    exit 0
fi

rm -fv data.tar.* control.tar.* debian-binary usr/LICENSE.txt
if [[ -d usr/lib && ! -e usr/lib64 ]]; then
    mv -v usr/lib usr/lib64
fi

# Informational: anything outside resources/ that the spec's %files may need to cover
printf "\nFiles outside AnycubicSlicerNext/resources (check against %%files):\n"
find usr -type f ! -path 'usr/share/AnycubicSlicerNext/resources/*' | sed 's/^/  /'

cd "$BUILD_SOURCES"
SRC_DIR="anycubicslicernext-$PKG_VERSION"
rm -rf "$SRC_DIR"
mv "$TMP_DIR" "$SRC_DIR"
tar cjf "$TARBALL" "$SRC_DIR"
rm -rf "$SRC_DIR"

printf "\nSuccess! To build the RPM, run:\nrpmbuild -ba %s\n" "$TARGET_SPEC"
