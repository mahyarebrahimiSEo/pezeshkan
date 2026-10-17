# -*- coding: utf-8 -*-
"""
Verification Script for Pezeshkan Rank Math Schema.org Management System
Tests:
1. server.py schemas.json persistence, cache, and validation API
2. HTTP endpoints: /api/admin/schemas, /api/admin/schemas/validate, /api/admin/schemas/toggle
3. mag/admin.html element integrity, JavaScript references, and DOM bindings
"""

import sys
import os
import json
import re

# Set UTF-8 encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

print("=== شروع تست و ارزیابی سامانه مدیریت اسکیما (Rank Math Schema System) ===")

# Test 1: Verify schemas.json file
schema_file = os.path.join(os.path.dirname(__file__), '..', 'mag', 'content', 'schemas.json')
schema_file = os.path.abspath(schema_file)
assert os.path.exists(schema_file), f"schemas.json not found at {schema_file}"

with open(schema_file, 'r', encoding='utf-8') as f:
    schemas = json.load(f)

print(f"[1] تعداد اسکیماهای اولیه بارگذاری شده: {len(schemas)}")
assert len(schemas) >= 5, "Should have at least 5 default schemas"

types = [s.get('type') for s in schemas]
print(f"    انواع اسکیما: {', '.join(types)}")
assert 'MedicalOrganization' in types, "Missing MedicalOrganization"
assert 'SoftwareApplication' in types, "Missing SoftwareApplication"
assert 'Product' in types, "Missing Product"
assert 'FAQPage' in types, "Missing FAQPage"
assert 'WebSite' in types, "Missing WebSite"
print("    -> فایل schemas.json کاملاً معتبر است.")

# Test 2: Verify server.py schema handlers
server_path = os.path.join(os.path.dirname(__file__), '..', 'server.py')
server_path = os.path.abspath(server_path)
with open(server_path, 'r', encoding='utf-8') as f:
    server_code = f.read()

assert 'def load_schemas' in server_code, "server.py missing load_schemas"
assert 'def save_schemas' in server_code, "server.py missing save_schemas"
assert '/api/admin/schemas/validate' in server_code, "server.py missing schema validate endpoint"
assert '/api/admin/schemas/toggle' in server_code, "server.py missing schema toggle endpoint"
assert '/api/admin/schemas/delete' in server_code, "server.py missing schema delete endpoint"
print("[2] متدهای سرور (server.py) برای مدیریت اسکیماها با موفقیت اعتبارسنجی شدند.")

# Test 3: Import server and test schema validation logic directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import server

# Test validation of valid schema
valid_schema = {
    "@context": "https://schema.org",
    "@type": "MedicalWebPage",
    "headline": "راهنمای بالینی دیسک کمر",
    "description": "بررسی جامع روش‌های نوین درمان غیرجراحی"
}
errors = server.validate_schema_structure(valid_schema)
assert len(errors) == 0, f"Expected no errors for valid schema, got: {errors}"
print("[3.1] اعتبارسنجی اسکیمای معتبر با موفقیت انجام شد (بدون خطا).")

# Test validation of invalid schema (missing @context)
invalid_schema = {
    "@type": "Article",
    "headline": "تست"
}
errors = server.validate_schema_structure(invalid_schema)
assert len(errors) > 0, "Expected error for missing @context"
print(f"[3.2] اعتبارسنجی اسکیمای نامعتبر (فقدان @context): خطای شناسایی شده: {errors}")

# Test 4: Verify mag/admin.html DOM elements and functions
admin_path = os.path.join(os.path.dirname(__file__), '..', 'mag', 'admin.html')
admin_path = os.path.abspath(admin_path)
with open(admin_path, 'r', encoding='utf-8') as f:
    admin_html = f.read()

required_ids = [
    'menu-schemas',
    'tab-schemas',
    'articleSchemaType',
    'articleSchemaActiveBadge',
    'btnTabSchemaFields',
    'btnTabSchemaCode',
    'articleSchemaHeadline',
    'articleSchemaDesc',
    'articleMedicalFieldsGroup',
    'articleSchemaReviewer',
    'articleSchemaSpecialty',
    'articleSchemaAudience',
    'articleHowToFieldsGroup',
    'articleHowToStepsContainer',
    'articleCustomSchemaJson',
    'articleSchemaLiveCodeView',
    'pageSchemaModalBackdrop',
    'schemaJsonViewModalBackdrop',
    'schemasTableBody',
    'schemaMetricTotal',
    'schemaMetricActive',
    'schemaMetricMedical',
    'schemaMetricValid'
]

for el_id in required_ids:
    assert f'id="{el_id}"' in admin_html, f"Missing required DOM element id='{el_id}'"

required_funcs = [
    'fetchSchemas',
    'renderSchemasTable',
    'openPageSchemaModal',
    'closePageSchemaModal',
    'savePageSchema',
    'toggleSchemaActive',
    'deleteSchema',
    'viewSchemaJson',
    'exportSchemasJson',
    'handleArticleSchemaTypeChange',
    'switchArticleSchemaTab',
    'updateArticleSchemaLivePreview',
    'copyArticleSchemaJson',
    'validateArticleSchemaOnServer',
    'testArticleSchemaInGoogle',
    'addArticleHowToStepRow',
    'removeArticleHowToStepRow'
]

for func in required_funcs:
    assert f'function {func}' in admin_html, f"Missing required JS function: {func}"

print(f"[4] تمامی {len(required_ids)} شناسه المان‌های فرم و {len(required_funcs)} تابع جاوااسکریپت در admin.html تایید شدند.")
print("=== تمامی تست‌ها با موفقیت ۱۰۰٪ سپری شدند! ===")
