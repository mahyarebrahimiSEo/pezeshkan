# -*- coding: utf-8 -*-
"""
Builds the Pezeshkan Magazine Tiptap CMS Studio (mag/admin.html)
A modern, Day-Mode medical content management system with Tiptap v2,
CleanPaste typography normalizer, clinical callouts, and live preview.
"""

import json
import os

BASE_DIR = r"e:\antigravity\pezeshkan_design"
MAG_DIR = os.path.join(BASE_DIR, "mag")

with open(os.path.join(MAG_DIR, "content", "pillars.json"), encoding="utf-8") as f:
    pillars_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "doctors.json"), encoding="utf-8") as f:
    doctors_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "articles.json"), encoding="utf-8") as f:
    articles_data = json.load(f)

pillars_json_str = json.dumps(pillars_data, ensure_ascii=False)
doctors_json_str = json.dumps(doctors_data, ensure_ascii=False)
articles_json_str = json.dumps(articles_data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>استودیو مدیریت محتوای بالینی پزشکآن | Tiptap CMS Studio</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Tiptap Standalone Production Bundle -->
  <script src="public/tiptap-bundle.min.js"></script>

  <style>
    :root {{
      --font-sans: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      --bg-app: #F8FAFC;
      --bg-card: #FFFFFF;
      --border-color: #E2E8F0;
      --border-focus: #0284C7;
      --text-main: #0F172A;
      --text-muted: #64748B;
      --text-sub: #475569;
      --primary: #0284C7;
      --primary-hover: #0369A1;
      --primary-light: #E0F2FE;
      --accent-teal: #0D9488;
      --accent-emerald: #059669;
      --accent-amber: #D97706;
      --accent-rose: #E11D48;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: var(--font-sans);
    }}

    body {{
      background: var(--bg-app);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* Header Bar */
    .cms-header {{
      background: #FFFFFF;
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 50;
      box-shadow: var(--shadow-sm);
    }}

    .header-inner {{
      max-width: 1560px;
      margin: 0 auto;
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}

    .brand-section {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .brand-logo-icon {{
      width: 42px;
      height: 42px;
      background: linear-gradient(135deg, #0284C7, #0D9488);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #FFFFFF;
      box-shadow: 0 4px 10px rgba(2, 132, 199, 0.25);
    }}

    .brand-info h1 {{
      font-size: 17px;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.3px;
    }}

    .brand-info p {{
      font-size: 11.5px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .tiptap-badge {{
      background: #F1F5F9;
      color: #0369A1;
      padding: 2px 7px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      border: 1px solid #BAE6FD;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      border: 1px solid transparent;
      outline: none;
      text-decoration: none;
    }}

    .btn-secondary {{
      background: #FFFFFF;
      border-color: var(--border-color);
      color: var(--text-sub);
    }}
    .btn-secondary:hover {{
      background: #F8FAFC;
      border-color: #CBD5E1;
      color: var(--text-main);
    }}

    .btn-clean {{
      background: #ECFDF5;
      border-color: #A7F3D0;
      color: #065F46;
    }}
    .btn-clean:hover {{
      background: #D1FAE5;
      border-color: #6EE7B7;
    }}

    .btn-primary {{
      background: var(--primary);
      color: #FFFFFF;
      box-shadow: 0 2px 6px rgba(2, 132, 199, 0.25);
    }}
    .btn-primary:hover {{
      background: var(--primary-hover);
    }}

    .btn-preview {{
      background: #F0FDF4;
      border-color: #BBF7D0;
      color: #166534;
    }}
    .btn-preview:hover {{
      background: #DCFCE7;
    }}

    /* Main Grid Layout */
    .cms-main {{
      max-width: 1560px;
      margin: 20px auto;
      padding: 0 24px;
      width: 100%;
      flex: 1;
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 24px;
      align-items: start;
    }}

    /* Sidebar: Metadata & Controls */
    .cms-sidebar {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 20px;
      box-shadow: var(--shadow-sm);
      position: sticky;
      top: 80px;
      max-height: calc(100vh - 100px);
      overflow-y: auto;
    }}

    .sidebar-section-title {{
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .sidebar-section-title svg {{
      color: var(--primary);
    }}

    .article-picker-box {{
      background: #F1F5F9;
      border: 1px solid #E2E8F0;
      border-radius: var(--radius-sm);
      padding: 10px 12px;
      margin-bottom: 20px;
    }}

    .article-picker-box label {{
      display: block;
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}

    .form-group {{
      margin-bottom: 16px;
    }}

    .form-group label {{
      display: block;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-sub);
      margin-bottom: 6px;
    }}

    .form-control {{
      width: 100%;
      padding: 9px 12px;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: #FFFFFF;
      color: var(--text-main);
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
      outline: none;
    }}

    .form-control:focus {{
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.12);
    }}

    textarea.form-control {{
      resize: vertical;
      min-height: 80px;
      line-height: 1.6;
    }}

    .form-hint {{
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 4px;
    }}

    .doctor-badge-preview {{
      background: #F8FAFC;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 10px 12px;
      margin-top: 8px;
      font-size: 12px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}

    .doctor-mc-pill {{
      display: inline-block;
      background: #E0F2FE;
      color: #0369A1;
      padding: 1px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      width: fit-content;
    }}

    /* Featured Image Box */
    .hero-thumb-preview {{
      width: 100%;
      height: 140px;
      border-radius: var(--radius-sm);
      border: 1px dashed var(--border-color);
      background: #F1F5F9;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      margin-top: 8px;
      position: relative;
    }}

    .hero-thumb-preview img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}

    .hero-thumb-empty {{
      font-size: 12px;
      color: var(--text-muted);
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }}

    /* Editor Container */
    .cms-editor-container {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      min-height: calc(100vh - 100px);
      overflow: hidden;
    }}

    /* Tiptap Toolbar */
    .editor-toolbar {{
      background: #FFFFFF;
      border-bottom: 1px solid var(--border-color);
      padding: 10px 14px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 6px;
      position: sticky;
      top: 65px;
      z-index: 20;
    }}

    .toolbar-group {{
      display: flex;
      align-items: center;
      gap: 3px;
      padding: 0 4px;
      border-left: 1px solid var(--border-color);
    }}
    .toolbar-group:last-child {{
      border-left: none;
    }}

    .tool-btn {{
      background: transparent;
      border: 1px solid transparent;
      border-radius: 6px;
      color: var(--text-sub);
      width: 34px;
      height: 34px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 13.5px;
      font-weight: 600;
      transition: all 0.12s ease;
    }}

    .tool-btn:hover {{
      background: #F1F5F9;
      color: var(--text-main);
      border-color: #E2E8F0;
    }}

    .tool-btn.is-active {{
      background: #E0F2FE;
      color: #0284C7;
      border-color: #BAE6FD;
    }}

    .tool-select {{
      padding: 5px 8px;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-sub);
      background: #FFFFFF;
      cursor: pointer;
      outline: none;
    }}
    .tool-select:focus {{
      border-color: var(--primary);
    }}

    .tool-dropdown-wrap {{
      position: relative;
      display: inline-block;
    }}

    .clinical-callout-btn {{
      background: #FEF3C7;
      color: #92400E;
      border: 1px solid #FDE68A;
      font-size: 12px;
      padding: 5px 10px;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      cursor: pointer;
      font-weight: 600;
    }}
    .clinical-callout-btn:hover {{
      background: #FDE68A;
    }}

    /* Dropdown Menus for Toolbar */
    .dropdown-content {{
      display: none;
      position: absolute;
      top: 100%;
      right: 0;
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-lg);
      min-width: 220px;
      padding: 6px;
      z-index: 100;
      margin-top: 4px;
    }}

    .dropdown-content.show {{
      display: block;
    }}

    .dropdown-item {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      font-size: 12.5px;
      color: var(--text-sub);
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.1s;
    }}
    .dropdown-item:hover {{
      background: #F1F5F9;
      color: var(--text-main);
    }}

    /* Clean Notification Toast */
    .toast-msg {{
      position: fixed;
      bottom: 24px;
      left: 24px;
      background: #0F172A;
      color: #FFFFFF;
      padding: 12px 20px;
      border-radius: var(--radius-md);
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: var(--shadow-lg);
      z-index: 200;
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .toast-msg.show {{
      transform: translateY(0);
      opacity: 1;
    }}

    /* Editor Typing Canvas */
    .editor-canvas {{
      flex: 1;
      padding: 36px 48px;
      overflow-y: auto;
      background: #FFFFFF;
    }}

    /* Tiptap / ProseMirror Styling */
    .ProseMirror {{
      outline: none;
      min-height: 480px;
      font-size: 16px;
      line-height: 1.95;
      color: #1E293B;
    }}

    .ProseMirror p {{
      margin-bottom: 1.25em;
    }}

    .ProseMirror h2 {{
      font-size: 22px;
      font-weight: 800;
      color: #0F172A;
      margin-top: 2em;
      margin-bottom: 0.75em;
      padding-bottom: 8px;
      border-bottom: 2px solid #F1F5F9;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .ProseMirror h2::before {{
      content: '';
      display: inline-block;
      width: 4px;
      height: 20px;
      background: var(--primary);
      border-radius: 2px;
    }}

    .ProseMirror h3 {{
      font-size: 18px;
      font-weight: 700;
      color: #1E293B;
      margin-top: 1.5em;
      margin-bottom: 0.5em;
    }}

    .ProseMirror ul, .ProseMirror ol {{
      padding-right: 24px;
      margin-bottom: 1.25em;
    }}

    .ProseMirror li {{
      margin-bottom: 0.5em;
    }}

    .ProseMirror blockquote {{
      border-right: 4px solid #CBD5E1;
      padding-right: 16px;
      margin: 1.5em 0;
      color: #475569;
      font-style: italic;
    }}

    .ProseMirror a {{
      color: var(--primary);
      text-decoration: underline;
      text-underline-offset: 4px;
    }}

    .ProseMirror hr {{
      border: none;
      border-top: 1px solid var(--border-color);
      margin: 2em 0;
    }}

    /* Clinical Callout Blocks in ProseMirror */
    .clinical-callout {{
      border-radius: var(--radius-md);
      padding: 18px 20px;
      margin: 24px 0;
      border: 1px solid transparent;
      position: relative;
    }}

    .clinical-callout.warning {{
      background: #FFFBEB;
      border-color: #FDE68A;
      color: #92400E;
    }}

    .clinical-callout.advice {{
      background: #F0FDF4;
      border-color: #BBF7D0;
      color: #166534;
    }}

    .clinical-callout.protocol {{
      background: #F0F9FF;
      border-color: #BAE6FD;
      color: #0369A1;
    }}

    .callout-header {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      font-size: 14.5px;
      margin-bottom: 8px;
    }}

    .callout-content {{
      font-size: 14px;
      line-height: 1.8;
      color: inherit;
    }}

    /* Image in Editor */
    .clinical-img-figure {{
      margin: 28px 0;
      text-align: center;
    }}

    .clinical-img-figure img {{
      max-width: 100%;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
    }}

    .clinical-img-figure.size-wide img {{
      max-width: 110%;
      margin-right: -5%;
    }}

    .clinical-img-figure.size-full img {{
      max-width: 100%;
      border-radius: 0;
    }}

    .clinical-img-caption {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }}

    /* Clinical Quote Block */
    .doctor-quote-block {{
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-right: 4px solid var(--primary);
      border-radius: var(--radius-md);
      padding: 18px 22px;
      margin: 26px 0;
    }}
    .quote-text {{
      font-size: 15.5px;
      font-weight: 500;
      line-height: 1.8;
      color: #1E293B;
      margin-bottom: 10px;
    }}
    .quote-author-info {{
      font-size: 12.5px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .quote-author-name {{
      font-weight: 700;
      color: var(--text-main);
    }}

    /* Status Bar at Bottom */
    .editor-status-bar {{
      background: #F8FAFC;
      border-top: 1px solid var(--border-color);
      padding: 8px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-muted);
    }}

    .status-left, .status-right {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      color: var(--accent-emerald);
      font-weight: 600;
    }}

    /* Live Preview Modal */
    .preview-modal-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }}

    .preview-modal-overlay.active {{
      display: flex;
    }}

    .preview-modal-card {{
      background: #FFFFFF;
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 960px;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      overflow: hidden;
    }}

    .preview-modal-header {{
      background: #F8FAFC;
      border-bottom: 1px solid var(--border-color);
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .preview-modal-header h3 {{
      font-size: 15px;
      font-weight: 700;
      color: var(--text-main);
    }}

    .preview-modal-body {{
      padding: 36px 48px;
      overflow-y: auto;
      flex: 1;
    }}

    /* Image Insert Modal */
    .img-modal-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    .img-modal-overlay.active {{
      display: flex;
    }}
    .img-modal-box {{
      background: #FFFFFF;
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 520px;
      padding: 24px;
      box-shadow: var(--shadow-lg);
    }}
    .img-modal-title {{
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    @media (max-width: 1024px) {{
      .cms-main {{
        grid-template-columns: 1fr;
      }}
      .cms-sidebar {{
        position: static;
        max-height: none;
      }}
      .editor-canvas {{
        padding: 20px 24px;
      }}
    }}
  </style>
</head>
<body>

  <!-- Header Bar -->
  <header class="cms-header">
    <div class="header-inner">
      <div class="brand-section">
        <div class="brand-logo-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2v20M2 12h20"></path>
          </svg>
        </div>
        <div class="brand-info">
          <h1>استودیو مدیریت محتوای بالینی پزشکآن</h1>
          <p>
            سیستم تحریریه استاندارد مجله سلامت
            <span class="tiptap-badge">موتور Tiptap v2</span>
          </p>
        </div>
      </div>

      <div class="header-actions">
        <button type="button" class="btn btn-clean" id="btnSmartClean" title="حذف فونت‌ها و رنگ‌های نامربوط، اصلاح ی/ک عربی و تنظیم نیم‌فاصله‌ها">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"></path>
          </svg>
          پاکسازی هوشمند و اصلاح تایپوگرافی
        </button>

        <button type="button" class="btn btn-preview" id="btnOpenPreview">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
          پیش‌نمایش در مجله
        </button>

        <button type="button" class="btn btn-secondary" id="btnExportHTML" title="کپی کد HTML استاندارد برای درج در سایت">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect width="14" height="14" x="8" y="8" rx="2" ry="2"></rect>
            <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"></path>
          </svg>
          کپی HTML
        </button>

        <button type="button" class="btn btn-primary" id="btnSaveDraft">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
            <polyline points="17 21 17 13 7 13 7 21"></polyline>
            <polyline points="7 3 7 8 15 8"></polyline>
          </svg>
          ذخیره پیش‌نویس
        </button>

        <a href="index.html" class="btn btn-secondary" target="_blank" title="مشاهده صفحه اصلی مجله سلامت">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
            <polyline points="15 3 21 3 21 9"></polyline>
            <line x1="10" y1="14" x2="21" y2="3"></line>
          </svg>
          نمای مجله
        </a>
      </div>
    </div>
  </header>

  <!-- Main Work Area -->
  <main class="cms-main">
    
    <!-- Sidebar: Article Clinical Metadata -->
    <aside class="cms-sidebar">
      <div class="article-picker-box">
        <label for="selectExistingArticle">بارگذاری از مقالات مجله سلامت:</label>
        <select id="selectExistingArticle" class="form-control">
          <option value="new">➕ ایجاد مقاله جدید (فرم خالی)</option>
        </select>
      </div>

      <div class="sidebar-section-title">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
        </svg>
        شناسنامه علمی مقاله
      </div>

      <div class="form-group">
        <label for="articleTitle">عنوان اصلی مقاله (H1)</label>
        <input type="text" id="articleTitle" class="form-control" placeholder="مثال: راهنمای درمان غیرجراحی دیسک کمر...">
      </div>

      <div class="form-group">
        <label for="articleSlug">شناسه انگلیسی آدرس (Slug)</label>
        <input type="text" id="articleSlug" class="form-control" placeholder="nonsurgical-lumbar-disc-treatments" dir="ltr">
      </div>

      <div class="form-group">
        <label for="articleSummary">چکیده بالینی و لید مقاله</label>
        <textarea id="articleSummary" class="form-control" placeholder="خلاصه علمی مقاله جهت نمایش در کارت‌ها و بالای مطلب..."></textarea>
      </div>

      <div class="form-group">
        <label for="pillarSelect">دپارتمان تخصصی (پیلار)</label>
        <select id="pillarSelect" class="form-control">
          <!-- Populated from pillars_data -->
        </select>
      </div>

      <div class="form-group">
        <label for="branchSelect">زیردسته بالینی</label>
        <select id="branchSelect" class="form-control">
          <!-- Populated dynamically based on pillar -->
        </select>
      </div>

      <div class="form-group">
        <label for="doctorSelect">پزشک نویسنده / ناظر بالینی</label>
        <select id="doctorSelect" class="form-control">
          <!-- Populated from doctors_data -->
        </select>
        <div id="doctorBadgePreview" class="doctor-badge-preview">
          <!-- Doctor info preview -->
        </div>
      </div>

      <div class="form-group">
        <label for="readTime">مدت زمان تخمینی مطالعه</label>
        <input type="text" id="readTime" class="form-control" value="۷ دقیقه">
      </div>

      <div class="form-group">
        <label>تصویر شاخص بالای مقاله (Hero Image)</label>
        <input type="text" id="heroImageUrl" class="form-control" placeholder="آدرس تصویر شاخص...">
        <div style="margin-top: 6px; display: flex; gap: 8px;">
          <input type="file" id="heroFileInput" accept="image/*" style="display: none;">
          <button type="button" class="btn btn-secondary" style="font-size: 12px; padding: 6px 12px; width: 100%; justify-content: center;" onclick="document.getElementById('heroFileInput').click()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            آپلود تصویر از کامپیوتر
          </button>
        </div>
        <div class="hero-thumb-preview" id="heroThumbBox">
          <div class="hero-thumb-empty">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect>
              <circle cx="9" cy="9" r="2"></circle>
              <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
            </svg>
            <span>پیش‌نمایش تصویر شاخص</span>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label for="heroCaption">زیرنویس بالینی و تفسیر تصویر شاخص</label>
        <input type="text" id="heroCaption" class="form-control" placeholder="مثال: بازسازی سه‌بعدی مداخله ستون فقرات">
      </div>

      <div class="form-group">
        <label for="articleTags">برچسب‌ها و موضوعات کلیدی (با کاما جدا کنید)</label>
        <input type="text" id="articleTags" class="form-control" placeholder="دیسک کمر، لیزر درمانی، شاک‌ویو، ستون فقرات">
      </div>
    </aside>

    <!-- Center: Tiptap v2 Editor Studio -->
    <section class="cms-editor-container">
      
      <!-- Editor Toolbar -->
      <div class="editor-toolbar">
        
        <!-- Heading / Style Selector -->
        <div class="toolbar-group">
          <select id="toolHeadingSelect" class="tool-select">
            <option value="p">متن ساده (پاراگراف)</option>
            <option value="h2">تیتر اصلی بخش (H2)</option>
            <option value="h3">زیرعنوان بخش (H3)</option>
          </select>
        </div>

        <!-- Inline Formats -->
        <div class="toolbar-group">
          <button type="button" class="tool-btn" id="toolBold" title="ضخیم (Ctrl+B)">
            <strong>B</strong>
          </button>
          <button type="button" class="tool-btn" id="toolItalic" title="مورب (Ctrl+I)">
            <em>I</em>
          </button>
          <button type="button" class="tool-btn" id="toolUnderline" title="زیرخط (Ctrl+U)">
            <u>U</u>
          </button>
          <button type="button" class="tool-btn" id="toolStrike" title="خط‌خورده">
            <s>S</s>
          </button>
        </div>

        <!-- Lists -->
        <div class="toolbar-group">
          <button type="button" class="tool-btn" id="toolBulletList" title="لیست نشانه‌دار">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="8" y1="6" x2="21" y2="6"></line>
              <line x1="8" y1="12" x2="21" y2="12"></line>
              <line x1="8" y1="18" x2="21" y2="18"></line>
              <line x1="3" y1="6" x2="3.01" y2="6"></line>
              <line x1="3" y1="12" x2="3.01" y2="12"></line>
              <line x1="3" y1="18" x2="3.01" y2="18"></line>
            </svg>
          </button>
          <button type="button" class="tool-btn" id="toolOrderedList" title="لیست شماره‌دار">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="10" y1="6" x2="21" y2="6"></line>
              <line x1="10" y1="12" x2="21" y2="12"></line>
              <line x1="10" y1="18" x2="21" y2="18"></line>
              <path d="M4 6h1v4"></path>
              <path d="M4 10h2"></path>
              <path d="M6 18H4c0-1 2-2 2-3s-1-1.5-2-1"></path>
            </svg>
          </button>
          <button type="button" class="tool-btn" id="toolBlockquote" title="نقل‌قول بالینی">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"></path>
              <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"></path>
            </svg>
          </button>
        </div>

        <!-- Clinical Blocks Dropdown -->
        <div class="toolbar-group">
          <div class="tool-dropdown-wrap">
            <button type="button" class="clinical-callout-btn" id="btnCalloutDropdown">
              <span>🩺 کادرهای بالینی ویژه</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <div class="dropdown-content" id="calloutDropdownMenu">
              <div class="dropdown-item" onclick="insertClinicalCallout('warning')">
                <span style="color: #D97706;">⚠️</span>
                <span>باکس هشدار بالینی (Warning)</span>
              </div>
              <div class="dropdown-item" onclick="insertClinicalCallout('advice')">
                <span style="color: #059669;">🩺</span>
                <span>باکس توصیه پزشک معالج (Advice)</span>
              </div>
              <div class="dropdown-item" onclick="insertClinicalCallout('protocol')">
                <span style="color: #0284C7;">ℹ️</span>
                <span>باکس پروتکل تریاژ و ارجاع (Protocol)</span>
              </div>
              <div class="dropdown-item" onclick="insertDoctorQuote()">
                <span style="color: #7C3AED;">💬</span>
                <span>نقل‌قول رسمی پزشک با مشخصات</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Media & Insertions -->
        <div class="toolbar-group">
          <button type="button" class="tool-btn" id="toolInsertImage" title="درج تصویر بالینی با کپشن">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect>
              <circle cx="9" cy="9" r="2"></circle>
              <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
            </svg>
          </button>
          <button type="button" class="tool-btn" id="toolInsertLink" title="درج پیوند اینترنتی">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
              <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
            </svg>
          </button>
          <button type="button" class="tool-btn" id="toolInsertHR" title="خط جداکننده بالینی">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="3" y1="12" x2="21" y2="12"></line>
            </svg>
          </button>
        </div>

        <!-- Undo / Redo -->
        <div class="toolbar-group">
          <button type="button" class="tool-btn" id="toolUndo" title="واگرد (Ctrl+Z)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 7v6h6"></path>
              <path d="M21 17a9 9 0 0 0-9-9 9 9 0 0 0-6 2.3L3 13"></path>
            </svg>
          </button>
          <button type="button" class="tool-btn" id="toolRedo" title="بازگرد (Ctrl+Y)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 7v6h-6"></path>
              <path d="M3 17a9 9 0 0 1 9-9 9 9 0 0 1 6 2.3l3 2.7"></path>
            </svg>
          </button>
        </div>

      </div>

      <!-- Editor Canvas -->
      <div class="editor-canvas">
        <div id="tiptapEditor"></div>
      </div>

      <!-- Bottom Status Bar -->
      <div class="editor-status-bar">
        <div class="status-left">
          <span>تعداد کلمات: <strong id="statWordCount">۰</strong></span>
          <span>تعداد کاراکتر: <strong id="statCharCount">۰</strong></span>
          <span>زمان مطالعه تخمینی: <strong id="statCalcReadTime">۱ دقیقه</strong></span>
        </div>
        <div class="status-right">
          <span class="status-badge" id="statusSaveBadge">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            ذخیره‌سازی خودکار فعال است
          </span>
        </div>
      </div>

    </section>

  </main>

  <!-- Image Insertion Modal -->
  <div class="img-modal-overlay" id="imgModal">
    <div class="img-modal-box">
      <div class="img-modal-title">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
        درج تصویر در متن مقاله
      </div>
      
      <div class="form-group">
        <label>انتخاب فایل تصویر از کامپیوتر</label>
        <input type="file" id="modalImgFile" accept="image/*" class="form-control">
      </div>

      <div class="form-group">
        <label>یا درج آدرس مستقیم تصویر (URL)</label>
        <input type="text" id="modalImgUrl" class="form-control" placeholder="https://..." dir="ltr">
      </div>

      <div class="form-group">
        <label>زیرنویس بالینی و توضیح تصویر (Caption)</label>
        <input type="text" id="modalImgCaption" class="form-control" placeholder="مثال: نمای میکروسکوپی سلول‌های بنیادی...">
      </div>

      <div class="form-group">
        <label>اندازه و چینش تصویر در صفحه</label>
        <select id="modalImgSize" class="form-control">
          <option value="normal">اندازه استاندارد (هم‌عرض متن)</option>
          <option value="wide">حالت عریض (Wide View)</option>
          <option value="full">تمام‌عرض (Full Bleed)</option>
        </select>
      </div>

      <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 20px;">
        <button type="button" class="btn btn-secondary" onclick="closeImgModal()">انصراف</button>
        <button type="button" class="btn btn-primary" id="btnConfirmInsertImg">درج تصویر در مقاله</button>
      </div>
    </div>
  </div>

  <!-- Live Magazine Preview Modal -->
  <div class="preview-modal-overlay" id="previewModal">
    <div class="preview-modal-card">
      <div class="preview-modal-header">
        <h3>پیش‌نمایش بالینی مقاله (استایل Day Mode مجله اکسون‌لایف)</h3>
        <button type="button" class="btn btn-secondary" onclick="closePreviewModal()">بستن پیش‌نمایش</button>
      </div>
      <div class="preview-modal-body" id="previewModalContent">
        <!-- Rendered live article preview -->
      </div>
    </div>
  </div>

  <!-- Toast Notification -->
  <div class="toast-msg" id="toastMsg">
    <span id="toastIcon">✅</span>
    <span id="toastText">عملیات با موفقیت انجام شد</span>
  </div>

  <script>
    // Embedded Data from Pezeshkan Magazine
    const PILLARS_DATA = {pillars_json_str};
    const DOCTORS_DATA = {doctors_json_str};
    const ARTICLES_DATA = {articles_json_str};

    let editorInstance = null;

    // Toast Helper
    function showToast(text, icon = '✅') {{
      const toast = document.getElementById('toastMsg');
      document.getElementById('toastText').innerText = text;
      document.getElementById('toastIcon').innerText = icon;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 3500);
    }}

    // CleanPaste Normalizer: Intelligent Persian & Typography Sanitization
    function cleanAndNormalizeHTML(rawHtml) {{
      if (!rawHtml) return '';
      
      let cleaned = rawHtml;

      // 1. Strip inline font and color styles (dirty paste from Word or foreign sites)
      cleaned = cleaned.replace(/style="[^"]*"/gi, '');
      cleaned = cleaned.replace(/class="Mso[^"]*"/gi, '');
      cleaned = cleaned.replace(/<font[^>]*>/gi, '');
      cleaned = cleaned.replace(/<\\/font>/gi, '');
      cleaned = cleaned.replace(/<span\s*>(.*?)<\\/span>/gi, '$1');

      // 2. Convert Arabic characters to standard Persian
      cleaned = cleaned.replace(/ي/g, 'ی');
      cleaned = cleaned.replace(/ك/g, 'ک');
      cleaned = cleaned.replace(/ة/g, 'ه');
      cleaned = cleaned.replace(/ؤ/g, 'و');

      // 3. Normalize Persian Half-Spaces (ZWNJ - \\u200c) for prefixes & suffixes
      // Prefixes: می and نمی
      cleaned = cleaned.replace(/(^|[\\s،.؛!؟])(می|نمی)\\s+([آ-ی])/g, '$1$2\\u200c$3');
      // Suffixes: ها, های, تر, ترین, هایش, هایمان, هایتان, هایشان
      cleaned = cleaned.replace(/([آ-ی])\\s+(ها|های|تر|ترین|ای|ام|ات|اش|مان|تان|شان)(?=[\\s،.؛!؟]|$)/g, '$1\\u200c$2');

      // 4. Remove multiple spaces and empty lines
      cleaned = cleaned.replace(/[ \\t]{{2,}}/g, ' ');
      cleaned = cleaned.replace(/(<p>\\s*(<br\\s*\\/?>)?\\s*<\\/p>\\s*){{2,}}/gi, '<p><br></p>');

      return cleaned;
    }}

    // Populate Selects
    function initSelectors() {{
      const pillarSelect = document.getElementById('pillarSelect');
      const branchSelect = document.getElementById('branchSelect');
      const doctorSelect = document.getElementById('doctorSelect');
      const articleSelect = document.getElementById('selectExistingArticle');

      // Fill Pillars
      PILLARS_DATA.forEach(p => {{
        const opt = document.createElement('option');
        opt.value = p.slug;
        opt.textContent = p.name;
        pillarSelect.appendChild(opt);
      }});

      // Populate branches when pillar changes
      function updateBranches() {{
        branchSelect.innerHTML = '';
        const currentPillarSlug = pillarSelect.value;
        const found = PILLARS_DATA.find(p => p.slug === currentPillarSlug) || PILLARS_DATA[0];
        if (found && found.branches) {{
          found.branches.forEach(b => {{
            const opt = document.createElement('option');
            opt.value = b.slug;
            opt.textContent = b.title;
            branchSelect.appendChild(opt);
          }});
        }}
      }}
      pillarSelect.addEventListener('change', updateBranches);
      updateBranches();

      // Fill Doctors
      DOCTORS_DATA.forEach(d => {{
        const opt = document.createElement('option');
        opt.value = d.id;
        opt.textContent = `${{d.name}} (${{d.title}})`;
        doctorSelect.appendChild(opt);
      }});

      function updateDoctorBadge() {{
        const docId = doctorSelect.value;
        const doc = DOCTORS_DATA.find(d => d.id === docId) || DOCTORS_DATA[0];
        const preview = document.getElementById('doctorBadgePreview');
        if (doc) {{
          preview.innerHTML = `
            <div style="font-weight: 700; color: #0F172A;">${{doc.name}}</div>
            <div style="color: #64748B;">${{doc.title}}</div>
            <div class="doctor-mc-pill">شماره نظام پزشکی: ${{doc.mcNumber}}</div>
          `;
        }}
      }}
      doctorSelect.addEventListener('change', updateDoctorBadge);
      updateDoctorBadge();

      // Fill Existing Articles
      ARTICLES_DATA.forEach((art, idx) => {{
        const opt = document.createElement('option');
        opt.value = idx;
        opt.textContent = `مقاله ${{idx + 1}}: ${{art.title.substring(0, 50)}}...`;
        articleSelect.appendChild(opt);
      }});

      articleSelect.addEventListener('change', (e) => {{
        if (e.target.value === 'new') {{
          resetToEmptyArticle();
        }} else {{
          loadArticleData(ARTICLES_DATA[parseInt(e.target.value)]);
        }}
      }});
    }}

    // Reset to empty article
    function resetToEmptyArticle() {{
      document.getElementById('articleTitle').value = '';
      document.getElementById('articleSlug').value = '';
      document.getElementById('articleSummary').value = '';
      document.getElementById('readTime').value = '۵ دقیقه';
      document.getElementById('heroImageUrl').value = '';
      document.getElementById('heroCaption').value = '';
      document.getElementById('articleTags').value = '';
      updateHeroThumb('');
      if (editorInstance) {{
        editorInstance.commands.setContent('<p>محتوای تخصصی مقاله را اینجا آغاز کنید یا برای درج کادرهای بالینی از نوار ابزار بالا استفاده نمایید...</p>');
      }}
      showToast('فرم مقاله جدید ایجاد شد', '📝');
    }}

    // Load an existing article into editor
    function loadArticleData(art) {{
      document.getElementById('articleTitle').value = art.title || '';
      document.getElementById('articleSlug').value = art.slug || '';
      document.getElementById('articleSummary').value = art.summary || '';
      document.getElementById('readTime').value = art.readTime || '۷ دقیقه';
      document.getElementById('articleTags').value = (art.tags || []).join('، ');

      if (art.pillarSlug) {{
        const pillarSelect = document.getElementById('pillarSelect');
        pillarSelect.value = art.pillarSlug;
        pillarSelect.dispatchEvent(new Event('change'));
      }}

      // Build initial HTML from article sections
      let contentHtml = '';
      if (art.sections && art.sections.length) {{
        art.sections.forEach(sec => {{
          if (sec.heading) {{
            contentHtml += `<h2>${{sec.heading}}</h2>`;
          }}
          if (sec.body) {{
            contentHtml += `<p>${{sec.body}}</p>`;
          }}
          if (sec.callout) {{
            contentHtml += `
              <div class="clinical-callout advice">
                <div class="callout-header">🩺 توصیه بالینی پزشک معالج</div>
                <div class="callout-content">${{sec.callout}}</div>
              </div>
            `;
          }}
          if (sec.warning) {{
            contentHtml += `
              <div class="clinical-callout warning">
                <div class="callout-header">⚠️ هشدار بالینی و احتیاط دارویی</div>
                <div class="callout-content">${{sec.warning}}</div>
              </div>
            `;
          }}
        }});
      }} else {{
        contentHtml = '<p>محتوای اولیه مقاله در دسترس نیست.</p>';
      }}

      if (editorInstance) {{
        editorInstance.commands.setContent(contentHtml);
      }}

      // Update doctor if matching
      if (art.author && art.author.name) {{
        const docOpt = DOCTORS_DATA.find(d => d.name === art.author.name);
        if (docOpt) {{
          document.getElementById('doctorSelect').value = docOpt.id;
          document.getElementById('doctorSelect').dispatchEvent(new Event('change'));
        }}
      }}

      updateHeroThumb('');
      showToast('مقاله با موفقیت در ویرایشگر بارگذاری شد', '📖');
      updateStats();
    }}

    // Hero Image Thumbnail updater
    function updateHeroThumb(url) {{
      const box = document.getElementById('heroThumbBox');
      if (url && url.trim()) {{
        box.innerHTML = `<img src="${{url}}" alt="Hero" onerror="this.onerror=null; this.parentElement.innerHTML='<span style=\\'color:#E11D48;font-size:11px;\\'>خطا در بارگذاری تصویر</span>'">`;
      }} else {{
        box.innerHTML = `
          <div class="hero-thumb-empty">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect>
              <circle cx="9" cy="9" r="2"></circle>
              <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
            </svg>
            <span>پیش‌نمایش تصویر شاخص</span>
          </div>
        `;
      }}
    }}
    document.getElementById('heroImageUrl').addEventListener('input', (e) => updateHeroThumb(e.target.value));

    // Handle Hero Local File Upload (FileReader -> Base64)
    document.getElementById('heroFileInput').addEventListener('change', function(e) {{
      if (e.target.files && e.target.files[0]) {{
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = function(evt) {{
          const b64 = evt.target.result;
          document.getElementById('heroImageUrl').value = b64;
          updateHeroThumb(b64);
          showToast('تصویر شاخص بارگذاری و ذخیره شد', '🖼️');
        }};
        reader.readAsDataURL(file);
      }}
    }});

    // Initialize Tiptap Editor
    function initTiptapEditor() {{
      const Tiptap = window.TiptapCore;
      if (!Tiptap) {{
        console.error('TiptapCore bundle not loaded');
        return;
      }}

      const {{ Editor, StarterKit, Image, Link, Placeholder, Underline }} = Tiptap;

      editorInstance = new Editor({{
        element: document.getElementById('tiptapEditor'),
        extensions: [
          StarterKit.configure({{
            heading: {{ levels: [2, 3] }}
          }}),
          Underline,
          Link.configure({{
            openOnClick: false,
            HTMLAttributes: {{ target: '_blank', rel: 'noopener noreferrer' }}
          }}),
          Placeholder.configure({{
            placeholder: 'محتوای مقاله را اینجا بنویسید یا متن خود را از نرم‌افزار Word / وب در این بخش Paste نمایید...'
          }}),
          Image.configure({{
            inline: false,
            allowBase64: true
          }})
        ],
        content: `
          <h2>درمان‌های نوین غیرجراحی در دردهای مزمن ستون فقرات</h2>
          <p>امروزه با پیشرفت‌های چشمگیر در حوزه طب فیزیکی و اینترونشنال، بیش از ۹۰ درصد بیماران مبتلا به فتق دیسک کمر و علائم سیاتیک، بدون نیاز به انجام جراحی‌های باز سنگین درمان می‌شوند.</p>
          <div class="clinical-callout advice">
            <div class="callout-header">🩺 توصیه بالینی پزشک معالج</div>
            <div class="callout-content">در صورت بروز درد تیرکشنده به اندام تحتانی، پیش از شروع هرگونه داروی مسکن سنگین، ارزیابی ام‌آر‌آی و معاینه بالینی دقیق توسط متخصص الزامی است.</div>
          </div>
          <h3>نقش شاک‌ویو و لیزر پرتوان در تسریع ترمیم بافتی</h3>
          <p>شاک‌ویوتراپی با ایجاد امواج صوتی پرانرژی، فرآیند رگزایی نوین (Angiogenesis) را در نواحی دچار التهاب مزمن فعال می‌سازد و زمان بازگشت بیمار به فعالیت‌های روزمره را به شکل محسوسی کاهش می‌دهد.</p>
        `,
        editorProps: {{
          attributes: {{
            dir: 'rtl'
          }},
          handlePaste: (view, event, slice) => {{
            // Custom paste handler can trigger clean paste
            return false; // let tiptap handle it, then clean button or auto-normalizer cleans it
          }}
        }},
        onUpdate: () => {{
          updateStats();
          triggerAutoSave();
        }}
      }});

      // Connect Toolbar Buttons to Tiptap Commands
      document.getElementById('toolBold').addEventListener('click', () => editorInstance.chain().focus().toggleBold().run());
      document.getElementById('toolItalic').addEventListener('click', () => editorInstance.chain().focus().toggleItalic().run());
      document.getElementById('toolUnderline').addEventListener('click', () => editorInstance.chain().focus().toggleUnderline().run());
      document.getElementById('toolStrike').addEventListener('click', () => editorInstance.chain().focus().toggleStrike().run());
      document.getElementById('toolBulletList').addEventListener('click', () => editorInstance.chain().focus().toggleBulletList().run());
      document.getElementById('toolOrderedList').addEventListener('click', () => editorInstance.chain().focus().toggleOrderedList().run());
      document.getElementById('toolBlockquote').addEventListener('click', () => editorInstance.chain().focus().toggleBlockquote().run());
      document.getElementById('toolInsertHR').addEventListener('click', () => editorInstance.chain().focus().setHorizontalRule().run());
      document.getElementById('toolUndo').addEventListener('click', () => editorInstance.chain().focus().undo().run());
      document.getElementById('toolRedo').addEventListener('click', () => editorInstance.chain().focus().redo().run());

      // Heading selector
      document.getElementById('toolHeadingSelect').addEventListener('change', (e) => {{
        const val = e.target.value;
        if (val === 'h2') {{
          editorInstance.chain().focus().toggleHeading({{ level: 2 }}).run();
        }} else if (val === 'h3') {{
          editorInstance.chain().focus().toggleHeading({{ level: 3 }}).run();
        }} else {{
          editorInstance.chain().focus().setParagraph().run();
        }}
      }});

      // Link insertion
      document.getElementById('toolInsertLink').addEventListener('click', () => {{
        const previousUrl = editorInstance.getAttributes('link').href;
        const url = window.prompt('نشانی اینترنتی معتبر را وارد کنید:', previousUrl || 'https://');
        if (url === null) return;
        if (url === '') {{
          editorInstance.chain().focus().extendMarkRange('link').unsetLink().run();
          return;
        }}
        editorInstance.chain().focus().extendMarkRange('link').setLink({{ href: url }}).run();
      }});

      // Image modal opener
      document.getElementById('toolInsertImage').addEventListener('click', () => {{
        document.getElementById('imgModal').classList.add('active');
      }});

      updateStats();
    }}

    // Insert Clinical Callouts
    window.insertClinicalCallout = function(type) {{
      const menu = document.getElementById('calloutDropdownMenu');
      menu.classList.remove('show');

      let header = '⚠️ هشدار بالینی و احتیاط دارویی';
      let content = 'متن هشدار یا تداخلات احتمالی دارویی را اینجا وارد کنید...';

      if (type === 'advice') {{
        header = '🩺 توصیه بالینی پزشک معالج';
        content = 'توصیه‌های پیشگیرانه و اقدامات تشخیصی لازم...';
      }} else if (type === 'protocol') {{
        header = 'ℹ️ پروتکل تریاژ و ارجاع فوری';
        content = 'در صورت مشاهده علائم خطر (Red Flags) فورا به مرکز درمانی مراجعه نمایید.';
      }}

      const html = `
        <div class="clinical-callout ${{type}}">
          <div class="callout-header">${{header}}</div>
          <div class="callout-content">${{content}}</div>
        </div>
        <p></p>
      `;

      if (editorInstance) {{
        editorInstance.chain().focus().insertContent(html).run();
        showToast('کادر بالینی با موفقیت افزوده شد', '🩺');
      }}
    }};

    // Insert Doctor Quote
    window.insertDoctorQuote = function() {{
      const menu = document.getElementById('calloutDropdownMenu');
      menu.classList.remove('show');

      const docId = document.getElementById('doctorSelect').value;
      const doc = DOCTORS_DATA.find(d => d.id === docId) || DOCTORS_DATA[0];

      const html = `
        <blockquote class="doctor-quote-block">
          <div class="quote-text">«نقل‌قول بالینی پزشک متخصص درباره اهمیت پیگیری به‌موقع درمان و مراقبت‌های دارویی...»</div>
          <div class="quote-author-info">
            <span class="quote-author-name">${{doc.name}}</span>
            <span>—</span>
            <span>${{doc.title}} (کد نظام پزشکی: ${{doc.mcNumber}})</span>
          </div>
        </blockquote>
        <p></p>
      `;

      if (editorInstance) {{
        editorInstance.chain().focus().insertContent(html).run();
        showToast('نقل‌قول بالینی پزشک درج شد', '💬');
      }}
    }};

    // Callout dropdown toggler
    document.getElementById('btnCalloutDropdown').addEventListener('click', (e) => {{
      e.stopPropagation();
      document.getElementById('calloutDropdownMenu').classList.toggle('show');
    }});
    document.addEventListener('click', () => {{
      document.getElementById('calloutDropdownMenu').classList.remove('show');
    }});

    // Close image modal
    window.closeImgModal = function() {{
      document.getElementById('imgModal').classList.remove('active');
    }};

    // Confirm image insertion
    document.getElementById('btnConfirmInsertImg').addEventListener('click', () => {{
      const urlInput = document.getElementById('modalImgUrl').value.trim();
      const fileInput = document.getElementById('modalImgFile');
      const caption = document.getElementById('modalImgCaption').value.trim();
      const size = document.getElementById('modalImgSize').value;

      function doInsert(src) {{
        if (!src) return;
        let figHtml = `
          <figure class="clinical-img-figure size-${{size}}">
            <img src="${{src}}" alt="${{caption || 'تصویر بالینی'}}">
            ${{caption ? `<figcaption class="clinical-img-caption"><span>📷</span> <span>${{caption}}</span></figcaption>` : ''}}
          </figure>
          <p></p>
        `;
        editorInstance.chain().focus().insertContent(figHtml).run();
        closeImgModal();
        showToast('تصویر بالینی در متن قرار گرفت', '🖼️');
      }}

      if (fileInput.files && fileInput.files[0]) {{
        const reader = new FileReader();
        reader.onload = (e) => doInsert(e.target.result);
        reader.readAsDataURL(fileInput.files[0]);
      }} else if (urlInput) {{
        doInsert(urlInput);
      }} else {{
        alert('لطفا فایل تصویر را انتخاب کرده یا نشانی URL آن را وارد نمایید.');
      }}
    }});

    // Update Statistics (words, characters, read time)
    function updateStats() {{
      if (!editorInstance) return;
      const text = editorInstance.getText();
      const charCount = text.length;
      const words = text.trim() ? text.trim().split(/\s+/).length : 0;
      
      document.getElementById('statWordCount').innerText = words.toLocaleString('fa-IR');
      document.getElementById('statCharCount').innerText = charCount.toLocaleString('fa-IR');

      const calcMinutes = Math.max(1, Math.ceil(words / 180));
      document.getElementById('statCalcReadTime').innerText = `${{calcMinutes.toLocaleString('fa-IR')}} دقیقه`;
    }}

    // Smart Clean & Normalize Button
    document.getElementById('btnSmartClean').addEventListener('click', () => {{
      if (!editorInstance) return;
      const currentHtml = editorInstance.getHTML();
      const cleaned = cleanAndNormalizeHTML(currentHtml);
      editorInstance.commands.setContent(cleaned);
      showToast('متن پاکسازی شد: فونت‌ها، ی/ک عربی و نیم‌فاصله‌ها اصلاح گردیدند', '✨');
    }});

    // Export Clean HTML
    document.getElementById('btnExportHTML').addEventListener('click', () => {{
      if (!editorInstance) return;
      const html = editorInstance.getHTML();
      navigator.clipboard.writeText(html).then(() => {{
        showToast('کد HTML استاندارد مقاله در حافظه کپی شد', '📋');
      }}).catch(() => {{
        prompt('کد HTML مقاله:', html);
      }});
    }});

    // Save Draft in LocalStorage
    let saveTimeout = null;
    function triggerAutoSave() {{
      clearTimeout(saveTimeout);
      saveTimeout = setTimeout(() => {{
        saveCurrentDraft(true);
      }}, 2500);
    }}

    function saveCurrentDraft(silent = false) {{
      if (!editorInstance) return;
      const draft = {{
        title: document.getElementById('articleTitle').value,
        slug: document.getElementById('articleSlug').value,
        summary: document.getElementById('articleSummary').value,
        pillarSlug: document.getElementById('pillarSelect').value,
        branchSlug: document.getElementById('branchSelect').value,
        doctorId: document.getElementById('doctorSelect').value,
        readTime: document.getElementById('readTime').value,
        heroImageUrl: document.getElementById('heroImageUrl').value,
        heroCaption: document.getElementById('heroCaption').value,
        tags: document.getElementById('articleTags').value,
        html: editorInstance.getHTML(),
        savedAt: new Date().toISOString()
      }};
      localStorage.setItem('pezeshkan_mag_cms_draft', JSON.stringify(draft));
      
      const badge = document.getElementById('statusSaveBadge');
      badge.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> آخرین ذخیره: ${{new Date().toLocaleTimeString('fa-IR')}}`;
      if (!silent) showToast('پیش‌نویس با موفقیت در سیستم ذخیره شد', '💾');
    }}

    document.getElementById('btnSaveDraft').addEventListener('click', () => saveCurrentDraft(false));

    // Live Magazine Preview Modal
    window.closePreviewModal = function() {{
      document.getElementById('previewModal').classList.remove('active');
    }};

    document.getElementById('btnOpenPreview').addEventListener('click', () => {{
      if (!editorInstance) return;
      const title = document.getElementById('articleTitle').value || 'عنوان پیش‌فرض مقاله بالینی';
      const summary = document.getElementById('articleSummary').value || 'چکیده و لید مقاله در این بخش نمایش داده خواهد شد.';
      const readTime = document.getElementById('readTime').value || '۵ دقیقه';
      const heroUrl = document.getElementById('heroImageUrl').value;
      const heroCaption = document.getElementById('heroCaption').value;
      const docId = document.getElementById('doctorSelect').value;
      const doc = DOCTORS_DATA.find(d => d.id === docId) || DOCTORS_DATA[0];
      const bodyHtml = editorInstance.getHTML();

      const modalContent = document.getElementById('previewModalContent');
      modalContent.innerHTML = `
        <article style="max-width: 820px; margin: 0 auto; color: #0F172A; font-family: var(--font-sans);">
          
          <!-- Clinical Trust Strip -->
          <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; padding: 12px 16px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; margin-bottom: 24px; font-size: 13px;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <span style="font-size: 20px;">👨‍⚕️</span>
              <div>
                <div style="font-weight: 700; color: #0F172A;">${{doc.name}}</div>
                <div style="font-size: 11.5px; color: #64748B;">${{doc.title}} • <span style="color: #0369A1; font-weight: 700;">نظام پزشکی: ${{doc.mcNumber}}</span></div>
              </div>
            </div>
            <div style="display: flex; align-items: center; gap: 12px; color: #64748B; font-size: 12px;">
              <span>⏱️ ${{readTime}}</span>
              <span style="background: #ECFDF5; color: #065F46; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">تاییدشده توسط هیئت تحریریه</span>
            </div>
          </div>

          <!-- Hero Title & Summary -->
          <h1 style="font-size: 26px; font-weight: 900; line-height: 1.5; color: #0F172A; margin-bottom: 14px;">${{title}}</h1>
          <p style="font-size: 16px; line-height: 1.9; color: #475569; margin-bottom: 24px; font-weight: 400; background: #F1F5F9; padding: 16px 20px; border-radius: 10px; border-right: 4px solid #0284C7;">
            ${{summary}}
          </p>

          <!-- Featured Hero Image -->
          ${{heroUrl ? `
            <figure style="margin: 24px 0; text-align: center;">
              <img src="${{heroUrl}}" alt="${{title}}" style="width: 100%; max-height: 380px; object-fit: cover; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06);">
              ${{heroCaption ? `<figcaption style="font-size: 12px; color: #64748B; margin-top: 8px;">📷 ${{heroCaption}}</figcaption>` : ''}}
            </figure>
          ` : ''}}

          <!-- Body Content from Tiptap -->
          <div class="ProseMirror" style="margin-top: 24px; font-size: 16px; line-height: 2;">
            ${{bodyHtml}}
          </div>

          <!-- Doctor Booking CTA Banner -->
          <div style="margin-top: 48px; padding: 28px; background: linear-gradient(135deg, #0284C7, #0D9488); border-radius: 16px; color: #FFFFFF; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 20px;">
            <div>
              <div style="font-size: 18px; font-weight: 800; margin-bottom: 4px;">از آگاهی تا درمان: مشاوره و ویزیت با ${{doc.name}}</div>
              <div style="font-size: 13px; opacity: 0.9;">امکان رزرو نوبت حضوری و مشاوره آنلاین تصویری در سامانه یکپارچه سلامت پزشکآن</div>
            </div>
            <a href="index.html" target="_blank" style="background: #FFFFFF; color: #0369A1; font-weight: 700; font-size: 13.5px; padding: 10px 22px; border-radius: 8px; text-decoration: none;">
              رزرو فوری نوبت
            </a>
          </div>

        </article>
      `;

      document.getElementById('previewModal').classList.add('active');
    }});

    // On Load
    window.addEventListener('DOMContentLoaded', () => {{
      initSelectors();
      initTiptapEditor();

      // Check if draft exists in localStorage
      const savedDraft = localStorage.getItem('pezeshkan_mag_cms_draft');
      if (savedDraft) {{
        try {{
          const parsed = JSON.parse(savedDraft);
          // If empty, offer to restore
          console.log('Found draft saved at:', parsed.savedAt);
        }} catch(e) {{}}
      }}
    }});
  </script>
</body>
</html>
'''

target_admin_path = os.path.join(MAG_DIR, "admin.html")
with open(target_admin_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated successfully: {target_admin_path} ({len(html_content)} bytes)")
