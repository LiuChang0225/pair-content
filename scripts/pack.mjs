// 零依赖打包：先跑校验，再把内容项 + catalog 打成 dist/pair-content-<version>.zip，
// 并生成 dist/content-latest.json（版本、sha256、条目摘要）供工位 pair-updater 消费。
import { spawnSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from 'node:fs'
import { join, dirname, relative, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const DIST = join(ROOT, 'dist')

// 1. 准入闸门：校验不过不打包
const validate = spawnSync(process.execPath, [join(ROOT, 'scripts', 'validate.mjs')], { stdio: 'inherit' })
if (validate.status !== 0) process.exit(validate.status ?? 1)

const catalog = JSON.parse(readFileSync(join(ROOT, 'catalog.json'), 'utf8'))

// 2. 收集内容包文件：catalog.json + 全部 file 类安装路径下的文件
const files = ['catalog.json']
for (const item of catalog.items) {
  if (item.install.kind !== 'file') continue
  const abs = join(ROOT, item.install.path)
  collect(abs, files)
}
function collect(abs, out) {
  const stat = statSync(abs)
  if (stat.isFile()) {
    out.push(relative(ROOT, abs).split(sep).join('/'))
    return
  }
  for (const entry of readdirSync(abs, { withFileTypes: true })) {
    collect(join(abs, entry.name), out)
  }
}

// 3. 打 zip。Node 无内置 zip；用 PowerShell Compress-Archive（Windows 工位/维护者机器均有）。
//    维护者若在 macOS/Linux 发布，则回退到系统 zip 命令。
rmSync(DIST, { recursive: true, force: true })
mkdirSync(DIST, { recursive: true })
const zipPath = join(DIST, `pair-content-${catalog.version}.zip`)
const staging = join(DIST, '_staging')
for (const rel of files) {
  const target = join(staging, rel)
  mkdirSync(dirname(target), { recursive: true })
  writeFileSync(target, readFileSync(join(ROOT, rel)))
}
const zip =
  process.platform === 'win32'
    ? spawnSync(
        'powershell.exe',
        ['-NoProfile', '-Command', `Compress-Archive -Path '${staging}\\*' -DestinationPath '${zipPath}' -Force`],
        { stdio: 'inherit' },
      )
    : spawnSync('zip', ['-r', '-q', zipPath, '.'], { cwd: staging, stdio: 'inherit' })
if (zip.status !== 0) {
  console.error('打包失败：Compress-Archive/zip 返回非零状态')
  process.exit(zip.status ?? 1)
}
rmSync(staging, { recursive: true, force: true })

// 4. 生成发布清单
const sha256 = createHash('sha256').update(readFileSync(zipPath)).digest('hex')
const manifest = {
  schemaVersion: 1,
  version: catalog.version,
  publishedAt: new Date().toISOString(),
  file: `pair-content-${catalog.version}.zip`,
  sha256,
  sizeBytes: statSync(zipPath).size,
  itemCount: catalog.items.length,
  items: catalog.items.map((i) => ({
    id: i.id,
    name: i.name,
    type: i.type,
    domain: i.domain,
    stage: i.stage,
    version: i.version,
  })),
}
writeFileSync(join(DIST, 'content-latest.json'), `${JSON.stringify(manifest, null, 2)}\n`)

console.log(`打包完成：dist/${relative(DIST, zipPath).split(sep).join('/')} (sha256 ${sha256.slice(0, 12)}…, ${manifest.sizeBytes} bytes)`)
console.log('发布：把 dist/pair-content-*.zip 与 dist/content-latest.json 上传到 OneDrive 共享的更新通道目录')
if (!existsSync(zipPath)) process.exit(1)
