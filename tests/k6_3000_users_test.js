import http from 'k6/http';
import { check, sleep, group } from 'k6';

// 3,000 Concurrent Users Stress & Load Test Specification
// Simulates 3,000 active concurrent users across marketing portal, magazine, directory, and lead workflows.
export const options = {
  stages: [
    { duration: '15s', target: 500 },   // Warmup to 500 VUs
    { duration: '20s', target: 1500 },  // Scale to 1,500 VUs
    { duration: '25s', target: 3000 },  // Scale to 3,000 VUs
    { duration: '30s', target: 3000 },  // Sustain 3,000 Concurrent Users
    { duration: '15s', target: 0 },     // Graceful ramp-down
  ],
  thresholds: {
    http_req_failed: ['rate<0.02'],     // Error rate must remain under 2%
    http_req_duration: ['p(95)<2500'],  // 95% of requests under 2.5s
  },
  batchPerHost: 1,
  noConnectionReuse: false,
};

const CLUSTER_TARGETS = [
  'http://127.0.0.1:3000',
  'http://127.0.0.1:3001',
  'http://127.0.0.1:3002',
  'http://127.0.0.1:3003',
];

function getTargetUrl() {
  if (__ENV.TARGET_URL) {
    return __ENV.TARGET_URL;
  }
  return CLUSTER_TARGETS[__VU % CLUSTER_TARGETS.length];
}

const DEFAULT_HEADERS = {
  'Connection': 'keep-alive',
  'User-Agent': 'k6-load-testing-agent/3000-VUs',
};

export default function () {
  const BASE_URL = getTargetUrl();
  const rand = Math.random();

  // 1. Portal Pages & Public Browsing (35% of users)
  if (rand < 0.35) {
    group('Portal Browsing', function () {
      const res1 = http.get(`${BASE_URL}/`, { headers: DEFAULT_HEADERS, tags: { name: 'Home' } });
      check(res1, { 'home status 200': (r) => r.status === 200 });

      sleep(1.0);

      const res2 = http.get(`${BASE_URL}/packages`, { headers: DEFAULT_HEADERS, tags: { name: 'Packages' } });
      check(res2, { 'packages status 200': (r) => r.status === 200 });

      sleep(1.0);

      const res3 = http.get(`${BASE_URL}/appointments`, { headers: DEFAULT_HEADERS, tags: { name: 'Appointments' } });
      check(res3, { 'appointments status 200': (r) => r.status === 200 });
    });
  }
  // 2. Magazine & Health Content (30% of users)
  else if (rand < 0.65) {
    group('Magazine Hub', function () {
      const res1 = http.get(`${BASE_URL}/mag`, { headers: DEFAULT_HEADERS, tags: { name: 'Mag_Home' } });
      check(res1, { 'mag status 200': (r) => r.status === 200 });

      sleep(1.0);

      const res2 = http.get(`${BASE_URL}/api/articles`, { headers: DEFAULT_HEADERS, tags: { name: 'API_Articles' } });
      check(res2, {
        'articles status 200': (r) => r.status === 200,
        'articles has data': (r) => r.body && r.body.length > 10,
      });

      sleep(1.0);

      const res3 = http.get(`${BASE_URL}/mag/newsletter`, { headers: DEFAULT_HEADERS, tags: { name: 'Mag_Newsletter' } });
      check(res3, { 'newsletter status 200': (r) => r.status === 200 });
    });
  }
  // 3. Clinical Public APIs (20% of users)
  else if (rand < 0.85) {
    group('Clinical APIs', function () {
      const resDir = http.get(`${BASE_URL}/api/v1/clinic/public/directory/`, {
        headers: DEFAULT_HEADERS,
        tags: { name: 'API_Clinic_Directory' },
      });
      check(resDir, {
        'directory status 200': (r) => r.status === 200,
        'directory has results': (r) => r.body && r.body.includes('results'),
      });

      sleep(0.5);

      const resPlans = http.get(`${BASE_URL}/api/v1/platform/public/plans/`, {
        headers: DEFAULT_HEADERS,
        tags: { name: 'API_Platform_Plans' },
      });
      check(resPlans, {
        'plans status 200': (r) => r.status === 200,
        'plans has items': (r) => r.body && r.body.includes('starter'),
      });

      sleep(0.5);

      const resDocs = http.get(`${BASE_URL}/api/doctors`, { headers: DEFAULT_HEADERS, tags: { name: 'API_Doctors' } });
      check(resDocs, { 'doctors status 200': (r) => r.status === 200 });

      sleep(0.5);

      const resPillars = http.get(`${BASE_URL}/api/pillars`, { headers: DEFAULT_HEADERS, tags: { name: 'API_Pillars' } });
      check(resPillars, { 'pillars status 200': (r) => r.status === 200 });
    });
  }
  // 4. Onboarding Lead Submission (15% of users - Write Load)
  else {
    group('Onboarding & Leads Write', function () {
      const payload = JSON.stringify({
        doctorName: `دکتر تست ${__VU}-${__ITER}`,
        mobile: `0912${Math.floor(1000000 + Math.random() * 9000000)}`,
        specialty: 'مغز و اعصاب',
        patientsVolume: '۲۰ تا ۶۰ بیمار',
        challenges: ['قلم نوری', 'کاهش لغو نوبت'],
        clinicAddress: 'تهران، سعادت‌آباد',
        chosenPlan: 'pro',
      });

      const params = {
        headers: Object.assign({}, DEFAULT_HEADERS, { 'Content-Type': 'application/json' }),
        tags: { name: 'POST_Lead_Start' },
      };

      const res = http.post(`${BASE_URL}/api/v1/leads/start/`, payload, params);
      check(res, {
        'lead created 201 or 200': (r) => r.status === 201 || r.status === 200,
        'has redirect_url': (r) => r.body && r.body.includes('redirect_url'),
      });
    });
  }

  sleep(1.5);
}
