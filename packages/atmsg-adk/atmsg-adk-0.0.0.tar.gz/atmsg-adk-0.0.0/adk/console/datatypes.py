class num():pass



class type():
    name = str()

    def __init__(self, src: str) -> None:
        pass

class auto(type):
    pass

class string(type, str): #!

    name = 'string'

    def __init__(self, src: str) -> None:
        self.__src = src

    def __str__(self) -> str:
        return self.__src
    

class version():pass

class list(type): # list<<string>>

    def __init__(self, src: str) -> None:
        self.__src = src.split('&')