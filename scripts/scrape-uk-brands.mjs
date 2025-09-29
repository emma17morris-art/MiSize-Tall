import fs from "node:fs/promises";
import path from "node:path";
import { request } from "undici";
import * as cheerio from "cheerio";

const ROOT = path.resolve(process.cwd());
const OUT_PATH = path.join(ROOT, "uk_brands.json");          // Your app fetches this path
const CFG_PATH = path.join(ROOT, "scripts", "brands.config.json");

// Helpers
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
      hips: num(get(sel.hips)),
      // add other fields if you need: inseam, chest, etc.
    };
    if (entry.label) rows.push(entry);
  });
  // basic clean: drop header-ish rows
  return rows.filter(r => !/size|cm|inch/i.test(r.label));
}

async function scrapeCategory(cat) {
  const html = await fetchHtml(cat.url);
  const $ = cheerio.load(html);
  let chart = [];
  switch (cat.parser) {
    case "table":
    default:
      chart = parseTable($, cat.selectors);
  }
  return {
    unit: cat.unit || "cm",
    chart
  };
}

async function run() {
  const cfg = JSON.parse(await fs.readFile(CFG_PATH, "utf8"));

  const out = {}; // <- target schema your UI expects
  for (const brand of cfg.brands) {
    const brandBlock = {
      lastUpdated: new Date().toISOString(),
      categories: {}
    };

    for (const cat of brand.categories) {
      try {
        const res = await scrapeCategory(cat);
        brandBlock.categories[cat.name] = res;
      } catch (e) {
        brandBlock.categories[cat.name] = {
          unit: cat.unit || "cm",
          chart: [],
          error: String(e.message || e)
        };
      }
    }

    out[brand.name] = brandBlock;
  }

  // Write where your front-end already fetches it
  await fs.writeFile(OUT_PATH, JSON.stringify(out, null, 2), "utf8");
  console.log(`✅ wrote ${OUT_PATH}`);
}

run().catch(e => {
  console.error(e);
  process.exit(1);
});
