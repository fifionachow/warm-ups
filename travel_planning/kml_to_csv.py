from fastkml import kml


def insert_into_row(f):
    long = str(f.geometry.x)
    lat = str(f.geometry.y)
    return ",".join([f.name, lat, long])+"\n"


def kml_to_csv(kml_path):
    with open(kml_path, 'rb') as myfile:
        doc = myfile.read()
    k = kml.KML()
    k.from_string(doc)
    features = list(k.features())
    csv_path = kml_path.replace(".kml", ".csv")
    with open(csv_path, "w") as csvfile:
        csvfile.write("name, lat, long\n")
        for feature in features:
            for f in feature.features():
                row = insert_into_row(f)
                csvfile.write(row)
    print("DONE")
