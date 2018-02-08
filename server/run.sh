#!/usr/bin/bash

# print the commands ran in this script
set -x

function _() {
    echo "==> $@"
}

function jumpto
{
    label=$1
    cmd=$(sed -n "/$label:/{:a;n;p;ba};" $0 | grep -v ':$')
    eval "$cmd"
    exit
}

_ "Cloning the source repository..."
git clone $SOURCE_REPOSITORY_URL||jumpto sendstatusmail


source_dirname=${SOURCE_REPOSITORY_URL##*/}
if [[ "$source_dirname" == *.git ]]
then
    source_dirname=${source_dirname%????}
fi

_ "Entering directory ${source_dirname##*/}"
cd ${source_dirname##*/}

_ "Changing repo branch ${REPO_BRANCH}"
git checkout $REPO_BRANCH||jumpto sendstatusmail

buildpath=${REPO_BUILD_PATH##/}
if [ "$buildpath" == "" ]; then
    buildpath="."
fi

_ "Going to build path "
cd ${buildpath}

_ "Checking cccp.yml exists or rename similar"
if [ ! -f cccp.yml ]; then
    mv *cccp.y*ml cccp.yml
    mv .cccp.y*ml cccp.yml
fi

_ "Copying index reader to docker file"
cp /cccp_reader.py .

_ "Put build,test, delivery scripts in proper place"
#python cccp_reader.py $TARGET_FILE

#_ "Adding index reader to docker file"
#echo "ADD /build_script /usr/bin/" >> $TARGET_FILE
#echo "ADD /test_script /usr/bin/" >> $TARGET_FILE
#echo "ADD /delivery_script /usr/bin/" >> $TARGET_FILE

# Alter target file, if openshift container is detected
CONTAINER_NAME="${APPID}/${JOBID}";
if [[ ${CONTAINER_NAME} =~ ^openshift\/(origin.*|node|openvswitch) ]]; then
    _ "Openshift container detected, checking if  ${TARGET_FILE} needs to be altered";
    if [[ ( ${DESIRED_TAG} == "v1.5" && ${CONTAINER_NAME} != "openshift/origin-base" ) && ${CONTAINER_NAME} != "openshift/origin-source" ]]; then
        sed -i "/^FROM/ s/$/:${DESIRED_TAG}/" ${TARGET_FILE};
    fi
fi

_ "Building the image in ${buildpath} with tag ${JOBID}:${TAG}"
docker build --rm --no-cache -t $JOBID:$TAG -f $TARGET_FILE ${BUILD_CONTEXT} || jumpto sendstatusmail

#_ "Checking local files form container"
#ls -a /set_env/

#_ "Running build steps"
#docker run --rm $TAG --entrypoint /bin/bash /usr/bin/build_script

TO=`python -c 'import json, os; print json.loads(os.environ["BUILD"])["spec"]["output"]["to"]["name"]'`

#TO=${DOCKER_REGISTRY_SERVICE_HOST}:${DOCKER_REGISTRY_SERVICE_PORT}/$TAG

docker tag ${JOBID}:${TAG} ${TO}

_ "Pushing the image to registry (${TO})"

if [[ -d /var/run/secrets/openshift.io/push ]] && [[ ! -e /root/.dockercfg ]]; then
  _ "Copying the dockercfg to home dir"
  cp /var/run/secrets/openshift.io/push/.dockercfg /root/.dockercfg
fi

if [ -n "${TO}" ] || [ -s "/root/.dockercfg" ]; then
  docker push "${TO}" || jumpto sendstatusmail
fi

_ "Cleaning environment"
docker rmi ${JOBID}:${TAG}
jumpto end

sendstatusmail:
  exit 1

end:
  exit 0
