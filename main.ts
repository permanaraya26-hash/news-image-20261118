// news-image-20261118: "The World Today" front page for Wednesday 18 November 2026.
// The entry image is entry.png beside this file; this program copies it to the
// grader's output directory. It runs with no network and no dependencies, so the
// copy is the whole job — the image itself is the entry.
//
// Local test:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = join(repoRoot, 'entry.png');

if (!existsSync(source)) {
  throw new Error(`entry image missing: ${source}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
