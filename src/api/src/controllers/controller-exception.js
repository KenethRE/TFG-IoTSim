import logger from '../components/log.js'

// eslint-disable-next-line no-unused-vars
const requestException = async (req, res, next) => {

    logger.info('uncontrolled error request example')

    //exception,try catch not required
    // eslint-disable-next-line no-shadow-restricted-names
    const undefined = undefined
    undefined.fakeValue
}

export default (req, res, next) => requestException(req, res, next).catch(next)