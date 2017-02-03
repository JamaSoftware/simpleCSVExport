import requests
import json


class Jama:
    def __init__(self):
        # replace {base_url}, username and password
        self.baseURL = "{base_url}/rest/v1/"
        self.username = "username"
        self.password = "password"
        self.auth = (self.username, self.password)

    def getItems(self, itemTypeId):
        # get all items of the specified item type
        return self.getAll("abstractitems?itemType={}".format(itemTypeId))

    def getProjects(self):
        return self.getAll("projects")

    def getItemTypes(self):
        # using this for the item type IDs and not for the configuration of fields
        return self.getAll("itemtypes")

    def getComments(self):
        return self.getAll("comments")

    def getRelationships(self, projectId):
        relationships = self.getAll("relationships?project={}".format(projectId))
        for relationship in relationships:
            relationship["project"] = projectId
        return relationships

    def getAll(self, resource):
        allResults = []
        resultsRemaining = True
        currentStartIndex = 0
        delim = '&' if '?' in resource else '?'
        while resultsRemaining:
            startAt = delim + "startAt={}".format(currentStartIndex)
            url = self.baseURL + resource + startAt
            print url
            response = requests.get(url, auth=self.auth)
            jsonResponse = json.loads(response.text)
            if "pageInfo" not in jsonResponse["meta"]:
                return [jsonResponse["data"]]
            resultCount = jsonResponse["meta"]["pageInfo"]["resultCount"]
            totalResults = jsonResponse["meta"]["pageInfo"]["totalResults"]
            print "startIndex={}".format(currentStartIndex)
            print "totalResults={}".format(totalResults)
            print "resultCount={}".format(resultCount)
            print "\n\n"
            resultsRemaining = currentStartIndex + resultCount != totalResults
            currentStartIndex += 20
            allResults.extend(jsonResponse["data"])

        return allResults

