import express, { json, urlencoded } from 'express'
import logger from './components/log.js'
import authenticate from './components/authentication.js'
import appRouter from './routes/app-router.js'
import { errorMiddleware } from './components/error-handler.js'
import { setStore } from './components/async-local-storage.js'
import { metrics } from './components/metrics.js'
import { PORT } from './config.js'

const app = express()
//express helpers
app.disable('x-powered-by')
app.use(json())
app.use(urlencoded({ extended: true }))
//set request store
app.use(setStore)
//prometheus
app.use(metrics)
//authentication filter
app.use(authenticate)
//bussiness logic router
app.use(appRouter)
//404 error
app.use((req, res, next) => next({status:404}))
//error handler
app.use(errorMiddleware)
//start app
app.listen(PORT, async () => logger.info(`Application listening on port ${PORT}`))