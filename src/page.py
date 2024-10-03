import json
import os

from src.pageConfig import pageConfig

JSON_FILE= "data.json"
HEADER_TEMPLATE="""\chapter*{{{.model}}}"""
DUAL_IMAGES_TEMPLATE="""\\begin{{figure*}}[ht!]
    \centering
    \\begin{{subfigure}}[b]{{0.5\\textwidth}}
        \centering
		\includegraphics[width=\\textwidth]{{{0.folder}/{1}}}
    \end{{subfigure}}%
    \\begin{{subfigure}}[b]{{0.5\\textwidth}}
        \centering
		\includegraphics[width=\\textwidth]{{{0.folder}/{2}}}
    \end{{subfigure}}
    %\caption{{Caption place holder}}
\end{{figure*}}\n"""
SINGLE_IMAGE_TEMPLATE="""\\begin{{figure*}}[ht!]
    \centering
    \\begin{{subfigure}}[b]{{0.5\\textwidth}}
        \centering
		\includegraphics[width=\\textwidth]{{{0.folder}/{1}}}
    \end{{subfigure}}%
\end{{figure*}}\n"""

TABLE_HEADER_TEMPLATE="""\\begin{{tabular}}{{p{{0.35\\linewidth}} | p{{0.6\\linewidth}}}}
    \hline
    \\textbf{{Model}} & \\textbf{{{.model}}} \\\\\n"""
TABLE_LINE_TEMPLATE="""{0} & {1} \\\\\n"""
TABLE_FOOTER_TEMPLATE="""\hline
\end{{tabular}}\n"""
DATA_BLACKLIST = [
    "model",
    "painted",
    "extra_images",
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
        self.first = "1.jpg"
        self.second = "2.jpg"

    def formatLine(self, line, value):
        line = line.replace('_', '\\_')
        value = value.replace('_', '\\_')

        isLink = value.startswith("https://")
        if isLink:
            value = "\\url{{" + value + "}}"

        return TABLE_LINE_TEMPLATE.format(line, value)

    def printLine(self, line, value):

        if value is None or len(value) == 0:
            return ""
        elif isinstance(value, list):
            retval = self.formatLine(line, value[0])
            for v in value[1:]:
                retval += self.formatLine('', v)
            return retval
        else:
            return self.formatLine(line, value)

    def getLineOrdinal(self, key):
        ORDER = [
            "model",
            "base",
            "width",
            "length",
            "height",
            "official model size",
            "notes",
        ]
        if key.lower() in ORDER:
            return ORDER.index(key.lower())

        return 1000

    def latex(self):
        retval = ""
        retval += HEADER_TEMPLATE.format(self)
        retval += DUAL_IMAGES_TEMPLATE.format(self, self.first, self.second)
        retval += TABLE_HEADER_TEMPLATE.format(self)

        for k in sorted(self.data.keys(), key=lambda x: self.getLineOrdinal(x)):
            if k in DATA_BLACKLIST:
                continue
            retval += self.printLine(k, self.data.get(k))

        if self.painted is None :
            retval += self.printLine("Paint", "\\textcolor{red}{\\textbf{Work in progress}}")

        retval += TABLE_FOOTER_TEMPLATE.format(self)

        extra_images = self.data.get("extra_images") or []
        if len(extra_images)> 0:
            for i in range(len(extra_images) // 2):
                retval += DUAL_IMAGES_TEMPLATE.format(self,
                                                  extra_images[ 2 * i],
                                                  extra_images[ 2 * i + 1])
            if len(extra_images) % 2 == 1:
                retval += SINGLE_IMAGE_TEMPLATE.format(self, extra_images[-1])

        return retval

    def render(self):
        print(self.latex())
