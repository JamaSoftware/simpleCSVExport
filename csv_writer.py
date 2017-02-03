import codecs
import csv
from BeautifulSoup import BeautifulSoup

import cStringIO
from collections import OrderedDict


class CSVWriter:
    def write(self, filename, items):
        writer = UnicodeWriter(open(filename, "wb"), dialect="excel")

        # aggregate the keys into a set across all artifacts of this type
        keySet = set()
        for item in items:
            for key, value in item.iteritems():
                # resources is an api-specific field that isn't relevant,
                # and we want id to be up front in the column list so we add it later
                if key != "id" and key != "resources":
                    self.getKeyPath(key, value, keySet)
        keyList = ["id"]
        keyList.extend(sorted(keySet))
        writer.writerow(keyList)

        for item in items:
            try:
                item["createdDate"] = item["createdDate"][:-9]
                item["modifiedDate"] = item["modifiedDate"][:-9]
            except KeyError:
               pass
            try:
                item["lock"]["lastLockedDate"] = item["lock"]["lastLockedDate"][:-9]
            except KeyError:
              pass
            try:
                item["lastActivityDate"] = item["lastActivityDate"][:-9]
            except KeyError:
              pass
            row = OrderedDict()
            row["id"] = u"id:"
            for key in keyList:
                # set the values to empty string instead of None
                if key != "id" and key != "resources":
                    row[key] = ""
            for key, value in sorted(item.iteritems()):
                # resources key is api-specific so it's just clutter
                # if a field is named "resources" its key will be fields.resources, so safe there
                if key == "resources":
                    continue
                keyValueList = list()
                self.checkKeyForNestedObjects(key, value, keyValueList)
                for keyValueTuple in keyValueList:
                    if keyValueTuple[0] not in keyList:
                        # this means that the key wasn't found in the initial aggregation,
                        # and this is show-stoppingly weird
                        raise Exception("field name wasn't found on first pass.  stopping")
                    row[keyValueTuple[0]] = u"{}".format(keyValueTuple[1])
            writer.writerow(row.values())

    # returns a key value pair with original value and key path
    # ie. fields.name instead of name
    def checkKeyForNestedObjects(self, key, value, keyValueList):
        if isinstance(value, dict):
            for subKey, subValue in value.iteritems():
                self.checkKeyForNestedObjects(u"{}.{}".format(key, subKey), subValue, keyValueList)
        else:
            keyValueList.append((key, value))

    def getKeyPath(self, key, value, keySet):
        if isinstance(value, dict):
            for subKey, subValue in value.iteritems():
                self.getKeyPath(u"{}.{}".format(key, subKey), subValue, keySet)
        else:
            keySet.add(key)

    # returns a string with original value and key path
    def handleValue(self, key, value):
        if isinstance(value, dict):
            for subKey, subValue in sorted(value.iteritems()):
                return self.handleValue(u"{}.{}".format(key, subKey), subValue)
        return u"{}:{}".format(key, value)


# from https://docs.python.org/2/library/csv.html at the bottom of the page
class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        originalData = data
        data = ''.join(BeautifulSoup(data).findAll(text=True))
        data = self.encoder.encode(data)


        try:
            self.stream.write(data)
            self.queue.truncate(0)

        except UnicodeEncodeError:
            print("Sorry the encoding for the row: " + str(data) + " was not recognized and will not be added to your output.")

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)