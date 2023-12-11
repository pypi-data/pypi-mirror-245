import adk.console as console

class err(Exception):

    def __call__(self) -> None:
        console.error(self.args[0])
        raise self
        

class NotInited(err):
    pass