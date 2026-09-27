import puppeteer from 'puppeteer';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

const PORT = 5198;
const WIDTH = 1080;
const HEIGHT = 1920;

const SNAPSHOT_TIMESTAMPS = [
  { time: 0.5, name: 'snap_01_intro_clamshell.jpg', label: 'Intro: Beinecke Restricted Access Unsealing' },
  { time: 4.5, name: 'snap_02_act1_closed_book.jpg', label: 'Act 1: Villa Mondragone & Closed Codex MS 408' },
  { time: 15.0, name: 'snap_03_act1_open_spread.jpg', label: 'Act 1: 240 Illustrated Vellum Folios & Glyphs' },
  { time: 27.0, name: 'snap_04_act2_impossible_botany.jpg', label: 'Act 2: 113 Impossible Alien Botanical Species' },
  { time: 39.0, name: 'snap_05_act2_zodiac_wheel.jpg', label: 'Act 2: Cosmological 30-Sector Celestial Star Wheel' },
  { time: 44.0, name: 'snap_06_act2_balneological_tubes.jpg', label: 'Act 2: Balneological Organic Fluid Conduits' },
  { time: 62.0, name: 'snap_07_act3_ams_laboratory.jpg', label: 'Act 3: University of Arizona AMS C-14 Laboratory' },
  { time: 75.0, name: 'snap_08_act3_carbon_dating_verdict.jpg', label: 'Act 3: 1404-1438 AD Calibration & Hoax Debunked' },
  { time: 88.0, name: 'snap_09_act4_zipf_law.jpg', label: 'Act 4: Zipf\'s Law Mathematical Distribution Proof' },
  { time: 102.0, name: 'snap_10_act4_linguistic_grammar.jpg', label: 'Act 4: Prefix, Root, Suffix Linguistic Architecture' },
  { time: 118.0, name: 'snap_11_act5_friedman_and_ai.jpg', label: 'Act 5: WW2 William Friedman & AI Model Defeat' },
  { time: 149.5, name: 'snap_12_outro_unresolved_stamp.jpg', label: 'Outro: Yale MS 408 & CASE UNRESOLVED Rubber Stamp' }
];

const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml'
};

function startStaticServer() {
  const server = http.createServer((req, res) => {
    let reqPath = req.url.split('?')[0];
    if (reqPath === '/' || reqPath === '/index.html') reqPath = '/index_ep8.html';
    const filePath = path.join(PROJECT_ROOT, decodeURIComponent(reqPath));

    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
        return;
      }
      const ext = path.extname(filePath).toLowerCase();
      const contentType = MIME_TYPES[ext] || 'application/octet-stream';
      res.writeHead(200, {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*'
      });
      res.end(data);
    });
  });

  return new Promise(resolve => {
    server.listen(PORT, '127.0.0.1', () => {
      console.log(`[Server] Static server running on http://127.0.0.1:${PORT}`);
      resolve(server);
    });
  });
}

async function takeSnapshots() {
  const server = await startStaticServer();
  const snapDir = path.join(PROJECT_ROOT, 'output', 'episode8_voynich_manuscript', 'snapshots');
  if (!fs.existsSync(snapDir)) fs.mkdirSync(snapDir, { recursive: true });

  console.log(`[Snapshots Ep8] Launching Puppeteer at ${WIDTH}x${HEIGHT}...`);
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: chromePath,
    args: ['--enable-gpu', '--use-gl=angle', '--enable-webgl', '--ignore-gpu-blocklist', '--disable-web-security']
  });

  const page = await browser.newPage();
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.error('PAGE ERROR:', err.message));
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  console.log(`[Snapshots Ep8] Loading http://127.0.0.1:${PORT}/index_ep8.html?clean=1`);
  await page.goto(`http://127.0.0.1:${PORT}/index_ep8.html?clean=1`, { waitUntil: 'load', timeout: 60000 });

  await page.waitForFunction(() => window.BANG_MOTION && window.BANG_MOTION.ready, { timeout: 30000 });
  console.log('[Snapshots Ep8] BANG_MOTION engine ready.');

  for (const snap of SNAPSHOT_TIMESTAMPS) {
    console.log(`[Snapshot] Seeking to ${snap.time}s -> ${snap.name} (${snap.label})...`);
    await page.evaluate((t) => {
      window.BANG_MOTION.seekFrame(t);
    }, snap.time);

    // Wait a brief tick for render
    await new Promise(r => setTimeout(r, 120));

    const outPath = path.join(snapDir, snap.name);
    await page.screenshot({ path: outPath, type: 'jpeg', quality: 95 });
    console.log(`  -> Saved: ${outPath}`);
  }

  await browser.close();
  server.close();
  console.log('\n[OK] All 12 snapshots captured successfully!');
}

takeSnapshots().catch(err => {
  console.error('[Error in takeSnapshots]:', err);
  process.exit(1);
});
