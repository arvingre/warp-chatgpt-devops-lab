from fastmcp import FastMCP
from pathlib import Path

server = FastMCP(name="filesystem")

@server.tool()
def read_file(path: str) -> str:
    p = Path(path).expanduser()
    return p.read_text()

@server.tool()
def list_dir(path: str=".") -> list[str]:
    p = Path(path).expanduser()
    return [str(x) for x in p.iterdir()]

if __name__ == "__main__":
    server.run()

