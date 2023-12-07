from .. import ClassError

class Class_List:
    def __init__(self):
        self._list:list[str] = list()

    def __repr__(self):
        return repr(self._list)
    
    def __iter__(self):
        return iter(self._list)
    
    def add(self, item:str):
        if item in self._list:
            raise ClassError('class already is in class list')
        self._list.append(item)
    
    def remove(self, item:str):
        if not item in self._list:
            raise ClassError('class do not exists in class list')
        self._list.remove(item)
    
    def replace(self, old_item:str, new_item:str):
        if not old_item in self._list:
            raise ClassError('class do not exists in class list')
        self._list[self._list.index(old_item)] = new_item
    
    @property
    def list(self):
        return self._list
