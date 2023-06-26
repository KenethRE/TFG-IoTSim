import { ENABLE_AUTH, AUTH_HEADER } from '../config.js'

const authenticate = async (req, res, next) => {
    if(ENABLE_AUTH){
        const authHeader = req.header(AUTH_HEADER)

        if (!authHeader) {
            next({status:401})    
        } else {
            //token authentication
            next()
        }
    }else{
        next()
    }
}

export default authenticate