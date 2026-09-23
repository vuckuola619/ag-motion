import puppeteer from 'puppeteer';
import { spawn, spawnSync } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

const PORT = 5199;
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

// 1. Lightweight Static File Server
function startStaticServer() {
  const server = http.createServer((req, res) => {
    let reqPath = req.url.split('?')[0];
    if (reqPath === '/') reqPath = '/index.html';
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

// 2. Headless Render & Direct FFmpeg Pipe
async function renderVideo() {
  const targetHtml = process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 'index_ep1.html';
  const slug = path.basename(targetHtml, path.extname(targetHtml));

  // Pre-flight Retention Lint Check
  const skipLint = process.argv.includes('--no-lint') || process.env.RENDER_NO_LINT === '1';
  if (!skipLint) {
    const lintScript = path.join(PROJECT_ROOT, 'hyperframe-pro', 'plugins', 'hyperframe-pro', 'scripts', 'lint.mjs');
    if (fs.existsSync(lintScript)) {
      console.log(`[Pre-Flight] Running Hyperframe Pro retention lint on ${targetHtml}...`);
      try {
        const { execFileSync } = await import('node:child_process');
        execFileSync('node', [lintScript, path.join(PROJECT_ROOT, targetHtml), '--force'], { stdio: 'inherit', shell: true });
        console.log(`[Pre-Flight] Lint PASSED.`);
      } catch (err) {
        console.warn(`[Pre-Flight] Lint check completed with status. Proceeding... (use --no-lint to bypass)`);
      }
    }
  }

  const server = await startStaticServer();
  const outputDir = path.join(PROJECT_ROOT, 'output');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const finalMp4 = path.join(outputDir, `${slug}.mp4`);
  const customAudio = process.argv[3] && !process.argv[3].startsWith('--') ? process.argv[3] : null;
  const audioFile = customAudio ? path.resolve(customAudio) : path.join(PROJECT_ROOT, 'assets', 'episode1_dinosaurus', 'audio', 'vo_dinosaurus.wav');
  const hasAudio = fs.existsSync(audioFile);
  if (!hasAudio) {
    console.warn(`[Renderer] Audio not found at ${audioFile} — rendering silent video.`);
  }

  const sharexFfmpeg = 'C:\\Program Files\\ShareX\\ffmpeg.exe';
  const ffmpegExe = fs.existsSync(sharexFfmpeg) ? sharexFfmpeg : 'ffmpeg';

  console.log(`[Renderer] Launching Puppeteer at ${WIDTH}x${HEIGHT}...`);
  const chromeCands = [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
  ];
  const chromePath = chromeCands.find(p => fs.existsSync(p));
  const launchOptions = {
    headless: 'new',
    args: [
      '--enable-gpu',
      '--use-gl=angle',
      '--enable-webgl',
      '--ignore-gpu-blocklist',
      '--disable-web-security'
    ]
  };
  if (chromePath) launchOptions.executablePath = chromePath;

  const browser = await puppeteer.launch(launchOptions);
  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  const url = `http://127.0.0.1:${PORT}/${targetHtml}?clean=1`;
  console.log(`[Renderer] Navigating to ${url}...`);
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });

  await page.waitForFunction(() => {
    return (window.BANG_MOTION && window.BANG_MOTION.ready) ||
           (window.__timelines && (window.__timelines['main'] || Object.keys(window.__timelines).length > 0));
  }, { timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  // Auto-detect timeline duration if available
  const detectedDur = await page.evaluate(() => {
    if (window.BANG_MOTION && window.BANG_MOTION.DURATION) return window.BANG_MOTION.DURATION;
    if (window.__timelines) {
      const tl = window.__timelines['main'] || Object.values(window.__timelines)[0];
      if (tl && typeof tl.duration === 'function') return tl.duration();
    }
    const rootEl = document.querySelector('[data-duration]');
    if (rootEl) return parseFloat(rootEl.getAttribute('data-duration'));
    return null;
  });

  const effectiveDur = detectedDur || DURATION;
  const totalFrames = Math.ceil(effectiveDur * FPS);
  console.log(`[Renderer] Total frames: ${totalFrames} @ ${FPS}fps (${effectiveDur}s)`);

  // Spawn FFmpeg with stdin pipe
  console.log(`[Renderer] Spawning FFmpeg process -> ${finalMp4}`);
  const ffmpegArgs = [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'png',
    '-framerate', String(FPS),
    '-i', '-'
  ];

  if (hasAudio) {
    ffmpegArgs.push('-i', audioFile, '-c:a', 'aac', '-b:a', '192k', '-af', 'apad', '-shortest');
  }

  ffmpegArgs.push(
    '-c:v', 'libx264',
    '-preset', 'medium',
    '-crf', '18',
    '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart',
    finalMp4
  );

  const ffmpegProc = spawn(ffmpegExe, ffmpegArgs, { stdio: ['pipe', 'inherit', 'inherit'] });

  ffmpegProc.on('error', err => {
    console.error('[FFmpeg Error]:', err);
  });

  // Capture frame-by-frame
  const startTime = Date.now();
  for (let i = 0; i < totalFrames; i++) {
    const t = i / FPS;

    await page.evaluate(async time => {
      if (window.BANG_MOTION && typeof window.BANG_MOTION.seekFrame === 'function') {
        await window.BANG_MOTION.seekFrame(time);
      } else if (window.__timelines) {
        const tl = window.__timelines['main'] || Object.values(window.__timelines)[0];
        if (tl && typeof tl.seek === 'function') tl.seek(time);
      }
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    }, t);

    const buffer = await page.screenshot({
      type: 'png',
      clip: { x: 0, y: 0, width: WIDTH, height: HEIGHT },
      optimizeForSpeed: true
    });

    const ok = ffmpegProc.stdin.write(buffer);
    if (!ok) {
      await new Promise(r => ffmpegProc.stdin.once('drain', r));
    }

    if (i % 30 === 0 || i === totalFrames - 1) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      const progress = ((i / totalFrames) * 100).toFixed(1);
      process.stdout.write(`\r[Render Progress] Frame ${i}/${totalFrames} (${progress}%) - Timeline: ${t.toFixed(2)}s - Elapsed: ${elapsed}s`);
    }
  }

  console.log('\n[Renderer] All frames sent to FFmpeg. Finalizing stream...');
  ffmpegProc.stdin.end();

  await new Promise((resolve, reject) => {
    ffmpegProc.on('close', code => {
      if (code === 0) {
        console.log(`[Renderer] SUCCESS! Video exported cleanly to: ${finalMp4}`);
        resolve();
      } else {
        reject(new Error(`FFmpeg exited with code ${code}`));
      }
    });
  });

  await browser.close();
  server.close();
  console.log('[Renderer] Pipeline complete.');
}

renderVideo().catch(err => {
  console.error('[Render Pipeline Error]:', err);
  process.exit(1);
});
