import puppeteer from 'puppeteer';
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

const PORT = 5195;
const FPS = 30;
const DURATION = 83.81;
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
      console.log(`[Server] Static server running on http://127.0.0.1:${PORT}`);
      resolve(server);
    });
  });
}

async function renderVideo() {
  const server = await startStaticServer();
  const outputDir = path.join(PROJECT_ROOT, 'output', 'episode14_glymphatic_brain_wash');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const finalMp4 = path.join(outputDir, 'episode14_glymphatic_brain_wash_en.mp4');
  const audioFile = path.join(PROJECT_ROOT, 'assets', 'episode14_glymphatic_brain_wash', 'audio_en', 'vo_ep14_en_master.wav');
  const ffmpegExe = 'C:\\Program Files\\ShareX\\ffmpeg.exe';

  console.log(`[Renderer Ep14 EN] Launching Puppeteer at ${WIDTH}x${HEIGHT}...`);
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

  const url = `http://127.0.0.1:${PORT}/index_ep14.html?clean=1`;
  console.log(`[Renderer Ep14 EN] Navigating to ${url}...`);
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });

  await page.waitForFunction('window.BANG_MOTION && window.BANG_MOTION.ready', { timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  const totalFrames = Math.ceil(DURATION * FPS);
  console.log(`[Renderer Ep14 EN] Total frames: ${totalFrames} @ ${FPS}fps (${DURATION}s)`);

  const ffmpegArgs = [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'png',
    '-r', String(FPS),
    '-i', 'pipe:0',
    '-i', audioFile,
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'fast',
    '-crf', '18',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    finalMp4
  ];

  console.log(`[FFmpeg] Spawning encoder -> ${finalMp4}`);
  const ffmpegProcess = spawn(ffmpegExe, ffmpegArgs, { stdio: ['pipe', 'inherit', 'inherit'] });

  const startTime = Date.now();
  for (let frame = 0; frame < totalFrames; frame++) {
    const t = frame / FPS;
    await page.evaluate((time) => {
      window.BANG_MOTION.seek(time);
    }, t);

    const screenshotBuffer = await page.screenshot({
      type: 'png',
      omitBackground: false
    });

    const canWrite = ffmpegProcess.stdin.write(screenshotBuffer);
    if (!canWrite) {
      await new Promise(r => ffmpegProcess.stdin.once('drain', r));
    }

    if (frame % 60 === 0 || frame === totalFrames - 1) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      const pct = ((frame / totalFrames) * 100).toFixed(1);
      const fpsReal = (frame / (Date.now() - startTime) * 1000).toFixed(1);
      console.log(`[Render] Frame ${frame}/${totalFrames} (${pct}%) | ${fpsReal} fps | Elapsed: ${elapsed}s`);
    }
  }

  ffmpegProcess.stdin.end();

  await new Promise((resolve, reject) => {
    ffmpegProcess.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`FFmpeg exited with code ${code}`));
    });
  });

  console.log(`[Success] Master MP4 saved: ${finalMp4}`);
  await browser.close();
  server.close();
}

renderVideo().catch(err => {
  console.error('[Fatal Error]', err);
  process.exit(1);
});
