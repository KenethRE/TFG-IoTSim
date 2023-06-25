import { AsyncLocalStorage } from 'node:async_hooks'
import { v4 as uuidv4 } from 'uuid'
import { TRACE_ID_HEADER, SPAN_ID_HEADER } from '../config.js'

const asyncLocalStorage = new AsyncLocalStorage()

const setStore = (req, res, next) => {
    const traceId = req.header[TRACE_ID_HEADER] ? req.header[TRACE_ID_HEADER] : uuidv4()
    const spanId = uuidv4()
    //set context
    asyncLocalStorage.run(new Map(), () => {
        asyncLocalStorage.getStore().set('traceContext', {traceId, spanId})
        res.header(TRACE_ID_HEADER, traceId)
        res.header(SPAN_ID_HEADER, spanId)
        return next()
    })
}

const getStore = (key) => {
    if(asyncLocalStorage.getStore()){
        return asyncLocalStorage.getStore().get(key)
    }else{
        return null
    }    
}

export {
    setStore,
    getStore
}