FROM node:latest

# Create app directory
WORKDIR /usr/src/app

COPY ./Node/app.js /usr/src/app/app.js

# Install app dependencies
COPY ./Node/package.json /usr/src/app/package.json
RUN npm install

# Bundle app source
COPY ./Node /usr/src/app

EXPOSE 3000
CMD [ "npm", "start" ]