// 零依赖校验：catalog.json 结构、枚举、id 唯一性、内容项文件存在性。
// 发布（pack）前必须通过；CI/PR 同样以本脚本为准入闸门。
import { existsSync, readFileSync, readdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const DOMAINS = new Set(['SYS', 'SWE', 'MEE', 'EEE', 'SUP', 'MAN', 'GEN'])
const STAGES = new Set([
  'requirement-analysis',
  'architecture-design',
  'detailed-design',
  'implementation',
  'unit-verification',
  'integration-verification',
  'acceptance',
  'general',
])
const TYPES = new Set(['skill', 'mcp', 'agent', 'script'])
const REQUIRED_FIELDS = ['id', 'name', 'type', 'domain', 'stage', 'version', 'owner', 'description', 'install']
const ID_RE = /^[a-z0-9][a-z0-9-]*$/
const VERSION_RE = /^\d+\.\d+\.\d+$/

const errors = []
const fail = (msg) => errors.push(msg)

let catalog
try {
  catalog = JSON.parse(readFileSync(join(ROOT, 'catalog.json'), 'utf8'))
} catch (err) {
  console.error(`catalog.json 无法解析: ${err.message}`)
  process.exit(1)
}

if (catalog.schemaVersion !== 1) fail(`schemaVersion 必须为 1，实际 ${catalog.schemaVersion}`)
if (!VERSION_RE.test(catalog.version ?? '')) fail(`顶层 version 不是语义化版本: ${catalog.version}`)
if (!Array.isArray(catalog.items)) fail('items 必须是数组')

const seenIds = new Set()
for (const item of catalog.items ?? []) {
  const at = `items[${item.id ?? '?'}]`
  for (const field of REQUIRED_FIELDS) {
    if (item[field] === undefined || item[field] === '') fail(`${at}: 缺少必填字段 ${field}`)
  }
  if (!ID_RE.test(item.id ?? '')) fail(`${at}: id 不匹配 ${ID_RE}`)
  if (seenIds.has(item.id)) fail(`${at}: id 重复`)
  seenIds.add(item.id)
  if (!TYPES.has(item.type)) fail(`${at}: type "${item.type}" 不在 ${[...TYPES].join('/')}`)
  if (!DOMAINS.has(item.domain)) fail(`${at}: domain "${item.domain}" 不在枚举`)
  if (!STAGES.has(item.stage)) fail(`${at}: stage "${item.stage}" 不在枚举`)
  if (!VERSION_RE.test(item.version ?? '')) fail(`${at}: version 不是语义化版本`)
  if (item.source !== undefined && !/^https?:\/\//.test(item.source)) fail(`${at}: source 必须是 http(s) URL`)

  const install = item.install ?? {}
  if (!['file', 'http'].includes(install.kind)) {
    fail(`${at}: install.kind 必须是 file 或 http`)
  } else if (install.kind === 'file') {
    const abs = join(ROOT, install.path)
    if (!existsSync(abs)) fail(`${at}: install.path "${install.path}" 在仓库中不存在`)
    if (item.type === 'skill') {
      if (!existsSync(join(abs, 'SKILL.md'))) {
        fail(`${at}: skill 目录缺少 SKILL.md（dsh-skill-filesystem 只认 <root>/<name>/SKILL.md）`)
      }
      if (install.path !== `skills/${item.id}`) {
        fail(`${at}: skill 的 install.path 必须为 skills/${item.id}`)
      }
    }
  } else if (!/^https?:\/\//.test(install.path ?? '')) {
    fail(`${at}: install.kind=http 时 path 必须是 URL`)
  }
}

// 反向检查：skills/ 与 mcp/ 下每个目录都必须在 catalog 中有对应条目（孤儿内容不允许发布）
for (const [dir, type] of [['skills', 'skill'], ['mcp', 'mcp']]) {
  const root = join(ROOT, dir)
  if (!existsSync(root)) continue
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue
    const registered = (catalog.items ?? []).some(
      (i) => i.type === type && i.install?.kind === 'file' && i.install.path.startsWith(`${dir}/${entry.name}`),
    )
    if (!registered) fail(`${dir}/${entry.name}: 目录存在但未在 catalog.json 登记（孤儿内容不允许发布）`)
  }
}

if (errors.length > 0) {
  console.error(`校验失败（${errors.length} 项）:`)
  for (const e of errors) console.error(`  - ${e}`)
  process.exit(1)
}
console.log(`校验通过：catalog v${catalog.version}，${catalog.items.length} 个内容项`)
