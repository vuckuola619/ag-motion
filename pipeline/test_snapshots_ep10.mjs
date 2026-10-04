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

const SNAPSHOT_TIMES = [
  { t: 5.0, name: 'snap_01_hook_mother_baby_cells.jpg' },
  { t: 16.0, name: 'snap_02_act1_cardiac_repair.jpg' },
  { t: 22.0, name: 'snap_03_act1_cardiac_ecg_curve.jpg' },
  { t: 34.0, name: 'snap_04_act2_grandmother_neural.jpg' },
  { t: 54.0, name: 'snap_05_act3_prophetic_hadith_3x.jpg' },
  { t: 72.0, name: 'snap_06_outro_holding_hands_stamp.jpg' }
];

const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.wav': 'audio/wav',
  '.mp3': 'audio/mpeg'
};

function startStaticServer() {
  const server = http.createServer((req, res) => {
    let reqPath = req.url.split('?')[0];
    if (reqPath === '/' || reqPath === '/index.html') reqPath = '/index_ep10.html';
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

async function captureSnapshots() {
  const server = await startStaticServer();
  const outputDir = path.join(PROJECT_ROOT, 'output', 'episode10_mother_microchimerism', 'snapshots');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  console.log(`[Snapshots Ep10] Launching Puppeteer at ${WIDTH}x${HEIGHT}...`);
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: chromePath,
    args: ['--enable-gpu', '--use-gl=angle', '--enable-webgl', '--ignore-gpu-blocklist', '--disable-web-security']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  const url = `http://127.0.0.1:${PORT}/index_ep10.html?clean=1`;
  console.log(`[Snapshots Ep10] Navigating to ${url}...`);
  await page.goto(url, { waitUntil: 'load', timeout: 30000 });

  await page.waitForFunction('window.BANG_MOTION && window.BANG_MOTION.ready', { timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  console.log('[Snapshots Ep10] Capturing frames...');
  for (const shot of SNAPSHOT_TIMES) {
    await page.evaluate((targetTime) => {
      window.BANG_MOTION.seekFrame(targetTime);
    }, shot.t);

    await new Promise(r => setTimeout(r, 200));

    const outPath = path.join(outputDir, shot.name);
    await page.screenshot({ path: outPath, type: 'jpeg', quality: 92 });
    console.log(`[OK] Snapshot at ${shot.t}s -> ${shot.name}`);
  }

  await browser.close();
  server.close();
  console.log(`\n[All Done] Snapshots saved to ${outputDir}`);
}

captureSnapshots().catch(err => {
  console.error('[Snapshot Error]:', err);
  process.exit(1);
});
