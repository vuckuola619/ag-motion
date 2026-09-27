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

const SNAPSHOT_TIMESTAMPS = [
  { time: 0.5, name: 'snap_01_intro_folder.jpg', label: 'Intro Unsealing Folder Card' },
  { time: 4.5, name: 'snap_02_act1_big_ear.jpg', label: 'Act 1: Big Ear Horn Antenna & OSU Badge' },
  { time: 16.0, name: 'snap_03_act1_seti_tape.jpg', label: 'Act 1: Project SETI 50-Channel Tape Deck' },
  { time: 26.0, name: 'snap_04_act2_drift_scan.jpg', label: 'Act 2: Earth Rotation Drift Scan' },
  { time: 35.0, name: 'snap_05_act2_bell_curve.jpg', label: 'Act 2: 72-Second Bell Curve Profile' },
  { time: 46.0, name: 'snap_06_act3_ibm1130.jpg', label: 'Act 3: IBM 1130 Mainframe Audit' },
  { time: 56.0, name: 'snap_07_act3_6equj5_surge.jpg', label: 'Act 3: 6EQUJ5 Spike & 30x Sigma' },
  { time: 70.0, name: 'snap_08_act3_hydrogen_line.jpg', label: 'Act 3: 1420.405 MHz Hydrogen Waterhole' },
  { time: 84.0, name: 'snap_09_act4_red_pilot_wow.jpg', label: 'Act 4: Red Pilot Pen & "Wow!" Annotation' },
  { time: 94.0, name: 'snap_10_act4_failed_theories.jpg', label: 'Act 4: All Terrestrial Candidates Ruled Out' },
  { time: 106.0, name: 'snap_11_act5_silent_void.jpg', label: 'Act 5: VLA Dish & Silent Chi Sagittarii' },
  { time: 122.0, name: 'snap_12_outro_unsolved_stamp.jpg', label: 'Outro: Investigation Unsolved Stamp on 6EQUJ5' }
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
    if (reqPath === '/' || reqPath === '/index.html') reqPath = '/index_ep7.html';
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
  const snapDir = path.join(PROJECT_ROOT, 'output', 'episode7_wow_signal', 'snapshots');
  if (!fs.existsSync(snapDir)) fs.mkdirSync(snapDir, { recursive: true });

  console.log(`[Snapshots Ep7] Launching Puppeteer at ${WIDTH}x${HEIGHT}...`);
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: chromePath,
    args: ['--enable-gpu', '--use-gl=angle', '--enable-webgl', '--ignore-gpu-blocklist', '--disable-web-security']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  const url = `http://127.0.0.1:${PORT}/index_ep7.html?clean=1`;
  console.log(`[Snapshots Ep7] Navigating to ${url}...`);
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });

  await page.waitForFunction('window.BANG_MOTION && window.BANG_MOTION.ready', { timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  console.log(`\n=== Capturing ${SNAPSHOT_TIMESTAMPS.length} QC Snapshots ===`);
  for (const item of SNAPSHOT_TIMESTAMPS) {
    await page.evaluate(t => window.BANG_MOTION.seekFrame(t), item.time);
    // Allow microtask ticks for DOM render
    await new Promise(r => setTimeout(r, 120));

    const snapPath = path.join(snapDir, item.name);
    await page.screenshot({
      path: snapPath,
      type: 'jpeg',
      quality: 92,
      clip: { x: 0, y: 0, width: WIDTH, height: HEIGHT }
    });
    const sz = (fs.statSync(snapPath).size / 1024).toFixed(1);
    console.log(`  [OK] ${item.name} (${sz} KB) @ ${item.time}s -> ${item.label}`);
  }

  await browser.close();
  server.close();
  console.log('\n[Snapshots Ep7] All snapshots saved successfully.');
}

takeSnapshots().catch(err => {
  console.error('[Snapshots Error Ep7]:', err);
  process.exit(1);
});
