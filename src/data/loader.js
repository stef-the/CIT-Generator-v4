import * as fs from "fs";

function displayRename(input) {
    let output = "";
    ("§a" + input).split("§").forEach((part) => {
        output += part.substring(1);
    });
    return output;
}

const RAWitems = fs.readdirSync("NotEnoughUpdates-REPO/items");
let items = [];
let duplicates = [];
let data = [];
let increment = 0;

for (const item of RAWitems) {
    items.push(item.substr(0, item.length - 5));
    data.push(
        JSON.parse(
            fs.readFileSync(`NotEnoughUpdates-REPO/items/${item}`, {
                encoding: "utf8",
                flag: "r",
            })
        )
    );
}

for (const item of data) {
    for (const part of data) {
        if (
            displayRename(item["displayname"]) ==
            displayRename(part["displayname"])
        ) {
            increment = increment + 1;
            if (increment > 1) {
                duplicates.push(displayRename(item["displayname"]));
            }
        }
    }
    increment = 0;
}

const output = Array.from(new Set(duplicates).values());

fs.writeFileSync(
    "./duplicates.json",
    JSON.stringify({
        data: output,
        timestamp: Date.now(),
    })
);