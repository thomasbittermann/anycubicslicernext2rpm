#!/bin/bash

# Konfiguration
REPO_URL="https://cdn-universe-slicer.anycubic.com/prod"
DIST_NAME="noble"  # z. B. noble (24.04), jammy (22.04)
ARCH="amd64"
COMP=main
PKG_URL="${REPO_URL}/dists/${DIST_NAME}/${COMP}/binary-${ARCH}/Packages"
FILE_URI=$(curl -s "$PKG_URL" | grep "^Filename:" | awk '{print $2}')
FILE_NAME=$(echo "$FILE_URI" | perl -pe 's;.*/([^/]+);$1;')
PKG_VERSION=$(echo $FILE_NAME | perl -pe 's/.*Next-([^_]+).*/$1/')

cd $HOME/rpmbuild/SOURCES

if [[ -f "$FILE_NAME" ]]; then
    echo "already downloaded $FILE_NAME"
    exit 1
fi

wget -nc "$REPO_URL/$FILE_URI"

SRC_DIR="anycubicslicernext-$PKG_VERSION"
rm -rf "$SRC_DIR"
mkdir "$SRC_DIR"
cd "$SRC_DIR"
ar x "../$FILE_NAME"
tar xzf data.tar.gz
rm -v *.gz debian-binary usr/LICENSE.txt
mv -v usr/lib{,64}
cd ..
tar cjf "$SRC_DIR".tar.bz2 "$SRC_DIR"
