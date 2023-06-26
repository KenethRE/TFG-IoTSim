import logger from '../components/log.js'

const request500 = async (req, res, next) => {

    logger.info('controlled error request example')

    const error = {
        'status': 500,
        'message': 'request failed example'
    }

    next(error)
}

export default (req, res, next) => request500(req, res, next).catch(next)