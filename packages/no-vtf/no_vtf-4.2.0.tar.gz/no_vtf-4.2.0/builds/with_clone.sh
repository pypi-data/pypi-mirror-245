#!/bin/bash

# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common || exit

git_cmd=()
while [ "$1" != '--' ]; do
    [ -n "$1" ]
    git_cmd+=("$1")
    shift
done
shift

[ -n "$1" ]

cd "$(mktemp --directory)"
# realpath hack to workaround Wine not accepting absolute Unix paths as-is
"${git_cmd[@]}" clone --quiet --no-checkout "$(realpath --relative-to=. "$OLDPWD")" .
"${git_cmd[@]}" checkout --quiet HEAD

exec "$@"
