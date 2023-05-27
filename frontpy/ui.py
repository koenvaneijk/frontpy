import js
from pyodide.ffi import create_proxy
from time import sleep

BOOTSTRAP_HREF = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"

class EventBus:
    def __init__(self):
        """Create a new event bus."""

class App:
    """
    The App class is the main entry point for the application. It is responsible for
    creating the HTML document and setting up the application.
    """
    def __init__(self, title="App", background_color="white"):
        """
        Create the HTML document and set up the application.

        :param title: The title of the application.
        :type title: str
        :param background_color: The background color of the application.
        :type background_color: str
        """
        self.head = js.document.head
        self.bootstrap()

        self.body = js.document.body
        self.title = title
        self.background_color = background_color

        self.event_bus = EventBus()

        self._event_handlers = {}

    def register_handler(self, event_type: str, handler: callable):
        """Register a new event handler."""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)

    def unregister_handler(self, event_type: str, handler: callable):
        """Unregister an event handler."""
        if event_type in self._event_handlers:
            self._event_handlers[event_type].remove(handler)

    def emit(self, event_type: str, *args, **kwargs):
        """Emit an event."""
        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                handler(*args, **kwargs)
                
    def main_loop(self):
        while True:
            sleep(0.1)
            print('looping')

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        self._background_color = value
        self.body.style.backgroundColor = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        js.document.getElementsByTagName('title')[0].innerText = value

    def bootstrap(self):
        self.bootstrap_link = js.document.createElement("link")
        self.bootstrap_link.href = BOOTSTRAP_HREF
        self.bootstrap_link.rel = "stylesheet"
        self.bootstrap_link.crossorigin = "anonymous"
        self.head.append(self.bootstrap_link)

    def append(self, element):
        self.body.append(element)
 
class Window:
    def __init__(self, parent, title=''):
        self.parent = parent
        self.title = title

        self.on_close_click_proxy = create_proxy(self.on_close_click)

        self.create_element()
 
        self.stop_drag_proxy = create_proxy(self.stop_drag)
        self.drag_proxy = create_proxy(self.drag)
        self.on_mouse_down_proxy = create_proxy(self.on_mouse_down)
    
        self.position = [0,0,0,0]

        self.render()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        self.element.style.top = f"{value[1]}px"
        self.element.style.left = f"{value[0]}px"

    def on_mouse_down(self, event=None):
        event.preventDefault()

        self.position[2] = event.clientX
        self.position[3] = event.clientY

        js.document.addEventListener("mouseup", self.stop_drag_proxy)
        js.document.addEventListener("mousemove", self.drag_proxy)

    def drag(self, event=None):
        event.preventDefault()

        self.position[0] = self.position[2] - event.clientX
        self.position[1] = self.position[3] - event.clientY
        self.position[2] = event.clientX
        self.position[3] = event.clientY
        
        self.element.style.top = (str(self.element.offsetTop - self.position[1]) + "px")
        self.element.style.left = (str(self.element.offsetLeft - self.position[0]) + "px")
        
    def stop_drag(self, event=None):
        js.document.removeEventListener("mouseup", self.stop_drag_proxy)
        js.document.removeEventListener("mousemove", self.drag_proxy)

    def close(self):
        self.element.remove()

    def on_close_click(self, event=None):
        self.close()

    def create_element(self):
        self.element = js.document.createElement("div")
        self.element.style.position = 'absolute'

    def render(self):
        header = js.document.createElement("div")
        header.innerHTML = self.title
        header.addEventListener("mousedown", self.on_mouse_down_proxy)
        header.style.border = "2px solid black"
        header.style.padding = "5px"

        close_button = js.document.createElement('button')
        # <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        close_button.type = "button"
        close_button.classList.add("close")
        close_button.setAttribute("data-dismiss", "modal")
        close_button.setAttribute("aria-label", "Close")

        span = js.document.createElement("span")
        span.setAttribute("aria-hidden", "true")
        span.innerHTML = "&times;"
        close_button.append(span)

        close_button.addEventListener("mousedown", self.on_close_click_proxy)
        header.append(close_button)


        self.element.append(header)


        
        self.body = js.document.createElement("div")
        self.element.append(self.body)
        
        self.parent.append(self.element)

    def append(self, element):
        self.body.append(element)

class Element:
    def __init__(self, parent):
        self.parent = parent

        self.render()

    def remove(self):
        self.element.remove()

    def render(self):
        self.parent.append(self.element)

    def create_element(self):
        self.element = js.document.createElement("div")

class Text:
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.element.innerHTML = str(value)

class Label(Element, Text):
    def __init__(self, parent, text):
        self.parent = parent
        self.create_element()
        self.text = text
        self.render()

class Button(Element, Text):
    def __init__(self, parent, text, on_click=None):
        self.parent = parent
        self.create_element()

        self.text = text

        self.on_click = create_proxy(on_click)

        self.render()

    def render(self):
        self.element = js.document.createElement("div")
        button = js.document.createElement("button")
        button.innerHTML = "Yo"
        button.addEventListener("click", self.on_click)
        button.className = "btn btn-primary"
        self.element.append(button)
        self.parent.append(self.element)


class Input(Element):
    def create_element(self):
        self.element = js.document.createElement("input")

class Alert(Element, Text):
    def __init__(self, parent, text, alert_type="primary"):
        self.parent = parent
        self.create_element()
        self.text = text
        self.alert_type = alert_type
        self.render()

    def render(self):
        self.element.classList.add("alert", f"alert-{self.alert_type}")
        self.element.setAttribute("role", "alert")
        self.element.innerHTML = self.text
        self.parent.append(self.element)

class Card(Element):
    def __init__(self, parent, header=None, body=None, footer=None):
        self.parent = parent
        self.create_element()
        self.header = header
        self.body = body
        self.footer = footer
        self.render()

    def render(self):
        self.element.classList.add("card")

        if self.header:
            card_header = js.document.createElement("div")
            card_header.classList.add("card-header")
            card_header.innerHTML = self.header
            self.element.append(card_header)

        if self.body:
            card_body = js.document.createElement("div")
            card_body.classList.add("card-body")
            card_body.innerHTML = self.body
            self.element.append(card_body)

        if self.footer:
            card_footer = js.document.createElement("div")
            card_footer.classList.add("card-footer")
            card_footer.innerHTML = self.footer
            self.element.append(card_footer)

        self.parent.append(self.element)


class TextField(Input):
    def __init__(self, parent, value="", placeholder=""):
        self.parent = parent

        self.create_element()
        
        self.placeholder = placeholder

        self.render()

    def render(self):
        self.element.type = "text"
        self.element.placeholder = self.placeholder
        self.element.value = self.value
        self.element.className = "form-control"
        self.parent.append(self.element)

    @property
    def value(self):
        return self.element.value

class Container(Element):
    def __init__(self, parent, fluid=False):
        self.parent = parent
        self.fluid = fluid
        self.create_element()
        self.render()

    def render(self):
        if self.fluid:
            self.element.classList.add("container-fluid")
        else:
            self.element.classList.add("container")
        self.parent.append(self.element)

class Row(Element):
    def __init__(self, parent):
        self.parent = parent
        self.create_element()
        self.render()

    def render(self):
        self.element.classList.add("row")
        self.parent.append(self.element)

class Column(Element):
    def __init__(self, parent, size=None, extra_classes=None):
        self.parent = parent
        self.size = size
        self.extra_classes = extra_classes if extra_classes else []
        self.create_element()
        self.render()

    def render(self):
        self.element.classList.add("col")
        if self.size:
            self.element.classList.add(f"col-{self.size}")

        for extra_class in self.extra_classes:
            self.element.classList.add(extra_class)

        self.parent.append(self.element)


class TextArea(Element):
    def __init__(self, parent, value="", placeholder=""):
        self.parent = parent

        self.create_element()

        self.value = value
        self.placeholder = placeholder

        self.render()

    def render(self):
        textarea = js.document.createElement("textarea")
        textarea.placeholder = self.placeholder
        textarea.value = self.value
        textarea.className = "form-control"
        self.element.append(textarea)
        self.parent.append(self.element)

    @property
    def value(self):
        return self.element.value

    @value.setter
    def value(self, value):
        self.element.value = value
        
class Image(Element):
    def __init__(self, parent, src, width=None, height=None):
        self.parent = parent

        self.create_element()

        self.src = src
        self.width = width
        self.height = height

        self.render()

    def render(self):
        img = js.document.createElement("img")
        img.src = self.src
        img.width = self.width
        img.height = self.height
        self.element.append(img)
        self.parent.append(self.element)