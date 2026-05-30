// Bicep template for the University AI Assistant core Azure resources.
// Deploy with:
//   az deployment group create -g <rg> -f main.bicep -p prefix=uniai location=eastus

@description('Resource name prefix.')
param prefix string = 'uniai'

@description('Azure region for all resources.')
param location string = resourceGroup().location

@description('SKU for the Azure AI Search service.')
param searchSku string = 'basic'

var storageName = toLower('${prefix}stor${uniqueString(resourceGroup().id)}')
var searchName = '${prefix}-search'
var openAiName = '${prefix}-openai'

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storage
  name: 'default'
}

resource documentsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: 'documents'
  properties: {
    publicAccess: 'None'
  }
}

resource search 'Microsoft.Search/searchServices@2024-03-01-preview' = {
  name: searchName
  location: location
  sku: {
    name: searchSku
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
  }
}

resource openAi 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: openAiName
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: openAiName
    publicNetworkAccess: 'Enabled'
  }
}

output storageAccountName string = storage.name
output searchServiceName string = search.name
output openAiEndpoint string = openAi.properties.endpoint
