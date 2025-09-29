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



// ------- Primark: WOMEN — JEANS/TROUSERS (waist cm) -------
function primarkWomensJeans($) {
  const squeeze = s => String(s || "").replace(/\s+/g, " ").trim();
  const txt = squeeze($.root().text());

  function tokensAfter(label) {
    const i = txt.toLowerCase().indexOf(label.toLowerCase());
    if (i === -1) return [];
    const tail = txt.slice(i + label.length);
    const cut = tail.split(/(?:Men's|Shoes|Bras|Tights|Socks|FAQs|Tips|#)/i)[0];
    return squeeze(cut).split(/\s+/).filter(Boolean);
  }
  function avgToken(tok) {
    if (!tok) return null;
    tok = tok.replace(/upto\s*/i, "");
    const m = tok.match(/(\d+(?:\.\d+)?)[-–](\d+(?:\.\d+)?)/);
    if (m) return (parseFloat(m[1]) + parseFloat(m[2])) / 2;
    const n = tok.match(/\d+(?:\.\d+)?/);
    return n ? parseFloat(n[0]) : null;
  }

  // Use the same UK sizes as the main women block, then pair with waist cm
  let sizes = [];
  const block = tokensAfter("Dress size & conversion chart");
  const ukIdx = block.findIndex(t => /^UK\/IRL$/i.test(t));
  if (ukIdx !== -1) {
    for (let i = ukIdx + 1; i < block.length; i++) {
      const t = block[i];
      if (/^[A-Z/]+$/.test(t)) break;
      if (/^\d{1,2}(?:\/\d{1,2})?$/.test(t)) sizes.push(`UK ${t}`);
    }
  }
  if (sizes.length === 0) {
    const guess = tokensAfter("UK");
    sizes = guess.filter(x => /^\d{1,2}$/.test(x)).map(x => `UK ${x}`);
  }

  const waist = tokensAfter("To fit waist, cm").map(avgToken).filter(v => v != null);
  const n = Math.min(sizes.length, waist.length);
  const chart = [];
  for (let i = 0; i < n; i++) chart.push({ label: sizes[i], bust: null, waist: waist[i], hips: null });
  return { unit: "cm", chart };
}

// ------- Primark: WOMEN — BRAS (band + cup → overbust cm) -------
function primarkWomensBras($) {
  const squeeze = s => String(s || "").replace(/\s+/g, " ").trim();
  const txt = squeeze($.root().text());

  // isolate the Bras section
  const start = txt.toLowerCase().indexOf("bras");
  const tail = start === -1 ? txt : txt.slice(start);
  const sec = tail.split(/(?:Shoes|Footwear|Men's|FAQs|Tips|#)/i)[0];

  function tokensAfterIn(section, label) {
    const i = section.toLowerCase().indexOf(label.toLowerCase());
    if (i === -1) return [];
    const t = section.slice(i + label.length);
    const cut = t.split(/(?:Shoes|Footwear|Men's|FAQs|Tips|#)/i)[0];
    return squeeze(cut).split(/\s+/).filter(Boolean);
  }
  function avgToken(tok) {
    if (!tok) return null;
    tok = tok.replace(/upto\s*/i, "");
    const m = tok.match(/(\d+(?:\.\d+)?)[-–](\d+(?:\.\d+)?)/);
    if (m) return (parseFloat(m[1]) + parseFloat(m[2])) / 2;
    const n = tok.match(/\d+(?:\.\d+)?/);
    return n ? parseFloat(n[0]) : null;
  }

  // Band labels (UK/IRL row typically 30 32 34 36 ... )
  const bandLabels = tokensAfterIn(sec, "UK/IRL").filter(x => /^\d{2}$/.test(x));
  // Underband measurements (cm)
  const underband = tokensAfterIn(sec, "Underband").map(avgToken).filter(v => v != null);

  // Overbust per cup
  const cups = ["A","B","C","D","DD","E","F","G"];
  const overbustByCup = {};
  for (const cup of cups) {
    const arr = tokensAfterIn(sec, `Cup ${cup}`).map(avgToken).filter(v => v != null);
    if (arr.length) overbustByCup[cup] = arr;
  }

  const chart = [];
  for (const cup of cups) {
    const over = overbustByCup[cup] || [];
    const n = Math.min(bandLabels.length, over.length);
    for (let i = 0; i < n; i++) {
      const band = bandLabels[i];
      // label like "34B"; we store overbust as 'bust' (so your UI has a number)
      chart.push({ label: `${band}${cup}`, bust: over[i], waist: null, hips: null });
    }
  }
  // If we at least got something, say unit cm (overbust)
  return { unit: "cm", chart };
}

// ------- Primark: SHOES (Women) — label-only UK↔EU/US -------
function primarkWomensShoes($) {
  const squeeze = s => String(s || "").replace(/\s+/g, " ").trim();
  const txt = squeeze($.root().text());
  const start = txt.toLowerCase().indexOf("shoes");
  const sec = start === -1 ? txt : txt.slice(start).split(/(?:Bras|Tights|Socks|FAQs|Tips|#)/i)[0];

  function tokensAfterIn(section, label) {
    const i = section.toLowerCase().indexOf(label.toLowerCase());
    if (i === -1) return [];
    const t = section.slice(i + label.length);
    const cut = t.split(/(?:UK|EU|USA|US|Men's|Women's|FAQs|Tips|#)/i)[0];
    return squeeze(cut).split(/\s+/).filter(Boolean);
  }

  // Try to align by position: UK/IRL, EU, USA
  const uk = tokensAfterIn(sec, "UK/IRL").filter(x => /^[0-9](?:\.[05])?$/.test(x)); // 2 .. 9, 9.5, etc
  const eu = tokensAfterIn(sec, "EU").filter(x => /^\d{2}$/.test(x));                // 35 .. 43
  const us = tokensAfterIn(sec, "USA").filter(x => /^[0-9](?:\.[05])?$/.test(x));

  const n = Math.max(uk.length, eu.length, us.length);
  const chart = [];
  for (let i = 0; i < n; i++) {
    const label = uk[i] ? `UK ${uk[i]}` : (eu[i] ? `EU ${eu[i]}` : (us[i] ? `US ${us[i]}` : `Size ${i+1}`));
    chart.push({ label, bust: null, waist: null, hips: null });
  }
  return { unit: "shoe", chart };
}

// ------- Primark: WOMEN — JEANS/TROUSERS (waist cm) -------
function primarkWomensJeans($) {
  const squeeze = s => String(s || "").replace(/\s+/g, " ").trim();
  const txt = squeeze($.root().text());

  function tokensAfter(label) {
    const i = txt.toLowerCase().indexOf(label.toLowerCase());
    if (i === -1) return [];
    const tail = txt.slice(i + label.length);
    const cut = tail.split(/(?:Men's|Shoes|Bras|Tights|Socks|FAQs|Tips|#)/i)[0];
    return squeeze(cut).split(/\s+/).filter(Boolean);
  }
  function avgToken(tok) {
    if (!tok) return null;
    tok = tok.replace(/upto\s*/i, "");
    const m = tok.match(/(\d+(?:\.\d+)?)[-–](\d+(?:\.\d+)?)/);
    if (m) return (parseFloat(m[1]) + parseFloat(m[2])) / 2;
    const n = tok.match(/\d+(?:\.\d+)?/);
    return n ? parseFloat(n[0]) : null;
  }

  // Use the same UK sizes as the main women block, then pair with waist cm
  let sizes = [];
  const block = tokensAfter("Dress size & conversion chart");
  const ukIdx = block.findIndex(t => /^UK\/IRL$/i.test(t));
  if (ukIdx !== -1) {
    for (let i = ukIdx + 1; i < block.length; i++) {
      const t = block[i];
      if (/^[A-Z/]+$/.test(t)) break;
      if (/^\d{1,2}(?:\/\d{1,2})?$/.test(t)) sizes.push(`UK ${t}`);
    }
  }
  if (sizes.length === 0) {
    const guess = tokensAfter("UK");
    sizes = guess.filter(x => /^\d{1,2}$/.test(x)).map(x => `UK ${x}`);
  }

  const waist = tokensAfter("To fit waist, cm").map(avgToken).filter(v => v != null);
  const n = Math.min(sizes.length, waist.length);
  const chart = [];
  for (let i = 0; i < n; i++) chart.push({ label: sizes[i], bust: null, waist: waist[i], hips: null });
  return { unit: "cm", chart };
}

// ------- Primark: WOMEN — BRAS (band + cup → overbust cm) -------
function primarkWomensBras($) {
  const squeeze = s => String(s || "").replace(/\s+/g, " ").trim();
  const txt = squeeze($.root().text());

  // isolate the Bras section
  const start = txt.toLowerCase().indexOf("bras");
  const tail = start === -1 ? txt : txt.slice(start);
  const sec = tail.split(/(?:Shoes|Footwear|Men's|FAQs|Tips|#)/i)[0];

  function tokensAfterIn(section, label) {
    const i = section.toLowerCase().indexOf(label.toLowerCase());
    if (i === -1) return [];
    const t = section.slice(i + label.length);
    const cut = t.split(/(?:Shoes|Footwear|Men's|FAQs|Tips|#)/i)[0];
    return squeeze(cut).split(/\s+/).filter(Boolean);
  }
  function avgToken(tok) {
    if (!tok) return null;
    tok = tok.replace(/upto\s*/i, "");
    const m = tok.match(/(\d+(?:\.\d+)?)[-–](\d+(?:\.\d+)?)/);
    if (m) return (parseFloat(m[1]) + parseFloat(m[2])) / 2;
    const n = tok.match(/\d+(?:\.\d+)?/);
    return n ? parseFloat(n[0]) : null;
  }

  // Band labels (UK/IRL row typically 30 32 34 36 ... )
  const bandLabels = tokensAfterIn(sec, "UK/IRL").filter(x => /^\d{2}$/.test(x));
  // Underband measurements (cm)
  const underband = tokensAfterIn(sec, "Underband").map(avgToken).filter(v => v != null);

  // Overbust per cup
  const cups = ["A","B","C","D","DD","E","F","G"];
  const overbustByCup = {};
  for (const cup of cups) {
    const arr = tokensAfterIn(sec, `Cup ${cup}`).map(avgToken).filter(v => v != null);
    if (arr.length) overbustByCup[cup] = arr;
  }

  const chart = [];
  for (const cup of cups) {
    const over = overbustByCup[cup] || [];
    const n = Math.min(bandLabels.length, over.length);
    for (let i = 0; i < n; i++) {
      const band = bandLabels[i];
      // label like "34B"; we store overbust as 'bust' (so your UI has a number)
      chart.push({ label: `${band}${cup}`, bust: over[i], waist: null, hips: null });
    }
  }
  // If we at least got something, say unit cm (overbust)
  return { unit: "cm", chart };
}

// ------- Primark: SHOES (Women) — label-only UK↔EU/US -------
function primarkWomensShoes($) {
  const squeeze = s => String(s || "").replace(/\s+/g, " ").trim();
  const txt = squeeze($.root().text());
  const start = txt.toLowerCase().indexOf("shoes");
  const sec = start === -1 ? txt : txt.slice(start).split(/(?:Bras|Tights|Socks|FAQs|Tips|#)/i)[0];

  function tokensAfterIn(section, label) {
    const i = section.toLowerCase().indexOf(label.toLowerCase());
    if (i === -1) return [];
    const t = section.slice(i + label.length);
    const cut = t.split(/(?:UK|EU|USA|US|Men's|Women's|FAQs|Tips|#)/i)[0];
    return squeeze(cut).split(/\s+/).filter(Boolean);
  }

  // Try to align by position: UK/IRL, EU, USA
  const uk = tokensAfterIn(sec, "UK/IRL").filter(x => /^[0-9](?:\.[05])?$/.test(x)); // 2 .. 9, 9.5, etc
  const eu = tokensAfterIn(sec, "EU").filter(x => /^\d{2}$/.test(x));                // 35 .. 43
  const us = tokensAfterIn(sec, "USA").filter(x => /^[0-9](?:\.[05])?$/.test(x));

  const n = Math.max(uk.length, eu.length, us.length);
  const chart = [];
  for (let i = 0; i < n; i++) {
    const label = uk[i] ? `UK ${uk[i]}` : (eu[i] ? `EU ${eu[i]}` : (us[i] ? `US ${us[i]}` : `Size ${i+1}`));
    chart.push({ label, bust: null, waist: null, hips: null });
  }
  return { unit: "shoe", chart };
}


// WOMEN — dresses/tops with Bust/Waist/Hips (cm)
function primarkWomensBWH($) {
  const squeeze = s => String(s || "").replace(/\s+/g, " ").trim();
  const txt = squeeze($.root().text());

  // helper: tokens after a heading
  function tokensAfter(label) {
    const i = txt.toLowerCase().indexOf(label.toLowerCase());
    if (i === -1) return [];
    const tail = txt.slice(i + label.length);
    // stop when we hit another section header word
    const cut = tail.split(/(?:Men's|Women|Bras|Shoes|FAQs|Tips|#)/i)[0];
    return squeeze(cut).split(/\s+/).filter(Boolean);
  }
  // numbers / ranges → a single number
  function avgToken(tok) {
    if (!tok) return null;
    tok = tok.replace(/upto\s*/i, "");
    const m = tok.match(/(\d+(?:\.\d+)?)[-–](\d+(?:\.\d+)?)/);
    if (m) return (parseFloat(m[1]) + parseFloat(m[2])) / 2;
    const n = tok.match(/\d+(?:\.\d+)?/);
    return n ? parseFloat(n[0]) : null;
  }

  // pull sizes and three measurement rows
  // Primark usually shows a UK/IRL row of sizes (4 6 8 10 ...)
  const block = tokensAfter("Dress size & conversion chart");
  let sizes = [];
  const ukIdx = block.findIndex(t => /^UK\/IRL$/i.test(t));
  if (ukIdx !== -1) {
    for (let i = ukIdx + 1; i < block.length; i++) {
      const t = block[i];
      if (/^[A-Z/]+$/.test(t)) break; // next header like EUR/USA/IT
      if (/^\d{1,2}(?:\/\d{1,2})?$/.test(t)) sizes.push(`UK ${t}`);
    }
  }

  // Some pages don’t show the UK row up front; if empty, fall back to any bare numbers we see
  if (sizes.length === 0) {
    const guesses = tokensAfter("UK");
    sizes = guesses.filter(x => /^\d{1,2}$/.test(x)).map(x => `UK ${x}`);
  }

  const bust  = tokensAfter("To fit bust, cm").map(avgToken).filter(v => v != null);
  const waist = tokensAfter("To fit waist, cm").map(avgToken).filter(v => v != null);
  const hips  = tokensAfter("To fit hips, cm").map(avgToken).filter(v => v != null);

  const n = Math.min(sizes.length, bust.length, waist.length, hips.length);
  const chart = [];
  for (let i = 0; i < n; i++) {
    chart.push({ label: sizes[i], bust: bust[i], waist: waist[i], hips: hips[i] });
  }
  return { unit: "cm", chart };
}

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
