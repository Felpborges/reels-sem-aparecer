// ESTILO C · busca o PRINT REAL do site e o LOGO OFICIAL de uma marca (regra do Felipe: logo oficial e print real, nunca redesenho).
// uso: node medir/marca.mjs <site, ex.: ifood.com.br> <slug>   -> assets/img/print-<slug>.jpg (1440x810, topo da home) e logo-<slug>.png
// Logo: o maior ícone declarado pelo próprio site (apple-touch-icon / icon / manifest); sem ele, o favicon de 256 px do Google.
// CONFERIR NO OLHO: banner de cookies, pop-up ou página em outro idioma -> refazer com outra URL (ex.: /sobre) ou recortar.
import { createRequire } from "module"; import { fileURLToPath } from "url"; import fs from "fs"; import path from "path";
const require = createRequire(process.env.RSA_NODE_MODULES || (process.env.HOME + "/.claude/skills/reels-sem-aparecer/ferramentas/node_modules/"));
const puppeteer = require("puppeteer-core");
const DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const [site, slug] = process.argv.slice(2); const url = site.startsWith("http") ? site : "https://" + site;
const browser = await puppeteer.launch({ executablePath: process.env.RSA_CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new",
  args: ["--hide-scrollbars", "--lang=pt-BR"] });
const page = await browser.newPage(); await page.setViewport({ width: 1440, height: 810, deviceScaleFactor: 1 });
await page.setExtraHTTPHeaders({ "Accept-Language": "pt-BR,pt;q=0.9" });
await page.setUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36");
try { await page.goto(url, { waitUntil: "networkidle2", timeout: 45000 }); } catch (e) { console.error("aviso:", e.message); }
await new Promise((r) => setTimeout(r, 2500));
// fecha banners comuns de cookies/consentimento (só clica em "recusar/fechar/aceitar só o necessário" — nunca em login)
await page.evaluate(() => { const alvo = /(rejeitar|recusar|somente (o )?necess|apenas (o )?necess|fechar|close|reject|decline|dismiss)/i;
  for (const b of document.querySelectorAll("button,[role=button],a")) if (alvo.test((b.innerText || b.getAttribute("aria-label") || "").trim()) && (b.innerText || "").length < 40) { try { b.click(); } catch (e) {} } });
await new Promise((r) => setTimeout(r, 1200));
const out = path.join(DIR, "assets", "img"); fs.mkdirSync(out, { recursive: true });
await page.screenshot({ path: path.join(out, `print-${slug}.jpg`), type: "jpeg", quality: 92 });
const icones = await page.evaluate(() => [...document.querySelectorAll("link[rel*=icon],link[rel=apple-touch-icon],link[rel=apple-touch-icon-precomposed]")]
  .map((l) => ({ href: l.href, s: parseInt((l.getAttribute("sizes") || "0").split("x")[0]) || (l.rel.includes("apple") ? 180 : 16) })).sort((a, b) => b.s - a.s));
let ok = false;
for (const ic of icones.filter((i) => i.s >= 96 && !i.href.endsWith(".svg"))) {
  try { const r = await page.goto(ic.href); const b = await r.buffer(); if (b.length > 1500) { fs.writeFileSync(path.join(out, `logo-${slug}.png`), b); ok = true; console.log("logo do site", ic.href, ic.s); break; } } catch (e) {}
}
if (!ok) { const h = new URL(url).hostname; const r = await page.goto(`https://www.google.com/s2/favicons?domain=${h}&sz=256`); fs.writeFileSync(path.join(out, `logo-${slug}.png`), await r.buffer()); console.log("logo via favicon 256"); }
await browser.close(); console.log(`print-${slug}.jpg · logo-${slug}.png`);
