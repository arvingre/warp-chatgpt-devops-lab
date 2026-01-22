from fastmcp import FastMCP
import subprocess

server = FastMCP(name="shell")

@server.tool()
def run(cmd: str) -> str:
    """
    Run a shell command and return stdout/stderr
    """
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    server.run()

