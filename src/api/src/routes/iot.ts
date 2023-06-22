import * as coreHttp from "@azure/core-http";
import * as coreArm from "@azure/core-arm";
import * as msRestNodeAuth from "@azure/ms-rest-nodeauth";
import {
  AzureDigitalTwinsAPI,
  AzureDigitalTwinsAPIModels,
  AzureDigitalTwinsAPIMappers
} from "@azure/digital-twins";
import express from "express";

const router = express.Router({ mergeParams: true });

router.get("/", async (req, res) => {

const subscriptionId = process.env["AZURE_SUBSCRIPTION_ID"];
msRestNodeAuth
  .interactiveLogin()
  .then((creds) => {
    const client = new AzureDigitalTwinsAPI(creds, subscriptionId);
    const dependenciesFor = ["testdependenciesFor"];
    const includeModelDefinition = true;
    const maxItemCount = 1;
    client.digitalTwinModels
      .list(dependenciesFor, includeModelDefinition, maxItemCount)
      .then((result) => {
        console.log("The result is:");
        console.log(result);
      });
  }
  .catch((err) => {
    console.error(err);
  }};

export default router;