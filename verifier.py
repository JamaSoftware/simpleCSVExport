from jama import Jama
from csv_writer import CSVWriter

def verify():
    jama = Jama()
    csv = CSVWriter()
    projects = jama.getProjects()
    csv.write("projects.csv", projects)
    project_ids = [project["id"] for project in projects]
    item_type_ids = [item_type["id"] for item_type in jama.getItemTypes()]
    for item_type_id in item_type_ids:
        csv.write("{}.csv".format(item_type_id), jama.getItems(item_type_id))
    relationships = []
    for project_id in project_ids:
        # if the relationships file gets too big you can create a file for each project's relationships
        # instead of extending this list
        relationships.extend(jama.getRelationships(project_id))
    csv.write("relationships.csv", relationships)

    # if the comments file gets too big you can split the list and scv.write() each half
    csv.write("comments.csv", jama.getComments())


if __name__ == "__main__":
    verify()
    print ("done")
