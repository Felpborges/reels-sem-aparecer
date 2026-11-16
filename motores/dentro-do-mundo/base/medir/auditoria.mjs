// ESTILO B · AUDITORIA QUADRO A QUADRO do texto (todo quadro do vídeo).
// uso: node medir/auditoria.mjs [fps=30] [porta=8731]   -> medir/auditoria.json
// Para cada quadro: avança a timeline, liga só os mundos ativos (como o HyperFrames) e mede CADA PALAVRA visível:
//   corte    — parte da palavra fora da tela (ou da faixa 1:1, ou de um contêiner que corta)
//   vaza     — a palavra sai da superfície onde mora (tela do aparelho, papel, lousa): marcadores .canto
//   coberta  — um objeto (imagem, placa, bloco com fundo) está por cima da palavra
//   encosta  — duas palavras de elementos diferentes se sobrepõem
//   pequena  — altura na tela < 20 px (em 1080x1920)
import { createRequire } from "module"; import { fileURLToPath } from "url"; import http from "http"; import fs from "fs"; import path from "path";
const require = createRequire(process.env.RSA_NODE_MODULES || (process.env.HOME + "/.claude/skills/reels-sem-aparecer/ferramentas/node_modules/"));
const puppeteer = require("puppeteer-core");
const DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const FPS = Number(process.argv[2] || 30), PORTA = Number(process.argv[3] || 8731);
const TIPOS = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".woff2": "font/woff2", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".json": "application/json" };
const srv = http.createServer((q, r) => { const f = path.join(DIR, decodeURIComponent(q.url.split("?")[0]));
  fs.readFile(f, (e, b) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { "Content-Type": TIPOS[path.extname(f)] || "application/octet-stream" }); r.end(b); }); }).listen(PORTA);
const browser = await puppeteer.launch({ executablePath: process.env.RSA_CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new", args: ["--hide-scrollbars"] });
const page = await browser.newPage(); await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
await page.goto(`http://localhost:${PORTA}/index.html`, { waitUntil: "load", timeout: 180000 });
await page.evaluate(async () => { await document.fonts.ready; await new Promise((r) => setTimeout(r, 300)); });
const dur = await page.evaluate(() => Number(document.getElementById("root").dataset.duration));
const res = [];
for (let q = 0; q < Math.round(dur * FPS); q++) {
  const t = (q + 0.5) / FPS;
  res.push(await page.evaluate((t) => {
    const tl = window.__timelines.main; tl.seek(t, false);
    for (const c of document.querySelectorAll("#stage > .clip")) { const a = +c.dataset.start, d = +c.dataset.duration; c.style.display = (t >= a && t < a + d) ? "" : "none"; }
    const opac = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === "none" || cs.visibility === "hidden") return 0; o *= +cs.opacity; } return o; };
    const dono = (el) => { for (let e = el; e; e = e.parentElement) if (e.id) return e.id; return "?"; };
    const out = [], W = 1080, H = 1920;
    const ativos = [...document.querySelectorAll("#stage > .mundo")].filter((c) => c.style.display !== "none");
    const topo = ativos.length ? ativos[ativos.length - 1] : null;
    const walker = document.createTreeWalker(document.getElementById("stage"), NodeFilter.SHOW_TEXT);
    let n; const palavras = [];
    while ((n = walker.nextNode())) {
      const el = n.parentElement; if (!n.data.trim() || el.closest(".deco")) continue;
      if (topo && el.closest(".mundo") !== topo) continue;
      const op = opac(el); if (op < 0.35) continue;
      const re = /\S+/g; let m;
      while ((m = re.exec(n.data))) {
        const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
        const r = rg.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
        if (r.height > 360) continue;                       // letra gigante de propósito (câmera atravessando a palavra)
        // máscara de "escrita" (escreve()): só conta a parte já revelada
        const mk = el.closest("[style*='mask-image']");
        if (mk && mk.style.maskImage && mk.style.maskImage.includes("90deg")) {
          const pm = mk.style.maskImage.match(/transparent ([-\d.]+)%/); const pr = pm ? +pm[1] : 100;
          const b0 = (() => { const sv = []; for (let e = mk; e && e.id !== "root"; e = e.parentElement) { sv.push([e, e.style.transform]); e.style.transform = "none"; }
            const bb = mk.getBoundingClientRect(), wr = rg.getBoundingClientRect(); for (const [e, t] of sv) e.style.transform = t; return (wr.right - bb.left) / bb.width * 100; })();
          if (b0 > pr) continue;
        }
        palavras.push({ w: m[0], el, r, op, k: palavras.filter((p) => p.el === el).length, rg });
      }
    }
    // mede "vaza" com as transformações desligadas (a superfície vira a caixa w x h original)
    const sups = new Set(palavras.map((p) => p.el.closest(".sup")).filter(Boolean));
    for (const sup of sups) {
      const salvos = []; for (let e = sup; e && e.id !== "root"; e = e.parentElement) { salvos.push([e, e.style.transform, e.style.filter]); e.style.transform = "none"; }
      const b = sup.getBoundingClientRect();
      for (const p of palavras) if (p.el.closest(".sup") === sup) {
        const q = p.rg.getBoundingClientRect(), tol = 2;
        const ix = Math.max(0, Math.min(q.right, b.right) - Math.max(q.left, b.left)) * Math.max(0, Math.min(q.bottom - q.height * .18, b.bottom) - Math.max(q.top + q.height * .22, b.top));
        p.vaza = ix < (q.width * q.height * .60) * 0.97 || q.left < b.left - tol || q.right > b.right + tol;
      }
      for (const [e, t, f] of salvos) { e.style.transform = t; }
    }
    for (const p of palavras) {
      const { r, el } = p; const iss = [];
      // região visível: tela, faixa (clip-path inset), contêineres com overflow
      let x0 = 0, y0 = 0, x1 = W, y1 = H, fx0 = 0, fy0 = 0, fx1 = W, fy1 = H;
      for (let e = el; e && e.id !== "stage"; e = e.parentElement) {
        const cs = getComputedStyle(e);
        if (e.classList.contains("fx") && cs.clipPath && cs.clipPath.startsWith("inset")) { let v = (cs.clipPath.match(/inset\(([^)]*)\)/)[1].match(/-?[\d.]+/g) || []).map(Number);
          v = v.length === 1 ? [v[0], v[0], v[0], v[0]] : v.length === 2 ? [v[0], v[1], v[0], v[1]] : v.length === 3 ? [v[0], v[1], v[2], v[1]] : v; const b = e.getBoundingClientRect(); const k = b.height / e.offsetHeight || 1; fy0 = b.top + v[0] * k; fy1 = b.bottom - v[2] * k; y0 = Math.max(y0, fy0); y1 = Math.min(y1, fy1); }
        if (cs.overflow !== "visible" && !e.classList.contains("cam") && !e.classList.contains("mundo") && !e.classList.contains("fx")) { const b = e.getBoundingClientRect(); x0 = Math.max(x0, b.left); y0 = Math.max(y0, b.top); x1 = Math.min(x1, b.right); y1 = Math.min(y1, b.bottom); }
      }
      const ix = Math.max(0, Math.min(r.right, x1) - Math.max(r.left, x0)), iy = Math.max(0, Math.min(r.bottom, y1) - Math.max(r.top, y0));
      const vis = (ix * iy) / (r.width * r.height);
      if (!Number.isFinite(vis)) throw new Error("medida inválida em " + dono(el));
      if (vis < 0.97) iss.push(vis < 0.03 ? "fora" : "corte");
      else if (r.left < fx0 + 54 || r.right > fx1 - 54 || r.top < fy0 + 30 || r.bottom > fy1 - 30) iss.push("rente");   // só a borda da tela/faixa
      // superfície em perspectiva: medida no espaço da própria superfície (sem câmera nem quad), contra a caixa w x h
      if (p.vaza) iss.push("vaza");
      // cobertura: pontos internos da palavra; o que está por cima?
      if (vis > 0.03) {
        let cob = 0, quem = "";
        const amostras = [[.5, .5], [.2, .5], [.8, .5], [.5, .3], [.5, .7]];
        for (const [fx, fy] of amostras) {
          const x = r.left + r.width * fx, y = r.top + r.height * fy; if (x < 0 || y < 0 || x >= W || y >= H) continue;
          for (const h of document.elementsFromPoint(x, y)) {
            if (h === el || el.contains(h) || h.contains(el)) break;
            if (opac(h) < 0.3) continue;
            const cs = getComputedStyle(h);
            const tem_fundo = (cs.backgroundColor && !/rgba\(.*, 0\)|transparent/.test(cs.backgroundColor)) || (cs.backgroundImage && cs.backgroundImage !== "none");
            if (h.tagName === "IMG" || h.closest(".occ") || (tem_fundo && !h.classList.contains("cam") && !h.classList.contains("mundo"))) { cob++; quem = dono(h); break; }
            if (h.tagName !== "DIV" && h.tagName !== "SPAN") continue;
          }
        }
        if (cob >= 2) iss.push("coberta:" + quem);
      }
      if (r.height < 20) iss.push("pequena");
      p.iss = iss;
    }
    // encosta: palavras de elementos diferentes que se sobrepõem
    for (let i = 0; i < palavras.length; i++) for (let j = i + 1; j < palavras.length; j++) {
      const a = palavras[i], b = palavras[j]; if (dono(a.el) === dono(b.el)) continue;
      if (a.iss.includes("fora") || b.iss.includes("fora")) continue;
      // faixa central da letra (a caixa da fonte é bem mais alta que o desenho, sobretudo nas manuscritas)
      const fa = (r) => ({ l: r.left + r.width * .04, r: r.right - r.width * .04, t: r.top + r.height * .28, b: r.bottom - r.height * .22 });
      const A_ = fa(a.r), B_ = fa(b.r);
      const ix = Math.max(0, Math.min(A_.r, B_.r) - Math.max(A_.l, B_.l)), iy = Math.max(0, Math.min(A_.b, B_.b) - Math.max(A_.t, B_.t));
      const menor = Math.min(a.r.width * a.r.height, b.r.width * b.r.height);
      if (ix * iy > 0.06 * menor) { a.iss.push("encosta:" + b.w); b.iss.push("encosta:" + a.w); }
    }
    // cobertura do fundo: a foto nítida (.cobre) ou o fundo da câmera (faixa) tem que cobrir toda a área visível
    if (topo) {
      const fx = topo.querySelector(".fx"), cs = getComputedStyle(fx); let ry0 = 0, ry1 = H;
      if (cs.clipPath && cs.clipPath.startsWith("inset")) { let v = (cs.clipPath.match(/inset\(([^)]*)\)/)[1].match(/-?[\d.]+/g) || []).map(Number);
        v = v.length === 1 ? [v[0], v[0], v[0], v[0]] : v.length === 2 ? [v[0], v[1], v[0], v[1]] : v.length === 3 ? [v[0], v[1], v[2], v[1]] : v; ry0 = v[0] * 1.5; ry1 = H - v[2] * 1.5; }
      const quads = [...topo.querySelectorAll(".cobre")].filter((c) => opac(c) > 0.9).map((c) => [...c.querySelectorAll(":scope > .canto")].map((q) => { const b = q.getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height / 2]; }));
      const cam = topo.querySelector(".cam");
      if (!quads.length && cam.style.background) { const b = cam.getBoundingClientRect(); quads.push([[b.left, b.top], [b.right, b.top], [b.right, b.bottom], [b.left, b.bottom]]); }
      const borr = +((getComputedStyle(cam).filter.match(/blur\(([\d.]+)px\)/) || [0, 0])[1]);
      if (quads.length && borr < 2) {                    // câmera borrada de propósito (giro, rolagem): o canto não conta
        const dentro = (Q, x, y) => { let s = 0; for (let i = 0; i < 4; i++) { const [ax, ay] = Q[i], [bx, by] = Q[(i + 1) % 4]; const c = (bx - ax) * (y - ay) - (by - ay) * (x - ax); s += c > 0 ? 1 : c < 0 ? -1 : 0; } return Math.abs(s) === 4; };
        const pts = [[2, ry0 + 2], [W / 2, ry0 + 2], [W - 2, ry0 + 2], [W - 2, (ry0 + ry1) / 2], [W - 2, ry1 - 2], [W / 2, ry1 - 2], [2, ry1 - 2], [2, (ry0 + ry1) / 2]];
        const fora = pts.filter(([x, y]) => !quads.some((Q) => dentro(Q, x, y)));
        if (fora.length) out.push({ w: "<fundo>", k: 0, id: topo.id, x: Math.round(fora[0][0]), y: Math.round(fora[0][1]), wd: 0, h: 0, iss: ["borda"] });
      }
    }
    // zona dos botões do Instagram (coluna direita) e da legenda (rodapé): texto importante não deve morar ali
    for (const p of palavras) if (!p.iss.includes("fora") && ((p.r.right > W * 0.86 && p.r.top > H * 0.52 && p.r.bottom < H * 0.84) || p.r.bottom > H * 0.86)) p.iss.push("zona-ig");
    for (const p of palavras) out.push({ w: p.w, k: p.k, id: dono(p.el), x: Math.round(p.r.left), y: Math.round(p.r.top), wd: Math.round(p.r.width), h: Math.round(p.r.height), iss: p.iss });
    return { t: +t.toFixed(3), palavras: out };
  }, t));
  if (q % 150 === 0) process.stderr.write(`quadro ${q}/${Math.round(dur * FPS)}\n`);
}
fs.writeFileSync(path.join(DIR, "medir", "auditoria.json"), JSON.stringify(res));
await browser.close(); srv.close(); console.log("ok", res.length, "quadros");
