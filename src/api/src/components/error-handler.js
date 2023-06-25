import status from 'http-status'
import logger from './log.js'

// eslint-disable-next-line no-unused-vars
const errorMiddleware = (err, req, res, next) => {
    const error = handleAndEnd(false)(err)
    res.status(error.code)
    res.json(error)
}

// end set to:
// true, non recoverable errors, like startup
// false everything else, job /routes
const handleAndEnd = (end) => (err) => {
    const statusCode = err.status ? err.status : 500
    const statusReason = status[statusCode]

    // log error
    const mesage = err.message === undefined ? '' : ` - ${err.message}`
    const stack = err.stack === undefined ? '' : ` - ${err.stack}`
    const log_trace = `Error ${statusCode} - ${statusReason}${mesage}${stack}`
    logger.error(log_trace)

    if(end){
        process.exit()
    }else{
        return {
            'code': statusCode,
            'reason': statusReason
        }
    }
}

export { errorMiddleware, handleAndEnd }