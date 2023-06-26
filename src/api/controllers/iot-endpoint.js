// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

import { DefaultAzureCredential } from '@azure/identity'
import { DigitalTwinsClient } from '@azure/digital-twins-core'
import inspect from 'util'
import { ADT_ENDPOINT, AZURE_CLIENT_ID, AZURE_TENANT_ID } from '../config/metaconfig.json'

// Simple example of how to:
// - create a DigitalTwins Service Client using the DigitalTwinsClient constructor
// - query digital twins
//
// Preconditions:
// - Environment variables have to be set
// - DigitalTwins enabled device must exist on the ADT hub

const iot_endpoint = async(req, res, next) => {
    // - AZURE_URL: The tenant ID in Azure Active Directory
    //const url = process.env.AZURE_URL
    process.env.AZURE_CLIENT_ID = AZURE_CLIENT_ID
    process.env.AZURE_TENANT_ID = AZURE_TENANT_ID

    // DefaultAzureCredential expects the following three environment variables:
    // - AZURE_TENANT_ID: The tenant ID in Azure Active Directory
    // - AZURE_CLIENT_ID: The application (client) ID registered in the AAD tenant
    // - AZURE_CLIENT_SECRET: The client secret for the registered application


    //const credential = new InteractiveBrowserCredential({
    //   tenantId: AZURE_TENANT_ID,
    //   clientId: AZURE_CLIENT_ID
    //})
    const serviceClient = new DigitalTwinsClient(ADT_ENDPOINT, new DefaultAzureCredential())
    
    // Query digital twins
    const queryResult = serviceClient.queryTwins(req.query)
    res.send(queryResult)
}

iot_endpoint().catch((err) => {
    console.log('error code: ', err.code)
    console.log('error message: ', err.message)
    console.log('error stack: ', err.stack)
})
export default (req, res, next) => iot_endpoint(req, res).catch(next)