import winston from 'winston'
import { LOG_LEVEL, LOG_JSON } from '../config.js'
import { getStore } from './async-local-storage.js'

const logFormat = (info) => {        
    if(info.traceContext){
        return `[${info.timestamp}] [${info.level}] [${info.traceContext.traceId}] [${info.traceContext.spanId}] ${info.message}`
    }else{
        return `[${info.timestamp}] [${info.level}] ${info.message}`
    }        
}

const logFormatJSON = (info) => {        
    if(!info.traceContext){
        delete info.traceContext
    }
    return JSON.stringify(info)       
}

if(LOG_JSON){
    winston.configure({
        level: LOG_LEVEL.toLowerCase(),
        transports: [new winston.transports.Console({
            format: winston.format.combine(
                winston.format.timestamp({
                    format:'YY-MM-DD HH:mm:ss'
                }),
                winston.format.printf(logFormatJSON)
            )
        })],
    })
}else{
    winston.configure({
        level: LOG_LEVEL.toLowerCase(),
        transports: [new winston.transports.Console({
            format: winston.format.combine(
                winston.format.colorize(),
                winston.format.timestamp({
                    format:'YY-MM-DD HH:mm:ss'
                }),
                winston.format.printf(logFormat)
            )
        })],
    })

    winston.addColors({
        info: 'italic green', 
        warn: 'italic yellow',
        error: 'italic red',
        debug: 'italic cyan',
    })
}

const logger = {
    debug: (message) => winston.debug(message, {traceContext:getStore('traceContext')}),
    info: (message) => winston.info(message, {traceContext:getStore('traceContext')}),
    warn: (message) => winston.warn(message, {traceContext:getStore('traceContext')}),
    error: (message) => winston.error(message, {traceContext:getStore('traceContext')})
}

export default logger