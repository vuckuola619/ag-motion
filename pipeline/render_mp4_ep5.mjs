import puppeteer from 'puppeteer';
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

const PORT = 5197;
const FPS = 30;
const DURATION = 60.0;
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

function startStaticServer() {
  const server = http.createServer((req, res) => {
    let reqPath = req.url.split('?')[0];
    if (reqPath === '/' || reqPath === '/index.html') reqPath = '/index_ep5.html';
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

async function renderVideo() {
  const server = await startStaticServer();
  const outputDir = path.join(PROJECT_ROOT, 'output', 'episode5_iridium_layer');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const finalMp4 = path.join(outputDir, 'episode5_iridium_layer.mp4');
  const audioFile = path.join(PROJECT_ROOT, 'assets', 'episode5_iridium_layer', 'audio', 'vo_iridium_layer_cinematic.wav');
  const ffmpegExe = 'C:\\Program Files\\ShareX\\ffmpeg.exe';

  console.log(`[Renderer Ep5] Launching Puppeteer at ${WIDTH}x${HEIGHT}...`);
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: chromePath,
    args: [
      '--enable-gpu',
      '--use-gl=angle',
      '--enable-webgl',
      '--ignore-gpu-blocklist',
      '--disable-web-security'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  const url = `http://127.0.0.1:${PORT}/index_ep5.html?clean=1`;
  console.log(`[Renderer Ep5] Navigating to ${url}...`);
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });

  await page.waitForFunction('window.BANG_MOTION && window.BANG_MOTION.ready', { timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  const totalFrames = Math.ceil(DURATION * FPS);
  console.log(`[Renderer Ep5] Total frames: ${totalFrames} @ ${FPS}fps (${DURATION}s)`);

  // Spawn FFmpeg with stdin pipe
  console.log(`[Renderer Ep5] Spawning FFmpeg process -> ${finalMp4}`);
  const ffmpegArgs = [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'png',
    '-framerate', String(FPS),
    '-i', '-',
    '-i', audioFile,
    '-c:v', 'libx264',
    '-preset', 'fast',
    '-crf', '18',
    '-pix_fmt', 'yuv420p',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    '-movflags', '+faststart',
    finalMp4
  ];

  const ffmpegProc = spawn(ffmpegExe, ffmpegArgs, { stdio: ['pipe', 'inherit', 'inherit'] });

  ffmpegProc.on('error', err => {
    console.error('[FFmpeg Error]:', err);
  });

  // Capture frame-by-frame
  const startTime = Date.now();
  for (let i = 0; i < totalFrames; i++) {
    const t = i / FPS;

    await page.evaluate(time => window.BANG_MOTION.seekFrame(time), t);

    const buffer = await page.screenshot({
      type: 'png',
      clip: { x: 0, y: 0, width: WIDTH, height: HEIGHT },
      optimizeForSpeed: true
    });

    const ok = ffmpegProc.stdin.write(buffer);
    if (!ok) {
      await new Promise(r => ffmpegProc.stdin.once('drain', r));
    }

    if (i % 60 === 0 || i === totalFrames - 1) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      const progress = ((i / totalFrames) * 100).toFixed(1);
      process.stdout.write(`\r[Render Progress Ep5] Frame ${i}/${totalFrames} (${progress}%) - Timeline: ${t.toFixed(2)}s - Elapsed: ${elapsed}s`);
    }
  }

  console.log('\n[Renderer Ep5] All frames sent to FFmpeg. Finalizing stream...');
  ffmpegProc.stdin.end();

  await new Promise((resolve, reject) => {
    ffmpegProc.on('close', code => {
      if (code === 0) {
        console.log(`[Renderer Ep5] SUCCESS! Master 60s video exported cleanly to: ${finalMp4}`);
        resolve();
      } else {
        reject(new Error(`FFmpeg exited with code ${code}`));
      }
    });
  });

  await browser.close();
  server.close();
  console.log('[Renderer Ep5] Pipeline complete.');
}

renderVideo().catch(err => {
  console.error('[Render Pipeline Error Ep5]:', err);
  process.exit(1);
});
