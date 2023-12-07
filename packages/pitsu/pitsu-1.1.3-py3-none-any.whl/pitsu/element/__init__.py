from . import _base

Element = _base.Element

Child = Element | str
Children = list[Child]

def _double_base(name):
    def a(*children:Child, **attributes:str):
        return Element(name, *children, **{**attributes, 'double': True})
    return a

def _not_double_base(name):
    def a(**attributes:str):
        return Element(name, **{**attributes, 'double': False})
    return a

def __html(*children:Child, **attributes:str):
    return _base.HtmlElement(*children, **{**attributes, 'double': True})

# funções
html = __html
head = _double_base('head')
body = _double_base('body')
anchor = a = _double_base('a')
audio = _double_base('audio')
br = lambda: '<br>'
video = _double_base('video')
image = img = _not_double_base('img')
button = btn = _double_base('button')
div = _double_base('div')
form = _double_base('form')
def text(name:str, *children:Child, **attributes:str):
    return _base.Element(name, *children, **{**attributes, 'double': True})
iframe = _double_base('iframe')
inp = _not_double_base('input')
label = _not_double_base('label')
link = _not_double_base('link')
meta = _not_double_base('meta')
paragraph = p = _double_base('p')
script = _double_base('script')
source = _not_double_base('source')
textarea = _double_base('textarea')
title = _double_base('title')
