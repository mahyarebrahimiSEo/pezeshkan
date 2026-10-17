import glob

portal_files = sorted(glob.glob('portal/*.html'))
root_files = [f.replace('portal\\', '') for f in portal_files]

all_files = portal_files + root_files

print(f"Total target files to check: {len(all_files)}")

failed = 0
for fpath in all_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    checks = {
        'site-header': '<header class="site-header">' in c,
        'brand-wrap': 'brand-wrap' in c,
        'main-nav': '<ul class="main-nav">' in c,
        'download-nav': 'href="/download"' in c,
        'mag-nav': 'href="/mag"' in c,
        'theme-toggle': 'id="themeToggleBtn"' in c,
        'auth-capsule': 'header-auth-capsule' in c,
        'auth-patient': 'auth-patient' in c,
        'auth-doctor': 'auth-doctor' in c,
        'mobile-toggle': 'mobile-menu-toggle' in c,
        'mobile-drawer': 'id="mobileNavDrawer"' in c,
    }

    missing = [k for k, v in checks.items() if not v]
    if missing:
        print(f"FAILED: {fpath} - Missing: {missing}")
        failed += 1
    else:
        print(f"OK: {fpath}")

print(f"\nSummary: {len(all_files) - failed}/{len(all_files)} passed.")
