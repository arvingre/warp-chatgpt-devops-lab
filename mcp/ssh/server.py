from fastmcp import FastMCP
import paramiko

server = FastMCP(name="ssh")

@server.tool()
def ssh_run(host: str, user: str, cmd: str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user)
    stdin, stdout, stderr = client.exec_command(cmd)
    return stdout.read().decode() + stderr.read().decode()

if __name__ == "__main__":
    server.run()

