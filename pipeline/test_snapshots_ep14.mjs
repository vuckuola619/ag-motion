import puppeteer from 'puppeteer';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

const PORT = 5196;
const WIDTH = 1080;
const HEIGHT = 1920;

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
    if (reqPath === '/' || reqPath === '/index.html') reqPath = '/index_ep14.html';
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
      resolve(server);
    });
  });
}

async function captureStills() {
  const server = await startStaticServer();
  const outputDir = path.join(PROJECT_ROOT, 'output', 'episode14_glymphatic_brain_wash', 'stills');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: chromePath,
    args: ['--enable-gpu', '--use-gl=angle', '--enable-webgl', '--ignore-gpu-blocklist', '--disable-web-security']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  const url = `http://127.0.0.1:${PORT}/index_ep14.html?clean=1`;
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  await page.waitForFunction('window.BANG_MOTION && window.BANG_MOTION.ready', { timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  const testTimes = [
    { label: 'scene1_nocturnal_secret', t: 6.0 },
    { label: 'scene2_astrocytic_highway', t: 24.0 },
    { label: 'scene3_alzheimer_purge', t: 42.0 },
    { label: 'scene4_sleep_debt_myth', t: 60.0 },
    { label: 'scene5_clean_temple', t: 76.0 }
  ];

  for (let shot of testTimes) {
    await page.evaluate((time) => {
      window.BANG_MOTION.seek(time);
    }, shot.t);

    const outPath = path.join(outputDir, `${shot.label}.png`);
    await page.screenshot({ path: outPath, type: 'png' });
    console.log(`[Snapshot] Captured ${shot.label} at t=${shot.t}s -> ${outPath}`);
  }

  await browser.close();
  server.close();
  console.log('[Snapshot] Stills capture completed successfully.');
}

captureStills().catch(err => {
  console.error('[Error]', err);
  process.exit(1);
});
