// The Pocket Cloud Maker (NIMBUS-1) — make.fun entry.
// Copies the committed entry.png to the output directory.
// Node 22 stdlib only; no network, no Python, no external files.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const SRC = fileURLToPath(new URL("./entry.png", import.meta.url));
const OUT_DIR = process.env.OUTPUT_DIR || "/output";
const DEST = join(OUT_DIR, "entry.png");

function fail(msg) {
  console.error(`error: ${msg}`);
  process.exit(1);
}

if (!existsSync(SRC)) fail(`entry.png not found at ${SRC}`);
const buf = readFileSync(SRC);
// PNG magic: 89 50 4E 47 0D 0A 1A 0A
const MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 33 || !buf.subarray(0, 8).equals(MAGIC)) fail("entry.png is not a PNG");
if (buf.readUInt32BE(12) !== 0x49484452) fail("entry.png missing IHDR chunk");
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) fail(`entry.png is ${width}x${height}, expected 1024x1024`);
if (buf.length > 1048576) fail(`entry.png is ${buf.length} bytes, over the 1 MiB limit`);

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, DEST);
const outSize = statSync(DEST).size;
if (outSize !== buf.length) fail(`copied size ${outSize} != source size ${buf.length}`);
console.log(`wrote ${DEST} (${outSize} bytes, 1024x1024 PNG)`);
