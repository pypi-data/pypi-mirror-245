from .classes import Class_List as _class
from .. import ElementError

def __base1(name, attrs, *Any):
    content = list()
    for nome in attrs:
        if attrs[nome] and isinstance(attrs[nome], bool):
            content.append(nome)
        elif attrs[nome] and isinstance(attrs[nome], str):
            content.append(f'{nome}=\"{attrs[nome]}\"')
    if content:
        return f'''<{name} {' '.join(content)}>'''
    return f'''<{name}>'''

def __base2(name, attrs, children):
    content = list()
    for nome in attrs:
        if attrs[nome] and isinstance(attrs[nome], bool):
            content.append(nome)
        elif attrs[nome] and isinstance(attrs[nome], str):
            content.append(f'{nome}=\"{attrs[nome]}\"')
    sep = '\n'
    children = [child.pack() if isinstance(child, Element) else child for child in children]
    if content:
        return f'''<{name} {' '.join(content)}>\n{sep.join(children)}\n</{name}>'''
    return f'''<{name}>\n{sep.join(children)}\n</{name}>'''

class Element:
    def __init__(self, __name:str, *child, **attributes):
        self.__name = __name
        self.__attributes = attributes
        double = attributes.get('__double')
        self.__double = double if isinstance(double, bool) else True
        if self.__double:
            self.__attributes['__double'] = None
        self.__class_list = _class()
        self.__children:list[Element | str] = list(child)
    
    def editAttribute(self, a:str, b:str):
        self.__attributes[a] = b

    def editAttributes(self, **a:str):
        for b in a:
            self.__attributes[b] = a[b]
    
    def __str__(self):
        return self.pack()
    
    def __repr__(self):
        return f'Element(\"{self.__name}\")'

    def pack(self):
        if self.__double:
            base = __base2
        else:
            base = __base1
        classes = ' '.join(self.__class_list)
        if classes:
            self.__attributes['class'] = classes
        return base(self.__name, self.__attributes, self.__children)
    
    @property
    def element_name(self):
        return self.__name
    
    @property
    def class_list(self):
        return self.__class_list
    
    @property
    def attributes(self):
        return self.__attributes
    
    @property
    def children(self):
        return self.__children
    
    @children.setter
    def children(self, value):
        for nome in value:
            if isinstance(nome, Element):
                continue
            elif isinstance(nome, str):
                continue
            else:
                raise ElementError(f'value: "{value}" is not a Iterable with only Elements or Strings')
        self.__children = list(value)

class HtmlElement(Element):
    def __init__(self, *children, **attributes):
        Element.__init__(self, 'html', *children, **attributes)
    
    def pack(self):
        content = list()
        for nome in self.attributes:
            if self.attributes[nome] and isinstance(self.attributes[nome], bool):
                content.append(nome)
            elif self.attributes[nome] and isinstance(self.attributes[nome], str):
                content.append(f'{nome}=\"{self.attributes[nome]}\"')
            else:
                pass
        sep = '\n'
        children = [child.pack() if isinstance(child, Element) else child for child in self.children]
        if content:
            return f'''<!DOCTYPE html>\n<{self.element_name} {' '.join(content)}>\n{sep.join(children)}\n</{self.element_name}>'''
        return f'''<!DOCTYPE html>\n<{self.element_name}>\n{sep.join(children)}\n</{self.element_name}>'''
