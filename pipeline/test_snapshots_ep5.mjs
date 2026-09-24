import puppeteer from 'puppeteer';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

const PORT = 5197;
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
    if (reqPath === '/' || reqPath === '/index.html') reqPath = '/index_ep5.html';
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
  await page.goto(`http://127.0.0.1:${PORT}/index_ep5.html?clean=1`, { waitUntil: 'load', timeout: 30000 });
  await page.waitForFunction('window.BANG_MOTION && window.BANG_MOTION.ready');
  await page.evaluate(() => document.fonts.ready);

  const times = [
    { t: 0.3, name: 'snap_ep5_intro.jpg' },
    { t: 4.0, name: 'snap_ep5_scene1_crime_scene.jpg' },
    { t: 10.1, name: 'snap_ep5_trans1_2.jpg' },
    { t: 14.5, name: 'snap_ep5_scene2_berkeley_lab.jpg' },
    { t: 24.0, name: 'snap_ep5_scene3_cosmic_suspect.jpg' },
    { t: 34.0, name: 'snap_ep5_scene4_yucatan_crater.jpg' },
    { t: 44.5, name: 'snap_ep5_scene5_drill_cores_tektites.jpg' },
    { t: 56.5, name: 'snap_ep5_scene6_case_closed.jpg' },
    { t: 58.5, name: 'snap_ep5_outro_stamp.jpg' }
  ];

  const outDir = path.join(PROJECT_ROOT, 'output', 'episode5_iridium_layer', 'snapshots');
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
  console.log('All Episode 5 snapshots captured cleanly!');
}

takeSnapshots().catch(err => {
  console.error('Snapshot error Ep5:', err);
  process.exit(1);
});
