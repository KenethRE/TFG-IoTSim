## KOALA example app
The purpose of this repository is to show a set of good practices or guidelines to organize the code of a modern microservice. It is based on common practices in the industry, and falls somewhere, according to KOALA's context/needs, between simple examples like the one given by [express](https://expressjs.com/en/starter/generator.html), and more professional options like [nest.js](https://nestjs.com/)

Special emphasis has been placed on features such as tracing and logs, error handling (critical especially in node apps), readability, and code reusability.

## Contents
1. [App](#app)
2. [Config](#config)
3. [Routes](#routes)
4. [Controllers](#controllers)
5. [Components](#components)
    1. [Async local storage](#async-local-storage)
    2. [Error handler](#error-handler)
    3. [Log](#log)
    4. [Metrics](#metrics)
    5. [JWT auth](#jwt-auth)
6. [Resources](#resources)
7. [Module system](#module-system)
8. [Style](#style)
9. [Docker image](#docker-image)
10. [Next steps](#next-steps)

## App
The app.js file in the root directory is the entry point of the application. It should only be limited to chaining middlewares, business logic handlers (usually grouped by routers) and error handlers.

We should avoid any kind of implementation or unrelated code, so that at a glance we can easily see all the layers a request goes through.

## Config

The configuration file will contain, as a constant, the variables that are configured locally for the microservice, and not in the specific centralized platform.

Normally the values will be obtained through the docker environment, using **process.env.VAR_NAME**

Hardcoded values should be avoided at all costs.

## Routes

Route files are used to easily see the mapping between a route and the code that handles it.

In an API rest resources are exposed, therefore it is a good way to organize the routes with a router for each one, that is to say for each resource, a router, in a file, with its declared routes and the handlers of each one apart.

This last point is important, since this way we obtain a clean and easy to read file, so that we can see all the routes of our application, or to go quickly to the code behind a route, without need of scroll, searches, etc...

## Controllers
In the controllers directory we should have all the handlers referenced in the routes file, or what is the same, the implementations of each one of these routes.

It is advisable to name each one of these files in a way that they can be easily associated to the route they implement (getUser.js, postUser.js, etc).

In case of having many routes grouped in routers, a directory can be created for each router, and put inside the respective files

The code of these files should be easy to read, avoid complex implementations (they will be moved to the components) so that you can easily see the logic that follows, validations, services, possible errors, etc.

## Components
Application components are the main way to reuse code and abstract/encapsulate complex implementations.

Clear examples of reusability are components common to the entire app, such as the log.
An example of encapsulation (also reusability) would be a client to an external service, such as a database.

This avoids duplication of code and keeps the code easy to read at the higher level layers (controllers).

It is important that these components **are not coupled, or in other words, that they have an API linked to the action they perform, and not to the service in which they are present**. This way we leave the door open to reuse these components in other microservices or extract them to a library common to all, if necessary.

An example of coupling would be to return an error specific to the microservice in a component.

### Async local storage
This component is a middleware that creates a context for each request, which will be available at all times, it is the equivalent of local thread storage in other languages.

This is especially useful to avoid passing extra parameters that would create large coupling in the components API.

In this app it is only used so that each request has a tracing context, with a trace and span id. This way the log component can access this context and log with traceability.

This component also adds trace and span id to the response headers.

### Error handler
This component function is to have all the logic related to errors centralized in a single place.
It provides a middleware to capture unrecoverable errors, and a handler to manage them, whether they come from the middleware itself, from a job, test, etc.

The idea is to always propagate non-recoverable errors (an object that does not pass validation for example) and exceptions, so that they reach the error handler, which will be in charge of logging and generating the correct response.
The case of exceptions is particularly critical in node js, since any uncontrolled error will stop our service.

This way we eliminate the need to use catch in all the code, practice that in the end is not sustainable, since we cannot guarantee that sooner or later there will not be an error out of a try. In addition this way we avoid duplicating code.

Recoverable errors should be handled, using try/catch in synchronous code, or Promise.catch in asynchronous code.

It can also be the case of a component that propagates a generic error (for example an error when inserting into a database due to incorrect formatting). In this case you can catch the error in the consumer of that component (usually the controller) and propagate a corresponding error (400 - bad request).
We should avoid things like a database component returning HTTP errors (mixing of concepts, coupling, etc).

### Log
This component is simply a wrapper over the logging library, in this case winston. The idea is to add the necessary metadata to the logger in a single point. 

In this app the tracing, context, and span id data are added through the store provided by the async-local-storage component.

### Metrics
Component for metrics. It is very simple, just expose to the rest of the code Prometheus counters, gauges or histogram.

### JWT auth
Very basic example of a middleware that acts as a JWT filter, checking if there is a token in the request.

## Resources
Under this directory we can have any file that does not contain code as such, for example certificates, Swagger json files, etc.
It's a bit like the wildcard folder

## Module System
Well, this is a very recurrent topic, common-js vs ES-modules.

The truth is that there is no obvious choice, common-js is the nodejs standard, when javacript itself did not have a module system, and ES-modules is the current javascript standard.

Each has advantages and disadvantages, common-js can be used anywhere in the code, conditionally for example, and ES-modules allows to load code asynchronously.

We have opted for ES-modules, because it is establishing itself as the industry standard, node-js itself has done to support it, and there are many libraries that are moving away from supporting common-js (although there are also older libraries that only support common-js).

Anyway, the trend seems to be ES-modules.

## Style
It is important that the code follows minimum style standards, so that all code is written in a similar way.
Obviously the choice is totally arbitrary and subjective, but, you have to choose, there really are no universal guidelines.

In this example app a linter is used to ensure these style guidelines, [eslint](https://eslint.org/).
The configuration file (.eslintrc.cjs) is configured as follows:
- 4 spaces indent
- es2021 javascript version in nodeJS
- unix line breaks
- single quotes
- no semicolon

Apart from the linter the nomenclature used is:
- vars: lowerCamelCase
- functions/classes: UpperCamelCase
- constants: CAPS

Additional recommendations:
- avoid var, in favor of let and const.
- use === operator
- avoid callbacks, use promises instead and async await
- use ES6 notation for functions
- as much as possible, group code into small functions
- use self-descriptive function/variable names
- comment the code
- avoid spaghetti code, things like many nested loops, count/aux vars, i j vars, etc. 
Code should be easy to read.

## Docker image
Two files are responsible for generating the docker image:
- Dockerfile: generates the image, it is parameterized so as not to have to change it regularly.
- docker-build.sh is a bash script that runs the dockerfile by passing parameters to it.

Simply with this you can build the image, the code is not necessary, since it is obtained by doing a pull to git, just execute sh script:

./docker-build.sh

The idea is to have a generic builder (the sh script) and multiple docker files, one per service.
Simply with this you can build the image, the code is not necessary, since it is obtained by doing a pull to git.

Regarding the image itself, it is built in multistage to save as much space as possible.
The final base image is distroless, the usual standard for mainly security reasons, as well as size.
The node-prune binary has been included in the code to avoid downloading and compiling it in the build phase (it's done in GOLANG).

## Next steps

This sample application currently has some clear points for improvement to consider:
- Swagger docs: standard to document rest API
- Unit test: the time cost of not having them, in the form of bugs and low-quality software, is exponentially higher than the time to develop them.
- Typescript: real gamechanger when developing business js, that is, many people touching the same code. In small projects or with a very disciplined team it is not so necessary, but it should be taken into account.