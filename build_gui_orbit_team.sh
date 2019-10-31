#!/bin/bash

export PACKAGE_NAME=${PACKAGE_NAME:-orbit-team-dev}

# convert the NEXUS_DOCKER_REGISTRY to the project specific domain if not converted before
if [[ $NEXUS_DOCKER_REGISTRY != *"$PACKAGE_NAME"* ]]; then
  export NEXUS_DOCKER_REGISTRY="$NEXUS_DOCKER_REGISTRY/$PACKAGE_NAME"
fi

python -m pip install setuptools_scm docker

pip_version=`foundations_contrib/src/foundations_contrib/resources/get_version.sh`
export build_version=`echo $pip_version | sed 's/+/_/g'`


if [ $? -eq 0 ]
then
    rm -rf tmp/pip_wheels \
        && mkdir -p tmp/pip_wheels \
        && cp dist/* tmp/pip_wheels \
        && python build_gui_orbit_team.py
fi