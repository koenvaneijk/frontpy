# FrontPy

## Introduction
FrontPy is a front-end web framework built on Pyodide and Flask. This allows you to build web apps all in Python, both front-end and back-end.

## Example usages
```python
from frontpy import App, Window, TextField, Button, Label, TextArea, Card

app = App(title="Welcome!")
window = Window(app, title="This is a window title")
window.position = [100, 200, 0, 0]

input_ = TextField(window, placeholder="Your name here")
label = Label(window, text="Hello")
textarea = TextArea(window, placeholder="Your text here")

card = Card(window, header="header!", body="body!", footer="footer!")

def on_click(event=None):
    button.remove()
    label.text = 'whooepsie'
    app.emit("button_clicked", button)

button = Button(window, text="Yo", on_click=on_click)

def button_handler(event=None):
    print("Button clicked!")
    label.text = "Button clicked!"

app.register_handler("button_clicked", button_handler)
```
