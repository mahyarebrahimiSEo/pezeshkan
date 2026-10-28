/**
 * اکوسیستم سلامت دیجیتال پزشکآن - اسکریپت‌های جامع و اشتراکی پرتال
 * مدیریت تم دوگانه (Day/Dark Mode)، انیمیشن نوار قلب تعاملی ECG،
 * ویزارد ۵ مرحله‌ای شروع همکاری و تعاملات ارگونومیک
 */

// 1. Theme Management (Day Mode Default & Clinical Dark Mode)
function initTheme() {
  const savedTheme = localStorage.getItem('pezeshkan_theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeButtonUI(savedTheme);
  updatePezShellTheme(savedTheme);
}
// Apply immediately to prevent any flash during navigation
(function applyInitialTheme() {
  try {
    const saved = localStorage.getItem('pezeshkan_theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
  } catch (e) {
    document.documentElement.setAttribute('data-theme', 'light');
  }
})();

function updatePezShellTheme(theme) {
  const shell = document.getElementById('shell') || document.querySelector('.pez-shell');
  const vital = document.getElementById('vital');
  const isDay = theme !== 'dark';
  if (shell) {
    shell.classList.toggle('pez-shell-day', isDay);
  }
  if (vital) {
    vital.src = isDay ? '/assets/vital-day.svg' : '/assets/vital-dark.svg';
  }
}

function toggleTheme() {
  const root = document.documentElement;
  root.classList.add('theme-transitioning');

  const current = root.getAttribute('data-theme') || 'light';
  const next = current === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  try {
    localStorage.setItem('pezeshkan_theme', next);
  } catch (e) {}
  updateThemeButtonUI(next);
  updatePezShellTheme(next);
  if (window.pezeshkan3D && typeof window.pezeshkan3D.updateThemeMaterials === 'function') {
    window.pezeshkan3D.updateThemeMaterials(next);
  }

  // Restore micro-interaction transitions on next frame
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      root.classList.remove('theme-transitioning');
    });
  });
}

function updateThemeButtonUI(theme) {
  const btns = document.querySelectorAll('.theme-toggle-btn, .theme-switch, #themeToggleBtn');
  const isDark = theme === 'dark';
  btns.forEach(btn => {
    btn.setAttribute('role', 'switch');
    btn.setAttribute('aria-checked', isDark ? 'true' : 'false');
    btn.setAttribute('title', isDark ? 'تغییر به حالت روز (روشن)' : 'تغییر به حالت شب (تاریک)');
    btn.setAttribute('aria-label', isDark ? 'تغییر به حالت روز (روشن)' : 'تغییر به حالت شب (تاریک)');
    btn.classList.add('theme-switch');

    if (!btn.querySelector('.theme-switch-track')) {
      btn.innerHTML = `
        <span class="theme-switch-track">
          <span class="theme-switch-icon sun-icon" aria-hidden="true">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="4.5"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="6.34" y2="6.34"/><line x1="17.66" y1="17.66" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="6.34" y2="17.66"/><line x1="17.66" y1="6.34" x2="19.07" y2="4.93"/></svg>
          </span>
          <span class="theme-switch-icon moon-icon" aria-hidden="true">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          </span>
          <span class="theme-switch-thumb" aria-hidden="true"></span>
        </span>
      `;
    }
  });
}

// 1.5. Persian Cursive Presentation-Form Shaper Engine
// Guarantees 100% connected, razor-sharp Persian ligatures in HTML5 Canvas 2D
const PERSIAN_GLYPH_TABLE = {
  0x0622: [0xFE81, 0xFE81, 0xFE82, 0xFE82], // آ
  0x0627: [0xFE8D, 0xFE8D, 0xFE8E, 0xFE8E], // ا
  0x0623: [0xFE83, 0xFE83, 0xFE84, 0xFE84], // أ
  0x0625: [0xFE87, 0xFE87, 0xFE88, 0xFE88], // إ
  0x0628: [0xFE8F, 0xFE91, 0xFE92, 0xFE90], // ب
  0x067E: [0xFB56, 0xFB58, 0xFB59, 0xFB57], // پ
  0x062A: [0xFE95, 0xFE97, 0xFE98, 0xFE96], // ت
  0x062B: [0xFE99, 0xFE9B, 0xFE9C, 0xFE9A], // ث
  0x062C: [0xFE9D, 0xFE9F, 0xFEA0, 0xFE9E], // ج
  0x0686: [0xFB7A, 0xFB7C, 0xFB7D, 0xFB7B], // چ
  0x062D: [0xFEA1, 0xFEA3, 0xFEA4, 0xFEA2], // ح
  0x062E: [0xFEA5, 0xFEA7, 0xFEA8, 0xFEA6], // خ
  0x062F: [0xFEA9, 0xFEA9, 0xFEAA, 0xFEAA], // د
  0x0630: [0xFEAB, 0xFEAB, 0xFEAC, 0xFEAC], // ذ
  0x0631: [0xFEAD, 0xFEAD, 0xFEAE, 0xFEAE], // ر
  0x0632: [0xFEAF, 0xFEAF, 0xFEB0, 0xFEB0], // ز
  0x0698: [0xFB8A, 0xFB8A, 0xFB8B, 0xFB8B], // ژ
  0x0633: [0xFEB1, 0xFEB3, 0xFEB4, 0xFEB2], // س
  0x0634: [0xFEB5, 0xFEB7, 0xFEB8, 0xFEB6], // ش
  0x0635: [0xFEB9, 0xFEBB, 0xFEBC, 0xFEBA], // ص
  0x0636: [0xFEBD, 0xFEBF, 0xFEC0, 0xFEBE], // ض
  0x0637: [0xFEC1, 0xFEC3, 0xFEC4, 0xFEC2], // ط
  0x0638: [0xFEC5, 0xFEC7, 0xFEC8, 0xFEC6], // ظ
  0x0639: [0xFEC9, 0xFECB, 0xFECC, 0xFECA], // ع
  0x063A: [0xFECD, 0xFECF, 0xFED0, 0xFECE], // غ
  0x0641: [0xFED1, 0xFED3, 0xFED4, 0xFED2], // ف
  0x0642: [0xFED5, 0xFED7, 0xFED8, 0xFED6], // ق
  0x06A9: [0xFB8E, 0xFB90, 0xFB91, 0xFB8F], // ک
  0x0643: [0xFED9, 0xFEDB, 0xFEDC, 0xFEDA], // ك
  0x06AF: [0xFB92, 0xFB94, 0xFB95, 0xFB93], // گ
  0x0644: [0xFEDD, 0xFEDF, 0xFEE0, 0xFEDE], // ل
  0x0645: [0xFEE1, 0xFEE3, 0xFEE4, 0xFEE2], // م
  0x0646: [0xFEE5, 0xFEE7, 0xFEE8, 0xFEE6], // ن
  0x0648: [0xFEED, 0xFEED, 0xFEEE, 0xFEEE], // و
  0x0624: [0xFE85, 0xFE85, 0xFE86, 0xFE86], // ؤ
  0x0647: [0xFEE9, 0xFEEB, 0xFEEC, 0xFEEA], // ه
  0x0629: [0xFE93, 0xFE93, 0xFE94, 0xFE94], // ة
  0x06CC: [0xFBFC, 0xFBFE, 0xFBFF, 0xFBFD], // ی
  0x064A: [0xFEF1, 0xFEF3, 0xFEF4, 0xFEF2], // ي
  0x0626: [0xFE89, 0xFE8B, 0xFE8C, 0xFE8A], // ئ
  0x0621: [0xFE80, 0xFE80, 0xFE80, 0xFE80]  // ء
};

function _connectsNext(code) {
  const rightOnly = [0x0622, 0x0627, 0x0623, 0x0625, 0x062F, 0x0630, 0x0631, 0x0632, 0x0698, 0x0648, 0x0624, 0x0629];
  return PERSIAN_GLYPH_TABLE[code] && !rightOnly.includes(code);
}

function _connectsPrev(code) {
  return !!PERSIAN_GLYPH_TABLE[code];
}

const _shapeCache = new Map();

function shapePersian(text) {
  if (!text || typeof text !== 'string') return text;
  if (_shapeCache.has(text)) return _shapeCache.get(text);

  let res = '';
  for (let i = 0; i < text.length; i++) {
    const code = text.charCodeAt(i);
    // Ignore ZWNJ glyph, breaking connection naturally
    if (code === 0x200C) {
      continue;
    }
    // Lam-Alef ligatures
    if (code === 0x0644 && i < text.length - 1) {
      const nextCode = text.charCodeAt(i + 1);
      const prev = i > 0 ? text.charCodeAt(i - 1) : 0;
      const pConn = _connectsNext(prev);
      if (nextCode === 0x0627) { // لا
        res += String.fromCharCode(pConn ? 0xFEFC : 0xFEFB);
        i++;
        continue;
      } else if (nextCode === 0x0622) { // لآ
        res += String.fromCharCode(pConn ? 0xFEF6 : 0xFEF5);
        i++;
        continue;
      }
    }

    const entry = PERSIAN_GLYPH_TABLE[code];
    if (!entry) {
      res += text[i];
      continue;
    }
    const prev = i > 0 ? text.charCodeAt(i - 1) : 0;
    const next = i < text.length - 1 ? text.charCodeAt(i + 1) : 0;
    const pConn = _connectsNext(prev);
    const nConn = _connectsPrev(next) && _connectsNext(code);

    let formIndex = 0; // isolated
    if (pConn && nConn) formIndex = 2; // medial
    else if (nConn) formIndex = 1;     // initial
    else if (pConn) formIndex = 3;     // final

    res += String.fromCharCode(entry[formIndex]);
  }

  _shapeCache.set(text, res);
  return res;
}

// 2. High-Performance Three.js 3D Medical Diagnostic Console
class Pezeshkan3DConsole {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container || typeof THREE === 'undefined') return;

    this.bpm = 72;
    this.isPaused = false;
    this.t = 0;
    this.trailX = 0;
    this.lastY = 0;
    this.introT = 0;

    // Dual Mode System: 'ecg' (نوار قلب) vs 'crm' (سیستم نوبت‌دهی و CRM)
    this.currentMode = 'ecg';
    this.morphProgress = 0;   // 0 = 100% ECG, 1 = 100% CRM
    this.morphTarget = 0;
    this.isMorphing = false;

    try {
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get('mode') === 'crm') {
        this.morphProgress = 1;
        this.currentMode = 'crm';
      }
    } catch(e) {}

    this.init();
  }

  createRoundedRectShape(w, h, r) {
    const shape = new THREE.Shape();
    const x = -w / 2;
    const y = -h / 2;
    shape.moveTo(x + r, y);
    shape.lineTo(x + w - r, y);
    shape.quadraticCurveTo(x + w, y, x + w, y + r);
    shape.lineTo(x + w, y + h - r);
    shape.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    shape.lineTo(x + r, y + h);
    shape.quadraticCurveTo(x, y + h, x, y + h - r);
    shape.lineTo(x, y + r);
    shape.quadraticCurveTo(x, y, x + r, y);
    return shape;
  }

  init() {
    const width = this.container.clientWidth || 1200;
    const height = this.container.clientHeight || 440;

    // 1. Scene & Perspective Camera (Orthogonal Straight View - کاملاً صاف و در مرکز بالا)
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(36, width / height, 0.1, 100);
    this.camera.position.set(0, 0.12, 11.6);
    this.adjustCameraDistance();

    // 2. High Performance WebGL Renderer with Capped DPR (Max 2)
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    this.container.innerHTML = '';
    this.container.appendChild(this.renderer.domElement);

    // 3. Dynamic 2D Offscreen Canvases (Ultra-sharp 1600x680)
    this.canvasW = 1600;
    this.canvasH = 680;

    // Main display canvas
    this.screenCanvas = document.createElement('canvas');
    this.screenCanvas.width = this.canvasW;
    this.screenCanvas.height = this.canvasH;
    this.screenCanvas.dir = 'rtl';
    this.ctx = this.screenCanvas.getContext('2d');
    this.ctx.direction = 'rtl';
    this.screenTexture = new THREE.CanvasTexture(this.screenCanvas);
    this.screenTexture.minFilter = THREE.LinearFilter;

    // Offscreen buffer for ECG mode
    this.ecgCanvas = document.createElement('canvas');
    this.ecgCanvas.width = this.canvasW;
    this.ecgCanvas.height = this.canvasH;
    this.ecgCanvas.dir = 'rtl';
    this.ecgCtx = this.ecgCanvas.getContext('2d');
    this.ecgCtx.direction = 'rtl';

    // Offscreen buffer for CRM mode
    this.crmCanvas = document.createElement('canvas');
    this.crmCanvas.width = this.canvasW;
    this.crmCanvas.height = this.canvasH;
    this.crmCanvas.dir = 'rtl';
    this.crmCtx = this.crmCanvas.getContext('2d');
    this.crmCtx.direction = 'rtl';

    // 4. Clinical Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.88);
    this.scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0x38bdf8, 1.4);
    dirLight1.position.set(6, 8, 9);
    this.scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x00e599, 0.95);
    dirLight2.position.set(-6, -2, 5);
    this.scene.add(dirLight2);

    // 5. 3D Model Group - Widescreen Console (کاملاً صاف، بدون تیزی حاشیه‌ها و با گوشه‌های گرد ارگونومیک)
    this.deviceGroup = new THREE.Group();
    this.scene.add(this.deviceGroup);

    // Main Chassis - Rounded & Beveled Medical Hardware (حاشیه‌های کاملاً نرم و غیرتیز)
    const chassisShape = this.createRoundedRectShape(13.8, 5.8, 0.65);
    const chassisGeo = new THREE.ExtrudeGeometry(chassisShape, {
      depth: 0.28,
      bevelEnabled: true,
      bevelSegments: 4,
      steps: 1,
      bevelSize: 0.05,
      bevelThickness: 0.05
    });
    chassisGeo.center();

    const chassisMat = new THREE.MeshStandardMaterial({
      color: 0x0f172a,
      roughness: 0.35,
      metalness: 0.7
    });
    const chassisMesh = new THREE.Mesh(chassisGeo, chassisMat);
    this.deviceGroup.add(chassisMesh);

    // Outer Bumper / Frame with smooth curved corners
    const frameShape = this.createRoundedRectShape(14.0, 6.0, 0.70);
    const frameGeo = new THREE.ExtrudeGeometry(frameShape, {
      depth: 0.22,
      bevelEnabled: true,
      bevelSegments: 4,
      steps: 1,
      bevelSize: 0.04,
      bevelThickness: 0.04
    });
    frameGeo.center();

    const frameMat = new THREE.MeshStandardMaterial({
      color: 0x1e293b,
      roughness: 0.2,
      metalness: 0.85
    });
    const frameMesh = new THREE.Mesh(frameGeo, frameMat);
    this.deviceGroup.add(frameMesh);

    this.chassisMat = chassisMat;
    this.frameMat = frameMat;
    const curTheme = document.documentElement.getAttribute('data-theme') || 'light';
    this.updateThemeMaterials(curTheme);

    // Front Screen with Dynamic Texture & Rounded Corners (Placed precisely on front face)
    const screenShape = this.createRoundedRectShape(13.2, 5.2, 0.45);
    const screenGeo = new THREE.ShapeGeometry(screenShape);
    const pos = screenGeo.attributes.position;
    const uvs = [];
    for (let i = 0; i < pos.count; i++) {
      const px = pos.getX(i);
      const py = pos.getY(i);
      const u = (px + 13.2 / 2) / 13.2;
      const v = (py + 5.2 / 2) / 5.2;
      uvs.push(u, v);
    }
    screenGeo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));

    const screenMat = new THREE.MeshBasicMaterial({
      map: this.screenTexture,
      side: THREE.DoubleSide
    });
    const screenMesh = new THREE.Mesh(screenGeo, screenMat);
    screenMesh.position.set(0, 0, 0.205);
    this.deviceGroup.add(screenMesh);

    // Top Camera & Status LED
    const camGeo = new THREE.CircleGeometry(0.08, 16);
    const camMat = new THREE.MeshBasicMaterial({ color: 0x05070a, side: THREE.DoubleSide });
    const camMesh = new THREE.Mesh(camGeo, camMat);
    camMesh.position.set(0, 2.76, 0.21);
    this.deviceGroup.add(camMesh);

    const ledGeo = new THREE.CircleGeometry(0.06, 16);
    const ledMat = new THREE.MeshBasicMaterial({ color: 0x00e599, side: THREE.DoubleSide });
    const ledMesh = new THREE.Mesh(ledGeo, ledMat);
    ledMesh.position.set(0.32, 2.76, 0.21);
    this.deviceGroup.add(ledMesh);

    // Soft Drop Shadow
    const shadowGeo = new THREE.PlaneGeometry(15.5, 5.2);
    const shadowCanvas = document.createElement('canvas');
    shadowCanvas.width = 256;
    shadowCanvas.height = 256;
    const sCtx = shadowCanvas.getContext('2d');
    const grad = sCtx.createRadialGradient(128, 128, 10, 128, 128, 120);
    grad.addColorStop(0, 'rgba(0,0,0,0.55)');
    grad.addColorStop(0.5, 'rgba(0,115,255,0.15)');
    grad.addColorStop(1, 'rgba(0,0,0,0)');
    sCtx.fillStyle = grad;
    sCtx.fillRect(0, 0, 256, 256);
    const shadowTexture = new THREE.CanvasTexture(shadowCanvas);
    const shadowMat = new THREE.MeshBasicMaterial({
      map: shadowTexture,
      transparent: true,
      opacity: 0.65
    });
    this.shadowMesh = new THREE.Mesh(shadowGeo, shadowMat);
    this.shadowMesh.position.set(0, -3.2, 0);
    this.shadowMesh.rotation.x = -Math.PI / 2;
    this.scene.add(this.shadowMesh);

    // Initial 3D Pose: Completely Straight, Zero Tilt/Slant (کاملاً صاف در مرکز)
    this.deviceGroup.position.set(0, 0, 0);
    this.deviceGroup.rotation.set(0, 0, 0);
    this.deviceGroup.scale.set(1, 1, 1);

    // Populate texture immediately so screen is never blank on frame 1
    this.drawScreen();

    // Resize listener (without mouse tilt)
    window.addEventListener('resize', () => this.onResize());

    // Optimization: Pause loop when scrolled offscreen
    if ('IntersectionObserver' in window) {
      const obs = new IntersectionObserver((entries) => {
        this.isPaused = !entries[0].isIntersecting;
      }, { threshold: 0.05 });
      obs.observe(this.container);
    }

    // Start render loop
    this.animate();

    // Start GSAP cinematic timeline
    this.startCinematicTimeline();

    // Re-draw screen once Web Fonts (Vazirmatn & JetBrains Mono) are completely loaded
    if (typeof document !== 'undefined' && document.fonts && document.fonts.ready) {
      document.fonts.ready.then(() => {
        this.drawScreen();
      }).catch(() => {});
    }
  }

  updateThemeMaterials(theme) {
    if (!this.chassisMat || !this.frameMat) return;
    const isDark = theme === 'dark';
    this.chassisMat.color.setHex(isDark ? 0x0f172a : 0xe2e8f0);
    this.frameMat.color.setHex(isDark ? 0x1e293b : 0x94a3b8);
  }

  startCinematicTimeline() {
    if (typeof gsap === 'undefined') return;

    // 1. One-time Smooth Cinematic 3D Entrance:
    // Glides into place strictly ONCE when the page loads, and remains 100% static afterwards
    this.deviceGroup.position.set(0, -0.85, 0);
    this.deviceGroup.rotation.set(0, 0, 0);
    this.deviceGroup.scale.set(0.97, 0.97, 0.97);

    gsap.to(this.deviceGroup.position, {
      x: 0,
      y: 0,
      z: 0,
      duration: 1.2,
      ease: "power3.out"
    });

    gsap.to(this.deviceGroup.scale, {
      x: 1,
      y: 1,
      z: 1,
      duration: 1.2,
      ease: "power3.out"
    });

    // 2. Continuous Screen Mode Loop (Device chassis stays 100% completely still and static)
    // Only the on-screen display content crossfades smoothly between ECG telemetry and CRM
    this.tl = gsap.timeline({ delay: 1.2, repeat: -1, repeatDelay: 2.5 });

    // Smoothly crossfades from ECG to CRM over 1.8 seconds with soft phosphor dissolve
    this.tl.to(this, {
      morphProgress: 1,
      duration: 1.8,
      ease: "power2.inOut",
      onComplete: () => {
        this.currentMode = 'crm';
      }
    }, 3.5);

    // Stays on CRM for 5.0 seconds, then smoothly crossfades back to live ECG telemetry
    this.tl.to(this, {
      morphProgress: 0,
      duration: 1.8,
      ease: "power2.inOut",
      onComplete: () => {
        this.currentMode = 'ecg';
      }
    }, 10.0);
  }

  adjustCameraDistance() {
    if (!this.container || !this.camera) return;
    const width = this.container.clientWidth || 1220;
    const height = this.container.clientHeight || 480;
    const aspect = width / height;

    const vFovRad = 36 * (Math.PI / 180);
    const isMobile = width < 768;
    // Generous safe framing: device frame is 14.08 units wide and 6.08 tall.
    // fitWidth 14.8 with fitFactor 0.88 (mobile) / 0.91 (desktop) ensures the entire chassis,
    // rounded corners, side bevels and shadow fit with a guaranteed 9-12% elegant breathing room.
    // Absolutely zero clipping or truncation on ANY device or screen size!
    const fitFactor = isMobile ? 0.88 : 0.91;
    const fitWidth = 14.8;
    const reqDistW = (fitWidth / fitFactor) / (2 * Math.tan(vFovRad / 2) * aspect);
    const reqDistH = (6.4 / fitFactor) / (2 * Math.tan(vFovRad / 2));

    this.camera.position.z = Math.max(reqDistH, reqDistW);
    this.camera.position.x = 0;
    this.camera.position.y = 0;
    this.camera.lookAt(0, 0, 0);
  }

  onResize() {
    if (!this.container || !this.renderer || !this.camera) return;
    const width = this.container.clientWidth;
    const height = this.container.clientHeight || 480;
    this.camera.aspect = width / height;
    this.adjustCameraDistance();
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  setBPM(newBpm) {
    if (typeof gsap !== 'undefined') {
      gsap.to(this, { bpm: newBpm, duration: 0.8, ease: "power2.out" });
    } else {
      this.bpm = newBpm;
    }
    document.querySelectorAll('.vital-btn').forEach(btn => {
      btn.classList.toggle('active', btn.innerText.includes(newBpm.toString()));
    });
  }

  setMode(targetMode) {
    if (typeof gsap !== 'undefined') {
      gsap.killTweensOf(this);
      gsap.to(this, {
        morphProgress: targetMode === 'crm' ? 1 : 0,
        duration: 1.2,
        ease: "power2.inOut",
        onUpdate: () => {
          if (this.morphProgress > 0.5) {
            this.syncTabs('crm');
          } else {
            this.syncTabs('ecg');
          }
        }
      });
    } else {
      this.morphProgress = targetMode === 'crm' ? 1 : 0;
      this.syncTabs(targetMode);
    }
  }

  syncTabs(targetMode) {
    this.currentMode = targetMode;
    document.querySelectorAll('.console-mode-tab').forEach(tab => {
      tab.classList.toggle('active', tab.getAttribute('data-mode') === targetMode);
    });
    const ecgControls = document.getElementById('ecgPulseControls');
    if (ecgControls) {
      ecgControls.style.display = targetMode === 'ecg' ? 'flex' : 'none';
    }
  }

  getECGOffset(cycle) {
    let offset = 0;
    if (cycle > 0.08 && cycle < 0.18) {
      // P-Wave (Atrial Depolarization)
      offset = -Math.sin((cycle - 0.08) * Math.PI / 0.10) * 16;
    } else if (cycle >= 0.20 && cycle < 0.23) {
      // Q-Wave (Septal Dip)
      offset = 10;
    } else if (cycle >= 0.23 && cycle < 0.31) {
      // R-Wave (Ventricular Depolarization Spike)
      offset = -Math.sin((cycle - 0.23) * Math.PI / 0.08) * 115;
    } else if (cycle >= 0.31 && cycle < 0.35) {
      // S-Wave (Basal Ventricular Undershoot)
      offset = Math.sin((cycle - 0.31) * Math.PI / 0.04) * 28;
    } else if (cycle >= 0.45 && cycle < 0.62) {
      // T-Wave (Ventricular Repolarization)
      offset = -Math.sin((cycle - 0.45) * Math.PI / 0.17) * 32;
    } else {
      offset = (Math.random() - 0.5) * 1.5;
    }
    const damp = Math.max(0, 1 - (this.morphProgress || 0));
    return offset * damp;
  }

  getPlethOffset(cycle) {
    // Photoplethysmogram arterial wave delayed by pulse transit time
    const c = (cycle + 0.85) % 1.0;
    let offset = 0;
    if (c < 0.24) {
      // Systolic upstroke
      offset = -Math.sin(c / 0.24 * Math.PI * 0.5) * 52;
    } else if (c < 0.42) {
      // Early diastolic downslope
      const f = (c - 0.24) / 0.18;
      offset = -52 + f * 26;
    } else if (c < 0.50) {
      // Dicrotic notch reflection
      const f = (c - 0.42) / 0.08;
      offset = -26 - Math.sin(f * Math.PI) * 10;
    } else if (c < 0.85) {
      // Diastolic runoff
      const f = (c - 0.50) / 0.35;
      offset = -26 + f * 26;
    }
    const damp = Math.max(0, 1 - (this.morphProgress || 0));
    return offset * damp;
  }

  drawECGToBuffer(ctx, w, h) {
    const y1 = h * 0.32; // Channel 1: Lead II Center
    const y2 = h * 0.62; // Channel 2: Pleth (SpO2) Center

    // Background trail clear for progressive phosphor decay
    ctx.fillStyle = 'rgba(6, 10, 20, 0.07)';
    ctx.fillRect(this.trailX, 52, 28, h - 172);

    // Initial grid render
    if (this.trailX === 0) {
      ctx.fillStyle = '#060A14';
      ctx.fillRect(0, 0, w, h);

      // Diagnostic millimetric grid (1mm and 5mm standard intervals)
      ctx.lineWidth = 1;
      for (let x = 0; x < w; x += 10) {
        ctx.strokeStyle = (x % 50 === 0) ? 'rgba(0, 229, 153, 0.12)' : 'rgba(0, 229, 153, 0.035)';
        ctx.beginPath();
        ctx.moveTo(x, 52);
        ctx.lineTo(x, h - 120);
        ctx.stroke();
      }
      for (let y = 52; y < h - 120; y += 10) {
        ctx.strokeStyle = ((y - 52) % 50 === 0) ? 'rgba(0, 229, 153, 0.12)' : 'rgba(0, 229, 153, 0.035)';
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }

      // Standard 1mV calibration pulse step indicator at x=14
      ctx.strokeStyle = '#00FFFF';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(14, y1);
      ctx.lineTo(24, y1);
      ctx.lineTo(24, y1 - 40);
      ctx.lineTo(44, y1 - 40);
      ctx.lineTo(44, y1);
      ctx.lineTo(54, y1);
      ctx.stroke();

      ctx.font = '10px JetBrains Mono, monospace';
      ctx.fillStyle = '#38BDF8';
      ctx.fillText('1mV', 24, y1 - 46);
    }

    // Top Diagnostic Header
    ctx.fillStyle = '#080E1C';
    ctx.fillRect(0, 0, w, 52);
    ctx.strokeStyle = 'rgba(0, 255, 255, 0.22)';
    ctx.beginPath();
    ctx.moveTo(0, 52);
    ctx.lineTo(w, 52);
    ctx.stroke();

    ctx.font = 'bold 14px "JetBrains Mono", monospace';
    ctx.fillStyle = '#00FFFF';
    ctx.direction = 'ltr';
    ctx.textAlign = 'left';
    ctx.fillText('● PEZESHKAN VITAL-PAD PRO X1 | ECG LEAD II & PLETH TELEMETRY', 28, 33);

    ctx.font = '13.5px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
    ctx.fillStyle = '#94A3B8';
    ctx.direction = 'rtl';
    ctx.textAlign = 'right';
    ctx.fillText(shapePersian('سرعت: 25 mm/s  •  حساسیت: 10 mm/mV  •  ریتم سینوسی نرمال  •  همگام با سپاس'), w - 28, 33);

    // Channel labels
    ctx.font = 'bold 13px "JetBrains Mono", monospace';
    ctx.fillStyle = '#00FFFF';
    ctx.direction = 'ltr';
    ctx.textAlign = 'left';
    ctx.fillText('II (Lead II)', 28, y1 - 50);

    ctx.fillStyle = '#00E599';
    ctx.fillText('PLETH (SpO2)', 28, y2 - 40);

    // Calculate wave cycle & offsets
    const waveFreq = this.bpm / 60;
    this.t += 0.0075 * waveFreq;
    const cycle = this.t % 1.0;

    const ecgY = y1 + this.getECGOffset(cycle);
    const plethY = y2 + this.getPlethOffset(cycle);

    // Synchronous R-Peak pulse trigger
    if (cycle >= 0.24 && cycle <= 0.29) {
      this.heartBeating = true;
      if (this.ledMat) this.ledMat.color.setHex(0x34d399);
    } else {
      this.heartBeating = false;
      if (this.ledMat) this.ledMat.color.setHex(0x059669);
    }

    // Draw Channel 1: Lead II Waveform (Cyan)
    ctx.beginPath();
    ctx.strokeStyle = '#00FFFF';
    ctx.lineWidth = 3.4;
    ctx.shadowColor = '#00FFFF';
    ctx.shadowBlur = 10;
    ctx.moveTo(this.trailX - 4, this.lastECGY || ecgY);
    ctx.lineTo(this.trailX, ecgY);
    ctx.stroke();

    // Draw Channel 2: Pleth Waveform (Emerald)
    ctx.beginPath();
    ctx.strokeStyle = '#00E599';
    ctx.lineWidth = 2.8;
    ctx.shadowColor = '#00E599';
    ctx.shadowBlur = 8;
    ctx.moveTo(this.trailX - 4, this.lastPlethY || plethY);
    ctx.lineTo(this.trailX, plethY);
    ctx.stroke();
    ctx.shadowBlur = 0;

    this.lastECGY = ecgY;
    this.lastPlethY = plethY;

    this.trailX += 4;
    if (this.trailX >= w) {
      this.trailX = 0;
    }

    // Bottom Clinical Metrics Strip
    ctx.fillStyle = '#070C18';
    ctx.fillRect(0, h - 120, w, 120);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.beginPath();
    ctx.moveTo(0, h - 120);
    ctx.lineTo(w, h - 120);
    ctx.stroke();

    const bpmVal = Math.round(this.bpm).toString();
    const metrics = [
      {
        label: 'ضربان قلب (HR / BPM)',
        val: bpmVal,
        sub: 'ریتم سینوسی نرمال',
        unit: 'bpm',
        color: this.heartBeating ? '#FF3366' : '#00FFFF',
        icon: this.heartBeating ? '●' : '○'
      },
      {
        label: 'فشار خون بالینی (NIBP)',
        val: '120/80',
        sub: 'میانگین شریانی: MAP 93',
        unit: 'mmHg',
        color: '#00E599',
        icon: '●'
      },
      {
        label: 'اشباع اکسیژن (SpO2)',
        val: '99%',
        sub: 'شاخص خون‌رسانی PI: 4.8%',
        unit: 'SAT',
        color: '#38BDF8',
        icon: '●'
      },
      {
        label: 'دمای بدن و تنفس (TEMP/RR)',
        val: '36.8°',
        sub: 'تنفس خودکار: 16 rpm',
        unit: 'C',
        color: '#F59E0B',
        icon: '●'
      }
    ];

    const boxW = (w - 70) / 4;
    metrics.forEach((m, idx) => {
      const bx = 30 + idx * (boxW + 13);
      ctx.fillStyle = 'rgba(15, 23, 42, 0.7)';
      ctx.fillRect(bx, h - 108, boxW, 96);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.strokeRect(bx, h - 108, boxW, 96);

      // Label & icon
      ctx.font = '12.5px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
      ctx.fillStyle = '#94A3B8';
      ctx.direction = 'rtl';
      ctx.textAlign = 'right';
      ctx.fillText(shapePersian(m.label) + ' ' + m.icon, bx + boxW - 14, h - 78);

      // Number
      ctx.font = 'bold 30px "JetBrains Mono", monospace';
      ctx.fillStyle = m.color;
      ctx.direction = 'ltr';
      ctx.textAlign = 'left';
      ctx.fillText(m.val, bx + 18, h - 38);

      // Sub description
      ctx.font = '11px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
      ctx.fillStyle = '#64748B';
      ctx.direction = 'rtl';
      ctx.textAlign = 'right';
      ctx.fillText(shapePersian(m.sub), bx + boxW - 14, h - 22);
    });
  }

  drawCRMToBuffer(ctx, w, h) {
    ctx.direction = 'rtl';

    // 1. Sleek Clinic Dashboard Surface Background
    ctx.fillStyle = '#080E1A';
    ctx.fillRect(0, 0, w, h);

    // 2. CRM Header Bar
    ctx.fillStyle = '#0D1527';
    ctx.fillRect(0, 0, w, 52);
    ctx.strokeStyle = 'rgba(0, 115, 255, 0.35)';
    ctx.beginPath();
    ctx.moveTo(0, 52);
    ctx.lineTo(w, 52);
    ctx.stroke();

    // Top Right: Title
    ctx.font = 'bold 15px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
    ctx.fillStyle = '#38BDF8';
    ctx.direction = 'rtl';
    ctx.textAlign = 'right';
    ctx.fillText(shapePersian('سامانه مدیریت پرونده الکترونیک سلامت و نوبت‌دهی هوشمند مطب پزشکآن'), w - 28, 33);

    // Top Left: AI & Hardware status badges
    ctx.font = '13px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
    ctx.fillStyle = '#00E599';
    ctx.direction = 'rtl';
    ctx.textAlign = 'left';
    ctx.fillText(shapePersian('● دستیار بالینی هوش مصنوعی: آنلاین   ● قلم نوری: متصل   ● اتصال سپاس و بیمه سلامت'), 28, 33);

    // 3. KPI Metric Summary Cards (Top Row)
    const kpis = [
      { title: shapePersian('کل نوبت‌های امروز'), val: shapePersian('۲۸ نوبت'), sub: shapePersian('۸۵٪ تکمیل ظرفیت مطب'), color: '#38BDF8' },
      { title: shapePersian('میانگین زمان ویزیت'), val: shapePersian('۱۲ دقیقه'), sub: shapePersian('۳+ دقیقه صرفه‌جویی هر ویزیت'), color: '#00E599' },
      { title: shapePersian('تداخل دارویی کشف‌شده'), val: shapePersian('۲ هشدار ایمن'), sub: shapePersian('پیشگیری خودکار توسط AI'), color: '#F59E0B' },
      { title: shapePersian('شاخص رضایت مراجعین'), val: '۹۹.۴٪', sub: shapePersian('بر پایه ۱۸۴ نظرسنجی اخیر'), color: '#A855F7' }
    ];

    const kpiW = (w - 70) / 4;
    kpis.forEach((k, i) => {
      const kx = 30 + i * (kpiW + 13);
      ctx.fillStyle = 'rgba(15, 23, 42, 0.8)';
      ctx.fillRect(kx, 66, kpiW, 82);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.strokeRect(kx, 66, kpiW, 82);

      // KPI title
      ctx.font = '12.5px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
      ctx.fillStyle = '#94A3B8';
      ctx.direction = 'rtl';
      ctx.textAlign = 'right';
      ctx.fillText(k.title, kx + kpiW - 14, 90);

      // KPI value
      ctx.font = 'bold 22px "Vazirmatn", "JetBrains Mono", sans-serif';
      ctx.fillStyle = k.color;
      ctx.direction = 'rtl';
      ctx.textAlign = 'right';
      ctx.fillText(k.val, kx + kpiW - 14, 122);

      // KPI sub
      ctx.font = '11px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
      ctx.fillStyle = '#64748B';
      ctx.direction = 'rtl';
      ctx.textAlign = 'left';
      ctx.fillText(k.sub, kx + 14, 122);
    });

    // 4. Live Appointment Queue Table
    const tableTop = 162;
    ctx.fillStyle = '#10172A';
    ctx.fillRect(30, tableTop, w - 60, 36);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.strokeRect(30, tableTop, w - 60, 36);

    ctx.font = 'bold 12.5px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
    ctx.fillStyle = '#94A3B8';
    ctx.direction = 'rtl';
    ctx.textAlign = 'right';
    ctx.fillText(shapePersian('زمان و نوبت'), w - 50, tableTop + 24);
    ctx.fillText(shapePersian('نام و کد پرونده بیمار'), w - 230, tableTop + 24);
    ctx.fillText(shapePersian('نوع ویزیت و شرح بالینی مراجع'), w - 540, tableTop + 24);
    ctx.fillText(shapePersian('دستیار بالینی و تجهیزات فعال'), w - 990, tableTop + 24);
    ctx.fillText(shapePersian('وضعیت پذیرش و نوبت'), w - 1320, tableTop + 24);

    // 4 Live Queue Rows
    const rows = [
      {
        time: shapePersian('نوبت ۱ • ۱۴:۳۰'),
        patient: shapePersian('خانم سارا احمدی (کد: ۸۴۲۱)'),
        desc: shapePersian('چکاپ دوره‌ای آریتمی قلبی و بررسی علائم تپش'),
        feature: shapePersian('قلم نوری متصل • نوار قلب Lead II ثبت شد'),
        status: shapePersian('در اتاق ویزیت پزشک'),
        statusColor: '#00E599',
        active: true
      },
      {
        time: shapePersian('نوبت ۲ • ۱۴:۴۵'),
        patient: shapePersian('دکتر کیانوش راد (کد: ۹۰۳۴)'),
        desc: shapePersian('تنظیم دوز داروی فشار خون و بازبینی آزمایشگاهی'),
        feature: shapePersian('هشدار تداخل: آملودیپین + کلاریترومایسین'),
        status: shapePersian('آماده فراخوان به اتاق'),
        statusColor: '#38BDF8',
        active: false
      },
      {
        time: shapePersian('نوبت ۳ • ۱۵:۰۰'),
        patient: shapePersian('خانم فاطمه خسروی (کد: ۷۲۱۹)'),
        desc: shapePersian('تفسیر سونوگرافی تیرویید و بررسی سابقه فامیلی'),
        feature: shapePersian('ضمیمه تصاویر بالینی به پرونده ابری امن'),
        status: shapePersian('پذیرش منشی شده'),
        statusColor: '#94A3B8',
        active: false
      },
      {
        time: shapePersian('نوبت ۴ • ۱۵:۱۵'),
        patient: shapePersian('آقای علی مظفری (کد: ۶۱۱۸)'),
        desc: shapePersian('ویزیت سلامت عمومی و چکاپ آزمایشگاهی سالیانه'),
        feature: shapePersian('پرونده الکترونیک فعال • پرداخت آنلاین شده'),
        status: shapePersian('نوبت آنلاین تأییدشده'),
        statusColor: '#94A3B8',
        active: false
      }
    ];

    rows.forEach((r, idx) => {
      const ry = tableTop + 44 + idx * 82;
      ctx.fillStyle = r.active ? 'rgba(0, 115, 255, 0.12)' : (idx % 2 === 0 ? 'rgba(15, 23, 42, 0.55)' : 'rgba(15, 23, 42, 0.3)');
      ctx.fillRect(30, ry, w - 60, 74);
      ctx.strokeStyle = r.active ? 'rgba(0, 115, 255, 0.45)' : 'rgba(255, 255, 255, 0.05)';
      ctx.strokeRect(30, ry, w - 60, 74);

      if (r.active) {
        ctx.fillStyle = '#00E599';
        ctx.fillRect(w - 34, ry, 4, 74);
      }

      ctx.direction = 'rtl';
      ctx.textAlign = 'right';

      // Time
      ctx.font = 'bold 15px "JetBrains Mono", "Vazirmatn", monospace';
      ctx.fillStyle = r.active ? '#38BDF8' : '#CBD5E1';
      ctx.fillText(r.time, w - 50, ry + 42);

      // Patient
      ctx.font = 'bold 14px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
      ctx.fillStyle = '#FFFFFF';
      ctx.fillText(r.patient, w - 230, ry + 42);

      // Description
      ctx.font = '13px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
      ctx.fillStyle = '#94A3B8';
      ctx.fillText(r.desc, w - 540, ry + 42);

      // Feature / AI
      ctx.font = '12px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
      ctx.fillStyle = r.feature.includes('هشدار') ? '#F59E0B' : '#64748B';
      ctx.fillText(r.feature, w - 990, ry + 42);

      // Status Badge Pill with rounded corners
      const badgeX = w - 1470;
      const badgeY = ry + 20;
      const badgeW = 150;
      const badgeH = 34;
      const r_pill = 8;
      ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
      ctx.beginPath();
      if (typeof ctx.roundRect === 'function') {
        ctx.roundRect(badgeX, badgeY, badgeW, badgeH, r_pill);
      } else {
        ctx.rect(badgeX, badgeY, badgeW, badgeH);
      }
      ctx.fill();
      ctx.strokeStyle = r.statusColor;
      ctx.lineWidth = 1.2;
      ctx.stroke();

      ctx.font = 'bold 12px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
      ctx.fillStyle = r.statusColor;
      ctx.textAlign = 'center';
      ctx.fillText(r.status, badgeX + badgeW / 2, badgeY + 22);
    });

    // 5. CRM Footer Actions Strip
    ctx.fillStyle = '#080D18';
    ctx.fillRect(0, h - 58, w, 58);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.beginPath();
    ctx.moveTo(0, h - 58);
    ctx.lineTo(w, h - 58);
    ctx.stroke();

    ctx.font = '12.5px "Vazirmatn", "Segoe UI", Tahoma, sans-serif';
    ctx.fillStyle = '#94A3B8';
    ctx.direction = 'rtl';
    ctx.textAlign = 'right';
    ctx.fillText(shapePersian('میانبرها: [ + ثبت نوبت فوری جدید ]   [ ● صدور نسخه الکترونیک تامین و سلامت ]   [ ● جستجوی پرونده با کدملی ]'), w - 30, h - 24);

    ctx.fillStyle = '#00E599';
    ctx.textAlign = 'left';
    ctx.fillText(shapePersian('● رمزنگاری انتها‌به‌انتها فعال • گواهینامه امنیت داده‌های سلامت PHI/EHR'), 30, h - 24);
  }

  drawScreen() {
    const w = this.canvasW;
    const h = this.canvasH;

    // Draw both modes to their respective buffer canvases
    this.drawECGToBuffer(this.ecgCtx, w, h);
    this.drawCRMToBuffer(this.crmCtx, w, h);

    const p = Math.max(0, Math.min(1, this.morphProgress));

    // Dynamic LED indicator: shifts from vital emerald green (ECG) to Pezeshkan clinical blue (CRM)
    if (this.ledMat) {
      const r = 0.02 * (1 - p);
      const g = 0.90 * (1 - p) + 0.45 * p;
      const b = 0.41 * (1 - p) + 1.0 * p;
      this.ledMat.color.setRGB(r, g, b);
    }

    // Composite onto main screen canvas based on morph progress
    if (p <= 0.001) {
      // 100% Clinical ECG Monitor
      this.ctx.globalAlpha = 1;
      this.ctx.drawImage(this.ecgCanvas, 0, 0);
    } else if (p >= 0.999) {
      // 100% CRM Clinic Management Panel
      this.ctx.globalAlpha = 1;
      this.ctx.drawImage(this.crmCanvas, 0, 0);
    } else {
      // Silky-smooth, harmonious medical crossfade (no jarring vertical lines or text clipping)
      this.ctx.globalAlpha = Math.cos(p * Math.PI * 0.5);
      this.ctx.drawImage(this.ecgCanvas, 0, 0);

      this.ctx.globalAlpha = Math.sin(p * Math.PI * 0.5);
      this.ctx.drawImage(this.crmCanvas, 0, 0);

      // Subtle organic medical phosphor shimmer that softly blooms at midpoint
      const bloom = Math.sin(p * Math.PI);
      if (bloom > 0.01) {
        const glow = this.ctx.createRadialGradient(w / 2, h / 2, 50, w / 2, h / 2, w * 0.58);
        glow.addColorStop(0, `rgba(0, 245, 255, ${bloom * 0.12})`);
        glow.addColorStop(0.6, `rgba(0, 229, 153, ${bloom * 0.05})`);
        glow.addColorStop(1, 'rgba(0, 0, 0, 0)');
        this.ctx.fillStyle = glow;
        this.ctx.fillRect(0, 0, w, h);
      }

      this.ctx.globalAlpha = 1;
    }

    this.screenTexture.needsUpdate = true;
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    if (this.isPaused) return;

    this.drawScreen();
    this.renderer.render(this.scene, this.camera);
  }
}

// 3. Mobile Navigation Drawer
function toggleMobileMenu() {
  const drawer = document.getElementById('mobileNavDrawer');
  if (drawer) {
    drawer.classList.toggle('active');
    const isActive = drawer.classList.contains('active');
    document.body.style.overflow = isActive ? 'hidden' : '';
    if (window.lenis) {
      if (isActive) window.lenis.stop();
      else window.lenis.start();
    }
  }
}

function handleDrawerBackdropClick(e) {
  if (e.target.id === 'mobileNavDrawer') {
    toggleMobileMenu();
  }
}

// 4. Hero Section Choreography (Seamless entrance and hint activation)
function initHeroChoreography() {
  const header = document.querySelector('.site-header');
  if (header) {
    header.classList.add('header-revealed');
  }

  const hint = document.getElementById('scrollPromptHint');
  if (hint) {
    hint.classList.add('visible');
  }

  const textItems = document.querySelectorAll('.hero-anim-item');
  textItems.forEach(el => {
    el.classList.add('animate-in');
  });
}

// Cinematic Smooth Scroll to the next section
function scrollToNextSection() {
  const tab = document.getElementById('pezShellTab') || document.getElementById('scrollPromptHint');
  if (tab) {
    tab.classList.add('clicked');
    setTimeout(() => tab.classList.remove('clicked'), 350);
  }

  const shellWrap = document.querySelector('.pez-shell-hero-wrap') || document.getElementById('shell');
  const target = (shellWrap && shellWrap.nextElementSibling) || document.querySelector('.vital-section-divider') || document.querySelector('.section-title-wrap');
  if (target) {
    if (window.lenis) {
      window.lenis.scrollTo(target, {
        offset: -40,
        duration: 1.4,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t))
      });
    } else {
      const y = target.getBoundingClientRect().top + window.pageYOffset - 40;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  }
}

// 5. Universal Scroll Reveal Animation System
function setupScrollRevealTargets() {
  const cardSelectors = [
    '.panel-card',
    '.pricing-card',
    '.journey-step',
    '.feature-deep-box',
    '.pillar-card',
    '.doc-card',
    '.stat-counter',
    '.vital-dial-card',
    '.vital-section-divider',
    '.faq-item',
    '.contact-card',
    '.service-item',
    '.cta-box',
    '.section-title-wrap'
  ];

  // Auto-tag children inside grids with staggered animation delays
  document.querySelectorAll('.grid-2, .grid-3, .grid-4, .journey-timeline, .features-grid, .faq-list, .vital-dial-grid').forEach(parent => {
    Array.from(parent.children).forEach((child, idx) => {
      if (!child.classList.contains('reveal-on-scroll')) {
        child.classList.add('reveal-on-scroll');
        child.classList.add(`reveal-stagger-${(idx % 4) + 1}`);
      }
    });
  });

  document.querySelectorAll(cardSelectors.join(', ')).forEach((el, idx) => {
    if (!el.classList.contains('reveal-on-scroll')) {
      el.classList.add('reveal-on-scroll');
      el.classList.add(`reveal-stagger-${(idx % 4) + 1}`);
    }
  });
}

function initScrollReveal() {
  setupScrollRevealTargets();

  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.reveal-on-scroll').forEach(el => el.classList.add('revealed'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  });

  document.querySelectorAll('.reveal-on-scroll').forEach(el => {
    observer.observe(el);
  });
}

// 5.5. Vital Dial Interactive Telemetry Sweep (10% Console Metaphor)
function initVitalDialInteractions() {
  document.querySelectorAll('.vital-dial-card').forEach(card => {
    if (!card.hasAttribute('tabindex')) {
      card.setAttribute('tabindex', '0');
    }
    const triggerSweep = () => {
      card.classList.toggle('dial-active-sweep');
      const valEl = card.querySelector('.vital-dial-number');
      const subEl = card.querySelector('.vital-dial-sub');
      const altVal = card.getAttribute('data-alt-val');
      const altSub = card.getAttribute('data-alt-sub');
      const origVal = card.getAttribute('data-orig-val');
      const origSub = card.getAttribute('data-orig-sub');
      if (valEl && altVal) {
        if (!origVal) card.setAttribute('data-orig-val', valEl.textContent);
        const isSwitched = card.classList.contains('dial-active-sweep');
        valEl.textContent = isSwitched ? altVal : (card.getAttribute('data-orig-val') || valEl.textContent);
      }
      if (subEl && altSub) {
        if (!origSub) card.setAttribute('data-orig-sub', subEl.textContent);
        const isSwitched = card.classList.contains('dial-active-sweep');
        subEl.textContent = isSwitched ? altSub : (card.getAttribute('data-orig-sub') || subEl.textContent);
      }
    };
    card.addEventListener('click', triggerSweep);
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        triggerSweep();
      }
    });
  });
}

// 6. High-Performance Inertial Smooth Scroll (Lenis Native RAF)
function initSmoothScroll() {
  if (typeof Lenis === 'undefined') return;

  const lenis = new Lenis({
    duration: 1.18,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    orientation: 'vertical',
    gestureOrientation: 'vertical',
    smoothWheel: true,
    wheelMultiplier: 0.95,
    touchMultiplier: 1.2,
    infinite: false,
    prevent: (node) => {
      return !!(
        node &&
        node.closest &&
        node.closest(
          '[data-lenis-prevent], .drawer-content, .clinical-auth-modal, .article-modal-dialog, .article-modal-body, .nl-modal-dialog, .nl-modal-body, .edition-modal-dialog, .edition-modal-body, .mobile-drawer-panel, .mobile-drawer-body'
        )
      );
    }
  });

  window.lenis = lenis;

  // Ultra-smooth native requestAnimationFrame loop for Lenis
  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  // Debounced auto-resize for Lenis (strictly suspended during active scroll to eliminate end-of-page jank)
  if (typeof ResizeObserver !== 'undefined' && document.body) {
    let resizeTimer = null;
    const ro = new ResizeObserver(() => {
      if (lenis.isScrolling) return; // Never recalculate layout during active user scrolling
      if (resizeTimer) clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (!lenis.isScrolling) {
          lenis.resize();
        }
      }, 200);
    });
    ro.observe(document.body);
  }

  // Smooth scroll delegation for all internal anchor links (static & dynamic)
  document.addEventListener('click', function(e) {
    const anchor = e.target && e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!anchor) return;
    const targetId = anchor.getAttribute('href');
    if (targetId && targetId !== '#' && !targetId.startsWith('#!')) {
      try {
        const targetEl = document.querySelector(targetId);
        if (targetEl) {
          e.preventDefault();
          lenis.scrollTo(targetEl, { offset: -75, duration: 1.18 });
        }
      } catch (err) {}
    }
  });
}

// 6.5. Sticky Header Sync (Pinned when scrolling past Hero - High Performance RAF Throttled)
function initStickyHeaderSync() {
  const stickyHeader = document.getElementById('stickySiteHeader');
  const heroShell = document.getElementById('shell') || document.querySelector('.pez-shell');
  if (!stickyHeader) return;

  let heroHeight = heroShell ? heroShell.offsetHeight : 0;
  window.addEventListener('resize', () => {
    if (heroShell) heroHeight = heroShell.offsetHeight;
  }, { passive: true });

  let ticking = false;
  function updateHeaderState() {
    if (!ticking) {
      requestAnimationFrame(() => {
        if (!heroShell) {
          stickyHeader.classList.add('is-pinned');
          ticking = false;
          return;
        }
        const scrollY = window.scrollY || window.pageYOffset || 0;
        const heroPassed = scrollY >= (heroHeight - 40);
        stickyHeader.classList.toggle('is-pinned', heroPassed);
        ticking = false;
      });
      ticking = true;
    }
  }

  window.addEventListener('scroll', updateHeaderState, { passive: true });
  if (window.lenis && typeof window.lenis.on === 'function') {
    window.lenis.on('scroll', updateHeaderState);
  }
  updateHeaderState();
}

// 7. Initializer on DOM ready (No Hibernate / Screen Saver on public pages)
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  
  // Theme toggle listeners (attach to all switches)
  document.querySelectorAll('.theme-toggle-btn, .theme-switch, #themeToggleBtn').forEach(btn => {
    btn.addEventListener('click', toggleTheme);
  });

  // Sticky Header Synchronization
  initStickyHeaderSync();

  // Natural Physiological ECG Wave Animation
  initNaturalEcg();

  // Hero Digital Counter Animations (4 cards)
  initHeroCounters();

  // Live Persian Date, Day & Digital Time Rail Widget
  initLiveDateTimeRail();

  // Initialize Three.js 3D Diagnostic Console (if container exists)
  if (document.getElementById('threeDeviceContainer') && typeof THREE !== 'undefined') {
    window.pezeshkan3D = new Pezeshkan3DConsole('threeDeviceContainer');
  }

  // Hero entrance choreography
  initHeroChoreography();

  // Universal scroll reveal
  initScrollReveal();

  // Vital Dial interactive sweep
  initVitalDialInteractions();

  // Premium Inertial Smooth Scroll
  initSmoothScroll();
});

// 7.1. Live Persian Date, Day & Digital Time Rail Widget (Asia/Tehran)
function initLiveDateTimeRail() {
  const clockEl = document.getElementById('railLiveClock');
  const dayEl = document.getElementById('railLiveDay');
  const dateEl = document.getElementById('railLiveDate');
  if (!clockEl && !dayEl && !dateEl) return;

  let dateFormatter, weekdayFormatter;
  try {
    dateFormatter = new Intl.DateTimeFormat('fa-IR-u-ca-persian', {
      timeZone: 'Asia/Tehran',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    weekdayFormatter = new Intl.DateTimeFormat('fa-IR-u-ca-persian', {
      timeZone: 'Asia/Tehran',
      weekday: 'long'
    });
  } catch (e) {}

  function update() {
    const now = new Date();
    
    // High-precision Tehran Time (Hour:Minute:Second)
    let tehranTimeStr = '';
    try {
      tehranTimeStr = now.toLocaleTimeString('en-GB', {
        timeZone: 'Asia/Tehran',
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    } catch (e) {}

    // Fallback if browser locale lacks Asia/Tehran
    if (!tehranTimeStr || tehranTimeStr.length < 7) {
      const tehranMillis = now.getTime() + (3.5 * 3600000) + (now.getTimezoneOffset() * 60000);
      const t = new Date(tehranMillis);
      const hh = String(t.getHours()).padStart(2, '0');
      const mm = String(t.getMinutes()).padStart(2, '0');
      const ss = String(t.getSeconds()).padStart(2, '0');
      tehranTimeStr = `${hh}:${mm}:${ss}`;
    }

    if (clockEl) clockEl.textContent = tehranTimeStr;
    if (dayEl && weekdayFormatter) dayEl.textContent = weekdayFormatter.format(now);
    if (dateEl && dateFormatter) dateEl.textContent = dateFormatter.format(now);
  }

  update();
  if (!window._railClockTimer) {
    window._railClockTimer = setInterval(update, 1000);
  }
}

// 7.2. Persian Number Formatter & Hero Digital Counters
function toPersianDigits(n) {
  const farsiDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
  return n.toString().replace(/\d/g, x => farsiDigits[x]);
}

function initHeroCounters() {
  const counterElements = document.querySelectorAll('.metric-number[data-target]');
  if (!counterElements.length) return;

  counterElements.forEach(el => {
    const target = parseFloat(el.getAttribute('data-target')) || 0;
    const formatComma = el.getAttribute('data-format') === 'comma';
    const duration = 1800; // ms
    const startTime = performance.now();

    function updateCounter(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Smooth easeOutExpo curve
      const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      const currentVal = Math.round(target * ease);

      let formattedNumber = currentVal.toString();
      if (formatComma) {
        formattedNumber = currentVal.toLocaleString('en-US');
      }
      el.textContent = formattedNumber;

      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      } else {
        let finalStr = target.toString();
        if (formatComma) finalStr = target.toLocaleString('en-US');
        el.textContent = finalStr;
      }
    }

    requestAnimationFrame(updateCounter);
  });
}

// 7.5. Natural Physiological Clinical ECG Wave Engine (72 BPM Lead II)
function initNaturalEcg() {
  const canvas = document.getElementById('naturalEcgCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  let width = 0;
  let height = 0;
  let dpr = 1;
  let buffer = [];
  let head = 0;
  let lastTime = 0;
  let beatPhase = 0; // 0 to 1 over cardiac cycle
  const BPM = 72;
  const cycleSeconds = 60 / BPM; // ~0.833s
  const sweepSpeed = 160; // px per second

  function resize() {
    const rect = canvas.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = Math.floor(rect.width * dpr);
    height = Math.floor(rect.height * dpr);
    canvas.width = width;
    canvas.height = height;

    if (buffer.length !== width) {
      buffer = new Array(width).fill(null);
      head = 0;
    }
  }

  resize();
  window.addEventListener('resize', resize, { passive: true });

  // Calculate clinical P-Q-R-S-T voltage (-0.3 to +1.0)
  function getEcgVoltage(p) {
    let v = 0;

    // Baseline micro-drift
    v += Math.sin(p * Math.PI * 4) * 0.008;

    // P-wave (atrial depolarization)
    const pDist = p - 0.16;
    v += 0.14 * Math.exp(-(pDist * pDist) / (2 * 0.022 * 0.022));

    // Q-wave (septal depolarization - small dip)
    const qDist = p - 0.29;
    v -= 0.12 * Math.exp(-(qDist * qDist) / (2 * 0.009 * 0.009));

    // R-wave (ventricular depolarization - sharp tall spike)
    const rDist = p - 0.32;
    v += 1.0 * Math.exp(-(rDist * rDist) / (2 * 0.012 * 0.012));

    // S-wave (late ventricular depolarization - sharp dip)
    const sDist = p - 0.35;
    v -= 0.28 * Math.exp(-(sDist * sDist) / (2 * 0.011 * 0.011));

    // T-wave (ventricular repolarization - smooth dome)
    const tDist = p - 0.54;
    const tSigma = tDist < 0 ? 0.045 : 0.055;
    v += 0.26 * Math.exp(-(tDist * tDist) / (2 * tSigma * tSigma));

    // Physiological micro-tremor
    v += (Math.random() - 0.5) * 0.012;

    return v;
  }

  let isVisible = true;
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      isVisible = entries[0].isIntersecting;
    }, { threshold: 0.05 });
    observer.observe(canvas);
  }

  function render(time) {
    requestAnimationFrame(render);
    if (!isVisible || !width || !height) return;

    if (!lastTime) lastTime = time;
    const dt = Math.min((time - lastTime) / 1000, 0.1);
    lastTime = time;

    // Advance sweep
    const pixelsToAdvance = Math.max(1, Math.round(sweepSpeed * dpr * dt));
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

    for (let i = 0; i < pixelsToAdvance; i++) {
      beatPhase = (beatPhase + (dt / pixelsToAdvance) / cycleSeconds) % 1.0;
      const voltage = getEcgVoltage(beatPhase);
      buffer[head] = voltage;

      // Erase window ahead of sweep
      const eraseWidth = Math.round(28 * dpr);
      for (let e = 1; e <= eraseWidth; e++) {
        buffer[(head + e) % width] = null;
      }

      head = (head + 1) % width;
    }

    // Draw background grid
    ctx.clearRect(0, 0, width, height);

    const midY = height * 0.52;
    const scale = height * 0.36;

    // Grid lines
    ctx.lineWidth = 1;
    ctx.strokeStyle = isDark ? 'rgba(0, 240, 255, 0.06)' : 'rgba(0, 115, 255, 0.06)';
    ctx.beginPath();
    const step = 20 * dpr;
    for (let x = 0; x < width; x += step) {
      ctx.moveTo(x + 0.5, 0);
      ctx.lineTo(x + 0.5, height);
    }
    for (let y = 0; y < height; y += step) {
      ctx.moveTo(0, y + 0.5);
      ctx.lineTo(width, y + 0.5);
    }
    ctx.stroke();

    // Major baseline
    ctx.strokeStyle = isDark ? 'rgba(0, 240, 255, 0.12)' : 'rgba(0, 115, 255, 0.12)';
    ctx.beginPath();
    ctx.moveTo(0, midY);
    ctx.lineTo(width, midY);
    ctx.stroke();

    // Draw ECG phosphor wave
    const mainColor = isDark ? '#00F0FF' : '#059669';
    const glowColor = isDark ? 'rgba(0, 240, 255, 0.6)' : 'rgba(5, 150, 105, 0.4)';

    ctx.save();
    ctx.shadowColor = glowColor;
    ctx.shadowBlur = isDark ? 8 * dpr : 5 * dpr;
    ctx.strokeStyle = mainColor;
    ctx.lineWidth = 2 * dpr;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    let inPath = false;
    ctx.beginPath();

    for (let x = 0; x < width; x++) {
      const val = buffer[x];
      if (val === null) {
        if (inPath) {
          ctx.stroke();
          ctx.beginPath();
          inPath = false;
        }
      } else {
        const y = midY - (val * scale);
        if (!inPath) {
          ctx.moveTo(x, y);
          inPath = true;
        } else {
          ctx.lineTo(x, y);
        }
      }
    }
    if (inPath) {
      ctx.stroke();
    }

    // Leading glowing scanhead dot
    const currentVal = buffer[(head - 1 + width) % width];
    if (currentVal !== null) {
      const scanX = (head - 1 + width) % width;
      const scanY = midY - (currentVal * scale);

      ctx.shadowBlur = 12 * dpr;
      ctx.shadowColor = isDark ? '#00FFFF' : '#00E599';
      ctx.fillStyle = isDark ? '#FFFFFF' : '#00E599';
      ctx.beginPath();
      ctx.arc(scanX, scanY, 3.5 * dpr, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }

  requestAnimationFrame(render);
}

// 8. Clinical Toast & Interactive Notice Handlers
function showClinicalToast(title, desc, type) {
  let container = document.querySelector('.clinical-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'clinical-toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'clinical-toast';
  toast.innerHTML = `
    <div class="clinical-toast-icon">
      <svg class="svg-icon" style="width:16px;height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="16" x2="12" y2="12"/>
        <line x1="12" y1="8" x2="12.01" y2="8"/>
      </svg>
    </div>
    <div class="clinical-toast-body">
      <strong>${title}</strong>
      <p>${desc}</p>
    </div>
    <button type="button" class="clinical-toast-close" onclick="this.parentElement.remove()" title="بستن" aria-label="بستن">
      <svg class="svg-icon" style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(15px)';
    setTimeout(() => toast.remove(), 400);
  }, 4500);
}

function openLoginNotice(type = 'select') {
  const activeRole = (type === 'doctor' || type === 'patient') ? type : 'select';
  let backdrop = document.getElementById('clinicalAuthModalBackdrop');
  if (!backdrop) {
    backdrop = document.createElement('div');
    backdrop.id = 'clinicalAuthModalBackdrop';
    backdrop.className = 'clinical-auth-modal-backdrop';
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) closeClinicalAuthModal();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeClinicalAuthModal();
    });
    document.body.appendChild(backdrop);
  }

  renderClinicalAuthModalContent(activeRole);
  requestAnimationFrame(() => {
    backdrop.classList.add('active');
  });
}

function closeClinicalAuthModal() {
  const backdrop = document.getElementById('clinicalAuthModalBackdrop');
  if (backdrop) {
    backdrop.classList.remove('active');
  }
}

function renderClinicalAuthModalContent(role = 'select') {
  const backdrop = document.getElementById('clinicalAuthModalBackdrop');
  if (!backdrop) return;

  const isDoctor = role === 'doctor';
  const isPatient = role === 'patient';
  const isSelect = !isDoctor && !isPatient;

  const selectBody = `
    <div style="margin-bottom:14px; text-align:center;">
      <span style="display:inline-flex; align-items:center; gap:6px; font-size:11.5px; font-weight:800; color:var(--brand-primary); background:rgba(0,115,255,0.08); padding:4px 12px; border-radius:9999px;">
        ورود یکپارچه به سامانه سلامت پزشکآن
      </span>
      <h4 style="font-size:17px; font-weight:900; color:var(--text-pure); margin:10px 0 6px;">لطفاً نقش خود را انتخاب نمایید</h4>
      <p style="font-size:12.5px; color:var(--text-secondary); line-height:1.6; margin:0 auto; max-width:440px;">
        برای ورود به بخش نوبت‌دهی آنلاین مراجعین، یا ورود به پنل جامع مدیریت مطب و EMR پزشک، درگاه مورد نظر را انتخاب نمایید:
      </p>
    </div>

    <div class="auth-role-cards-grid">
      <!-- Role Card 1: Patient -->
      <div class="auth-role-card auth-role-card-patient">
        <div class="auth-role-card-header">
          <div class="auth-role-card-icon">
            <svg class="svg-icon" style="width:20px;height:20px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
          <div>
            <span class="auth-role-card-badge">مراجعین و بیماران</span>
            <h5 class="auth-role-card-title">درگاه سلامت و نوبت‌دهی بیمار</h5>
          </div>
        </div>
        <p class="auth-role-card-desc">
          رزرو نوبت پزشکان متخصص، دریافت نسخه الکترونیک، مشاهده جواب آزمایش‌ها و یادآور دارو.
        </p>
        <div style="display:flex; flex-direction:column; gap:8px; margin-top:auto;">
          <a href="/appointments" class="btn btn-primary auth-card-btn" style="background:var(--brand-primary) !important;">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
            <span>ورود و نوبت‌دهی آنلاین</span>
          </a>
          <a href="/download?role=patients" class="btn btn-secondary auth-card-btn">
            <span>دریافت اپلیکیشن بیمار</span>
          </a>
          <button type="button" class="auth-card-link" onclick="renderClinicalAuthModalContent('patient')">
            امکانات و راهنمای پنل بیمار ←
          </button>
        </div>
      </div>

      <!-- Role Card 2: Doctor -->
      <div class="auth-role-card auth-role-card-doctor">
        <div class="auth-role-card-header">
          <div class="auth-role-card-icon">
            <svg class="svg-icon" style="width:20px;height:20px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/><path d="M12 11v6"/><path d="M9 14h6"/></svg>
          </div>
          <div>
            <span class="auth-role-card-badge">پزشکان و کلینیک‌ها</span>
            <h5 class="auth-role-card-title">سامانه مدیریت مطب و پرونده (EMR)</h5>
          </div>
        </div>
        <p class="auth-role-card-desc">
          پرونده الکترونیک پزشکی، نوبت‌دهی منشی، باشگاه مراجعین، CRM و سامانه مالی ابری.
        </p>
        <div style="display:flex; flex-direction:column; gap:8px; margin-top:auto;">
          <a href="https://app.pezeshk-on.ir/" target="_blank" rel="noopener noreferrer" class="btn btn-primary auth-card-btn" style="background:var(--brand-gradient-primary) !important;">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
            <span>ورود به پنل مطب (app.pezeshk-on.ir) ↗</span>
          </a>
          <a href="/start" class="btn btn-secondary auth-card-btn" style="color:var(--brand-primary); font-weight:800;">
            <span>ثبت‌نام پزشک (۳ ماه رایگان)</span>
          </a>
          <button type="button" class="auth-card-link" onclick="renderClinicalAuthModalContent('doctor')">
            امکانات و راهنمای پنل پزشک ←
          </button>
        </div>
      </div>
    </div>
  `;

  const patientBody = `
    <div style="margin-bottom:10px;">
      <span style="display:inline-flex; align-items:center; gap:6px; font-size:11.5px; font-weight:800; color:var(--brand-primary); background:rgba(0,115,255,0.1); padding:4px 10px; border-radius:9999px;">
        ویژه بیماران، مراجعین و شهروندان
      </span>
      <h4 style="font-size:16.5px; font-weight:900; color:var(--text-pure); margin:10px 0 6px;">درگاه سلامت و پرونده پزشکی بیمار</h4>
      <p style="font-size:12.5px; color:var(--text-secondary); line-height:1.7; margin:0;">
        دسترسی یکپارچه به خدمات درمانی، نوبت‌دهی و پرونده پزشکی بدون نیاز به نسخه‌های کاغذی:
      </p>
    </div>
    <ul class="auth-modal-feature-list">
      <li class="auth-modal-feature-item">
        <div class="auth-modal-feature-icon">
          <svg class="svg-icon" style="width:15px;height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        </div>
        <div class="auth-modal-feature-text">
          <strong>نوبت‌دهی آنلاین و سریع</strong>
          <span>رزرو مستقیم نوبت ویزیت حضوری و مشاوره آنلاین از پزشکان متخصص.</span>
        </div>
      </li>
      <li class="auth-modal-feature-item">
        <div class="auth-modal-feature-icon">
          <svg class="svg-icon" style="width:15px;height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        </div>
        <div class="auth-modal-feature-text">
          <strong>مشاهده نسخه‌ها و نتایج آزمایش</strong>
          <span>دسترسی دائمی به سوابق پزشکی، داروهای تجویزشده و جواب آزمایش‌ها.</span>
        </div>
      </li>
      <li class="auth-modal-feature-item">
        <div class="auth-modal-feature-icon">
          <svg class="svg-icon" style="width:15px;height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
        </div>
        <div class="auth-modal-feature-text">
          <strong>یادآور هوشمند مصرف دارو و چکاپ</strong>
          <span>دریافت هشدار زمان مصرف داروها و پیگیری مستمر روند بهبودی.</span>
        </div>
      </li>
    </ul>
    <div class="auth-modal-actions">
      <a href="/appointments" class="btn btn-primary" style="width:100%; justify-content:center; font-size:13.5px; gap:8px;">
        <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
        <span>نوبت‌دهی آنلاین و دریافت نوبت سریع مطب</span>
      </a>
      <a href="/download?role=patients" class="btn btn-secondary" style="width:100%; justify-content:center; font-size:12.5px;">دریافت و نصب اپلیکیشن بیمار</a>
      <button type="button" onclick="renderClinicalAuthModalContent('select')" class="auth-card-link" style="margin-top:4px; color:var(--text-secondary);">
        ← بازگشت به صفحه انتخاب نقش
      </button>
    </div>
  `;

  const doctorBody = `
    <div style="margin-bottom:10px;">
      <span style="display:inline-flex; align-items:center; gap:6px; font-size:11.5px; font-weight:800; color:var(--brand-emerald-vital); background:rgba(5,150,105,0.1); padding:4px 10px; border-radius:9999px;">
        ویژه پزشکان، کلینیک‌ها و کادر درمان
      </span>
      <h4 style="font-size:16.5px; font-weight:900; color:var(--text-pure); margin:10px 0 6px;">سامانه مدیریت مطب و پرونده الکترونیک (EMR)</h4>
      <p style="font-size:12.5px; color:var(--text-secondary); line-height:1.7; margin:0;">
        مدیریت هوشمند مطب، پرونده‌های بالینی بیماران و ارتباط حرفه‌ای با مراجعان:
      </p>
    </div>
    <ul class="auth-modal-feature-list">
      <li class="auth-modal-feature-item">
        <div class="auth-modal-feature-icon">
          <svg class="svg-icon" style="width:15px;height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
        </div>
        <div class="auth-modal-feature-text">
          <strong>پرونده الکترونیک بیماران (EMR)</strong>
          <span>ثبت سریع شرح‌حال، نسخه‌نویسی دیجیتال و آرشیو ابری مدارک بالینی هر بیمار.</span>
        </div>
      </li>
      <li class="auth-modal-feature-item">
        <div class="auth-modal-feature-icon">
          <svg class="svg-icon" style="width:15px;height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div class="auth-modal-feature-text">
          <strong>باشگاه بیماران و CRM پزشکی</strong>
          <span>ارسال پیامک خودکار یادآور نوبت، پیگیری پس از درمان و افزایش رضایت مراجعین.</span>
        </div>
      </li>
      <li class="auth-modal-feature-item">
        <div class="auth-modal-feature-icon">
          <svg class="svg-icon" style="width:15px;height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        </div>
        <div class="auth-modal-feature-text">
          <strong>مدیریت مالی و پذیرش هوشمند مطب</strong>
          <span>نوبت‌دهی یکپارچه منشی، گزارش‌های دقیق درآمدی و کاهش بار تلفنی مطب.</span>
        </div>
      </li>
    </ul>
    <div class="auth-modal-actions">
      <a href="https://app.pezeshk-on.ir/" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="width:100%; justify-content:center; font-size:13.5px; gap:8px;">
        <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
        <span>ورود به پنل مطب (app.pezeshk-on.ir) ↗</span>
      </a>
      <a href="https://app.pezeshk-on.ir/demo/doctor" target="_blank" rel="noopener noreferrer" class="btn btn-secondary" style="width:100%; justify-content:center; font-size:12.5px; gap:8px;">
        <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        <span>مشاهده دموی زنده و بدون لاگین پزشک</span>
      </a>
      <a href="/start" style="text-align:center; font-size:11.8px; color:var(--brand-primary); text-decoration:none; margin-top:4px; font-weight:700;">هنوز عضو پزشکآن نشده‌اید؟ ثبت‌نام و دریافت ۳ ماه رایگان ←</a>
      <button type="button" onclick="renderClinicalAuthModalContent('select')" class="auth-card-link" style="margin-top:4px; color:var(--text-secondary);">
        ← بازگشت به صفحه انتخاب نقش
      </button>
    </div>
  `;

  let currentBody = selectBody;
  if (isDoctor) currentBody = doctorBody;
  else if (isPatient) currentBody = patientBody;

  backdrop.innerHTML = `
    <div class="clinical-auth-modal" role="dialog" aria-modal="true" aria-label="راهنمای ورود به سامانه‌های پزشکآن">
      <div class="auth-modal-header">
        <span style="font-size:14px; font-weight:900; color:var(--text-pure);">ورود و ثبت‌نام در سامانه سلامت پزشکآن</span>
        <button type="button" onclick="closeClinicalAuthModal()" style="background:var(--bg-surface-secondary); border:1px solid var(--glass-border); color:var(--text-secondary); width:32px; height:32px; border-radius:8px; cursor:pointer; display:inline-flex; align-items:center; justify-content:center;" title="بستن" aria-label="بستن">
          <svg class="svg-icon" style="width:15px;height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
      <div class="auth-modal-tabs">
        <button type="button" class="auth-modal-tab ${isSelect ? 'active-tab' : ''}" onclick="renderClinicalAuthModalContent('select')">
          <svg class="svg-icon" style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
          <span>انتخاب نقش</span>
        </button>
        <button type="button" class="auth-modal-tab ${isPatient ? 'active-patient' : ''}" onclick="renderClinicalAuthModalContent('patient')">
          <svg class="svg-icon" style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          <span>پنل بیمار</span>
        </button>
        <button type="button" class="auth-modal-tab ${isDoctor ? 'active-doctor' : ''}" onclick="renderClinicalAuthModalContent('doctor')">
          <svg class="svg-icon" style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/><path d="M12 11v6"/><path d="M9 14h6"/></svg>
          <span>پنل پزشک</span>
        </button>
      </div>
      ${currentBody}
    </div>
  `;
}

function openDownloadNotice(platform) {
  const platformNames = {
    'patient-apk': 'نسخه مستقیم اندروید (APK)',
    'patient-pwa': 'وب‌اپلیکیشن PWA آیفون',
    'bazaar': 'کافه‌بازار',
    'myket': 'مایکت',
    'doctor-win': 'نسخه ویندوز مدیریت مطب',
    'doctor-apk': 'اپلیکیشن همراه پزشک'
  };
  const name = platformNames[platform] || 'اپلیکیشن سلامت دیجیتال';
  showClinicalToast(
    `درخواست دریافت ${name}`,
    'بسته نصب نسخه ۲.۴.۰ در حال آماده‌سازی و همگام‌سازی نهایی روی سرورهای توزیع است و به زودی به صورت مستقیم فعال می‌شود.'
  );
}

function openDirectInstallNotice(type) {
  let label = 'بسته نصب مستقیم اپلیکیشن';
  if (type === 'patients') label = 'بسته نصب مستقیم اپلیکیشن ویژه مراجعان';
  else if (type === 'doctors') label = 'بسته نصب مستقیم سامانه و اپلیکیشن پزشکان';
  else if (type === 'android') label = 'بسته نصب مستقیم اندروید (APK)';
  else if (type === 'windows') label = 'بسته نصب مستقیم نسخه ویندوز مطب';
  else if (type === 'ios') label = 'وب‌اپلیکیشن پیش‌رونده آیفون (PWA)';
  
  showClinicalToast(
    `نصب مستقیم: ${label}`,
    'فایل اجرایی و بسته نصب در حال آپلود و اعتبارسنجی امنیتی روی سرور اختصاصی است و به زودی جهت دانلود مستقیم فعال خواهد شد.'
  );
}

// 8.5. Download Page Role Switcher (همه نسخه‌ها / مراجعان / پزشکان)
function filterDownloadByRole(role, pushUrl = true) {
  const validRole = (role === 'patients' || role === 'doctors') ? role : 'all';

  document.querySelectorAll('.download-role-tab').forEach(btn => {
    const r = btn.getAttribute('data-role');
    btn.classList.toggle('active', r === validRole);
    btn.setAttribute('aria-selected', r === validRole ? 'true' : 'false');
  });

  const patientBox = document.getElementById('directInstallPatients');
  const doctorBox = document.getElementById('directInstallDoctors');
  const patientSec = document.getElementById('download-patients-section');
  const doctorSec = document.getElementById('download-doctors-section');
  const guideSec = document.getElementById('download-guide-section');
  const doctorCtaSec = document.getElementById('download-doctor-cta-section');
  const dualInstallGrid = document.getElementById('directInstallDualGrid');

  if (patientBox) {
    patientBox.style.display = (validRole === 'all' || validRole === 'patients') ? 'block' : 'none';
  }
  if (doctorBox) {
    doctorBox.style.display = (validRole === 'all' || validRole === 'doctors') ? 'block' : 'none';
  }
  if (dualInstallGrid) {
    dualInstallGrid.classList.toggle('single-role-mode', validRole !== 'all');
  }
  if (patientSec) {
    patientSec.style.display = (validRole === 'all' || validRole === 'patients') ? 'block' : 'none';
  }
  if (doctorSec) {
    doctorSec.style.display = (validRole === 'all' || validRole === 'doctors') ? 'block' : 'none';
  }
  if (guideSec) {
    guideSec.style.display = (validRole === 'all' || validRole === 'patients') ? 'block' : 'none';
  }
  if (doctorCtaSec) {
    doctorCtaSec.style.display = (validRole === 'all' || validRole === 'doctors') ? 'block' : 'none';
  }

  if (pushUrl && window.history && window.history.replaceState) {
    const url = new URL(window.location.href);
    if (validRole === 'all') {
      url.searchParams.delete('role');
    } else {
      url.searchParams.set('role', validRole);
    }
    window.history.replaceState({}, '', url.pathname + url.search);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('.download-role-switcher')) {
    const params = new URLSearchParams(window.location.search);
    const roleParam = params.get('role');
    if (roleParam === 'patients' || roleParam === 'patient' || roleParam === 'user') {
      filterDownloadByRole('patients', false);
    } else if (roleParam === 'doctors' || roleParam === 'doctor') {
      filterDownloadByRole('doctors', false);
    } else {
      filterDownloadByRole('all', false);
    }
  }
});


// 9. Axon-Style Header Dropdown & Mobile Accordion Controllers
function toggleDesktopDropdown(event, dropdownId) {
  if (event) {
    event.stopPropagation();
  }
  const target = document.getElementById(dropdownId);
  if (!target) return;
  const wasOpen = target.classList.contains('is-open');
  document.querySelectorAll('.nav-dropdown.is-open').forEach(el => {
    el.classList.remove('is-open');
    const btn = el.querySelector('.nav-dropdown-trigger');
    if (btn) btn.setAttribute('aria-expanded', 'false');
  });
  if (!wasOpen) {
    target.classList.add('is-open');
    const btn = target.querySelector('.nav-dropdown-trigger');
    if (btn) btn.setAttribute('aria-expanded', 'true');
  }
}

function toggleDrawerNavAccordion(accId) {
  const target = document.getElementById(accId);
  if (!target) return;
  const wasOpen = target.classList.contains('is-open');
  document.querySelectorAll('.drawer-accordion').forEach(el => {
    el.classList.remove('is-open');
  });
  if (!wasOpen) {
    target.classList.add('is-open');
  }
}

document.addEventListener('click', (e) => {
  if (!e.target || !e.target.closest || !e.target.closest('.nav-dropdown')) {
    document.querySelectorAll('.nav-dropdown.is-open').forEach(el => {
      el.classList.remove('is-open');
      const btn = el.querySelector('.nav-dropdown-trigger');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    });
  }
});



// ==============================================================================
// Universal Dynamic Site Images Hydration & Customizer
// ==============================================================================
(function() {
  function applySitePageImages() {
    let images = window.__SITE_IMAGES__;
    if (!images) {
      try {
        const cached = localStorage.getItem('pezeshkan_site_images');
        if (cached) images = JSON.parse(cached);
      } catch (e) {}
    }

    if (!images) {
      fetch('/api/site-images')
        .then(res => res.json())
        .then(list => {
          if (Array.isArray(list)) {
            const map = {};
            list.forEach(item => { if (item.key) map[item.key] = item.currentUrl || item.defaultUrl; });
            window.__SITE_IMAGES__ = map;
            try { localStorage.setItem('pezeshkan_site_images', JSON.stringify(map)); } catch (e) {}
            applyImageMap(map);
          }
        })
        .catch(() => {});
      return;
    }

    applyImageMap(images);
  }

  function applyImageMap(map) {
    if (!map || typeof map !== 'object') return;

    // 1. Data slot attributes: [data-img-slot="key"]
    document.querySelectorAll('[data-img-slot]').forEach(el => {
      const slot = el.getAttribute('data-img-slot');
      if (slot && map[slot]) {
        if (el.tagName === 'IMG') el.src = map[slot];
        else el.style.backgroundImage = `url("${map[slot]}")`;
      }
    });

    // 2. Specific known site slots:
    if (map.site_logo) {
      document.querySelectorAll('.brand-logo-emblem img, .nav-logo img, [data-img-slot="site_logo"]').forEach(el => {
        el.src = map.site_logo;
      });
    }
    if (map.footer_logo) {
      document.querySelectorAll('.footer-brand-emblem img, [data-img-slot="footer_logo"]').forEach(el => {
        el.src = map.footer_logo;
      });
    }
    if (map.home_vital_dial) {
      const vitalEl = document.getElementById('vital');
      if (vitalEl) vitalEl.src = map.home_vital_dial;
    }
    if (map.favicon_icon) {
      document.querySelectorAll('link[rel="apple-touch-icon"], link[rel="icon"]').forEach(el => {
        el.href = map.favicon_icon;
      });
    }
    if (map.og_image) {
      const ogEl = document.querySelector('meta[property="og:image"]');
      if (ogEl) ogEl.setAttribute('content', map.og_image);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applySitePageImages);
  } else {
    applySitePageImages();
  }
  window.refreshSitePageImages = applySitePageImages;
})();


// Dynamic Magazine Articles on Homepage (Shows ONLY when published articles exist)
(function() {
  function initHomeMagazine() {
    const section = document.getElementById('home-magazine-section');
    const grid = document.getElementById('home-magazine-grid');
    if (!section || !grid) return;

    fetch('/api/articles')
      .then(res => {
        if (!res.ok) throw new Error('Network error');
        return res.json();
      })
      .then(articles => {
        if (!Array.isArray(articles)) return;
        const published = articles.filter(a => !a.status || a.status === 'published').slice(0, 3);
        if (published.length === 0) {
          section.style.display = 'none';
          grid.innerHTML = '';
          return;
        }

        let html = '';
        published.forEach(art => {
          const slug = encodeURIComponent(art.slug || art.id || '');
          const title = escapeHtml(art.title || '');
          const summary = escapeHtml(art.summary || '');
          const img = art.image || 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=600&q=80';
          const alt = escapeHtml(art.imageAlt || art.title || '');
          const cat = escapeHtml(art.categoryName || art.tag || 'مجله سلامت');

          html += `
            <div class="panel-card" style="padding:0; overflow:hidden;">
              <img src="${img}" alt="${alt}" width="600" height="180" loading="lazy" decoding="async" style="width:100%; height:180px; object-fit:cover;">
              <div style="padding:20px;">
                <span style="font-size:11px; background:var(--signal-cyan-bg); color:var(--signal-cyan); border:1px solid var(--signal-cyan-border); padding:2px 8px; border-radius:4px; font-weight:700;">${cat}</span>
                <h3 style="font-size:15.5px; font-weight:800; margin:10px 0 6px;"><a href="/mag/${slug}">${title}</a></h3>
                <p style="font-size:12.5px; color:var(--text-muted); line-height:1.6;">${summary}</p>
              </div>
            </div>
          `;
        });

        grid.innerHTML = html;
        section.style.display = 'block';
      })
      .catch(() => {
        if (!grid.children.length) {
          section.style.display = 'none';
        }
      });
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHomeMagazine);
  } else {
    initHomeMagazine();
  }
  window.refreshHomeMagazine = initHomeMagazine;
})();
