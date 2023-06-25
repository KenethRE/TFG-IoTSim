import { Counter } from 'prom-client'
import express_prom_bundle from 'express-prom-bundle'

//default metrics
const metrics = express_prom_bundle({includeMethod: true})

const request_ok = new Counter({
    name: 'request_ok',
    help: 'request_ok'    
})

const request_ko = new Counter({
    name: 'request_ko',
    help: 'request_ko',
    labelNames: ['statusCode']
})

export { 
    metrics,
    request_ok,
    request_ko
}