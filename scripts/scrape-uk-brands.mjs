import fs from "node:fs/promises";
import path from "node:path";
import { request } from "undici";
import * as cheerio from "cheerio";

const ROOT = path.resolve(process.cwd());
const OUT_PATH = path.join(ROOT, "uk_brands.json");
const CFG_PATH = path.join(ROOT, "scripts", "brands.config.json");
const UA = "MiSizeBot/1.0 (contact: you@example.com)";

const num = v => {
  if (v == null) return null;
  const n = String(v).replace(/[^\d.,-]/g, "").replace(",", ".");
  const f = parseFloat(n);
  return Number.isFinite(f) ? f : null;
};

async function fetchHtml(url) {
  const res = await request(url, { headers: { "User-Agent": UA }});
  if (res.statusCode >= 400) throw new Error(`Fetch ${url} → ${res.statusCode}`);
  return await res.body.text();
}

function parseTable($, sel) {
  const rows = [];
  $(sel.row).each((_, tr) => {
    const get = s => (s ? $(tr).find(s).first().text().trim() : null);
    const entry = {
      label: get(sel.size) || get(sel.label) || null,
      bust: num(get(sel.bust)),
      waist: num(get(sel.waist)),
      hips: num(get(sel.hips))
    };
    if (entry.label) rows.push(entry);
  });
  return rows.filter(r => !/size|cm|inch/i.test(r.label));
}

// ===== Primark helpers (added) =====
const squeeze = s => String(s || "").replace(/\s+/g, " ").trim();

// Turn "91-96" into 93.5, "upto 90" into 90, or "90" into 90
function avgToken(tok) {
  if (!tok) return null;
  tok = tok.replace(/upto\s*/i, "");
  const m = tok.match(/(\d+(?:\.\d+)?)[-–](\d+(?:\.\d+)?)/);
  if (m) return (parseFloat(m[1]) + parseFloat(m[2])) / 2;
  const n = tok.match(/\d+(?:\.\d+)?/);
  return n ? parseFloat(n[0]) : null;
}

// Grab tokens after a heading phrase
function tokensAfter(text, label, stopRegex = /(?:#|Men's|Women’s|Women'|Tips|FAQs)/i) {
  const i = text.search(new RegExp(label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i"));
  if (i === -1) return [];
  const tail = text.slice(i + label.length);
  const cut = tail.split(stopRegex)[0];
  return squeeze(cut).split(/\s+/).filter(Boolean);
}

// MEN — CASUAL TOPS (XS..3XL + chest cm)
function primarkMensTops($) {
  const txt = squeeze($.root().text());
  const sizes = tokensAfter(txt, "UK/IRL/EU/US/IT");
  const chest = tokensAfter(txt, "To fit chest, cm");
  const chestVals = chest.map(avgToken).filter(v => v != null);

  const chart = [];
  const n = Math.min(sizes.length, chestVals.length);
  for (let i = 0; i < n; i++) {
    chart.push({ label: sizes[i], bust: chestVals[i], waist: null, hips: null });
  }
  return { unit: "cm", chart };
}

// MEN — JEANS/TROUSERS (W26.. + waist cm)
function primarkMensJeans($) {
  const txt = squeeze($.root().text());
  const wSizes = tokensAfter(txt, "UK/IRL/US Inches");
  const waistCm = tokensAfter(txt, "IT Inches CM");
  const waistVals = waistCm.map(avgToken).filter(v => v != null);

  const chart = [];
  const n = Math.min(wSizes.length, waistVals.length);
  for (let i = 0; i < n; i++) {
    chart.push({ label: `W${wSizes[i]}`, bust: null, waist: waistVals[i], hips: null });
  }
  return { unit: "cm", chart };
}

// WOMEN — Dress size conversion (UK)
function primarkWomensDressConv($) {
  const txt = squeeze($.root().text());
  const block = tokensAfter(txt, "Dress size & conversion chart");
  const ukIdx = block.findIndex(t => /^UK\/IRL$/i.test(t));
  const labels = [];
  if (ukIdx !== -1) {
    for (let i = ukIdx + 1; i < block.length; i++) {
      const t = block[i];
      if (/^[A-Z/]+$/.test(t)) break; // hit next header like EUR/USA/IT
      if (/^\d{1,2}(?:\/\d{1,2})?$/.test(t)) labels.push(`UK ${t}`);
    }
  }
  const chart = labels.map(l => ({ label: l, bust: null, waist: null, hips: null }));
  return { unit: "size", chart };
}
// ===== end Primark helpers =====

async function scrapeCategory(cat) {
  const html = await fetchHtml(cat.url);
  const $ = cheerio.load(html);

  // Table (default)
  if ((cat.parser || "table") === "table") {
    const chart = parseTable($, cat.selectors);
    return { unit: cat.unit || "cm", chart };
  }

  // Primark custom parsers
  if (cat.parser === "primark_mens_tops")   return primarkMensTops($);
  if (cat.parser === "primark_mens_jeans")  return primarkMensJeans($);
  if (cat.parser === "primark_womens_dress_conv") return primarkWomensDressConv($);

  // Fallback
  const chart = parseTable($, cat.selectors);
  return { unit: cat.unit || "cm", chart };
}

async function run() {
  const cfg = JSON.parse(await fs.readFile(CFG_PATH, "utf8"));
  const out = {};

  for (const brand of cfg.brands) {
    const block = { lastUpdated: new Date().toISOString(), categories: {} };
    for (const cat of brand.categories) {
      try {
        block.categories[cat.name] = await scrapeCategory(cat);
      } catch (e) {
        block.categories[cat.name] = {
          unit: cat.unit || "cm",
          chart: [],
          error: String(e.message || e)
        };
      }
    }
    out[brand.name] = block;
  }
  await fs.writeFile(OUT_PATH, JSON.stringify(out, null, 2), "utf8");
  console.log(`✅ wrote ${OUT_PATH}`);
}

run().catch(e => { console.error(e); process.exit(1); });
