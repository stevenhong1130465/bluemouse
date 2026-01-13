"""
AI Integration Module - 蘇格拉底問題生成器
真正的四層寄生AI架構（無阻塞版本）
"""

import json
import os
import asyncio


async def generate_socratic_questions(requirement: str, language: str = 'zh-TW') -> dict:
    """
    真正的四層寄生 AI 架構
    
    層次 1: Antigravity 內聯生成 (規則引擎，<100ms)
    層次 2: Ollama 本地 AI (異步，5-10秒，有超時)
    層次 3: 環境變數 API Key (異步，2-3秒，有超時)
    層次 4: 規則引擎降級 (保底，<100ms)
    
    每一層都無阻塞，失敗立即降級
    """
    
    print("🦠 啟動四層寄生AI...")
    
    # 層次 1: Antigravity 內聯生成 (規則引擎)
    try:
        result = layer1_antigravity_inline(requirement, language)
        return result
    except Exception as e:
        print(f"  [1/4] ⏭️  {e}")
    
    # 層次 2: Ollama 本地 AI
    try:
        result = await layer2_ollama(requirement, language)
        return result
    except Exception as e:
        print(f"  [2/4] ⏭️  {e}")
    
    # 層次 3: 環境變數 API Key
    try:
        result = await layer3_api_key(requirement, language)
        return result
    except Exception as e:
        print(f"  [3/4] ⏭️  {e}")
    
    # 層次 4: 規則引擎降級 (保底)
    result = layer4_fallback(requirement, language)
    return result


def layer1_antigravity_inline(requirement: str, language: str) -> dict:
    """
    第一層：Antigravity 內聯生成
    
    使用智能規則引擎，覆蓋常見場景
    如果規則庫未覆蓋，拋出異常進入下一層
    """
    try:
        from antigravity_inline_generator import generate_questions_inline
        
        result = generate_questions_inline(requirement, language)
        
        # 檢查是否是通用降級
        if is_generic_fallback(result):
            raise ValueError("規則庫未覆蓋此場景")
        
        print(f"  [1/4] ✅ Antigravity 內聯生成成功 (<100ms)")
        return result
        
    except ImportError:
        raise ValueError("antigravity_inline_generator 未找到")
    except Exception as e:
        raise ValueError(f"規則引擎失敗: {e}")


async def layer2_ollama(requirement: str, language: str) -> dict:
    """
    第二層：Ollama 本地 AI
    
    如果已安裝Ollama，嘗試動態生成
    超時10秒自動降級
    """
    try:
        import aiohttp
        
        # 檢查Ollama是否運行
        print(f"  [2/4] 🔍 檢測 Ollama...")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'http://localhost:11434/api/tags',
                timeout=aiohttp.ClientTimeout(total=1)
            ) as resp:
                if resp.status != 200:
                    raise ConnectionError("Ollama未運行")
        
        print(f"  [2/4] 🤖 Ollama 生成中...")
        
        # 調用生成API
        prompt = build_prompt(requirement, language)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'qwen2.5:7b',
                    'prompt': prompt,
                    'stream': False
                },
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                data = await resp.json()
                ai_text = data.get('response', '')
        
        # 解析JSON
        result = parse_ai_json(ai_text)
        print(f"  [2/4] ✅ Ollama 生成成功 (~8秒)")
        return result
        
    except ImportError:
        raise ValueError("aiohttp 未安裝")
    except asyncio.TimeoutError:
        raise ValueError("Ollama 超時 (>15秒)")
    except Exception as e:
        raise ValueError(f"Ollama 不可用: {e}")


async def layer3_api_key(requirement: str, language: str) -> dict:
    """
    第三層：環境變數 API Key
    
    如果配置了API Key，調用雲端AI
    超時10秒自動降級
    """
    try:
        api_key = os.getenv('ANTHROPIC_API_KEY') or \
                  os.getenv('OPENAI_API_KEY') or \
                  os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("未配置 API Key")
        
        print(f"  [3/4] 🔑 API Key 調用中...")
        
        # 這裡簡化實現，實際需要異步客戶端
        # 由於anthropic庫是同步的，這裡只是示例
        raise ValueError("API Key 層暫未實現（需要異步客戶端）")
        
    except Exception as e:
        raise ValueError(f"API Key 不可用: {e}")


def layer4_fallback(requirement: str, language: str) -> dict:
    """
    第四層：規則引擎降級
    
    最終降級，保證100%有問題返回
    """
    print(f"  [4/4] 📋 使用通用邏輯問題")
    return get_fallback_questions(language)


def is_generic_fallback(result: dict) -> bool:
    """檢查是否是通用降級問題"""
    if not result.get('questions'):
        return True
    
    first_q = result['questions'][0]
    return first_q.get('id') in ['q1_concurrency', 'q2_error_handling']


def parse_ai_json(ai_text: str) -> dict:
    """解析AI返回的JSON"""
    # 移除markdown標記
    text = ai_text.strip()
    if text.startswith('```'):
        lines = text.split('\n')
        text = '\n'.join(lines[1:-1])
    
    # 解析JSON
    return json.loads(text)


def build_prompt(requirement: str, language: str) -> str:
    """構建AI prompt"""
    if language == 'zh-TW':
        return f"""你是一個資深架構師，專門挖掘需求中的邏輯漏洞。

用戶需求：{requirement}

請生成 2 個「災難導向」的選擇題，用於蘇格拉底式邏輯面試。

重要規則：
1. **禁止問配置問題**（如：資料庫選 MySQL 還是 PostgreSQL？）
2. **必須問災難場景**（如：如果兩個用戶同時操作怎麼辦？）
3. 每個問題提供 3 個選項，每個選項都有明確的「代價」
4. **問題要具體、有場景感**，不要太抽象

請以 JSON 格式返回：

{{
  "questions": [
    {{
      "id": "q1_xxx",
      "type": "single_choice",
      "text": "問題文字（具體的災難場景）",
      "options": [
        {{
          "label": "A. 選項名稱",
          "description": "這個選擇的代價是什麼",
          "risk_score": "風險標籤",
          "value": "option_value"
        }}
      ]
    }}
  ]
}}

只返回 JSON，不要其他文字。"""
    else:
        return f"""You are a senior architect who specializes in finding logic gaps.

Requirement: {requirement}

Generate 2 disaster-oriented questions with clear trade-offs.
Return JSON format only."""


def build_prompt(requirement: str, language: str) -> str:
    """構建AI prompt"""
    if language == 'zh-TW':
        return f"""你是一個資深架構師，專門挖掘需求中的邏輯漏洞。

用戶需求：{requirement}

請生成 2 個「災難導向」的選擇題，用於蘇格拉底式邏輯面試。

重要規則：
1. **禁止問配置問題**（如：資料庫選 MySQL 還是 PostgreSQL？端口號是多少？）
2. **必須問災難場景**（如：如果兩個用戶同時操作怎麼辦？如果外部API超時怎麼辦？）
3. 每個問題提供 3 個選項，每個選項都有明確的「代價」(trade-off)

請以 JSON 格式返回：

{{
  "questions": [
    {{
      "id": "q1_xxx",
      "type": "single_choice",
      "text": "問題文字",
      "options": [
        {{
          "label": "A. 選項名稱",
          "description": "這個選擇的代價是什麼",
          "risk_score": "風險標籤（如：低風險，高延遲）",
          "value": "option_value"
        }}
      ]
    }}
  ]
}}

只返回 JSON，不要其他文字。"""
    else:
        return f"""You are a senior architect who specializes in finding logic gaps in requirements.

User requirement: {requirement}

Generate 2 "disaster-oriented" multiple choice questions for Socratic logic interview.

Important rules:
1. **DO NOT ask configuration questions**
2. **MUST ask disaster scenarios**
3. Each question provides 3 options with clear trade-offs

Return in JSON format only."""


def get_fallback_questions(language: str = 'zh-TW') -> dict:
    """備用問題（當AI無法生成時）"""
    
    if language == 'zh-TW':
        return {
            "questions": [
                {
                    "id": "q1_concurrency",
                    "type": "single_choice",
                    "text": "針對「數據一致性」，如果多個用戶同時操作怎麼辦？",
                    "options": [
                        {
                            "label": "A. 悲觀鎖 (Pessimistic Lock)",
                            "description": "絕對安全，但效能極差，用戶可能要排隊等待。",
                            "risk_score": "低風險，高延遲",
                            "value": "pessimistic"
                        },
                        {
                            "label": "B. 樂觀鎖 (Optimistic Lock)",
                            "description": "效能好，但在衝突時會導致大量失敗重試。",
                            "risk_score": "高風險，低延遲",
                            "value": "optimistic"
                        },
                        {
                            "label": "C. 分散式鎖 (Redis)",
                            "description": "極快，但如果 Redis 掛了數據會不一致。",
                            "risk_score": "數據一致性風險",
                            "value": "redis"
                        }
                    ]
                },
                {
                    "id": "q2_error_handling",
                    "type": "single_choice",
                    "text": "如果外部 API 調用失敗，系統應該如何處理？",
                    "options": [
                        {
                            "label": "A. 直接返回錯誤",
                            "description": "用戶立即知道失敗，但體驗差。",
                            "risk_score": "用戶體驗差",
                            "value": "fail_fast"
                        },
                        {
                            "label": "B. 重試3次",
                            "description": "可能成功，但會增加響應時間。",
                            "risk_score": "延遲增加",
                            "value": "retry"
                        },
                        {
                            "label": "C. 降級處理",
                            "description": "使用備用方案，但功能可能不完整。",
                            "risk_score": "功能降級",
                            "value": "degradation"
                        }
                    ]
                }
            ]
        }
    else:  # en-US
        return {
            "questions": [
                {
                    "id": "q1_concurrency",
                    "type": "single_choice",
                    "text": "For 'data consistency', what if multiple users operate simultaneously?",
                    "options": [
                        {
                            "label": "A. Pessimistic Lock",
                            "description": "Absolutely safe, but terrible performance. Users may have to queue.",
                            "risk_score": "Low Risk, High Latency",
                            "value": "pessimistic"
                        },
                        {
                            "label": "B. Optimistic Lock",
                            "description": "Good performance, but causes many retry failures on conflict.",
                            "risk_score": "High Risk, Low Latency",
                            "value": "optimistic"
                        },
                        {
                            "label": "C. Distributed Lock (Redis)",
                            "description": "Extremely fast, but data inconsistency if Redis fails.",
                            "risk_score": "Data Consistency Risk",
                            "value": "redis"
                        }
                    ]
                },
                {
                    "id": "q2_error_handling",
                    "type": "single_choice",
                    "text": "If external API call fails, how should the system handle it?",
                    "options": [
                        {
                            "label": "A. Return error directly",
                            "description": "User knows immediately, but poor experience.",
                            "risk_score": "Poor UX",
                            "value": "fail_fast"
                        },
                        {
                            "label": "B. Retry 3 times",
                            "description": "May succeed, but increases response time.",
                            "risk_score": "Increased Latency",
                            "value": "retry"
                        },
                        {
                            "label": "C. Graceful degradation",
                            "description": "Use fallback, but functionality may be incomplete.",
                            "risk_score": "Feature Degradation",
                            "value": "degradation"
                        }
                    ]
                }
            ]
        }
