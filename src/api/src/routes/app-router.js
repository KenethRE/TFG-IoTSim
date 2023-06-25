import { Router } from 'express'
import controller200 from '../controllers/controller-200.js'
import controller500 from '../controllers/controller-500.js'
import controllerException from '../controllers/controller-exception.js'

const appRouter = Router()

appRouter.get('/200', controller200)
appRouter.get('/500', controller500)
appRouter.get('/exception', controllerException)

export default appRouter