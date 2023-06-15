var mongoClient = require("mongodb").MongoClient;
mongoClient.connect("mongodb://tfg-mongodb:rwd3TIxjxr1MM026O3S80LzBrcSx9FGESMdnhJcvHd8rBvyucVExO6RQJOVmrEo6wcOaxEZRmVTWACDb5bLWmg%3D%3D@tfg-mongodb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&maxIdleTimeMS=120000&appName=@tfg-mongodb@", function (err, client) {
  client.close();
});