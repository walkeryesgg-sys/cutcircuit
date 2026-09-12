import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { pathToFileURL } from "node:url";
import { spawnSync } from "node:child_process";

interface ParsedArticle {
  title: string;
  author: string;
  summary: string;
  htmlPath: string;
  contentImages: Array<{ localPath: string; placeholder: string }>;
}

function value(name: string): string {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] || "" : "";
}

const editUrl = value("--url");
const markdown = path.resolve(value("--markdown"));
const theme = value("--theme") || "simple";
const color = value("--color") || "blue";
const port = Number(value("--cdp-port") || "9223");
if (!editUrl || !markdown) throw new Error("--url and --markdown are required");
if (!fs.existsSync(markdown)) throw new Error(`Markdown not found: ${markdown}`);

const baoyuRoot = process.env.BAOYU_POST_TO_WECHAT_DIR
  || path.join(os.homedir(), ".agents/skills/baoyu-post-to-wechat");
const renderer = path.join(baoyuRoot, "scripts/md-to-wechat.ts");
const cdpModule = path.join(baoyuRoot, "node_modules/baoyu-chrome-cdp/dist/index.js");
if (!fs.existsSync(renderer) || !fs.existsSync(cdpModule)) {
  throw new Error("baoyu-post-to-wechat runtime not found; set BAOYU_POST_TO_WECHAT_DIR");
}

const rendered = spawnSync("bun", [renderer, markdown, "--theme", theme, "--color", color], {
  encoding: "utf8",
});
if (rendered.status !== 0) throw new Error(rendered.stderr || "Markdown rendering failed");
const article = JSON.parse(rendered.stdout) as ParsedArticle;
if (article.contentImages.length) {
  throw new Error("Existing-draft updater currently requires an article without inline local images");
}

const { CdpConnection } = await import(pathToFileURL(cdpModule).href);
const version = await fetch(`http://127.0.0.1:${port}/json/version`).then((response) => response.json()) as {
  webSocketDebuggerUrl: string;
};
const cdp = await CdpConnection.connect(version.webSocketDebuggerUrl, 10_000);
const targets = await cdp.send("Target.getTargets") as {
  targetInfos: Array<{ targetId: string; type: string; url: string }>;
};
const page = targets.targetInfos.find((target) => target.type === "page" && target.url.includes("mp.weixin.qq.com"))
  || targets.targetInfos.find((target) => target.type === "page");
if (!page) throw new Error("No browser page found");
const attached = await cdp.send("Target.attachToTarget", { targetId: page.targetId, flatten: true }) as {
  sessionId: string;
};
const sessionId = attached.sessionId;
await cdp.send("Page.enable", {}, { sessionId });
await cdp.send("Runtime.enable", {}, { sessionId });
await cdp.send("DOM.enable", {}, { sessionId });
await cdp.send("Page.navigate", { url: editUrl }, { sessionId });

async function sleep(ms: number) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function evaluate<T>(expression: string, awaitPromise = false): Promise<T> {
  const result = await cdp.send("Runtime.evaluate", {
    expression,
    returnByValue: true,
    awaitPromise,
  }, { sessionId }) as { result: { value: T } };
  return result.result.value;
}

const start = Date.now();
while (Date.now() - start < 30_000) {
  if (await evaluate<boolean>("!!document.querySelector('#title') && !!document.querySelector('.rich_media_content .ProseMirror')")) break;
  await sleep(500);
}
if (!await evaluate<boolean>("!!document.querySelector('#title')")) throw new Error("Draft editor did not load");

const html = fs.readFileSync(article.htmlPath, "utf8");
const updateResult = await evaluate<{ title: string; summary: string; bodyLength: number }>(`
  (() => {
    const title = document.querySelector('#title');
    const author = document.querySelector('#author');
    const summary = document.querySelector('#js_description');
    const editor = document.querySelector('.rich_media_content .ProseMirror');
    if (!title || !summary || !editor) throw new Error('Required editor field missing');

    title.value = ${JSON.stringify(article.title)};
    title.dispatchEvent(new Event('input', { bubbles: true }));
    title.dispatchEvent(new Event('change', { bubbles: true }));
    if (author && ${JSON.stringify(article.author)}) {
      author.value = ${JSON.stringify(article.author)};
      author.dispatchEvent(new Event('input', { bubbles: true }));
    }

    const template = document.createElement('template');
    template.innerHTML = ${JSON.stringify(html)};
    const output = template.content.querySelector('#output');
    editor.focus();
    editor.innerHTML = output ? output.innerHTML : template.innerHTML;
    editor.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertHTML' }));

    summary.value = ${JSON.stringify(article.summary)};
    summary.dispatchEvent(new Event('input', { bubbles: true }));
    summary.dispatchEvent(new Event('change', { bubbles: true }));
    summary.dispatchEvent(new Event('blur', { bubbles: true }));

    return {
      title: title.value,
      summary: summary.value,
      bodyLength: (editor.innerText || '').trim().length
    };
  })()
`);
if (updateResult.title !== article.title || updateResult.summary !== article.summary || updateResult.bodyLength < 100) {
  throw new Error(`Draft field verification failed: ${JSON.stringify(updateResult)}`);
}

const coverVerified = await evaluate<boolean>(`
  (() => {
    const preview = document.querySelector('#js_cover_area .js_cover_preview_new');
    return !!preview && getComputedStyle(preview).display !== 'none';
  })()
`);
if (!coverVerified) throw new Error("Existing cover preview is missing; refusing to save");

await evaluate("document.querySelector('#js_submit button')?.click()");
let savedId = "";
const saveStart = Date.now();
while (Date.now() - saveStart < 60_000) {
  const state = await evaluate<{ id: string; loading: boolean }>(`
    (() => {
      const submit = document.querySelector('#js_submit');
      return {
        id: new URL(location.href).searchParams.get('appmsgid') || '',
        loading: !!submit?.classList.contains('btn_loading') || !!submit?.querySelector('button')?.disabled
      };
    })()
  `);
  if (state.id && !state.loading) {
    savedId = state.id;
    break;
  }
  await sleep(1000);
}
if (!savedId) throw new Error("Draft save did not complete");
cdp.close();
console.log(JSON.stringify({
  result: "success",
  action: "updated-draft",
  appmsgid: savedId,
  theme,
  color,
  cover: "verified",
  title: article.title,
}, null, 2));
