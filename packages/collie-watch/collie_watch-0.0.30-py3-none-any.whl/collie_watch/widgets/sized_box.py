from .widget import Widget

class SizedBox(Widget):
    def __init__(self, width="0px", height="0px",flex="", id=""):
        super().__init__(id=id,flex=flex)
        self.width = width
        self.height = height

    def render(self):
        return f'''<div id="{self.id}" style="
        {"flex: {};".format(self.flex) if self.flex != "" else ""}
        width: {self.width}; 
        height: {self.height};">
        </div>'''
