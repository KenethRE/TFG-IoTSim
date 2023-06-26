import logger from '../components/log.js'
import { request_ok } from '../components/metrics.js'

// eslint-disable-next-line no-unused-vars
const request200 = async (req, res, next) => {

    logger.info('successfull request example')

    request_ok.inc(1)

    const response = {
        'code': '200',
        'mesage': 'request ok'
    }

    res.json(response)
}

export default (req, res, next) => request200(req, res, next).catch(next)