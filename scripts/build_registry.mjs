import fs from "fs";
import path from "path";

const AIRTABLE_TOKEN = process.env.AIRTABLE_TOKEN;
const BASE_ID = process.env.AIRTABLE_BASE_ID;
const TABLE = process.env.AIRTABLE_TABLE_NAME || "Certification_Registry";
const VIEW = process.env.AIRTABLE_VIEW_NAME || "PUBLISH_REGISTRY";

const PUBLISHER_NAME = process.env.REGISTRY_PUBLISHER_NAME || "AI Fiduciary Governance Certification\u2122";
const DISCLAIMER = process.env.REGISTRY_DISCLAIMER || "Registry confirms certification status only.";

if (!AIRTABLE_TOKEN || !BASE_ID) {
  console.error("Missing AIRTABLE_TOKEN or AIRTABLE_BASE_ID");
  process.exit(1);
}

const REGISTRY_DIR = path.resolve("registry");
const SCHEMA_SRC = path.resolve("scripts", "schema_v1_0.json");
const SCHEMA_DEST = path.join(REGISTRY_DIR, "afgc-registry.schema.json");
const JSON_DEST = path.join(REGISTRY_DIR, "afgc-registry.json");

function isoDate(value) {
  if (!value) return null;
  const s = String(value).trim();
  if (/^\d{4}-\d{2}-\d{2}$/.test(s)) return s;
  const d = new Date(s);
  if (Number.isNaN(d.getTime())) return null;
  return d.toISOString().slice(0, 10);
}

function normStatus(s) {
  const v = String(s || "").trim();
  if (["Active", "Expired", "Revoked"].includes(v)) return v;
  return "Active";
}

function normEntityType(s) {
  const v = String(s || "").trim();
  const allowed = new Set(["Trust", "Corporation", "NGO", "Public Entity", "SPV", "Other"]);
  return allowed.has(v) ? v : "Other";
}

function clamp(str, max) {
  const v = String(str || "").trim();
  return v.length > max ? v.slice(0, max) : v;
}

async function fetchAllRecords() {
  const baseUrl = `https://api.airtable.com/v0/${BASE_ID}/${encodeURIComponent(TABLE)}`;
  let offset = undefined;
  const all = [];

  while (true) {
    const url = new URL(baseUrl);
    url.searchParams.set("view", VIEW);
    url.searchParams.set("pageSize", "100");
    if (offset) url.searchParams.set("offset", offset);

    const res = await fetch(url.toString(), {
      headers: { Authorization: `Bearer ${AIRTABLE_TOKEN}` }
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`Airtable fetch failed: ${res.status} ${txt}`);
    }

    const data = await res.json();
    all.push(...(data.records || []));
    offset = data.offset;
    if (!offset) break;
  }
  return all;
}

function mapRecord(r) {
  const f = r.fields || {};
  const entry = {
    certification_id: clamp(f.Certification_ID, 20),
    entity_legal_name: clamp(f.Entity_Name, 200),
    jurisdiction: clamp(f.Jurisdiction, 120),
    entity_type: normEntityType(f.Entity_Type),
    status: normStatus(f.Status),
    issued_date: isoDate(f.Issued_Date),
    expiration_date: isoDate(f.Expiration_Date),
    scope_high_level: clamp(f.High_Level_Scope, 280)
  };

  const note = clamp(f.Public_Note, 240);
  if (note) entry.notes_public = note;

  if (!entry.issued_date || !entry.expiration_date) {
    throw new Error(`Missing issued_date/expiration_date for ${entry.certification_id || "(no id)"}`);
  }

  if (!/^AFGC-\d{4}-\d{4}$/.test(entry.certification_id)) {
    throw new Error(`Bad certification_id format: ${entry.certification_id}`);
  }

  return entry;
}

async function main() {
  if (!fs.existsSync(REGISTRY_DIR)) fs.mkdirSync(REGISTRY_DIR, { recursive: true });

  fs.copyFileSync(SCHEMA_SRC, SCHEMA_DEST);

  const records = await fetchAllRecords();
  const entries = records.map(mapRecord);

  entries.sort((a, b) => a.certification_id.localeCompare(b.certification_id));

  const out = {
    registry_version: "v1.0",
    generated_utc: new Date().toISOString(),
    publisher: {
      name: PUBLISHER_NAME,
      disclaimer: DISCLAIMER
    },
    entries
  };

  fs.writeFileSync(JSON_DEST, JSON.stringify(out, null, 2) + "\n", "utf8");
  console.log(`Wrote ${JSON_DEST} with ${entries.length} entries`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
