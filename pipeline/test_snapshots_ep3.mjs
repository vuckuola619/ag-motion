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

const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.wav': 'audio/wav',
  '.mp3': 'audio/mpeg',
  '.mp4': 'video/mp4'
};

function startServer() {
  const server = http.createServer((req, res) => {
    let reqPath = req.url.split('?')[0];
    if (reqPath === '/' || reqPath === '/index.html') reqPath = '/index_ep3.html';
    const filePath = path.join(PROJECT_ROOT, decodeURIComponent(reqPath));

    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end('Not Found');
        return;
      }
      const ext = path.extname(filePath).toLowerCase();
      res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
      res.end(data);
    });
  });

  return new Promise(resolve => {
    server.listen(PORT, '127.0.0.1', () => resolve(server));
  });
}

async function takeSnapshots() {
  const server = await startServer();
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: chromePath,
    args: ['--enable-gpu', '--use-gl=angle', '--enable-webgl', '--disable-web-security']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });
  await page.goto(`http://127.0.0.1:${PORT}/index_ep3.html?clean=1`, { waitUntil: 'networkidle0' });
  await page.waitForFunction('window.BANG_MOTION && window.BANG_MOTION.ready');
  await page.evaluate(() => document.fonts.ready);

  const times = [
    { t: 5.0, name: 'snap_ep3_scene1_arid_pangea.jpg' },
    { t: 9.8, name: 'snap_ep3_trans1_2_wrangellia.jpg' },
    { t: 15.0, name: 'snap_ep3_scene2_wrangellia.jpg' },
    { t: 26.0, name: 'snap_ep3_scene3_deluge_rain.jpg' },
    { t: 37.0, name: 'snap_ep3_scene4_amber_conifers.jpg' },
    { t: 48.0, name: 'snap_ep3_scene5_carnian_extinction.jpg' },
    { t: 59.0, name: 'snap_ep3_scene6_dinosaur_dawn.jpg' },
    { t: 67.0, name: 'snap_ep3_outro_card.jpg' }
  ];

  const outDir = path.join(PROJECT_ROOT, 'output', 'episode3_carnian_pluvial', 'snapshots');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  for (const item of times) {
    await page.evaluate(async time => {
      await window.BANG_MOTION.seekFrame(time);
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    }, item.t);

    const outPath = path.join(outDir, item.name);
    await page.screenshot({ path: outPath, type: 'jpeg', quality: 90 });
    console.log(`Saved snapshot: ${item.name} at ${item.t}s`);
  }

  await browser.close();
  server.close();
  console.log('All Episode 3 snapshots captured cleanly!');
}

takeSnapshots().catch(err => {
  console.error('Snapshot error Ep3:', err);
  process.exit(1);
});
