# stage 1
FROM node:18.12.1-bullseye AS BUILD_IMAGE
# get env params
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG GIT_ACCESS
ARG GIT_TAG
# set HPE proxy
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}
# install GIT and get source code
RUN apt-get -y update && \
    apt-get install -y  dpkg-dev  git && \
    git clone --depth 1 --branch ${GIT_TAG} ${GIT_ACCESS}/hpe/VAMP_KOALA_nodeapp_structure
# set source code directory
WORKDIR /VAMP_KOALA_nodeapp_structure
# install node prune
RUN chmod u+x node-prune
RUN mv node-prune /usr/local/bin
# install app dependencies
RUN npm ci --only=production
# remove development dependencies
RUN npm prune --production
# run node prune to remove not needed files in dependencies
RUN node-prune

#stage 2
FROM gcr.io/distroless/nodejs18-debian11
# set app directory
WORKDIR /
# copy only required source code from build image
# distroless images search code under "node" folder by default
COPY --from=BUILD_IMAGE /VAMP_KOALA_nodeapp_structure/package*.json /node/
COPY --from=BUILD_IMAGE /VAMP_KOALA_nodeapp_structure/app.js /node/
COPY --from=BUILD_IMAGE /VAMP_KOALA_nodeapp_structure/config.js /node/
COPY --from=BUILD_IMAGE /VAMP_KOALA_nodeapp_structure/node_modules /node/node_modules
COPY --from=BUILD_IMAGE /VAMP_KOALA_nodeapp_structure/components /node/components
COPY --from=BUILD_IMAGE /VAMP_KOALA_nodeapp_structure/controllers /node/controllers
COPY --from=BUILD_IMAGE /VAMP_KOALA_nodeapp_structure/routes /node/routes
# set ports
EXPOSE 5000
# start app
CMD [ "node", "app.js" ]