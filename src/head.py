HEAD_TEMPLATE = """\\documentclass[preprint, onecolumn]{{report}}

\\title{{proxyrequests}}
\\author{{satan}}


\\usepackage{{graphicx}}
\\usepackage{{caption}}
\\usepackage{{subcaption}}
\\usepackage[textwidth=18cm]{{geometry}}
\\usepackage{{xcolor}}


\\thispagestyle{{plain}}
\\begin{{document}}
\\onecolumn
\\date{{}}
\\maketitle
"""

class Head:
    def render(self):
        print(HEAD_TEMPLATE.format(self))