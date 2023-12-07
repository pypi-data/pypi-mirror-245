def create_ontology_dict():
    ontology_input = input("Enter the ontology as a comma-separated list (e.g.,car:car or more classes  car:vehicle,person:human): ")

    if ":" in ontology_input:
        ontology_dict = dict(item.split(":") for item in ontology_input.split(","))
    else:
        ontology_dict = {ontology_input: ontology_input}

    return ontology_dict

# Example usage:
#ontology_dict = create_ontology_dict()
#print("Ontology Dictionary:", ontology_dict)
