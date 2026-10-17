# -*- coding: utf-8 -*-
"""
Builder for WordPress-grade Pezeshkan CMS Studio (mag/admin.html)
"""
import os
import json

BASE_DIR = r"e:\antigravity\pezeshkan_design"
MAG_DIR = os.path.join(BASE_DIR, "mag")

with open(os.path.join(MAG_DIR, "content", "pillars.json"), encoding="utf-8") as f:
    pillars_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "doctors.json"), encoding="utf-8") as f:
    doctors_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "articles.json"), encoding="utf-8") as f:
    articles_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "settings.json"), encoding="utf-8") as f:
    settings_data = json.load(f)

media_file = os.path.join(MAG_DIR, "content", "media.json")
if os.path.exists(media_file):
    with open(media_file, encoding="utf-8") as f:
        media_data = json.load(f)
else:
    media_data = []

pillars_json = json.dumps(pillars_data, ensure_ascii=False)
doctors_json = json.dumps(doctors_data, ensure_ascii=False)
articles_json = json.dumps(articles_data, ensure_ascii=False)
settings_json = json.dumps(settings_data, ensure_ascii=False)
media_json = json.dumps(media_data, ensure_ascii=False)

# Build HTML content
part1_head = '''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>پیشخوان مدیریت محتوای بالینی مجله سلامت پزشکآن | استودیوی تحریریه و سئو</title>
  <meta name="robots" content="noindex, nofollow, noarchive">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="alternate icon" href="/favicon.ico">
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Editor Engine Core -->
  <script src="public/tiptap-bundle.min.js"></script>

  <style>
    @font-face {
      font-family: 'Vazirmatn';
      src: url('/fonts/Vazirmatn-Regular.woff2') format('woff2');
      font-weight: 400;
      font-style: normal;
      font-display: swap;
    }
    @font-face {
      font-family: 'Vazirmatn';
      src: url('/fonts/Vazirmatn-Medium.woff2') format('woff2');
      font-weight: 500;
      font-style: normal;
      font-display: swap;
    }
    @font-face {
      font-family: 'Vazirmatn';
      src: url('/fonts/Vazirmatn-Bold.woff2') format('woff2');
      font-weight: 700;
      font-style: normal;
      font-display: swap;
    }

    :root {
      --font-sans: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --bg-page: #F8FAFC;
      --bg-surface: #FFFFFF;
      --border-color: #E2E8F0;
      --border-subtle: #F1F5F9;
      --border-focus: #0284C7;
      --text-main: #0F172A;
      --text-muted: #64748B;
      --text-sub: #334155;
      --primary: #0284C7;
      --primary-hover: #0369A1;
      --primary-light: #E0F2FE;
      --wp-sidebar-bg: #0F172A;
      --wp-sidebar-hover: #1E293B;
      --wp-sidebar-active: #0284C7;
      --wp-sidebar-text: #E2E8F0;
      --accent-emerald: #059669;
      --accent-amber: #D97706;
      --accent-rose: #E11D48;
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: var(--font-sans);
    }

    body {
      background: var(--bg-page);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }

    /* Top Admin Bar */
    .wp-admin-bar {
      background: #0F172A;
      color: #F8FAFC;
      height: 50px;
      padding: 0 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 2px 8px rgba(0,0,0,0.18);
    }

    .admin-bar-right, .admin-bar-left {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .admin-bar-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 14px;
      font-weight: 800;
      color: #FFFFFF;
      text-decoration: none;
    }

    .brand-cross-icon {
      width: 28px;
      height: 28px;
      background: linear-gradient(135deg, #0284C7, #0D9488);
      border-radius: 7px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: #FFFFFF;
      box-shadow: 0 2px 6px rgba(2, 132, 199, 0.4);
    }

    .admin-bar-link {
      color: #94A3B8;
      text-decoration: none;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      border-radius: 6px;
      transition: all 0.12s ease;
      cursor: pointer;
    }
    .admin-bar-link:hover {
      color: #FFFFFF;
      background: #1E293B;
    }

    .btn-new-post-quick {
      background: #0284C7;
      color: #FFFFFF !important;
      font-weight: 700;
    }
    .btn-new-post-quick:hover {
      background: #0369A1 !important;
    }

    .user-profile-bar {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13px;
      color: #E2E8F0;
    }

    .user-avatar-circle {
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background: #0284C7;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 12px;
    }

    /* Layout Wrapper */
    .admin-layout-wrapper {
      display: flex;
      flex: 1;
      min-height: calc(100vh - 50px);
    }

    /* Sidebar */
    .wp-sidebar {
      width: 250px;
      background: var(--wp-sidebar-bg);
      color: var(--wp-sidebar-text);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      padding: 16px 0;
      border-left: 1px solid #1E293B;
    }

    .sidebar-nav-group {
      list-style: none;
      padding: 0 8px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .sidebar-nav-item {
      position: relative;
    }

    .sidebar-nav-link {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 14px;
      color: #94A3B8;
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 600;
      border-radius: 8px;
      transition: all 0.15s ease;
      cursor: pointer;
    }

    .sidebar-nav-link:hover {
      color: #FFFFFF;
      background: var(--wp-sidebar-hover);
    }

    .sidebar-nav-link.active {
      color: #FFFFFF;
      background: var(--wp-sidebar-active);
      font-weight: 700;
      box-shadow: 0 2px 6px rgba(2, 132, 199, 0.35);
    }

    .nav-count-badge {
      margin-right: auto;
      background: #1E293B;
      color: #94A3B8;
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 12px;
      font-weight: 700;
    }
    .sidebar-nav-link.active .nav-count-badge {
      background: rgba(255, 255, 255, 0.25);
      color: #FFFFFF;
    }

    .sidebar-footer-info {
      margin-top: auto;
      padding: 16px 20px;
      font-size: 11.5px;
      color: #64748B;
      border-top: 1px solid #1E293B;
      line-height: 1.8;
    }

    /* Main Content Area */
    .admin-main-canvas {
      flex: 1;
      background: var(--bg-page);
      padding: 28px 36px;
      overflow-y: auto;
      max-width: 1440px;
    }

    .tab-section {
      display: none;
    }
    .tab-section.active {
      display: block;
      animation: fadeIn 0.15s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Section Headers */
    .section-header-box {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
    }

    .section-title-wrap h2 {
      font-size: 20px;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .section-title-wrap p {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .header-actions-group {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 600;
      border: none;
      cursor: pointer;
      transition: all 0.12s ease;
      text-decoration: none;
    }

    .btn-primary {
      background: var(--primary);
      color: #FFFFFF;
      box-shadow: 0 2px 4px rgba(2, 132, 199, 0.25);
    }
    .btn-primary:hover {
      background: var(--primary-hover);
      box-shadow: 0 4px 8px rgba(2, 132, 199, 0.35);
    }

    .btn-secondary {
      background: #FFFFFF;
      color: var(--text-sub);
      border: 1px solid var(--border-color);
    }
    .btn-secondary:hover {
      background: #F1F5F9;
      color: var(--text-main);
    }

    .btn-success {
      background: var(--accent-emerald);
      color: #FFFFFF;
    }
    .btn-success:hover {
      background: #047857;
    }

    .btn-danger {
      background: #FEE2E2;
      color: var(--accent-rose);
      border: 1px solid #FECDD3;
    }
    .btn-danger:hover {
      background: #FEE2E2;
      color: #BE123C;
    }

    .btn-preview {
      background: #F0FDF4;
      color: #166534;
      border: 1px solid #BBF7D0;
    }
    .btn-preview:hover {
      background: #DCFCE7;
    }

    .btn-clean {
      background: #F5F3FF;
      color: #6D28D9;
      border: 1px solid #DDD6FE;
    }
    .btn-clean:hover {
      background: #EDE9FE;
    }

    /* Cards */
    .card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 24px;
      box-shadow: var(--shadow-sm);
      margin-bottom: 24px;
    }

    /* Welcome Card */
    .welcome-card {
      background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
      color: #FFFFFF;
      border-radius: var(--radius-lg);
      padding: 28px 32px;
      margin-bottom: 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
      box-shadow: var(--shadow-md);
    }

    .welcome-text h3 {
      font-size: 19px;
      font-weight: 800;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .admin-role-badge {
      background: rgba(2, 132, 199, 0.3);
      color: #38BDF8;
      border: 1px solid rgba(56, 189, 248, 0.3);
      font-size: 11px;
      font-weight: 700;
      padding: 2px 10px;
      border-radius: 12px;
    }

    .welcome-text p {
      font-size: 13.5px;
      color: #94A3B8;
      line-height: 1.7;
      max-width: 680px;
    }

    /* Metrics Grid */
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 20px;
      margin-bottom: 28px;
    }

    .metric-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      box-shadow: var(--shadow-sm);
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .metric-icon-wrap {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      flex-shrink: 0;
    }

    .metric-info h4 {
      font-size: 12.5px;
      color: var(--text-muted);
      font-weight: 600;
      margin-bottom: 4px;
    }

    .metric-num {
      font-size: 24px;
      font-weight: 900;
      color: var(--text-main);
    }

    /* WordPress Style Table */
    .wp-table-wrap {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      overflow: hidden;
      box-shadow: var(--shadow-sm);
    }

    .wp-table-filters {
      padding: 12px 20px;
      background: #FAFBFD;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }

    .status-pills-list {
      display: flex;
      align-items: center;
      gap: 6px;
      list-style: none;
    }

    .status-pill {
      font-size: 12.5px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 6px;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.12s ease;
    }
    .status-pill:hover {
      background: #E2E8F0;
      color: var(--text-main);
    }
    .status-pill.active {
      background: #0284C7;
      color: #FFFFFF;
    }

    .wp-table {
      width: 100%;
      border-collapse: collapse;
      text-align: right;
      font-size: 13px;
    }

    .wp-table th {
      background: #FAFBFD;
      color: var(--text-sub);
      font-weight: 700;
      padding: 14px 16px;
      border-bottom: 1px solid var(--border-color);
      white-space: nowrap;
    }

    .wp-table td {
      padding: 14px 16px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-sub);
      vertical-align: middle;
    }

    .wp-table tr:hover {
      background: #F8FAFC;
    }

    .post-title-cell {
      font-weight: 700;
      color: var(--text-main);
      font-size: 14px;
    }

    .post-row-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 11.5px;
      color: var(--text-muted);
      margin-top: 6px;
      visibility: hidden;
    }
    .wp-table tr:hover .post-row-actions {
      visibility: visible;
    }

    .post-action-btn {
      color: var(--primary);
      text-decoration: none;
      cursor: pointer;
      font-weight: 600;
    }
    .post-action-btn:hover {
      text-decoration: underline;
    }
    .post-action-btn.danger {
      color: var(--accent-rose);
    }

    /* Badges */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 700;
    }
    .badge-published {
      background: #DCFCE7;
      color: #15803D;
    }
    .badge-draft {
      background: #FEF3C7;
      color: #B45309;
    }
    .badge-trash {
      background: #FEE2E2;
      color: #B91C1C;
    }

    .badge-seo-score {
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11.5px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .seo-good {
      background: #DCFCE7;
      color: #15803D;
    }
    .seo-ok {
      background: #FEF3C7;
      color: #B45309;
    }
    .seo-bad {
      background: #FEE2E2;
      color: #B91C1C;
    }

    /* Forms */
    .form-group {
      margin-bottom: 16px;
    }

    .form-group label {
      display: block;
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-sub);
      margin-bottom: 6px;
    }

    .form-control {
      width: 100%;
      padding: 8px 12px;
      font-size: 13.5px;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      background: #FFFFFF;
      color: var(--text-main);
      outline: none;
      transition: border-color 0.12s ease;
    }
    .form-control:focus {
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.12);
    }

    /* 2-Column Editor Workspace */
    .article-editor-workspace {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 340px;
      gap: 28px;
      align-items: start;
    }

    /* Paper Document Card */
    .editor-paper-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .editor-paper-header {
      padding: 24px 32px 18px 32px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .input-title-h1 {
      width: 100%;
      border: none;
      outline: none;
      font-size: 24px;
      font-weight: 900;
      color: var(--text-main);
      padding: 6px 0;
      line-height: 1.4;
      background: transparent;
    }
    .input-title-h1::placeholder {
      color: #94A3B8;
    }

    .input-lead-box {
      margin-top: 14px;
      background: var(--bg-page);
      border-right: 4px solid var(--primary);
      border-radius: var(--radius-sm);
      padding: 12px 16px;
    }
    .input-lead-box label {
      display: block;
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-muted);
      margin-bottom: 6px;
    }
    .textarea-lead {
      width: 100%;
      border: none;
      outline: none;
      background: transparent;
      font-size: 13.5px;
      color: var(--text-sub);
      line-height: 1.7;
      resize: vertical;
      min-height: 60px;
    }

    /* Sticky Formatting Toolbar */
    .editorial-toolbar-sticky {
      position: sticky;
      top: 50px;
      z-index: 50;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border-color);
      padding: 8px 24px;
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }

    .toolbar-cluster {
      display: flex;
      align-items: center;
      gap: 2px;
      padding-left: 8px;
      border-left: 1px solid var(--border-color);
    }
    .toolbar-cluster:last-child {
      border-left: none;
      padding-left: 0;
    }

    .tbtn {
      width: 32px;
      height: 32px;
      border-radius: 6px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-sub);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.1s ease;
    }
    .tbtn:hover {
      background: #F1F5F9;
      color: var(--text-main);
    }
    .tbtn.active {
      background: var(--primary-light);
      color: var(--primary);
      border-color: rgba(2, 132, 199, 0.3);
    }

    .tbtn-pill {
      height: 30px;
      padding: 0 10px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 700;
      border: 1px solid transparent;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.12s ease;
    }
    .tbtn-warning {
      background: #FEF3C7;
      color: #92400E;
      border-color: #FCD34D;
    }
    .tbtn-advice {
      background: #DCFCE7;
      color: #166534;
      border-color: #86EFAC;
    }
    .tbtn-protocol {
      background: #E0F2FE;
      color: #075985;
      border-color: #7DD3FC;
    }
    .tbtn-media {
      background: #F0FDF4;
      color: #15803D;
      border-color: #86EFAC;
      font-weight: 800;
    }

    /* Editor Typing Canvas */
    .editor-canvas-body {
      padding: 24px 32px;
      min-height: 480px;
    }

    .ProseMirror {
      outline: none;
      font-size: 15.5px;
      line-height: 2.0;
      color: #1E293B;
      min-height: 440px;
    }
    .ProseMirror p {
      margin-bottom: 16px;
    }
    .ProseMirror h2 {
      font-size: 20px;
      font-weight: 800;
      color: var(--text-main);
      margin: 28px 0 14px 0;
      border-right: 4px solid var(--primary);
      padding-right: 12px;
    }
    .ProseMirror h3 {
      font-size: 17px;
      font-weight: 700;
      color: var(--text-main);
      margin: 22px 0 10px 0;
    }
    .ProseMirror ul, .ProseMirror ol {
      margin: 14px 28px;
    }
    .ProseMirror li {
      margin-bottom: 8px;
    }
    .ProseMirror blockquote {
      border-right: 4px solid #CBD5E1;
      padding: 8px 18px;
      margin: 18px 0;
      color: #475569;
      font-style: italic;
      background: #F8FAFC;
      border-radius: 4px;
    }
    .ProseMirror hr {
      border: none;
      border-top: 2px dashed #E2E8F0;
      margin: 28px 0;
    }
    .ProseMirror figure.clinical-img-figure {
      margin: 24px auto;
      text-align: center;
      background: #F8FAFC;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 10px;
      max-width: 100%;
    }
    .ProseMirror figure.clinical-img-figure img {
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      display: block;
      margin: 0 auto;
    }
    .ProseMirror figcaption.clinical-img-caption {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 8px;
      font-weight: 600;
    }
    .ProseMirror .clinical-callout {
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin: 20px 0;
      border-right: 5px solid;
    }
    .ProseMirror .clinical-callout.warning {
      background: #FFFBEB;
      border-color: #F59E0B;
      color: #78350F;
    }
    .ProseMirror .clinical-callout.advice {
      background: #F0FDF4;
      border-color: #10B981;
      color: #064E3B;
    }
    .ProseMirror .clinical-callout.protocol {
      background: #F0F9FF;
      border-color: #0284C7;
      color: #0C4A6E;
    }
    .ProseMirror .clinical-callout .callout-header {
      font-weight: 800;
      font-size: 13.5px;
      margin-bottom: 6px;
    }

    /* Editor Status Strip */
    .editor-status-strip {
      padding: 12px 24px;
      background: #FAFBFD;
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-muted);
    }
    .editor-status-strip .status-group {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    /* Side Inspector Cards */
    .editor-inspector-column {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .inspector-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      box-shadow: var(--shadow-sm);
    }

    .inspector-card-title {
      font-size: 13px;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 14px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .hero-preview-box {
      width: 100%;
      height: 140px;
      border: 1px dashed var(--border-color);
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      background: #FAFBFD;
      margin-top: 10px;
      position: relative;
    }
    .hero-preview-box img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    /* ================= Comprehensive SEO Suite Box ================= */
    .seo-suite-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      margin-top: 24px;
      overflow: hidden;
    }

    .seo-suite-header {
      background: #FAFBFD;
      border-bottom: 1px solid var(--border-color);
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .seo-suite-tabs {
      display: flex;
      align-items: center;
      gap: 8px;
      list-style: none;
    }

    .seo-tab-btn {
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.12s ease;
    }
    .seo-tab-btn:hover {
      background: #E2E8F0;
      color: var(--text-main);
    }
    .seo-tab-btn.active {
      background: #0284C7;
      color: #FFFFFF;
    }

    .seo-suite-body {
      padding: 24px;
    }

    .seo-pane {
      display: none;
    }
    .seo-pane.active {
      display: block;
    }

    /* Google SERP Card Preview */
    .google-serp-preview {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 18px 22px;
      margin-bottom: 24px;
      max-width: 650px;
      font-family: Roboto, -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    }
    .serp-device-toggle {
      display: flex;
      gap: 8px;
      margin-bottom: 14px;
    }
    .serp-device-btn {
      padding: 4px 10px;
      font-size: 11.5px;
      font-weight: 700;
      border: 1px solid var(--border-color);
      background: #FFFFFF;
      border-radius: 6px;
      cursor: pointer;
    }
    .serp-device-btn.active {
      background: #0F172A;
      color: #FFFFFF;
      border-color: #0F172A;
    }

    .serp-site-info {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
    }
    .serp-favicon {
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: #0284C7;
      color: #FFF;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      font-weight: 800;
    }
    .serp-url-breadcrumb {
      font-size: 12px;
      color: #202124;
      line-height: 1.3;
      direction: ltr;
      text-align: left;
    }
    .serp-url-breadcrumb span {
      color: #5f6368;
    }
    .serp-title-link {
      font-size: 19px;
      color: #1a0dab;
      text-decoration: none;
      font-weight: 500;
      line-height: 1.3;
      display: block;
      margin-bottom: 6px;
      cursor: pointer;
    }
    .serp-title-link:hover {
      text-decoration: underline;
    }
    .serp-snippet-desc {
      font-size: 13.5px;
      color: #4d5156;
      line-height: 1.55;
    }
    .serp-snippet-desc strong {
      color: #202124;
      font-weight: 700;
    }

    /* SEO Progress Bars */
    .seo-progress-track {
      width: 100%;
      height: 6px;
      background: #E2E8F0;
      border-radius: 3px;
      overflow: hidden;
      margin-top: 6px;
    }
    .seo-progress-fill {
      height: 100%;
      width: 0%;
      background: #059669;
      transition: width 0.2s ease, background 0.2s ease;
    }
    .seo-counter-label {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    /* SEO Checklist */
    .seo-checklist-grid {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .seo-check-item {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 12px 16px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
      background: #FAFBFD;
      font-size: 13px;
    }
    .seo-check-icon {
      font-size: 16px;
      line-height: 1;
      margin-top: 2px;
    }
    .seo-check-details strong {
      display: block;
      color: var(--text-main);
      margin-bottom: 3px;
    }
    .seo-check-details p {
      color: var(--text-muted);
      font-size: 12px;
      line-height: 1.5;
    }

    /* FAQ Builder in SEO */
    .faq-builder-item {
      background: #F8FAFC;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      margin-bottom: 12px;
      position: relative;
    }
    .faq-item-delete-btn {
      position: absolute;
      top: 12px;
      left: 12px;
      background: none;
      border: none;
      color: var(--accent-rose);
      cursor: pointer;
      font-size: 14px;
    }

    /* ================= Media Library Tab ================= */
    .media-dropzone {
      border: 2px dashed #CBD5E1;
      border-radius: var(--radius-lg);
      padding: 36px 24px;
      text-align: center;
      background: #F8FAFC;
      cursor: pointer;
      transition: all 0.15s ease;
      margin-bottom: 24px;
    }
    .media-dropzone:hover, .media-dropzone.dragover {
      border-color: var(--primary);
      background: var(--primary-light);
    }
    .dropzone-icon {
      font-size: 38px;
      margin-bottom: 10px;
    }
    .dropzone-text h4 {
      font-size: 15px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 4px;
    }
    .dropzone-text p {
      font-size: 12.5px;
      color: var(--text-muted);
    }

    .media-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 16px;
    }

    .media-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      overflow: hidden;
      cursor: pointer;
      position: relative;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
    }
    .media-card:hover {
      box-shadow: var(--shadow-md);
      border-color: var(--primary);
    }
    .media-card.selected {
      border: 2px solid var(--primary);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.25);
    }

    .media-thumb-wrap {
      width: 100%;
      height: 120px;
      background: #F1F5F9;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }
    .media-thumb-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .media-meta-wrap {
      padding: 8px 10px;
      background: #FFFFFF;
    }
    .media-title-txt {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .media-size-txt {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 2px;
    }

    /* ================= WordPress Media Inserter Modal ================= */
    .media-modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(4px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .media-modal-card {
      background: var(--bg-surface);
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 980px;
      height: 85vh;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-lg);
      overflow: hidden;
    }
    .media-modal-header {
      padding: 16px 24px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #FAFBFD;
    }
    .media-modal-tabs {
      display: flex;
      align-items: center;
      gap: 10px;
      list-style: none;
    }
    .media-tab-btn {
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
    }
    .media-tab-btn.active {
      background: var(--primary);
      color: #FFFFFF;
    }

    .media-modal-body {
      flex: 1;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 300px;
      overflow: hidden;
    }
    .media-modal-content-area {
      padding: 20px;
      overflow-y: auto;
      border-left: 1px solid var(--border-color);
    }
    .media-modal-sidebar-area {
      padding: 20px;
      background: #FAFBFD;
      overflow-y: auto;
    }
    .media-modal-footer {
      padding: 14px 24px;
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #FAFBFD;
    }

    /* Live Preview Modal */
    .preview-modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(4px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .preview-modal-card {
      background: var(--bg-surface);
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 900px;
      height: 90vh;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-lg);
      overflow: hidden;
    }
    .preview-modal-header {
      padding: 14px 24px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #FAFBFD;
    }
    .preview-modal-body {
      flex: 1;
      padding: 32px 48px;
      overflow-y: auto;
      background: #FFFFFF;
      font-size: 15px;
      line-height: 2.0;
    }

    /* Toast */
    .toast-msg {
      position: fixed;
      bottom: 24px;
      left: 24px;
      background: #0F172A;
      color: #FFFFFF;
      padding: 12px 20px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: var(--shadow-lg);
      z-index: 9999;
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      font-size: 13.5px;
      font-weight: 600;
      border: 1px solid #334155;
    }
    .toast-msg.show {
      transform: translateY(0);
      opacity: 1;
    }

    @media (max-width: 1024px) {
      .admin-layout-wrapper {
        flex-direction: column;
      }
      .wp-sidebar {
        width: 100%;
        border-left: none;
        border-bottom: 1px solid #1E293B;
      }
      .article-editor-workspace {
        grid-template-columns: 1fr;
      }
      .media-modal-body {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>

  <!-- Top Admin Bar -->
  <header class="wp-admin-bar">
    <div class="admin-bar-right">
      <a href="javascript:void(0)" onclick="switchTab('dashboard')" class="admin-bar-brand">
        <span class="brand-cross-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
        </span>
        <span>پیشخوان مجله سلامت پزشکآن</span>
      </a>

      <a href="/mag" target="_blank" class="admin-bar-link" title="مشاهده مجله سلامت در پنجره جدید">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        <span>مشاهده مجله ↗</span>
      </a>

      <button type="button" class="btn btn-new-post-quick" onclick="createNewPost()" style="padding: 4px 12px; font-size: 12px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
        <span>نوشته تازه</span>
      </button>

      <button type="button" class="admin-bar-link" onclick="openMediaModal('upload')" style="background:none; border:none;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
        <span>بارگذاری تصویر</span>
      </button>
    </div>

    <div class="admin-bar-left">
      <div class="user-profile-bar">
        <div class="user-avatar-circle">م‌ا</div>
        <span id="barUserName">مهیار ابراهیمی (مدیر ارشد)</span>
      </div>
      <a href="/logout" class="admin-bar-link" title="خروج امن از سیستم">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        <span>خروج</span>
      </a>
    </div>
  </header>

  <div class="admin-layout-wrapper">
    
    <!-- Sidebar Navigation -->
    <aside class="wp-sidebar">
      <ul class="sidebar-nav-group">
        <li class="sidebar-nav-item">
          <a class="sidebar-nav-link active" id="nav-dashboard" onclick="switchTab('dashboard')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="7" height="9" x="3" y="3" rx="1"></rect><rect width="7" height="5" x="14" y="3" rx="1"></rect><rect width="7" height="9" x="14" y="12" rx="1"></rect><rect width="7" height="5" x="3" y="16" rx="1"></rect></svg>
            <span>پیشخوان</span>
          </a>
        </li>
        <li class="sidebar-nav-item">
          <a class="sidebar-nav-link" id="nav-posts" onclick="switchTab('posts')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
            <span>همه نوشته‌ها</span>
            <span class="nav-count-badge" id="sidebarPostCount">۴</span>
          </a>
        </li>
        <li class="sidebar-nav-item">
          <a class="sidebar-nav-link" id="nav-editor" onclick="switchTab('editor')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
            <span>ویرایشگر پیشرفته مقاله</span>
          </a>
        </li>
        <li class="sidebar-nav-item">
          <a class="sidebar-nav-link" id="nav-media" onclick="switchTab('media')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
            <span>کتابخانه رسانه‌ها</span>
            <span class="nav-count-badge" id="sidebarMediaCount">۶</span>
          </a>
        </li>
        <li class="sidebar-nav-item">
          <a class="sidebar-nav-link" id="nav-categories" onclick="switchTab('categories')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
            <span>دپارتمان‌ها و شاخه‌ها</span>
            <span class="nav-count-badge">۹</span>
          </a>
        </li>
        <li class="sidebar-nav-item">
          <a class="sidebar-nav-link" id="nav-doctors" onclick="switchTab('doctors')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            <span>پزشکان و اعضای هیئت علمی</span>
            <span class="nav-count-badge">۵</span>
          </a>
        </li>
        <li class="sidebar-nav-item">
          <a class="sidebar-nav-link" id="nav-seo" onclick="switchTab('seo')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><path d="M11 8v6M8 11h6"/></svg>
            <span>بهینه‌سازی و سئو سایت</span>
          </a>
        </li>
        <li class="sidebar-nav-item">
          <a class="sidebar-nav-link" id="nav-settings" onclick="switchTab('settings')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
            <span>تنظیمات عمومی سایت</span>
          </a>
        </li>
      </ul>

      <div class="sidebar-footer-info">
        <div><strong>نسخه سامانه:</strong> ۳.۵ بالینی و سئو</div>
        <div><strong>محیط:</strong> لوکال‌هاست امن (پورت ۳۰۰۰)</div>
        <div><strong>امنیت:</strong> PBKDF2 + SHA-256 + CSP</div>
      </div>
    </aside>

    <!-- Main Canvas -->
    <main class="admin-main-canvas">
      
      <!-- ================= 1. TAB: DASHBOARD ================= -->
      <section id="tab-dashboard" class="tab-section active">
        
        <div class="welcome-card">
          <div class="welcome-text">
            <h3>
              خوش‌آمدید به استودیوی مدیریت محتوای مجله سلامت پزشکآن!
              <span class="admin-role-badge">سردبیر ارشد و مدیر پلتفرم</span>
            </h3>
            <p>
              از این پیشخوان جامع می‌توانید مقالات علمی را منتشر نمایید، کتابخانه رسانه‌ها را مدیریت کنید، وضعیت بهینه‌سازی سئوی گوگل را رصد نموده و ساختار دپارتمان‌های ۹‌گانه را هدایت فرمایید.
            </p>
          </div>
          <div style="display:flex; gap:10px;">
            <button type="button" class="btn btn-primary" onclick="createNewPost()">
              ✍️ نگارش مقاله تازه
            </button>
            <button type="button" class="btn btn-secondary" onclick="switchTab('media')">
              🖼️ مدیریت رسانه‌ها
            </button>
          </div>
        </div>

        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-icon-wrap" style="background: #E0F2FE; color: #0284C7;">📄</div>
            <div class="metric-info">
              <h4>کل مقالات منتشرشده</h4>
              <div class="metric-num" id="metricTotalArticles">۴</div>
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-icon-wrap" style="background: #F0FDF4; color: #059669;">🖼️</div>
            <div class="metric-info">
              <h4>پرونده‌های چندرسانه‌ای</h4>
              <div class="metric-num" id="metricTotalMedia">۶</div>
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-icon-wrap" style="background: #FEF3C7; color: #D97706;">🩺</div>
            <div class="metric-info">
              <h4>پزشکان تاییدشده</h4>
              <div class="metric-num">۵ متخصص</div>
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-icon-wrap" style="background: #F3E8FF; color: #7C3AED;">🔍</div>
            <div class="metric-info">
              <h4>وضعیت سئو و ساختار E-E-A-T</h4>
              <div class="metric-num" style="font-size: 18px; color: #059669;">عالی و فعال (۹۴٪)</div>
            </div>
          </div>
        </div>

        <!-- Recent Posts Summary Card -->
        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
            <h3 style="font-size: 16px; font-weight: 800;">آخرین مقالات مجله سلامت</h3>
            <button type="button" class="btn btn-secondary" onclick="switchTab('posts')">مشاهده همه مقالات ↗</button>
          </div>
          <div class="wp-table-wrap">
            <table class="wp-table">
              <thead>
                <tr>
                  <th>عنوان مقاله</th>
                  <th>دپارتمان</th>
                  <th>پزشک ناظر</th>
                  <th>نمره سئو</th>
                  <th>وضعیت</th>
                </tr>
              </thead>
              <tbody id="dashboardRecentPosts"></tbody>
            </table>
          </div>
        </div>

      </section>

      <!-- ================= 2. TAB: POSTS LIST ================= -->
      <section id="tab-posts" class="tab-section">
        <div class="section-header-box">
          <div class="section-title-wrap">
            <h2>
              <span>نوشته‌ها و مقالات مجله</span>
              <button type="button" class="btn btn-primary" style="font-size: 12px; padding: 4px 12px;" onclick="createNewPost()">افزودن نوشته تازه</button>
            </h2>
            <p>مدیریت کامل مقالات علمی منتشرشده، پیش‌نویس‌ها و تنظیمات اختصاصی سئو</p>
          </div>
          <div class="header-actions-group">
            <select id="postPillarFilter" class="form-control" style="width: 200px;" onchange="filterPosts()">
              <option value="">همه دپارتمان‌ها</option>
            </select>
            <input type="text" id="postSearchInput" class="form-control" placeholder="جستجو در مقالات..." style="width: 220px;" oninput="filterPosts()">
          </div>
        </div>

        <div class="wp-table-wrap">
          <div class="wp-table-filters">
            <ul class="status-pills-list">
              <li class="status-pill active" id="pill-filter-all" onclick="setPostStatusFilter('all')">همه (<span id="countFilterAll">۴</span>)</li>
              <li class="status-pill" id="pill-filter-published" onclick="setPostStatusFilter('published')">منتشر شده (<span id="countFilterPublished">۴</span>)</li>
              <li class="status-pill" id="pill-filter-draft" onclick="setPostStatusFilter('draft')">پیش‌نویس‌ها (<span id="countFilterDraft">۰</span>)</li>
              <li class="status-pill" id="pill-filter-trash" onclick="setPostStatusFilter('trash')">زباله‌دان (<span id="countFilterTrash">۰</span>)</li>
            </ul>
          </div>
          <table class="wp-table">
            <thead>
              <tr>
                <th style="width: 40px;"><input type="checkbox" id="selectAllPosts"></th>
                <th style="width: 70px;">تصویر</th>
                <th style="width: 38%;">عنوان نوشته</th>
                <th>دپارتمان</th>
                <th>پزشک ناظر</th>
                <th>کلیدواژه سئو</th>
                <th>امتیاز سئو</th>
                <th>وضعیت</th>
              </tr>
            </thead>
            <tbody id="postsTableBody"></tbody>
          </table>
        </div>
      </section>

      <!-- ================= 3. TAB: ARTICLE WRITING STUDIO ================= -->
      <section id="tab-editor" class="tab-section">
        
        <!-- Editor Header Actions Bar -->
        <div class="section-header-box">
          <div class="section-title-wrap">
            <h2 id="editorPageHeading">استودیوی نگارش و تدوین مقاله علمی</h2>
            <p>محیط استاندارد تحریریه، مجهز به سیستم پیشرفته بهینه‌سازی سئو، کتابخانه پرونده‌های چندرسانه‌ای و استانداردهای پزشکی</p>
          </div>
          <div class="header-actions-group">
            <button type="button" class="btn btn-clean" id="btnSmartCleanEditor" title="پاکسازی فونت‌ها و رنگ‌های نامربوط، اصلاح ی/ک عربی و نیم‌فاصله‌ها">
              ✨ پاکسازی هوشمند متن
            </button>
            <button type="button" class="btn btn-preview" id="btnLivePreviewArticle">
              👁️ پیش‌نمایش در مجله
            </button>
            <button type="button" class="btn btn-secondary" onclick="saveArticle('draft')">
              💾 ذخیره پیش‌نویس
            </button>
            <button type="button" class="btn btn-primary" onclick="saveArticle('published')">
              🚀 انتشار در مجله
            </button>
          </div>
        </div>

        <!-- 2-Column Structured Document Workspace -->
        <div class="article-editor-workspace">
          
          <!-- Column 1: Main Paper Document Canvas -->
          <div class="editor-paper-card">
            
            <!-- Article Document Header: Title & Lead -->
            <div class="editor-paper-header">
              <input type="text" id="editTitle" class="input-title-h1" placeholder="عنوان اصلی مقاله علمی را وارد کنید (H1)..." oninput="handleTitleChange()">
              
              <div class="input-lead-box">
                <label for="editSummary">چکیده و لید بالینی مقاله (جهت نمایش در کارت‌ها، پیش‌نمایش گوگل و شبکه‌های اجتماعی):</label>
                <textarea id="editSummary" class="textarea-lead" placeholder="خلاصه بالینی و پیام کلیدی مقاله برای خوانندگان..." oninput="handleSummaryChange()"></textarea>
              </div>
            </div>

            <!-- Sticky Formatting Toolbar -->
            <div class="editorial-toolbar-sticky">
              
              <!-- Headings -->
              <div class="toolbar-cluster">
                <button type="button" class="tbtn" id="tH2" title="تیتر اصلی بخش (H2)">H2</button>
                <button type="button" class="tbtn" id="tH3" title="زیرعنوان بخش (H3)">H3</button>
                <button type="button" class="tbtn" id="tP" title="متن عادی (پاراگراف)">P</button>
              </div>

              <!-- Inline Formats -->
              <div class="toolbar-cluster">
                <button type="button" class="tbtn" id="tBold" title="ضخیم (Ctrl+B)">B</button>
                <button type="button" class="tbtn" id="tItalic" title="مورب (Ctrl+I)">I</button>
                <button type="button" class="tbtn" id="tUnderline" title="زیرخط (Ctrl+U)">U</button>
                <button type="button" class="tbtn" id="tStrike" title="خط‌خورده">S</button>
              </div>

              <!-- Lists & Quotes -->
              <div class="toolbar-cluster">
                <button type="button" class="tbtn" id="tBullet" title="لیست نقطه‌ای">•</button>
                <button type="button" class="tbtn" id="tOrdered" title="لیست عددی">1.</button>
                <button type="button" class="tbtn" id="tQuote" title="نقل‌قول بالینی">”</button>
              </div>

              <!-- Clinical Callout Blocks -->
              <div class="toolbar-cluster">
                <button type="button" class="tbtn-pill tbtn-warning" onclick="insertCallout('warning')">
                  <span>⚠️ هشدار بالینی</span>
                </button>
                <button type="button" class="tbtn-pill tbtn-advice" onclick="insertCallout('advice')">
                  <span>🩺 توصیه پزشک</span>
                </button>
                <button type="button" class="tbtn-pill tbtn-protocol" onclick="insertCallout('protocol')">
                  <span>ℹ️ پروتکل تریاژ</span>
                </button>
              </div>

              <!-- Media Inserter & Links -->
              <div class="toolbar-cluster">
                <button type="button" class="tbtn-pill tbtn-media" onclick="openMediaModal('editor')" title="افزودن تصویر از سیستم یا کتابخانه رسانه‌ها">
                  <span>🖼️ افزودن رسانه</span>
                </button>
                <button type="button" class="tbtn" id="tLink" title="درج پیوند اینترنتی">🔗</button>
                <button type="button" class="tbtn" id="tHR" title="خط جداکننده">➖</button>
              </div>

              <!-- History -->
              <div class="toolbar-cluster" style="margin-right: auto;">
                <button type="button" class="tbtn" id="tUndo" title="واگرد">↩️</button>
                <button type="button" class="tbtn" id="tRedo" title="بازگرد">↪️</button>
              </div>
            </div>

            <!-- Typing Canvas -->
            <div class="editor-canvas-body">
              <div id="editorialCanvasContainer"></div>
            </div>

            <!-- Bottom Status Strip -->
            <div class="editor-status-strip">
              <div class="status-group">
                <span>تعداد کلمات: <strong id="statWordCount">۰</strong></span>
                <span>کاراکترها: <strong id="statCharCount">۰</strong></span>
                <span>زمان مطالعه: <strong id="statReadTimeCalc">۱ دقیقه</strong></span>
              </div>
              <div class="status-group">
                <span id="statSaveIndicator" style="color: #059669; font-weight: 700;">آماده برای انتشار</span>
              </div>
            </div>

          </div>

          <!-- Column 2: Side Inspector & Metadata Cards -->
          <div class="editor-inspector-column">
            
            <!-- Card 1: Publish Settings -->
            <div class="inspector-card">
              <div class="inspector-card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M2 12h20"/></svg>
                <span>وضعیت و انتشار</span>
              </div>

              <div class="form-group">
                <label for="editStatusSelect">وضعیت نوشته</label>
                <select id="editStatusSelect" class="form-control">
                  <option value="published">منتشر شده در مجله</option>
                  <option value="draft">پیش‌نویس تحریریه</option>
                </select>
              </div>

              <div class="form-group">
                <label for="editReadTime">مدت زمان تخمینی مطالعه</label>
                <input type="text" id="editReadTime" class="form-control" value="۷ دقیقه">
              </div>

              <div style="display:flex; flex-direction:column; gap:8px; margin-top: 14px;">
                <button type="button" class="btn btn-primary" style="justify-content: center;" onclick="saveArticle('published')">
                  🚀 انتشار مستقیم در مجله
                </button>
                <button type="button" class="btn btn-secondary" style="justify-content: center;" onclick="saveArticle('draft')">
                  💾 ذخیره به عنوان پیش‌نویس
                </button>
              </div>
            </div>

            <!-- Card 2: Department & Structure -->
            <div class="inspector-card">
              <div class="inspector-card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                <span>دپارتمان و شاخه تخصصی</span>
              </div>

              <div class="form-group">
                <label for="editPillar">دپارتمان تخصصی (پیلار ۹‌گانه)</label>
                <select id="editPillar" class="form-control"></select>
              </div>
            </div>

            <!-- Card 3: Supervising Doctor -->
            <div class="inspector-card">
              <div class="inspector-card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
                <span>پزشک ناظر بالینی (E-E-A-T)</span>
              </div>

              <div class="form-group">
                <label for="editDoctor">انتخاب متخصص ناظر</label>
                <select id="editDoctor" class="form-control" onchange="updateDoctorBadge()"></select>
              </div>
              <div id="inspectorDoctorInfo" style="font-size: 11.5px; color: #64748B; margin-top: 6px; line-height: 1.5;"></div>
            </div>

            <!-- Card 4: Featured Hero Image -->
            <div class="inspector-card">
              <div class="inspector-card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                <span>تصویر شاخص نوشته</span>
              </div>

              <div class="hero-preview-box" id="heroPreviewBox">
                <span style="font-size: 12px; color: #94A3B8;">تصویری انتخاب نشده است</span>
              </div>

              <div style="display:flex; gap:8px; margin-top:10px;">
                <button type="button" class="btn btn-secondary" style="flex:1; justify-content: center; font-size: 12px;" onclick="openMediaModal('featured')">
                  📁 انتخاب یا بارگذاری تصویر
                </button>
                <button type="button" class="btn btn-danger" id="btnRemoveHero" style="padding:4px 8px; display:none;" onclick="removeHeroImage()" title="حذف تصویر شاخص">
                  ✕
                </button>
              </div>

              <input type="hidden" id="editHeroUrl">

              <div class="form-group" style="margin-top: 12px;">
                <label for="editHeroAlt">متن جایگزین تصویر شاخص (الزامی برای سئو Alt)</label>
                <input type="text" id="editHeroAlt" class="form-control" placeholder="توصیف دقیق برای گوگل و دسترس‌پذیری...">
              </div>

              <div class="form-group" style="margin-top: 8px;">
                <label for="editHeroCaption">زیرنویس بالینی تصویر</label>
                <input type="text" id="editHeroCaption" class="form-control" placeholder="مثال: بازسازی سه‌بعدی مداخله ستون فقرات">
              </div>
            </div>

            <!-- Card 5: Tags -->
            <div class="inspector-card">
              <div class="inspector-card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>
                <span>برچسب‌ها و تگ‌های تخصصی</span>
              </div>

              <div class="form-group">
                <input type="text" id="editTags" class="form-control" placeholder="ستون فقرات، لیزر، توانبخشی">
                <span style="font-size: 11px; color: #94A3B8; margin-top: 4px; display: block;">کلمات کلیدی را با ویرگول (،) جدا فرمایید.</span>
              </div>
            </div>

          </div>

        </div>

        <!-- ================= Comprehensive Yoast/RankMath SEO Suite ================= -->
        <div class="seo-suite-card">
          <div class="seo-suite-header">
            <div style="display:flex; align-items:center; gap:12px;">
              <h3 style="font-size: 15.5px; font-weight: 800; color: var(--text-main); display:flex; align-items:center; gap:8px;">
                <span>🔍 بهینه‌سازی و آنالیز سئو (Pezeshkan SEO Suite)</span>
              </h3>
              <span id="seoOverallScoreBadge" class="badge-seo-score seo-good">🟢 نمره سئو: ۹۵/۱۰۰</span>
            </div>

            <ul class="seo-suite-tabs">
              <li class="seo-tab-btn active" id="btnSeoTab-snippet" onclick="switchSeoTab('snippet')">پیش‌نمایش گوگل و اسنیپت</li>
              <li class="seo-tab-btn" id="btnSeoTab-audit" onclick="switchSeoTab('audit')">چک‌لیست آنالیز سئو</li>
              <li class="seo-tab-btn" id="btnSeoTab-schema" onclick="switchSeoTab('schema')">اسکیما و سوالات متداول (FAQ)</li>
              <li class="seo-tab-btn" id="btnSeoTab-social" onclick="switchSeoTab('social')">پیش‌نمایش شبکه‌های اجتماعی</li>
            </ul>
          </div>

          <div class="seo-suite-body">
            
            <!-- Pane 1: Google Snippet Preview & Inputs -->
            <div class="seo-pane active" id="seoPane-snippet">
              
              <div class="form-group" style="max-width: 650px; margin-bottom: 20px;">
                <label for="seoFocusKeyword" style="font-size: 13.5px; color: #0284C7; font-weight: 800;">
                  🎯 کلیدواژه کانونی (Focus Keyphrase)
                </label>
                <input type="text" id="seoFocusKeyword" class="form-control" placeholder="مثال: درمان غیرجراحی دیسک کمر" oninput="runLiveSeoAudit()">
                <span style="font-size: 11px; color: #64748B; margin-top: 4px; display: block;">کلمه یا عبارتی که می‌خواهید مقاله در نتایج سرچ گوگل با آن رتبه بگیرد.</span>
              </div>

              <!-- Google SERP Snippet Preview Box -->
              <div class="google-serp-preview">
                <div class="serp-device-toggle">
                  <button type="button" class="serp-device-btn active" id="btnSerpMobile" onclick="setSerpDevice('mobile')">📱 نسخه موبایل</button>
                  <button type="button" class="serp-device-btn" id="btnSerpDesktop" onclick="setSerpDevice('desktop')">💻 نسخه دسکتاپ</button>
                </div>

                <div class="serp-site-info">
                  <div class="serp-favicon">پ</div>
                  <div class="serp-url-breadcrumb">
                    https://pezeshkan.me &rsaquo; mag &rsaquo; <span id="serpBreadcrumbSlug">nonsurgical-treatments</span>
                  </div>
                </div>

                <a href="javascript:void(0)" class="serp-title-link" id="serpTitlePreview">
                  راهنمای بالینی درمان غیرجراحی دیسک کمر و سیاتیک | مجله سلامت پزشکآن
                </a>

                <div class="serp-snippet-desc" id="serpDescPreview">
                  بررسی علمی راهکارهای نوین توانبخشی و مداخله‌ای بدون نیاز به بیهوشی و تیغ جراحی، همراه با معیارهای تریاژ اورژانس سندرم دم اسب.
                </div>
              </div>

              <!-- Snippet Controls -->
              <div style="max-width: 650px; display:flex; flex-direction:column; gap:16px;">
                
                <div class="form-group">
                  <label for="seoMetaTitle">عنوان سئو (Google SEO Title)</label>
                  <input type="text" id="seoMetaTitle" class="form-control" placeholder="عنوان مقاله در نتایج جستجوی گوگل..." oninput="handleMetaTitleInput()">
                  <div class="seo-progress-track">
                    <div class="seo-progress-fill" id="barTitleFill"></div>
                  </div>
                  <div class="seo-counter-label">
                    <span id="labelTitleCount">۰ / ۶۰ کاراکتر</span>
                    <span>طول ایده‌آل: ۵۰ الی ۶۰ کاراکتر</span>
                  </div>
                </div>

                <div class="form-group">
                  <label for="seoMetaDesc">توضیحات متا (Meta Description)</label>
                  <textarea id="seoMetaDesc" class="form-control" rows="3" placeholder="توضیحاتی ترغیب‌کننده و خلاصه برای جلب کلیک کاربر در گوگل..." oninput="handleMetaDescInput()"></textarea>
                  <div class="seo-progress-track">
                    <div class="seo-progress-fill" id="barDescFill"></div>
                  </div>
                  <div class="seo-counter-label">
                    <span id="labelDescCount">۰ / ۱۶۰ کاراکتر</span>
                    <span>طول ایده‌آل: ۱۲۰ الی ۱۶۰ کاراکتر</span>
                  </div>
                </div>

                <div class="form-group">
                  <label for="editSlug">نامک پیوند یکتا (Slug / آدرس اینترنتی URL)</label>
                  <div style="display:flex; gap:8px;">
                    <input type="text" id="editSlug" class="form-control" placeholder="nonsurgical-treatments-lumbar-disc" dir="ltr" oninput="handleSlugInput()">
                    <button type="button" class="btn btn-secondary" onclick="generateAutoSlug()" style="white-space:nowrap; font-size:12px;" title="تولید خودکار نامک استاندارد از روی عنوان">
                      🔄 ساخت خودکار
                    </button>
                  </div>
                </div>

              </div>

            </div>

            <!-- Pane 2: Live SEO Audit Checklist -->
            <div class="seo-pane" id="seoPane-audit">
              <h4 style="font-size: 14px; font-weight: 800; color: var(--text-main); margin-bottom: 16px;">
                چک‌لیست ارزیابی هوشمند سئو و استانداردهای رتبه‌بندی محتوا
              </h4>
              <div class="seo-checklist-grid" id="seoChecklistGrid"></div>
            </div>

            <!-- Pane 3: Schema & FAQ Builder -->
            <div class="seo-pane" id="seoPane-schema">
              <div style="max-width: 680px;">
                <div class="form-group">
                  <label for="seoSchemaType">نوع ساختار داده اسکیما (Schema.org Type)</label>
                  <select id="seoSchemaType" class="form-control">
                    <option value="MedicalWebPage">MedicalWebPage (پیشنهادی سلامت و پزشکی E-E-A-T)</option>
                    <option value="Article">Article (مقاله استاندارد تحریریه)</option>
                    <option value="NewsArticle">NewsArticle (خبر علمی پزشکی)</option>
                    <option value="FAQPage">FAQPage (صفحه سوال و جواب)</option>
                  </select>
                  <span style="font-size: 11.5px; color: #64748B; margin-top: 4px; display: block;">ساختار داده‌ها مطابق آخرین گایدلاین‌های الگوریتم Medical E-E-A-T گوگل تولید می‌گردد.</span>
                </div>

                <div class="form-group">
                  <label for="seoCanonicalUrl">نشانی کانونیکال اختصاصی (Canonical URL)</label>
                  <input type="text" id="seoCanonicalUrl" class="form-control" placeholder="https://pezeshkan.me/mag/your-article" dir="ltr">
                </div>

                <div class="form-group">
                  <label for="seoRobotsSelect">تنظیمات ربات‌های موتور جستجو (Robots Meta)</label>
                  <select id="seoRobotsSelect" class="form-control">
                    <option value="index, follow">ایندکس شود و پیوندها دنبال گردند (index, follow)</option>
                    <option value="noindex, follow">عدم نمایش در گوگل ولی دنبال‌کردن لینک‌ها (noindex, follow)</option>
                    <option value="noindex, nofollow">مسدودسازی کامل ربات‌ها (noindex, nofollow)</option>
                  </select>
                </div>

                <!-- Interactive FAQ Builder -->
                <div style="margin-top: 24px; padding-top: 20px; border-top: 1px solid var(--border-color);">
                  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px;">
                    <div>
                      <h4 style="font-size: 13.5px; font-weight: 800; color: var(--text-main);">سازنده سوالات متداول (FAQ Schema Builder)</h4>
                      <p style="font-size: 11.5px; color: var(--text-muted);">پرسش و پاسخ‌ها مستقیماً در انتهای مقاله و ساختار داده اسکیما برای ریچ اسنیپت گوگل ثبت می‌شوند.</p>
                    </div>
                    <button type="button" class="btn btn-secondary" onclick="addFaqRow()" style="font-size: 12px;">
                      + افزودن پرسش جدید
                    </button>
                  </div>

                  <div id="faqListContainer"></div>
                </div>

              </div>
            </div>

            <!-- Pane 4: Social Media Preview -->
            <div class="seo-pane" id="seoPane-social">
              <div style="max-width: 580px;">
                <h4 style="font-size: 14px; font-weight: 800; color: var(--text-main); margin-bottom: 14px;">
                  پیش‌نمایش کارت اشتراک‌گذاری در شبکه‌های اجتماعی (Open Graph)
                </h4>
                <div style="border:1px solid #E2E8F0; border-radius:12px; overflow:hidden; background:#FFFFFF; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                  <div id="socialCardImage" style="height:220px; background:#F1F5F9; display:flex; align-items:center; justify-content:center; overflow:hidden;">
                    <img src="" id="socialPreviewImg" style="width:100%; height:100%; object-fit:cover; display:none;" alt="">
                    <span id="socialPlaceholderTxt" style="color:#94A3B8; font-size:12px;">تصویر شاخص مقاله در اینجا قرار می‌گیرد</span>
                  </div>
                  <div style="padding:16px 20px;">
                    <span style="font-size:11px; text-transform:uppercase; color:#64748B; font-weight:700;">PEZESHKAN.ME</span>
                    <h4 id="socialPreviewTitle" style="font-size:15px; font-weight:800; color:#0F172A; margin:6px 0;">عنوان مقاله علمی</h4>
                    <p id="socialPreviewDesc" style="font-size:12.5px; color:#64748B; line-height:1.6; margin:0;">توضیحات و لید مقاله جهت اشتراک در شبکه‌های اجتماعی...</p>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>

      </section>

      <!-- ================= 4. TAB: MEDIA LIBRARY ================= -->
      <section id="tab-media" class="tab-section">
        <div class="section-header-box">
          <div class="section-title-wrap">
            <h2>کتابخانه پرونده‌های چندرسانه‌ای مجله سلامت</h2>
            <p>بارگذاری، سازماندهی و بهینه‌سازی تصاویر پزشکی با متاتگ‌های سئو و متن جایگزین (Alt)</p>
          </div>
          <div class="header-actions-group">
            <input type="text" id="mediaSearchInput" class="form-control" placeholder="جستجو در نام یا Alt تصاویر..." style="width: 240px;" oninput="filterMediaLibrary()">
            <button type="button" class="btn btn-primary" onclick="document.getElementById('mediaLibraryUploadInput').click()">
              📤 بارگذاری پرونده تازه
            </button>
            <input type="file" id="mediaLibraryUploadInput" accept="image/*" multiple style="display:none;" onchange="handleMediaLibraryUpload(this)">
          </div>
        </div>

        <!-- Drag & Drop Zone -->
        <div class="media-dropzone" id="mediaLibraryDropzone" onclick="document.getElementById('mediaLibraryUploadInput').click()">
          <div class="dropzone-icon">🖼️</div>
          <div class="dropzone-text">
            <h4>تصاویر را به اینجا بکشید و رها کنید، یا برای انتخاب از سیستم کلیک فرمایید</h4>
            <p>فرمت‌های مجاز: WebP, PNG, JPG, JPEG, SVG (حداکثر ۱۵ مگابایت)</p>
          </div>
        </div>

        <!-- Media Grid -->
        <div class="media-grid" id="mediaLibraryGrid"></div>
      </section>

      <!-- ================= 5. TAB: CATEGORIES & PILLARS ================= -->
      <section id="tab-categories" class="tab-section">
        <div class="section-header-box">
          <div class="section-title-wrap">
            <h2>دپارتمان‌ها و دسته‌بندی‌های ۹‌گانه مجله سلامت</h2>
            <p>ساختار ستون‌های علمی، زیردسته‌ها و چیپ‌های جستجوی داغ</p>
          </div>
          <button type="button" class="btn btn-primary" onclick="showToast('تغییرات ساختار دپارتمان‌ها در سامانه ذخیره است.', '✅')">
            💾 ذخیره تغییرات دپارتمان‌ها
          </button>
        </div>

        <div class="wp-table-wrap">
          <table class="wp-table">
            <thead>
              <tr>
                <th>شناسه</th>
                <th>نام دپارتمان</th>
                <th>اسلاگ (Slug)</th>
                <th>تعداد زیردسته‌ها</th>
                <th>چیپ‌های جستجوی داغ</th>
                <th>عملیات</th>
              </tr>
            </thead>
            <tbody id="pillarsTableBody"></tbody>
          </table>
        </div>
      </section>

      <!-- ================= 6. TAB: DOCTORS & REVIEWERS ================= -->
      <section id="tab-doctors" class="tab-section">
        <div class="section-header-box">
          <div class="section-title-wrap">
            <h2>پزشکان ناظر و اعضای هیئت تحریریه بالینی</h2>
            <p>مشاهده و ویرایش مشخصات متخصصان، کد نظام پزشکی و تخصص‌ها</p>
          </div>
          <button type="button" class="btn btn-primary" onclick="showToast('فهرست پزشکان تاییدشده و به‌روز است.', '👨‍⚕️')">
            + افزودن پزشک جدید
          </button>
        </div>

        <div class="wp-table-wrap">
          <table class="wp-table">
            <thead>
              <tr>
                <th>نام پزشک</th>
                <th>تخصص بالینی</th>
                <th>کد نظام پزشکی</th>
                <th>کلینیک / دپارتمان</th>
                <th>وضعیت نوبت‌دهی</th>
              </tr>
            </thead>
            <tbody id="doctorsTableBody"></tbody>
          </table>
        </div>
      </section>

      <!-- ================= 7. TAB: SITE-WIDE SEO SUITE ================= -->
      <section id="tab-seo" class="tab-section">
        <div class="section-header-box">
          <div class="section-title-wrap">
            <h2>مرکز بهینه‌سازی فنی و تنظیمات سراسری سئو (Technical SEO Suite)</h2>
            <p>مدیریت سرچ کنسول گوگل، متاتگ‌های تایید هویت، فایل robots.txt و نقشه سایت XML</p>
          </div>
          <button type="button" class="btn btn-primary" onclick="saveSiteSeoSettings()">
            💾 ذخیره تنظیمات سئو
          </button>
        </div>

        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:24px;">
          
          <div class="card">
            <h3 style="font-size:15px; font-weight:800; color:var(--text-main); margin-bottom:16px;">
              🔍 هویت و پیش‌فرض‌های متاتگ در گوگل
            </h3>
            
            <div class="form-group">
              <label for="seoSettingTitleTemplate">قالب پیش‌فرض عنوان صفحات (Title Template)</label>
              <input type="text" id="seoSettingTitleTemplate" class="form-control" value="%title% | مجله سلامت پزشکآن" dir="ltr">
            </div>

            <div class="form-group">
              <label for="seoSettingHomeDesc">توضیحات متای صفحه اصلی مجله سلامت</label>
              <textarea id="seoSettingHomeDesc" class="form-control" rows="3">پایگاه جامع دانش سلامت، راهنماهای بالینی پزشکی، ارزیابی آنلاین علائم و رزرو نوبت با تایید هیئت علمی و پزشکان متخصص.</textarea>
            </div>

            <div class="form-group">
              <label for="seoSettingKeywords">کلمات کلیدی اصلی پلتفرم</label>
              <input type="text" id="seoSettingKeywords" class="form-control" value="مجله سلامت, دیسک کمر, ارزیابی علائم, سونوگرافی بارداری, تریاژ اورژانس, پزشکآن">
            </div>
          </div>

          <div class="card">
            <h3 style="font-size:15px; font-weight:800; color:var(--text-main); margin-bottom:16px;">
              🛡️ اتصال به ابزارهای وبمستر و آنالیتیکس
            </h3>

            <div class="form-group">
              <label for="seoSettingGoogleVerify">کد تایید سرچ کنسول گوگل (google-site-verification)</label>
              <input type="text" id="seoSettingGoogleVerify" class="form-control" value="google-site-verification=pezeshkan_mag_secure_token_2026" dir="ltr">
            </div>

            <div class="form-group">
              <label for="seoSettingBingVerify">کد تایید موتور بینگ (Bing Webmaster Verification)</label>
              <input type="text" id="seoSettingBingVerify" class="form-control" value="bing-site-verification=pezeshkan_bing_token_2026" dir="ltr">
            </div>

            <div class="form-group">
              <label for="seoSettingAnalyticsId">شناسه Google Analytics 4 (GA4)</label>
              <input type="text" id="seoSettingAnalyticsId" class="form-control" value="G-PEZESHKAN2026" dir="ltr">
            </div>

            <div style="background:#FAFBFD; border:1px solid #E2E8F0; border-radius:8px; padding:12px; margin-top:14px; font-size:12px; line-height:1.7;">
              <strong>وضعیت فایل‌های فنی سئو:</strong>
              <div style="display:flex; gap:16px; margin-top:6px;">
                <a href="/robots.txt" target="_blank" style="color:var(--primary); text-decoration:none; font-weight:700;">📄 مشاهده robots.txt ↗</a>
                <a href="/sitemap.xml" target="_blank" style="color:var(--primary); text-decoration:none; font-weight:700;">🗺️ مشاهده sitemap.xml ↗</a>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- ================= 8. TAB: SITE SETTINGS ================= -->
      <section id="tab-settings" class="tab-section">
        <div class="section-header-box">
          <div class="section-title-wrap">
            <h2>تنظیمات عمومی سامانه مجله سلامت</h2>
            <p>پیکربندی مشخصات پلتفرم، بنر اعلان سراسری و شماره‌های پشتیبانی</p>
          </div>
          <button type="button" class="btn btn-primary" onclick="saveSiteSettings()">
            💾 ذخیره تنظیمات سایت
          </button>
        </div>

        <div class="card" style="max-width: 720px;">
          <div class="form-group">
            <label for="settingSiteTitle">عنوان اصلی مجله</label>
            <input type="text" id="settingSiteTitle" class="form-control" value="مجله سلامت پزشکآن">
          </div>

          <div class="form-group">
            <label for="settingSiteSubtitle">شعار و زیرعنوان پلتفرم</label>
            <input type="text" id="settingSiteSubtitle" class="form-control" value="پلتفرم دانش سلامت، ارزیابی بالینی و نوبت‌دهی آنلاین">
          </div>

          <div class="form-group">
            <label for="settingEditorialLeader">سردبیر علمی مجله</label>
            <input type="text" id="settingEditorialLeader" class="form-control" value="دکتر مهران رادمنش (متخصص جراحی مغز و اعصاب)">
          </div>

          <div class="form-group">
            <label for="settingBannerText">متن بنر اعلان بالای سایت</label>
            <input type="text" id="settingBannerText" class="form-control" value="ویژه‌نامه راهنمای درمان غیرجراحی ستون فقرات و روش‌های نوین طب فیزیکی منتشر شد.">
          </div>

          <div class="form-group">
            <label for="settingContactPhone">تلفن پشتیبانی و پذیرش</label>
            <input type="text" id="settingContactPhone" class="form-control" value="۰۲۱-۸۸۸۸۴۴۴۴" dir="ltr">
          </div>
        </div>
      </section>

    </main>

  </div>

  <!-- ================= WordPress Media Inserter Modal ================= -->
  <div class="media-modal-overlay" id="mediaModal">
    <div class="media-modal-card">
      <div class="media-modal-header">
        <ul class="media-modal-tabs">
          <li class="media-tab-btn active" id="btnMediaTab-library" onclick="switchMediaModalTab('library')">🖼️ کتابخانه رسانه‌ها</li>
          <li class="media-tab-btn" id="btnMediaTab-upload" onclick="switchMediaModalTab('upload')">📤 بارگذاری از کامپیوتر</li>
          <li class="media-tab-btn" id="btnMediaTab-url" onclick="switchMediaModalTab('url')">🔗 از طریق نشانی اینترنتی (URL)</li>
        </ul>
        <button type="button" class="btn btn-secondary" onclick="closeMediaModal()" style="padding:4px 8px; font-size:12px;">✕ بستن</button>
      </div>

      <div class="media-modal-body">
        
        <!-- Left: Gallery / Upload View -->
        <div class="media-modal-content-area">
          
          <!-- View 1: Library Grid -->
          <div id="modalView-library">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
              <input type="text" id="modalMediaSearch" class="form-control" placeholder="جستجو در تصاویر..." style="max-width:240px; font-size:12.5px;" oninput="filterModalMedia()">
              <span id="modalMediaCountLabel" style="font-size:12px; color:#64748B;">۶ تصویر در کتابخانه</span>
            </div>
            <div class="media-grid" id="modalMediaGrid"></div>
          </div>

          <!-- View 2: Upload Zone -->
          <div id="modalView-upload" style="display:none; text-align:center; padding:40px 20px;">
            <div class="media-dropzone" onclick="document.getElementById('modalDirectUploadInput').click()">
              <div class="dropzone-icon">📤</div>
              <div class="dropzone-text">
                <h4>تصویر خود را اینجا رها کنید، یا برای انتخاب فایل کلیک فرمایید</h4>
                <p>فرمت‌های مجاز: WebP, PNG, JPG, SVG (تا سقف ۱۵ مگابایت)</p>
              </div>
            </div>
            <input type="file" id="modalDirectUploadInput" accept="image/*" style="display:none;" onchange="handleModalDirectUpload(this)">
          </div>

          <!-- View 3: URL View -->
          <div id="modalView-url" style="display:none; padding:20px;">
            <div class="form-group">
              <label for="modalDirectUrlInput">نشانی کامل تصویر (Image URL)</label>
              <input type="text" id="modalDirectUrlInput" class="form-control" placeholder="https://..." dir="ltr" oninput="handleModalDirectUrlInput()">
            </div>
          </div>

        </div>

        <!-- Right: Inspector for Selected Image -->
        <div class="media-modal-sidebar-area">
          <h4 style="font-size:13px; font-weight:800; color:var(--text-main); margin-bottom:14px; border-bottom:1px solid #E2E8F0; padding-bottom:8px;">
            مشخصات تصویر انتخابی
          </h4>

          <div style="width:100%; height:130px; border-radius:8px; overflow:hidden; background:#E2E8F0; margin-bottom:14px; display:flex; align-items:center; justify-content:center;">
            <img src="" id="modalSelectedPreviewImg" style="width:100%; height:100%; object-fit:cover; display:none;" alt="">
            <span id="modalNoSelectionTxt" style="font-size:11.5px; color:#64748B;">تصویری انتخاب نشده</span>
          </div>

          <div class="form-group">
            <label for="modalImageAlt" style="color:#0284C7;">
              متن جایگزین (Alt Text)
              <span style="font-size:10px; color:#D97706; display:block;">الزامی برای سئو و هوش مصنوعی گوگل</span>
            </label>
            <input type="text" id="modalImageAlt" class="form-control" placeholder="توصیف بالینی و محتوایی تصویر...">
          </div>

          <div class="form-group">
            <label for="modalImageCaption">زیرنویس بالینی (Caption)</label>
            <input type="text" id="modalImageCaption" class="form-control" placeholder="زیرنویس زیر عکس...">
          </div>

          <div class="form-group" id="groupModalAlign">
            <label for="modalImageAlign">چیدمان تصویر</label>
            <select id="modalImageAlign" class="form-control">
              <option value="align-center">وسط‌چین (Center)</option>
              <option value="align-right">راست‌چین (Right)</option>
              <option value="align-left">چپ‌چین (Left)</option>
              <option value="align-full">تمام‌عرض بالینی (Full Bleed)</option>
            </select>
          </div>
        </div>

      </div>

      <div class="media-modal-footer">
        <button type="button" class="btn btn-secondary" onclick="closeMediaModal()">انصراف</button>
        <button type="button" class="btn btn-primary" id="btnConfirmMediaModal" onclick="confirmMediaModalSelection()">
          درج در نوشته
        </button>
      </div>
    </div>
  </div>

  <!-- Live Magazine Preview Modal -->
  <div class="preview-modal-overlay" id="previewModal">
    <div class="preview-modal-card">
      <div class="preview-modal-header">
        <h3 style="font-size: 15px; font-weight: 700; color: #0F172A;">پیش‌نمایش بالینی مقاله (استایل مجله سلامت پزشکآن)</h3>
        <button type="button" class="btn btn-secondary" onclick="closePreviewModal()">بستن پیش‌نمایش</button>
      </div>
      <div class="preview-modal-body" id="previewModalContent"></div>
    </div>
  </div>

  <!-- Toast Notification -->
  <div class="toast-msg" id="toastMsg">
    <span id="toastIcon">✅</span>
    <span id="toastText">عملیات با موفقیت انجام شد</span>
  </div>
'''

print("Head and HTML markup part 1 prepared.")
