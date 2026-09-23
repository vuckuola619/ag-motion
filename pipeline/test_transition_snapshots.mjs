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
    if (reqPath === '/') reqPath = '/index.html';
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

async function testTransitions() {
  const server = await startServer();
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: chromePath,
    args: ['--enable-gpu', '--use-gl=angle', '--enable-webgl', '--disable-web-security']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });
  await page.goto(`http://127.0.0.1:${PORT}/index.html?clean=1`, { waitUntil: 'networkidle0' });
  await page.waitForFunction('window.BANG_MOTION && window.BANG_MOTION.ready');
  await page.evaluate(() => document.fonts.ready);

  const outDir = path.join(PROJECT_ROOT, 'output', 'transition_verify');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  // Test transition 1 -> 2: 9.1s to 10.5s at 0.15s intervals
  const testTimes = [
    9.10, // Hold Scene 1
    9.30, // Exit starts + Glide starts
    9.45, // Outgoing slide left + Camera acceleration
    9.60, // Camera mid-transit + Optical streak active
    9.75, // Camera in corridor + Ghost watermark & ruler visible
    9.90, // Incoming Scene 2 card entering from right
    10.05, // Hero cutout entering + Camera cushioning
    10.20, // Camera settled at Xc=2540 + Scene 2 cards landing
    10.50, // Scene 2 settled with full typography & gauges
    11.20  // Narration headline active
  ];

  console.log(`[Test] Capturing ${testTimes.length} transition verification frames...`);

  for (let idx = 0; idx < testTimes.length; idx++) {
    const t = testTimes[idx];
    await page.evaluate(async time => {
      await window.BANG_MOTION.seekFrame(time);
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    }, t);

    const filename = `trans_${String(idx + 1).padStart(2, '0')}_${t.toFixed(2)}s.jpg`;
    const outPath = path.join(outDir, filename);
    await page.screenshot({ path: outPath, type: 'jpeg', quality: 90 });
    console.log(`  Saved: ${filename}`);
  }

  await browser.close();
  server.close();
  console.log('[Test] All transition verification frames captured successfully!');
}

testTransitions().catch(err => {
  console.error('[Test Error]:', err);
  process.exit(1);
});
