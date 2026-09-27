import puppeteer from 'puppeteer';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

const PORT = 5199;
const WIDTH = 1080;
const HEIGHT = 1920;

const SNAPSHOT_TIMES = [
  { t: 5.0, name: 'snap_01_hook_atm_dad.jpg' },
  { t: 20.0, name: 'snap_02_act1_paternal_brain.jpg' },
  { t: 26.0, name: 'snap_03_act1_yale_oxytocin_curve.jpg' },
  { t: 40.0, name: 'snap_04_act2_rough_play_airplane.jpg' },
  { t: 45.0, name: 'snap_05_act2_stress_resilience.jpg' },
  { t: 58.0, name: 'snap_06_act3_prophetic_mercy.jpg' },
  { t: 65.0, name: 'snap_07_act3_sahih_bukhari_hadith.jpg' },
  { t: 78.0, name: 'snap_08_outro_be_truly_present.jpg' }
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
    if (reqPath === '/' || reqPath === '/index.html') reqPath = '/index_ep9.html';
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

async function runSnapshots() {
  const server = await startStaticServer();
  const outputDir = path.join(PROJECT_ROOT, 'output', 'episode9_father_parenting', 'snapshots');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: chromePath,
    args: ['--enable-gpu', '--use-gl=angle', '--enable-webgl', '--ignore-gpu-blocklist', '--disable-web-security']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.error('PAGE ERROR:', err.message));

  const url = `http://127.0.0.1:${PORT}/index_ep9.html?clean=1`;
  console.log(`[Snapshots Ep9] Navigating to ${url}...`);
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });

  await page.waitForFunction('window.BANG_MOTION && window.BANG_MOTION.ready', { timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  for (const item of SNAPSHOT_TIMES) {
    const snapPath = path.join(outputDir, item.name);
    console.log(`[Snapshots Ep9] Capturing snapshot at t=${item.t}s -> ${item.name}...`);
    
    await page.evaluate((targetTime) => {
      window.BANG_MOTION.seekFrame(targetTime);
    }, item.t);

    await page.screenshot({
      path: snapPath,
      type: 'jpeg',
      quality: 90
    });
  }

  await browser.close();
  server.close();
  console.log('[OK] All snapshots captured successfully.');
}

runSnapshots().catch(err => {
  console.error('[Error]:', err);
  process.exit(1);
});
