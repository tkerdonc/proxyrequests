HEAD_TEMPLATE = """\\documentclass[preprint, onecolumn]{{report}}

\\title{{{0.title}}}
\\author{{Joueur: {0.player}}}

\\usepackage{{graphicx}}
\\usepackage{{caption}}
\\usepackage{{subcaption}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}
\\usepackage[explicit,compact]{{titlesec}}

\\usepackage[
    top    = 1in,
    bottom = 1in,
    left   = 1.25in,
    right  = 1.25in]{{geometry}}

\\thispagestyle{{plain}}
\\begin{{document}}
\\onecolumn
\\date{{}}
\\maketitle

\\titleformat{{\\chapter}}[block]
    {{\\bfseries\\huge}}{{\\filright\\normalsize\\thechapter.}}{{1ex}}{{\\normalsize\\filright #1}}

"""

HEADER_TEMPLATE="""\chapter*{Foreword}"""
ITEMIZE_HEADER="""\\begin{itemize}"""
ITEMIZE_FOOTER="""\\end{itemize}"""
ITEMIZE_ITEM_TEMPLATE="""\\item {{{0}}}"""

defaultConfig = {
    "title": "Proxy Requests",
    "player": "Satan",
    "team": "Team",
    "items_header": "",
    "items": []
}

import os
import json


CONFIG = "config.json"

class Head:


    def __init__(self, root):
        self.root = root
        self.config = os.path.join(self.root, CONFIG)
        if not os.path.exists(self.config):
            outF = open(self.config, 'w')
            outF.write(json.dumps(defaultConfig))
            outF.close()

        self.data = {}
        if os.path.exists(self.config) and os.path.isfile(self.config):
            self.data = json.load(open(self.config, 'r'))

        self.title = self.data.get("title")
        self.player = self.data.get("player")
        self.team = self.data.get("team")
        self.items = self.data.get("items") or []
        self.items_header = self.data.get("items_header") or ""

    def render(self):
        print(HEAD_TEMPLATE.format(self))

        if len(self.items) > 0 or len(self.items_header) > 0:
            print(HEADER_TEMPLATE)
            if len(self.items_header) > 0:
                print(self.items_header)
            if len(self.items) > 0:
                print(ITEMIZE_HEADER)
                for item in self.items:
                    print(ITEMIZE_ITEM_TEMPLATE.format(item))
                print(ITEMIZE_FOOTER)
