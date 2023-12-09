from .. import ClassError

class Class_List:
    def __init__(self):
        self.__list:list[str] = list()

    def __repr__(self):
        return repr(self.__list)
    
    def __iter__(self):
        return iter(self.__list)
    
    def add(self, item:str):
        if item in self.__list:
            raise ClassError("class already is in class list")
        self.__list.append(item)
    
    append = add
    
    def remove(self, item:str):
        if not item in self.__list:
            raise ClassError("class do not exists in class list")
        self.__list.remove(item)
    
    def replace(self, old_item:str, new_item:str):
        if not old_item in self.__list:
            raise ClassError("class do not exists in class list")
        self.__list[self.__list.index(old_item)] = new_item
