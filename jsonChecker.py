import json

errorMsg = ": Don't exist in "


def checkFile(filepath, directory):
    print(filepath)
    print(directory)
    print()

    with open(filepath) as json_file:
        data = json.load(json_file)

        if(directory == "data/monster/"):
            if "name" not in data:
                print("(name)"+errorMsg+filepath)