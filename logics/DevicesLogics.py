import requests
import json
import sys
import os
import urllib.parse

sys.path.insert(1, './libs')
sys.path.insert(1, './transformers')
import DataUtils
import GenericTransformers
import DevicesTransformers
import StdResponses
import StdAPIUtils

def get_device_update_resrouces(sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(token)

    api_call_type = "POST"
    #print("Debug:"+JsonData['deviceid'])
# Modify True to False if you wish to untrust a device as opposed to trust it
    variables = {"deviceID":JsonData['itemid'] ,"isTrusted":JsonData['trust']}

    Body = """
    mutation
        updateDeviceTrust($deviceID: ID!, $isTrusted: Boolean!){
            deviceUpdate(id: $deviceID, isTrusted: $isTrusted) {
                ok
                error
                entity {
                    id
                    name
                    isTrusted

                }
            }
        }
    """

    return True,api_call_type,Headers,Body,variables


def get_device_list_resources(sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(token)

    api_call_type = "POST"

    Body = """{
          devices(after: null, first:10000) {
            edges {
              node {
                id
                name
                isTrusted
                osName
                deviceType
                lastFailedLoginAt
                lastSuccessfulLoginAt
                osVersion
                hardwareModel
                hostname
                username
                serialNumber
                user{
                    firstName
                    lastName
                    email
                }
                lastConnectedAt
                osName
                deviceType
                clientVersion
                manufacturerName
              }
            }
            pageInfo {
              startCursor
              hasNextPage
            }
          }
        }"""

    return True,api_call_type,Headers,Body,None

def get_device_show_resources(sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(token)

    api_call_type = "POST"
    variables = {"deviceID":JsonData['itemid']}
    Body = """
         query
            getDevice($deviceID: ID!){
          device(id:$deviceID) {
            id
            name
            isTrusted
            osName
            deviceType
            lastFailedLoginAt
            lastSuccessfulLoginAt
            osVersion
            hardwareModel
            hostname
            username
            serialNumber
            user
            lastConnectedAt
            osName
            deviceType
            clientVersion
            manufacturerName
              }
          }
    """

    return True,api_call_type,Headers,Body,variables


def item_list(outputFormat,sessionname,idsfile,idsonly):
    r,j = StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_device_list_resources,{},GenericTransformers.GetListAsCsv,"devices")
    if idsonly:
        j = GenericTransformers.GetIds(j,"devices")
        print(j)
        exit(0)
    else:
        if idsfile != "":
            itemsAdded,itemsRemoved = GenericTransformers.GetIdsAndCompareToFile(j,idsfile,"devices")
            print({'itemsAddedCount':len(list(itemsAdded)),'itemsAdded':list(itemsAdded),'itemsRemovedCount':len(list(itemsRemoved)),'itemsRemoved':list(itemsRemoved)})
        else:
            print(r)

def item_show(outputFormat,sessionname,itemid):
    r,j = StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_device_show_resources,{'itemid':itemid},DevicesTransformers.GetShowAsCsv,"devices")
    print(r)
def item_update(outputFormat,sessionname,itemid,trust):
    r,j = StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_device_update_resrouces,{'itemid':itemid,'trust':trust},DevicesTransformers.GetUpdateAsCsv,"devices")
    print(r)
