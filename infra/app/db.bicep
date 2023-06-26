param accountName string
param location string = resourceGroup().location
param tags object = {}

param collections array = [
  {
    name: 'Environments'
    id: 'Environments'
    shardKey: 'Hash'
    indexKey: '_id'
  }
  {
    name: 'Rooms'
    id: 'Rooms'
    shardKey: 'Hash'
    indexKey: '_id'
  }
  {
    name: 'Objects'
    id: 'Objects'
    shardKey: 'Hash'
    indexKey: '_id'
  }
  {
    name: 'Users'
    id: 'Users'
    shardKey: 'Hash'
    indexKey: '_id'
  }
]
param databaseName string = ''
param keyVaultName string

// Because databaseName is optional in main.bicep, we make sure the database name is set here.
var defaultDatabaseName = 'adt-tfg'
var actualDatabaseName = !empty(databaseName) ? databaseName : defaultDatabaseName

module cosmos '../core/database/cosmos/mongo/cosmos-mongo-db.bicep' = {
  name: 'cosmos-mongo'
  params: {
    accountName: accountName
    databaseName: actualDatabaseName
    location: location
    collections: collections
    keyVaultName: keyVaultName
    tags: tags
  }
}

output connectionStringKey string = cosmos.outputs.connectionStringKey
output databaseName string = cosmos.outputs.databaseName
output endpoint string = cosmos.outputs.endpoint
