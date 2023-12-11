def success(content: str) -> None:
    print('\x1b[1;32m[SUC]\x1b[0m', content)

def warning(content: str) -> None:
    print('\x1b[1;33m[WARN]\x1b[0m', content)

def error(content: str) -> None:
    print('\x1b[1;31m[ERR]\x1b[0m', content)

def info(content: str) -> None:
    print('\x1b[1m[INFO]\x1b[0m', content)

def log(content: str) -> None:
    print('\x1b[1m[LOG]\x1b[0m', content)