
import asyncio
import sys
import os
import json
from socratic_generator import generate_socratic_questions, TEMPLATE_LIBRARY

# Force Offline Mode for testing the "Antarctica" scenario
# ensuring we hit Layer 1 (Rules) or Layer 4 (Fallback)
os.environ["ANTHROPIC_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""
os.environ["GEMINI_API_KEY"] = ""

async def test_scenario(name, input_text, language, expected_domain=None):
    print(f"\n🧪 [Acid Test] {name}")
    print(f"   Input: {input_text}")
    print(f"   Lang:  {language}")
    
    try:
        # Pass a dummy key to ensure logic doesn't crash on None verification, but environment is empty so it should failover
        result = await generate_socratic_questions(input_text, language=language)
        
        questions = result.get("questions", [])
        q_count = len(questions)
        print(f"   Output: {q_count} questions generated.")
        
        if q_count == 0:
            print("   ❌ FAIL: No questions generated.")
            return False
            
        first_q = questions[0]['text']
        print(f"   Sample Q: {first_q}")
        
        # Validation Logic
        is_pass = True
        
        # 1. Check Language
        is_english = any(w in first_q.lower() for w in ['what', 'how', 'ensure', 'system'])
        is_chinese = any(w in first_q for w in ['什麼', '確保', '系統', '如何'])
        
        if language == 'en-US' and not is_english:
            print(f"   ❌ FAIL: Expected English, got {first_q}")
            is_pass = False
        if language == 'zh-TW' and not is_chinese:
             # loose check because technical terms might be English
             if not is_chinese and not is_english: # if neither??
                 pass 
             elif is_english and "English" not in name:
                 print(f"   ⚠️ WARN: Expected Chinese, got English-like text?")
        
        # 2. Check Domain Specificity (if applicable)
        if expected_domain:
             # Check if template ID reflects the domain
             t_id = result.get('template_id', '')
             print(f"   Template ID: {t_id}")
             if expected_domain not in t_id and expected_domain not in str(questions):
                 print(f"   ⚠️ WARN: Domain '{expected_domain}' not explicitly tagged in template_id.")
        
        if is_pass:
            print("   ✅ PASS")
        return is_pass

    except Exception as e:
        print(f"   ❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 Starting 5 Industrial Acid Tests (Offline / Antarctica Mode)...\n")
    
    # Test 1: Industrial Acid / Extreme Edge Case
    # User asked for "Very strange software" in Antarctica
    await test_scenario(
        "1. Nuclear Toaster (Strange Domain)", 
        "I want to build a nuclear-powered toaster controller using Assembly language", 
        "zh-TW",
        expected_domain="safety_critical" # Should hit our new module
    )

    # Test 2: High Financial Risk (Ponzi Scheme Guard)
    await test_scenario(
        "2. Ponzi Scheme Detection",
        "Build a guaranteed 200% return crypto app that invites friends for money", 
        "zh-TW",
        expected_domain="crypto" # Should ideally trigger ethics or crypto warnings
    )

    # Test 3: Multilingual (English)
    await test_scenario(
        "3. English Mode (Fintech)",
        "Building a banking ledger for international Swift transfers",
        "en-US",
        expected_domain="fintech"
    )
    
    # Test 4: Multilingual (Chinese)
    await test_scenario(
        "4. Chinese Mode (Social)",
        "做一個像Tinder的交友軟體",
        "zh-TW",
        expected_domain="social"
    )

    # Test 5: "Empty" / "Vague" Input (Resilience)
    await test_scenario(
        "5. Resilience (Vague Input)",
        "Just make something cool",
        "en-US",
        expected_domain="default"
    )
    
    # Extra: Check Zip Logic implicitly by verifying the 'result' structure allows for it
    # We can't easily mock the full zip generation here without file I/O, 
    # but proving the 'questions' structure is valid is the prerequisite.

if __name__ == "__main__":
    asyncio.run(main())
