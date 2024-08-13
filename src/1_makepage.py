#!/usr/bin/env python3

import sys
import json

HEADER_TEMPLATE="""\chapter*{{{.model}}}"""

IMAGES_TEMPLATE="""\\begin{{figure*}}[ht!]
    \centering
    \\begin{{subfigure}}[b]{{0.5\\textwidth}}
        \centering
		\includegraphics[width=\\textwidth]{{figures/testPicture}}
    \end{{subfigure}}%
    \\begin{{subfigure}}[b]{{0.5\\textwidth}}
        \centering
		\includegraphics[width=\\textwidth]{{figures/testPicture}}
    \end{{subfigure}}
    %\caption{{Caption place holder}}
\end{{figure*}}\n"""


TABLE_HEADER_TEMPLATE="""\\begin{{tabular}}{{|c|c|}}
    \hline
    \\textbf{{Model}} & \\textbf{{{.model}}} \\\\\n"""
TABLE_LINE_TEMPLATE="""{0} & {1} \\\\\n"""
TABLE_FOOTER_TEMPLATE="""\hline
\end{{tabular}}\n"""


class page:
    def __init__(self, data):
        self.model = data["model"]
        self.height = data.get("height")

    def printLine(self, line, value):
        if value is None:
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

        retval += self.printLine("Height", self.height)

        retval += TABLE_FOOTER_TEMPLATE.format(self)
        return retval

inF = open(sys.argv[1], 'r')
for page_data in json.load(inF)["models"]:
    print(page(page_data).latex())
