import json
import os

from src.pageConfig import pageConfig

JSON_FILE= "data.json"
HEADER_TEMPLATE="""\chapter*{{{.model}}}"""
IMAGES_TEMPLATE="""\\begin{{figure*}}[ht!]
    \centering
    \\begin{{subfigure}}[b]{{0.5\\textwidth}}
        \centering
		\includegraphics[width=\\textwidth]{{{0.folder}/1.jpg}}
    \end{{subfigure}}%
    \\begin{{subfigure}}[b]{{0.5\\textwidth}}
        \centering
		\includegraphics[width=\\textwidth]{{{0.folder}/2.jpg}}
    \end{{subfigure}}
    %\caption{{Caption place holder}}
\end{{figure*}}\n"""
TABLE_HEADER_TEMPLATE="""\\begin{{tabular}}{{|c|c|}}
    \hline
    \\textbf{{Model}} & \\textbf{{{.model}}} \\\\\n"""
TABLE_LINE_TEMPLATE="""{0} & {1} \\\\\n"""
TABLE_FOOTER_TEMPLATE="""\hline
\end{{tabular}}\n"""
DATA_BLACKLIST = [
    "model",
    "painted",
]

class Page:
    def __init__(self, folder):
        self.folder = folder
        configPath = os.path.join(folder, JSON_FILE)
        if not os.path.exists(configPath):
            pConf = pageConfig(folder)
            outF = open(configPath, 'w')
            outF.write(pConf.dump())
            outF.close()
        
        inF = open(configPath, 'r')
        self.data = json.load(inF)
        self.model = self.data.get("model")
        self.painted = self.data.get("painted")

    def printLine(self, line, value):
        if value is None or len(value) == 0:
            return ""
        else:
            return TABLE_LINE_TEMPLATE.format(line, value)

    def latex(self):
        retval = ""
        for template in [
                HEADER_TEMPLATE,
                IMAGES_TEMPLATE,
                TABLE_HEADER_TEMPLATE,
                ]:
            retval += template.format(self)

        for k in self.data.keys():
            if k in DATA_BLACKLIST:
                continue
            retval += self.printLine(k, self.data.get(k))
                
        if self.painted is None :
            retval += self.printLine("Paint", "\\textcolor{red}{\\textbf{Work in progress}}")

        retval += TABLE_FOOTER_TEMPLATE.format(self)
        return retval

    def render(self):
        print(self.latex())