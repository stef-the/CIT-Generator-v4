import json
import time
from os import listdir
import os.path


def main():
    start_time = time.time()  # Get starting time
    print("STARTING DUPLICATES\n--- %s seconds ---" % (time.time() - start_time))

    items_path = "src/data/items/"

    files = [
        f for f in listdir(items_path) if os.path.isfile(os.path.join(items_path, f))
    ]
    file_names = []
    duplicates_output = {}

    for file in files:
        with open(items_path + file, encoding="utf-8") as json_data:
            file_names.append(json.load(json_data)["displayname"].split("§")[-1])

    duplicates = []
    for i in file_names:
        if not i in duplicates:
            increment = 0
            for j in file_names:
                if i == j:
                    increment += 1
                    if increment > 1:
                        duplicates.append(i)
                        break

    duplicates_output["duplicates"] = duplicates
    duplicates_output["count"] = len(duplicates)
    duplicates_output["timestamp"] = time.time()

    with open("src/data/duplicates.json", "w") as outfile:
        json.dump(duplicates_output, outfile)

    print("DUPLICATES COMPLETE\n--- %s seconds ---" % (time.time() - start_time))

    print("STARTING OUTPUT CONFIG\n--- %s seconds ---" % (time.time() - start_time))

    fileList = []
    path = "src/data/items"
    for filenames in os.walk(path):
        fileList.append(filenames)

    data_list = {}

    for i in fileList[0][2]:
        try:
            data = json.load(open(path + "/" + i, encoding="utf-8"))
            data_list[i.split(".")[0]] = data
        except Exception as e:
            print(e)

    out_file = open("src/data/items.json", "w")
    json.dump(data_list, out_file, indent=4)
    out_file.close()

    print("OUTPUT CONFIG COMPLETE\n--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
