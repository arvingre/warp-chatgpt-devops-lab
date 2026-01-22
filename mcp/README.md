# 🚀 Warp + ChatGPT + DevOps MCP Lab

本仓库是一个实践项目，用来探索 **Warp 终端 + ChatGPT + MCP** 如何高效结合，完成 DevOps / SRE 场景下的自动化运维与诊断。

当前目标（v1）：

- 在本地 Mac 上运行一个 DevOps MCP Server
- 通过 Cloudflare Tunnel 暴露为 HTTPS 服务
- 在 ChatGPT Web 端作为 App / Connector 接入
- 使用自然语言远程调用本机的 `kubectl` / `gcloud` 等 CLI 工具

---

## 🧱 架构概览

层次拆分：

| 层级 | 角色 | 说明 |
|------|------|------|
| UI 层 | ChatGPT Web / Desktop | 和模型对话、发出指令 |
| 控制层 | MCP（DevOps Control Plane） | 把模型请求转成具体 CLI 命令 |
| 执行层 | `kubectl` / `gcloud` / `docker` / `helm` | 真正操作集群和基础设施 |
| 操作终端 | Warp | 人类直接手工操作、调试 |
| 基础设施 | Kubernetes / GCP 等 | 实际运行环境 |

调用路径示意：

```text
ChatGPT Web  →  DevOps MCP (HTTP /mcp)  →  Shell + CLI  →  Kubernetes / GCP / Infra
                            ↑
                     Cloudflare Tunnel
                            ↑
                         本地 Mac


在 Warp 中运行：

python mcp/devops/devops_mcp.py


保持这个进程不要关闭。

#### 3. 通过 Cloudflare Tunnel 暴露 MCP

新开一个 Warp 窗口：

cloudflared tunnel --url http://localhost:7420


终端会输出类似：

Your quick Tunnel has been created! Visit it at:
https://allied-directed-pty-handmade.trycloudflare.com


记下这个域名，后面会用到。

4. 在 ChatGPT Web 中创建 MCP App

打开 ChatGPT Web → Apps（或对应入口）

选择 New App (BETA) → 选择自定义 MCP

填写：

Name：DevOps Control Plane

Description：Control Kubernetes and GCP via my local CLI tools.

MCP Server URL：
https://allied-directed-pty-handmade.trycloudflare.com/mcp

Authentication：No Auth

勾选风险提示「I understand and want to continue」

点击 Create

创建成功后，在对话中选择该 App，就可以调用 MCP 工具。

🧪 使用示例（在 ChatGPT 对话里）

检查本机 DevOps 环境：

调用 health_check()


查看 default 命名空间下的 Pods：

调用 k8s_get_pods(namespace="default")，并帮我按 pod 名称排序。


拉取某个 Pod 的日志并分析错误原因：

调用 k8s_logs(pod="my-app-123", namespace="app", tail=200)，
然后帮我分析可能的报错原因，并给出排查建议。


安全地执行一个自定义命令：

通过 run_safe 执行命令：
"kubectl get nodes -o wide"
并解释一下输出。

🧵 与 Warp 的配合方式

日常开发 / 手工操作：

在 Warp 中直接使用 kubectl / gcloud / docker。

深度分析 / 自动诊断：

在 ChatGPT Web 中调用 DevOps MCP 工具，让模型自动执行命令并总结结果。

Git 管理：

所有 MCP 代码和文档统一存放在本仓库，用分支和提交记录迭代。

推荐别名示例（可写入 ~/.zshrc）：

alias devops-mcp="python ~/workspace/warp-chatgpt-devops-lab/mcp/devops/devops_mcp.py"
alias devops-tunnel="cloudflared tunnel --url http://localhost:7420"

🛣️ 下一步计划

 拆分工具：k8s / gcloud / docker / logs 各自独立 tool

 增加只读 RBAC 支持，降低集群操作风险

 将 MCP Server 打包成 Docker 镜像，部署到 Kubernetes

 增加规则：禁止执行 kubectl delete 等危险命令

 集成 GitOps：自动生成/检查 K8s manifests，创建 PR

📄 License

MIT


---

## 四、后面我们就按“Git 节奏”来推进

以后每做一个阶段性的东西，我们都按这个套路来：

1. 先在这里讨论设计和内容  
2. 再在仓库里新建 `feature/...` 分支  
3. 我帮你写 / 修改具体文件内容（代码、README、docs）  
4. 你在本地 `git add` + `git commit` + `git push`  
5. 你自己在 GitHub 上开 PR，review 一眼再合并  

这样：

- 你的仓库会很干净；
- 每个 milestone 都有一组清晰的 commit；
- 以后回头看也知道“这一步是干嘛的”。

---

你现在可以先做这两步：

1. 把上面 README 复制到仓库根目录 `README.md`  
2. 按我前面给的 Git 命令，走一遍 `feature/devops-mcp-v1` 的流程并 push

做完之后，如果你愿意，我们下一步就可以在仓库里新建一个 `docs/devops-mcp-architecture.md`，专门画出架构图和调用流程，让这个项目从“实验”升级成“可以分享给别人的作品”。
::contentReference[oaicite:0]{index=0}

