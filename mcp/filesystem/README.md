# filesystem MCP connector

官方 `@modelcontextprotocol/server-filesystem`（MIT License）的连接配置模板。
让 agent 以受控方式访问指定本地目录（默认限定到工作区，可按需扩展 allowed dirs）。

## 工位侧挂载（cordis.yml / cordis.patch.yml 片段）

```yaml
- id: mcp-filesystem
  name: '@deepseek-ai/dsh-mcp-client'
  config:
    serverName: filesystem
    transport: stdio
    command: npx
    args: ['-y', '@modelcontextprotocol/server-filesystem', '{{workspaceRoot}}']
```

说明：
- `serverName` 决定工具前缀：模型看到 `mcp__filesystem__read_file` 等工具
- args 最后一个参数是允许访问的目录白名单；**只放任务需要的目录**，不放盘符根
- 桌面壳预置 node/npx 运行时后此配置开箱即用；HMR 支持改配置即热重连
- 本目录仅含配置模板与说明，不复制 server 源代码（合规见 THIRD_PARTY_NOTICES.md）
