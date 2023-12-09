from . import _base

Element = _base.Element

_Child = Element | str

def __double_base(name:str):
    def a(*child:_Child, **attributes:str):
        return Element(name, *child, **{**attributes, "__double": True})
    return a

def __not_double_base(name:str):
    def a(**attributes:str):
        return Element(name, **{**attributes, "__double": False})
    return a

def __html(*child:_Child, **attributes:str):
    return _base.HtmlElement(*child, **{**attributes, "__double": True})

def __title(title:str):
    return f"<title>{title}</title>"

# funções
html = __html
head = __double_base("head")
body = __double_base("body")
anchor = a = __double_base("a")
audio = __double_base("audio")
br = lambda: "<br>"
video = __double_base("video")
image = img = __not_double_base("img")
button = btn = __double_base("button")
div = __double_base("div")
form = __double_base("form")
iframe = __double_base("iframe")
inp = __not_double_base("input")
label = __not_double_base("label")
link = __not_double_base("link")
meta = __not_double_base("meta")
paragraph = p = __double_base("p")
script = __double_base("script")
source = __not_double_base("source")
textarea = __double_base("textarea")
title = __title
