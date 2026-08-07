#!/usr/bin/env node
/**
 * Verifies that every Tailwind @theme mirror (any file named brand.css)
 * carries exactly the values declared in brand/tokens.css.
 *
 * Drift between the canonical tokens and a Tailwind mirror is the exact
 * failure mode this design system exists to prevent, so this exits
 * non-zero and is safe to wire into CI.
 *
 * Usage:  node brand/verify-tokens.mjs
 */
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, dirname, relative } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CANON = join(ROOT, "brand", "tokens.css");
const SKIP = new Set(["node_modules", ".git", "dist", "build", ".venv", ".next"]);
// Covers every token duplicated between brand/tokens.css and a mirror.
// --wash-* and --dur-* are triplicated across the canonical file and both
// Tailwind mirrors, so leaving them untracked let them drift silently.
const TRACKED = /^--(color|font|radius|ease|wash|dur)-/;

/** Extract tracked `--name: value` pairs from a stylesheet. */
function tokensOf(css) {
  const out = new Map();
  for (const m of css.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;]+);/gi)) {
    const name = m[1].trim().toLowerCase();
    if (!TRACKED.test(name)) continue;
    out.set(name, m[2].replace(/\s+/g, " ").trim().toLowerCase());
  }
  return out;
}

function findMirrors(dir, acc = []) {
  let entries;
  try {
    entries = readdirSync(dir);
  } catch {
    return acc;
  }
  for (const entry of entries) {
    if (SKIP.has(entry)) continue;
    const p = join(dir, entry);
    let st;
    try {
      st = statSync(p);
    } catch {
      continue;
    }
    if (st.isDirectory()) findMirrors(p, acc);
    else if (entry === "brand.css") acc.push(p);
  }
  return acc;
}

if (!existsSync(CANON)) {
  console.error(`✗ canonical token file missing: ${relative(ROOT, CANON)}`);
  process.exit(1);
}

const canon = tokensOf(readFileSync(CANON, "utf8"));
const mirrors = findMirrors(ROOT);

if (canon.size === 0) {
  console.error(`✗ no tracked tokens parsed from ${relative(ROOT, CANON)}`);
  process.exit(1);
}

if (mirrors.length === 0) {
  console.log(
    `✓ ${canon.size} canonical tokens; no Tailwind mirrors in this repo — nothing to drift.`,
  );
  process.exit(0);
}

let failed = false;

for (const file of mirrors) {
  const rel = relative(ROOT, file);
  const mirror = tokensOf(readFileSync(file, "utf8"));
  const problems = [];

  for (const [name, want] of canon) {
    if (!mirror.has(name)) {
      problems.push(`  missing  ${name}  (expected ${want})`);
    } else if (mirror.get(name) !== want) {
      problems.push(`  drifted  ${name}\n    canonical: ${want}\n    mirror:    ${mirror.get(name)}`);
    }
  }

  for (const name of mirror.keys()) {
    if (!canon.has(name)) {
      problems.push(`  extra    ${name}  (not in brand/tokens.css)`);
    }
  }

  if (problems.length) {
    failed = true;
    console.error(`✗ ${rel}`);
    for (const p of problems) console.error(p);
  } else {
    console.log(`✓ ${rel} — ${mirror.size} tokens in sync`);
  }
}

if (failed) {
  console.error(
    "\nTailwind mirror has drifted from brand/tokens.css. Update the mirror, " +
      "or change brand/tokens.css and propagate to all four repositories.",
  );
  process.exit(1);
}

console.log(`\n✓ all mirrors match brand/tokens.css (${canon.size} tokens)`);
