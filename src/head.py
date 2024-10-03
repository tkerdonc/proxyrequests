HEAD_TEMPLATE = """\\documentclass[preprint, onecolumn]{{report}}

\\title{{Proxy Requests L3}}
\\author{{Joueur: Satan}}

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

class Head:
    def render(self):
        print(HEAD_TEMPLATE.format(self))
