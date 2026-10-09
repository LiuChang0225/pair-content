# pair-content

PAIR 中央内容库——全部已发布内容项（skill / MCP connector / Agent 应用 / 自动化脚本）的唯一真源。

对应平台侧术语见 PAIR 仓库根目录 `CONTEXT.md`；架构决策见 PAIR 仓库 `docs/adr/0001~0004`。

## 仓库结构

```
catalog.schema.json   内容项元数据 schema（研发域 × 研发阶段双轴）
catalog.json          已发布内容项权威清单（唯一真源，版本号在此）
skills/<name>/SKILL.md  skill 内容项（平铺一层——dsh-skill-filesystem 只发现
                        <root>/<name>/SKILL.md，不递归；阶段归类放 catalog 元数据，
                        不要试图用嵌套目录表达）
mcp/<name>/           MCP connector 内容项（配置 + 必要的随包文件）
docs/                 面向使用者的流程指引等文档（不随内容包分发）
scripts/              维护者工具（校验、打包）
dist/                 打包产物（不入库）
```

## 贡献与准入流程（准入管控）

1. 从 `main` 拉分支，添加内容项文件，并在 `catalog.json` 登记条目
2. 本地跑 `npm run validate` 通过后发 PR
3. **PR 必须由仓库 owner 审批合入**——合入即视为 approved，未合入的内容永不发布
4. 合入后由维护者执行发布（见下）

## 打包与发布

```sh
npm install
npm run validate      # catalog.json 对 schema 校验 + 内容项文件存在性检查
npm run pack          # 产出 dist/pair-content-<version>.zip + dist/content-latest.json
```

发布 = 把 `dist/` 中两个文件上传到 OneDrive 共享的更新通道目录（最终形态为阿里云 OSS）。
工位侧 `pair-updater` 读取 `content-latest.json` 比对版本、校验 sha256 后热更新。

**回滚** = 将上一版 zip + 清单重新上传覆盖。

## 版本号

`catalog.json` 顶层 `version` 为内容包版本，语义化、只增不减；每次发布前手动 bump。

## 安全约定

- 任何 key/token 不得入库（百炼共享 key 由桌面安装包渠道下发，与内容库解耦）
- 公开源改造的内容项必须在 catalog 条目 `source` 字段记录来源 URL（管控与合规追溯）
