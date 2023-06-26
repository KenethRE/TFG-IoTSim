import { startServer } from "./app";
import { logger } from "./config/observability";
const metaconfig = require('./config/metaconfig.json')

const main = async () => {
    const app = await startServer();
    const port = process.env.FUNCTIONS_CUSTOMHANDLER_PORT || process.env.PORT || metaconfig.PORT || 3100;

    app.listen(port, () => {
        logger.info(`Started listening on port ${port}`);
    });
};

main();