import json
import time
from os import listdir
from os.path import isfile, join

start_time = time.time()  # Get starting time
print("STARTING DUPLICATES\n--- %s seconds ---" % (time.time() - start_time))

items_path = "src/data/items/"

files = [f for f in listdir(items_path) if isfile(join(items_path, f))]
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

internal_names = [x.split(".")[0] for x in files]

# Output should look like this:
# { internal_name_a, internal_name_b, internal_name_c, ... }

import_set = set()
for i in internal_names:
    import_set.add(i)

with open("src/data/index.js", "w") as outfile:
    outfile.write(f'import f{import_set} from "./items/"')