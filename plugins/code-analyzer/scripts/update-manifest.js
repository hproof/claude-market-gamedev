#!/usr/bin/env node
/**
 * update-manifest.js
 * 扫描 docs/code-analyzer/ 目录，从 frontmatter 提取元信息，生成 manifest.md
 */

const fs = require('fs');
const path = require('path');

const DOCS_DIR = './docs/code-analyzer';
const MANIFEST_FILE = path.join(DOCS_DIR, 'manifest.md');

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const fm = {};
  const lines = match[1].split('\n');
  let currentKey = null;
  let isMultiline = false;

  for (const line of lines) {
    if (isMultiline) {
      if (line.startsWith('  ')) {
        fm[currentKey] += '\n' + line.trim();
        continue;
      }
      isMultiline = false;
    }

    const kvMatch = line.match(/^(\w+):\s*(.*)$/);
    if (kvMatch) {
      currentKey = kvMatch[1];
      const value = kvMatch[2].trim();

      if (value === '|') {
        fm[currentKey] = '';
        isMultiline = true;
      } else {
        fm[currentKey] = value.replace(/^['"]|['"]$/g, '');
      }
    }
  }

  return fm;
}

function formatDate() {
  const now = new Date();
  const pad = n => String(n).padStart(2, '0');
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}`;
}

function generateManifest(docs) {
  const byType = { 'full-scan': [], 'module': [], 'feature': [] };
  const byScope = {};

  for (const doc of docs) {
    const type = doc.type || 'unknown';
    if (byType[type]) byType[type].push(doc);
    else byType[type].push(doc);

    const scopeKey = doc.scope || '.';
    if (!byScope[scopeKey]) byScope[scopeKey] = [];
    byScope[scopeKey].push(doc);
  }

  let tableRows = '';
  for (const doc of docs) {
    const desc = doc.description
      ? doc.description.split('\n')[0].trim().substring(0, 50)
      : '';
    tableRows += `| [${doc.name}](./${doc.name}.md) | ${doc.type || '-'} | ${doc.scope || '.'} | ${doc.date || '-'} | ${desc} |\n`;
  }

  let typeNav = '';
  for (const [type, docList] of Object.entries(byType)) {
    const links = docList.map(d => `[${d.name}](./${d.name}.md)`).join(', ');
    typeNav += `- **${type}**: ${links || '(暂无)'}\n`;
  }

  let scopeNav = '';
  for (const [scope, docList] of Object.entries(byScope)) {
    const links = docList.map(d => `[${d.name}](./${d.name}.md)`).join(', ');
    scopeNav += `- **${scope}**: ${links}\n`;
  }

  const now = formatDate();

  return `---
name: manifest
description: |
  Code Analyzer 文档清单。
---

# Code Analyzer 文档清单

> 自动生成，请勿手动编辑。

## 文档列表

| name | type | scope | date | description |
|------|------|-------|------|-------------|
${tableRows || '| (暂无文档) | | | | |\n'}

## 快速导航

### 按类型

${typeNav}### 按范围

${scopeNav}

---

*最后更新: ${now}*
`;
}

function main() {
  // 确保目录存在
  if (!fs.existsSync(DOCS_DIR)) {
    console.log(`目录不存在: ${DOCS_DIR}`);
    process.exit(1);
  }

  // 扫描 md 文件
  const files = fs.readdirSync(DOCS_DIR)
    .filter(f => f.endsWith('.md') && f !== 'manifest.md');

  const docs = [];
  let skipped = 0;

  for (const file of files) {
    const filePath = path.join(DOCS_DIR, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    const fm = parseFrontmatter(content);

    if (fm && fm.name && fm.description) {
      docs.push({
        name: fm.name,
        description: fm.description,
        type: fm.type,
        scope: fm.scope,
        date: fm.date,
        file: file
      });
    } else {
      skipped++;
    }
  }

  // 生成 manifest
  const manifest = generateManifest(docs);
  fs.writeFileSync(MANIFEST_FILE, manifest, 'utf-8');

  console.log(`完成：发现 ${docs.length} 个文档，跳过 ${skipped} 个`);
  if (skipped > 0) {
    console.log('（跳过：无 frontmatter 或信息不完整）');
  }
}

main();
