import os
import json

SKELETON_CONFIG = {
	"model": "MODEL",
	"height": "",
	"width": "",
	"length": "",
	"base": "",
	"painted": 1,
	"notes": "",
	"Official Model Size": ["", ""]
}

class pageConfig:
    def __init__(self, folder):
        self.name = folder.split(os.path.sep)[-1]

    def dump(self):
        data = SKELETON_CONFIG
        data["model"] = self.name
        return json.dumps(data)
