#!/usr/bin/env bash

# shellcheck disable=SC2164
pushd "$( dirname $0 )" > /dev/null
CURDIR=$( pwd )
echo $CURDIR

# build base images
docker build $1 -t hyperbill-api:0.0 -f docker/base/hyperbill-api/Dockerfile $CURDIR

# shellcheck disable=SC2164
popd > /dev/null
