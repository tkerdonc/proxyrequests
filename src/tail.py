TAIL_TEMPLATE = """\\end{{document}}"""

class Tail:
    def render(self):
        print(TAIL_TEMPLATE.format(self))
