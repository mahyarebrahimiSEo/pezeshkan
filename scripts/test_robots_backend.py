import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import analyze_robots_txt, BASE_DIR

def run_tests():
    print("=== Testing Robots.txt Intelligence & Audit Engine ===")
    
    # Test 1: Real Pezeshkan robots.txt
    real_path = os.path.join(BASE_DIR, "robots.txt")
    with open(real_path, "r", encoding="utf-8") as f:
        real_content = f.read()
    
    res1 = analyze_robots_txt(real_content)
    print(f"Test 1 - Official robots.txt: Score={res1['score']}, Suitable={res1['isSuitable']}, Verdict='{res1['verdict']}'")
    assert res1["score"] >= 90, f"Expected >= 90, got {res1['score']}"
    assert res1["isSuitable"] is True
    assert res1["verdictType"] == "optimal"
    
    # Test 2: Catastrophic Disallow: /
    bad_content = """
User-agent: *
Disallow: /
"""
    res2 = analyze_robots_txt(bad_content)
    print(f"Test 2 - Fatal Disallow: /: Score={res2['score']}, Suitable={res2['isSuitable']}, Verdict='{res2['verdict']}'")
    assert res2["isSuitable"] is False
    assert res2["score"] <= 40
    assert any(c["id"] == "blanket_disallow" and c["status"] == "fail" for c in res2["checks"])
    assert any(c["id"] == "sitemap_declaration" and c["status"] == "fail" for c in res2["checks"])
    
    # Test 3: Blocking CSS/JS rendering
    css_block = """
User-agent: *
Disallow: /shared.css
Disallow: /shared.js
Disallow: /fonts/
Sitemap: https://pezeshkan.me/sitemap.xml
"""
    res3 = analyze_robots_txt(css_block)
    print(f"Test 3 - CSS/JS blocked: Score={res3['score']}, Status={res3['verdictType']}")
    assert any(c["id"] == "rendering_assets" and c["status"] == "fail" for c in res3["checks"])
    
    # Test 4: HTTP Sitemap warning
    http_sitemap = """
User-agent: *
Allow: /
Disallow: /admin
Disallow: /login
Disallow: /api/
Disallow: /*.json$
Allow: /shared.css
Allow: /shared.js
Allow: /fonts/
Sitemap: http://pezeshkan.me/sitemap.xml
"""
    res4 = analyze_robots_txt(http_sitemap)
    print(f"Test 4 - HTTP Sitemap: Score={res4['score']}, Checks={len(res4['checks'])}")
    assert any(c["id"] == "sitemap_declaration" and c["status"] == "warn" for c in res4["checks"])
    
    # Test 5: Empty Content
    res5 = analyze_robots_txt("")
    print(f"Test 5 - Empty Content: Score={res5['score']}, Suitable={res5['isSuitable']}")
    assert res5["score"] == 0
    assert res5["isSuitable"] is False
    
    # Test 6: Syntax Error
    syntax_error_content = """
User-agent: *
Allow /invalid-line-without-colon
Sitemap: https://pezeshkan.me/sitemap.xml
"""
    res6 = analyze_robots_txt(syntax_error_content)
    print(f"Test 6 - Syntax Error: Score={res6['score']}")
    assert any(c["id"] == "syntax_errors" and c["status"] == "fail" for c in res6["checks"])

    print("\nALL 6 ROBOTS.TXT INTELLIGENCE AUDIT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
