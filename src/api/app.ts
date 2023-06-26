import express, { Express } from "express";
const bodyParser = require('body-parser')
const metaconfig = require('./config/metaconfig.json')
const { getConfig } = require('./config/config')
const cors = require('cors')
const { configureMongoose } = require('./components/mongoose')
const { observability } = require('./config/observability')
import { logger } from './config/observability'

const allowOrigins = process.env.API_ALLOW_ORIGINS || '*'

export const startServer = async (): Promise<Express> => {
    logger.info('Starting application...')
    const config = await getConfig()
    const app = express()

    observability(config.observability)
    await configureMongoose(config.database)
    app.use(bodyParser.json())
    app.use(express.json())
    app.use(cors({ origin: allowOrigins }))

    //express helpers
    app.disable('x-powered-by')
    app.use(express.urlencoded({ extended: true }))
    //404 error
    app.use((req, res, next) => next({status:404}))
}

