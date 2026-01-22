from fastmcp import FastMCP
import subprocess
from typing import List

mcp = FastMCP("DevOps Control Plane")


def _run(cmd: str) -> str:
    """内部封装：执行 shell 命令"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


@mcp.tool()
def health_check() -> str:
    """检查本机是否能访问 gcloud 和 kubectl"""
    out = []
    out.append(_run("gcloud --version | head -n 1"))
    out.append(_run("kubectl version --client --short || kubectl version --short"))
    return "\n".join(out)


@mcp.tool()
def k8s_get_pods(namespace: str = "default") -> str:
    """列出指定命名空间的 Pods（使用本机 kubeconfig）"""
    return _run(f"kubectl get pods -n {namespace}")


@mcp.tool()
def k8s_logs(pod: str, namespace: str = "default", tail: int = 200) -> str:
    """查看某个 Pod 的最后 N 行日志"""
    return _run(f"kubectl logs {pod} -n {namespace} --tail={tail}")


@mcp.tool()
def run_safe(command: str) -> str:
    """
    运行一个“相对安全”的命令（仅供开发环境使用）。

    只允许前缀是这些的命令：
    - kubectl
    - gcloud
    - docker
    - helm
    """
    allowed_prefixes: List[str] = ["kubectl", "gcloud", "docker", "helm"]
    if not any(command.strip().startswith(p) for p in allowed_prefixes):
        return f"Command '{command}' not allowed. Allowed prefixes: {allowed_prefixes}"
    return _run(command)


if __name__ == "__main__":
    # 用 SSE 方式在 0.0.0.0:7420 跑一个 MCP server
    # mcp.run(transport="sse", host="0.0.0.0", port=7420)
    mcp.run(transport="http", host="0.0.0.0", port=7420)

