
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents

class Button(Widget):
    def __init__(self, text="",callback=None,id="",width="",height="",flex=""):
        super().__init__(id=id,flex=flex)
        self.text = text
        self.callback = callback
        
        if id != "" and callback != None:
            CollieWatch.add_callback_by_id(self.id,[CollieWatchHtmlEvents.CLICK],self.callback)

        
    def render(self):
        if self.callback == None:
            return f'<div class="button_like">{self.text}</div>'
        return f'<button id="{self.id}">{self.text}</button>'
