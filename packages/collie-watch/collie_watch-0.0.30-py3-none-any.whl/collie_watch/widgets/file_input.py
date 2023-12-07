
from .alignment import CrossAxisAlignment, MainAxisAlignment
from .column import Column
from .button import Button
from .loader import Loader
from .text import Text
from .widget import Widget
from ..main_module import CollieWatch,CollieWatchHtmlEvents,CollieWatchHtmlInternalEvents

class FileInput(Widget):
    def __init__(self,id="",flex="",file_types=[],label=Button(text="Upload File")):
        """
        Initialize a FileInput widget.
        
        Arguments:
            id: An required identifier for the widget.

            flex: The flex attribute for the widget, determining how it'll grow in relation to its siblings in a flex container.

            file_types: A list of file types to accept. For example, ["image/png","image/jpeg"]. You can also use file extensions, like [".png",".jpg"].
        """

        super().__init__(id,flex)
        
        self.file_types = file_types
        self.__updating = False
        self.label = label

        if id != "":
            CollieWatch.add_callback_by_id(self.id,[CollieWatchHtmlInternalEvents.SENDING_FILE_CHUNK],self.__callback_on_file_chunk_received)
            CollieWatch.add_callback_by_id(self.id,[CollieWatchHtmlEvents.RECEIVED_FILE],self.__callback_on_file_received)
        else:
            raise Exception("FileInput must have an id")
    def __callback_on_file_chunk_received(self,event):
        if not self.__updating:
            self.__updating = True
            html = Column(crossAxisAlignment=CrossAxisAlignment.CENTER,id=self.id,children=[
                Text("Uploading File"),
                Loader()
            ]).render()
            print(html)
            CollieWatch.replace_html_element_by_id(self.id,html)

    def __callback_on_file_received(self,event):
        self.__updating = False
        CollieWatch.replace_html_element_by_id(self.id,self.render())
        
    def render(self):
        return f"""
    <div id="{self.id}">
    <label for="{self.id}_input">{self.label if not isinstance(self.label,Widget) else self.label.render()}</label>
    <input style="display: none;" type="file" id="{self.id}_input" accept="{' '.join(self.file_types)}">
    </div>
"""
