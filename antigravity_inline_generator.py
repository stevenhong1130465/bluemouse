"""
Antigravity 內聯問題生成器
在 Antigravity 環境中直接生成蘇格拉底問題，無需外部 AI 調用
"""

import re
from typing import Dict, List


def generate_questions_inline(requirement: str, language: str = 'zh-TW') -> dict:
    """
    根據需求智能生成災難導向問題
    
    🎯 真正智能化：根據複雜度動態調整問題數量 (1-5個)
    讓每個有需求的人都能得到最適合的問題
    """
    
    # 1. 分析需求複雜度
    from requirement_complexity_analyzer import analyze_requirement_complexity
    
    complexity_info = analyze_requirement_complexity(requirement)
    question_count = complexity_info['question_count']
    detected_scenarios = complexity_info['scenarios']
    
    print(f"  🎯 複雜度分析: 分數={complexity_info['complexity_score']}, 問題數={question_count}")
    print(f"  🔍 檢測場景: {detected_scenarios}")
    
    # 正規化需求
    req_lower = requirement.lower()
    
    # 場景匹配
    scenarios = {
        '部落格|blog|post|cms|內容管理': 'blog',
        '電商|購物|訂單|商品|庫存|ecommerce|shop|cart|order': 'ecommerce',
        '預約|預訂|排程|日曆|booking|calendar|schedule': 'booking',
        '聊天|即時通訊|訊息|社交|chat|message|social': 'chat',
        '待辦|任務|todo|gtd|list|task': 'todo',
        '視頻|影片|直播|媒體|video|stream|media': 'video',
        '支付|金流|交易|錢包|payment|wallet|transaction': 'payment',
        '用戶|會員|帳號|user|auth|login|register': 'user_auth',
        '搜尋|檢索|查詢|search|query|find': 'search',
        '文件|檔案|上傳|儲存|file|upload|storage': 'file_storage',
    }
    
    detected_scenario = None
    for pattern, scenario in scenarios.items():
        if re.search(pattern, req_lower):
            detected_scenario = scenario
            break
    
    # 如果沒有匹配，使用通用場景
    if not detected_scenario:
        detected_scenario = 'generic'
    
    # 2. 根據場景和複雜度生成問題
    questions_map = {
        'blog': generate_blog_questions,
        'ecommerce': generate_ecommerce_questions,
        'booking': generate_booking_questions,
        'chat': generate_chat_questions,
        'todo': generate_todo_questions,
        'video': generate_video_questions,
        'payment': generate_payment_questions,
        'user_auth': generate_user_auth_questions,
        'search': generate_search_questions,
        'file_storage': generate_file_storage_questions,
        'generic': generate_generic_questions,
    }
    
    generator = questions_map.get(detected_scenario, generate_generic_questions)
    
    # 3. 生成問題並根據複雜度動態裁剪
    result = generator(requirement, language)
    
    # 4. 智能調整問題數量
    if 'questions' in result:
        original_count = len(result['questions'])
        
        # 多場景混合：只要檢測到2個以上場景，就混合生成
        if len(detected_scenarios) >= 2:
            result = generate_mixed_scenario_questions(detected_scenarios, question_count, language)
            print(f"  🔄 多場景混合: {len(detected_scenarios)}個場景 → {question_count}個問題")
        elif original_count > question_count:
            # 單場景但問題太多，裁剪
            result['questions'] = result['questions'][:question_count]
            print(f"  ✂️ 問題裁剪: {original_count} → {question_count}")
    
    return result


# ===== 各場景問題生成器 =====

def generate_blog_questions(requirement: str, language: str) -> dict:
    """部落格系統問題"""
    if language == 'zh-TW':
        return {
            "questions": [
                {
                    "id": "q1_blog_draft_recovery",
                    "type": "single_choice",
                    "text": "如果作者正在編輯文章時突然斷線或當機，未保存的內容該如何處理？",
                    "options": [
                        {
                            "label": "A. 每30秒自動保存草稿",
                            "description": "內容不會丟失，但會產生大量冗餘版本，佔用儲存空間。",
                            "risk_score": "儲存空間浪費",
                            "value": "auto_save"
                        },
                        {
                            "label": "B. 僅在手動保存時儲存",
                            "description": "節省空間，但用戶容易忘記保存，斷線時所有內容丟失。",
                            "risk_score": "高數據丟失風險",
                            "value": "manual_save"
                        },
                        {
                            "label": "C. 使用瀏覽器 localStorage 暫存",
                            "description": "體驗好，但有5MB容量限制，隱私模式下不可用。",
                            "risk_score": "容量限制，隱私問題",
                            "value": "localstorage"
                        }
                    ]
                },
                {
                    "id": "q2_blog_spam",
                    "type": "single_choice",
                    "text": "如果部落格每秒收到數百條垃圾留言攻擊，系統如何防禦？",
                    "options": [
                        {
                            "label": "A. 所有評論需人工審核",
                            "description": "最安全，但嚴重延遲顯示，降低用戶互動意願。",
                            "risk_score": "用戶體驗極差",
                            "value": "manual_review"
                        },
                        {
                            "label": "B. AI 自動過濾",
                            "description": "高效，但可能誤刪正常評論，引發用戶抱怨。",
                            "risk_score": "誤殺率10-20%",
                            "value": "ai_filter"
                        },
                        {
                            "label": "C. IP速率限制（每分鐘3條）",
                            "description": "簡單有效，但無法防禦分散式攻擊，誤傷共用IP用戶。",
                            "risk_score": "誤傷正常用戶",
                            "value": "rate_limit"
                        }
                    ]
                }
            ]
        }
    else:
        return generate_blog_questions_en(requirement, language)


def generate_ecommerce_questions(requirement: str, language: str) -> dict:
    """電商系統問題"""
    if language == 'zh-TW':
        return {
            "questions": [
                {
                    "id": "q1_ecommerce_inventory",
                    "type": "single_choice",
                    "text": "如果商品庫存只剩1件，但2個用戶幾乎同時下單，系統該如何處理？",
                    "options": [
                        {
                            "label": "A. 悲觀鎖：只讓第一個下單",
                            "description": "絕對不會超賣，但高流量時用戶需排隊，體驗差。",
                            "risk_score": "高並發性能差",
                            "value": "pessimistic_lock"
                        },
                        {
                            "label": "B. 樂觀鎖：讓兩個都下單，後取消一個",
                            "description": "性能好，但被取消的用戶會不滿，可能流失。",
                            "risk_score": "用戶體驗衝突",
                            "value": "optimistic_lock"
                        },
                        {
                            "label": "C. 預留庫存：下單時先鎖定，15分鐘內付款",
                            "description": "平衡性能與體驗，但可能被惡意佔用庫存。",
                            "risk_score": "庫存佔用攻擊",
                            "value": "reserve_inventory"
                        }
                    ]
                },
                {
                    "id": "q2_ecommerce_payment",
                    "type": "single_choice",
                    "text": "如果用戶付款成功，但支付回調失敗（網絡問題），訂單狀態錯誤怎麼辦？",
                    "options": [
                        {
                            "label": "A. 定期輪詢支付平台核對",
                            "description": "最可靠，但增加系統負載，且有延遲。",
                            "risk_score": "延遲5-10分鐘",
                            "value": "polling"
                        },
                        {
                            "label": "B. 依賴支付平台重試回調",
                            "description": "零負載，但如果平台也失敗，就永遠不會更新。",
                            "risk_score": "數據不一致風險",
                            "value": "rely_callback"
                        },
                        {
                            "label": "C. 人工介入處理異常訂單",
                            "description": "準確率100%，但人力成本高，處理慢。",
                            "risk_score": "人力成本高",
                            "value": "manual_fix"
                        }
                    ]
                }
            ]
        }
    else:
        return generate_ecommerce_questions_en(requirement, language)


def generate_booking_questions(requirement: str, language: str) -> dict:
    """預約系統問題"""
    if language == 'zh-TW':
        return {
            "questions": [
                {
                    "id": "q1_booking_conflict",
                    "type": "single_choice",
                    "text": "如果2個用戶同時預約同一時段，系統如何避免衝突？",
                    "options": [
                        {
                            "label": "A. 先到先得，鎖定時段",
                            "description": "公平簡單，但高峰期很多用戶會預約失敗。",
                            "risk_score": "用戶滿意度低",
                            "value": "first_come"
                        },
                        {
                            "label": "B. 候補機制，自動遞補",
                            "description": "最大化利用率，但候補通知延遲，用戶可能錯過。",
                            "risk_score": "通知不及時",
                            "value": "waitlist"
                        },
                        {
                            "label": "C. 彈性時段，建議替代時間",
                            "description": "降低衝突，但用戶可能不接受替代時段。",
                            "risk_score": "用戶接受度低",
                            "value": "flexible_slot"
                        }
                    ]
                },
                {
                    "id": "q2_booking_no_show",
                    "type": "single_choice",
                    "text": "如果用戶預約後爽約（no-show），浪費服務資源，如何應對？",
                    "options": [
                        {
                            "label": "A. 收取訂金，爽約不退款",
                            "description": "有效減少爽約，但可能嚇跑新用戶，降低轉化率。",
                            "risk_score": "轉化率下降20%",
                            "value": "deposit"
                        },
                        {
                            "label": "B. 信用評分制，多次爽約限制預約",
                            "description": "懲罰慣犯，但初犯用戶可能因一次意外被誤判。",
                            "risk_score": "誤傷正常用戶",
                            "value": "credit_score"
                        },
                        {
                            "label": "C. 提前24小時提醒，可免費取消",
                            "description": "用戶體驗好，但仍有20%爽約率，資源浪費。",
                            "risk_score": "20%資源浪費",
                            "value": "reminder_only"
                        }
                    ]
                }
            ]
        }
    else:
        return generate_booking_questions_en(requirement, language)


def generate_chat_questions(requirement: str, language: str) -> dict:
    """聊天系統問題"""
    if language == 'zh-TW':
        return {
            "questions": [
                {
                    "id": "q1_chat_offline",
                    "type": "single_choice",
                    "text": "如果用戶離線時收到100條訊息，重新上線後如何同步？",
                    "options": [
                        {
                            "label": "A. 一次性推送所有訊息",
                            "description": "最完整，但可能導致UI卡頓，流量爆炸。",
                            "risk_score": "UI卡頓，流量消耗大",
                            "value": "push_all"
                        },
                        {
                            "label": "B. 分批推送，每次10條",
                            "description": "流暢，但用戶需等待多次載入，體驗不連貫。",
                            "risk_score": "體驗不連貫",
                            "value": "batch_push"
                        },
                        {
                            "label": "C. 只顯示摘要+未讀數，用戶主動查看",
                            "description": "節省流量，但用戶可能錯過重要訊息。",
                            "risk_score": "錯過重要訊息",
                            "value": "summary_only"
                        }
                    ]
                },
                {
                    "id": "q2_chat_delivery",
                    "type": "single_choice",
                    "text": "如果訊息發送時網絡不穩定，如何確保送達？",
                    "options": [
                        {
                            "label": "A. 無限重試直到成功",
                            "description": "送達率100%，但可能產生重複訊息，且耗電。",
                            "risk_score": "重複訊息，耗電",
                            "value": "infinite_retry"
                        },
                        {
                            "label": "B. 重試3次後標記為失敗",
                            "description": "節能，但用戶需手動重發，體驗差。",
                            "risk_score": "用戶體驗差",
                            "value": "limited_retry"
                        },
                        {
                            "label": "C. 背景持續重試，但不阻塞UI",
                            "description": "體驗好，但實現複雜，可能有狀態不一致。",
                            "risk_score": "狀態同步複雜",
                            "value": "background_retry"
                        }
                    ]
                }
            ]
        }
    else:
        return generate_chat_questions_en(requirement, language)


def generate_todo_questions(requirement: str, language: str) -> dict:
    """待辦清單問題"""
    if language == 'zh-TW':
        return {
            "questions": [
                {
                    "id": "q1_todo_delete",
                    "type": "single_choice",
                    "text": "如果用戶刪除了一個包含10個子任務的父任務，系統應該如何處理？",
                    "options": [
                        {
                            "label": "A. 連同子任務一起刪除",
                            "description": "邏輯清晰，但用戶可能誤刪重要子任務。",
                            "risk_score": "意外數據丟失",
                            "value": "cascade_delete"
                        },
                        {
                            "label": "B. 只刪除父任務，子任務變成獨立任務",
                            "description": "保留數據，但可能產生大量孤兒任務，難管理。",
                            "risk_score": "數據混亂",
                            "value": "orphan_children"
                        },
                        {
                            "label": "C. 刪除前強制確認，並支持撤銷",
                            "description": "最安全，但多一步操作，降低效率。",
                            "risk_score": "操作繁瑣",
                            "value": "confirm_undo"
                        }
                    ]
                },
                {
                    "id": "q2_todo_sync",
                    "type": "single_choice",
                    "text": "如果用戶在手機和電腦同時編輯同一任務，如何解決衝突？",
                    "options": [
                        {
                            "label": "A. 最後寫入者獲勝",
                            "description": "實現簡單，但先編輯的內容會被覆蓋。",
                            "risk_score": "數據丟失",
                            "value": "last_write_wins"
                        },
                        {
                            "label": "B. 提示用戶手動合併",
                            "description": "保證不丟失，但需要用戶理解技術概念，門檻高。",
                            "risk_score": "用戶體驗差",
                            "value": "manual_merge"
                        },
                        {
                            "label": "C. 智能合併（如附加而非覆蓋）",
                            "description": "體驗好，但邏輯複雜，可能產生奇怪結果。",
                            "risk_score": "合併錯誤",
                            "value": "auto_merge"
                        }
                    ]
                }
            ]
        }
    else:
        return generate_todo_questions_en(requirement, language)


def generate_generic_questions(requirement: str, language: str) -> dict:
    """通用問題（未匹配到具體場景）"""
    if language == 'zh-TW':
        return {
            "questions": [
                {
                    "id": "q1_concurrency",
                    "type": "single_choice",
                    "text": "如果多個用戶同時操作同一數據，如何保證一致性？",
                    "options": [
                        {
                            "label": "A. 悲觀鎖（Pessimistic Lock）",
                            "description": "絕對安全，但性能極差，用戶可能需排隊。",
                            "risk_score": "低風險，高延遲",
                            "value": "pessimistic"
                        },
                        {
                            "label": "B. 樂觀鎖（Optimistic Lock）",
                            "description": "性能好，但衝突時會大量失敗重試。",
                            "risk_score": "高風險，低延遲",
                            "value": "optimistic"
                        },
                        {
                            "label": "C. 分散式鎖（Redis）",
                            "description": "極快，但如果Redis掛了會數據不一致。",
                            "risk_score": "依賴外部服務",
                            "value": "redis"
                        }
                    ]
                },
                {
                    "id": "q2_error_handling",
                    "type": "single_choice",
                    "text": "如果外部API調用失敗，系統應該如何處理？",
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
    else:
        return generate_generic_questions_en(requirement, language)


# ===== 英文版本 =====


def generate_blog_questions_en(requirement: str, language: str) -> dict:
    """Blog System Questions (English)"""
    return {
        "questions": [
            {
                "id": "q1_blog_draft_recovery",
                "type": "single_choice",
                "text": "If the author loses connection while editing, how should unsaved content be handled?",
                "options": [
                    {
                        "label": "A. Auto-save draft every 30s",
                        "description": "Safe, but creates many redundant versions and uses storage.",
                        "risk_score": "Storage Overhead",
                        "value": "auto_save"
                    },
                    {
                        "label": "B. Save only on manual click",
                        "description": "Saves space, but high risk of data loss if forgotten.",
                        "risk_score": "High Data Loss Risk",
                        "value": "manual_save"
                    },
                    {
                        "label": "C. Cache in browser LocalStorage",
                        "description": "Good UX, but 5MB limit and fails in Incognito mode.",
                        "risk_score": "Browser Limitations",
                        "value": "localstorage"
                    }
                ]
            },
            {
                "id": "q2_blog_spam",
                "type": "single_choice",
                "text": "If the blog receives hundreds of spam comments per second, how to defend?",
                "options": [
                    {
                        "label": "A. Manual review for all",
                        "description": "Safest, but severe delay in visibility.",
                        "risk_score": "Poor UX",
                        "value": "manual_review"
                    },
                    {
                        "label": "B. AI automated filtering",
                        "description": "Efficient, but may delete legit comments (false positives).",
                        "risk_score": "False Positive Risk",
                        "value": "ai_filter"
                    },
                    {
                        "label": "C. IP Rate Limiting (3/min)",
                        "description": "Simple, but fails against simple attacks and blocks shared IPs.",
                        "risk_score": "Collateral Damage",
                        "value": "rate_limit"
                    }
                ]
            }
        ]
    }

def generate_ecommerce_questions_en(requirement: str, language: str) -> dict:
    """E-commerce System Questions (English)"""
    return {
        "questions": [
            {
                "id": "q1_ecommerce_inventory",
                "type": "single_choice",
                "text": "If only 1 item remains but 2 users place orders simultaneously, what to do?",
                "options": [
                    {
                        "label": "A. Pessimistic Lock: First one wins",
                        "description": "No overselling, but users may queue during high traffic.",
                        "risk_score": "Low Concurrency Performance",
                        "value": "pessimistic_lock"
                    },
                    {
                        "label": "B. Optimistic Lock: Allow both, cancel later",
                        "description": "High performance, but cancelled user will be angry.",
                        "risk_score": "User Conflict",
                        "value": "optimistic_lock"
                    },
                    {
                        "label": "C. Reserve Inventory: Lock on checkout",
                        "description": "Balances UX, but inventory can be held maliciously.",
                        "risk_score": "Inventory Hoarding Attack",
                        "value": "reserve_inventory"
                    }
                ]
            },
            {
                "id": "q2_ecommerce_payment",
                "type": "single_choice",
                "text": "If payment succeeds but callback fails (network issue), causing order error, what to do?",
                "options": [
                    {
                        "label": "A. Poll payment gateway periodically",
                        "description": "Reliable, but increases load and latency.",
                        "risk_score": "Latency increase",
                        "value": "polling"
                    },
                    {
                        "label": "B. Rely on gateway retry",
                        "description": "Zero load, but if gateway fails, data never updates.",
                        "risk_score": "Data Inconsistency",
                        "value": "rely_callback"
                    },
                    {
                        "label": "C. Manual intervention",
                        "description": "100% accurate, but high operational cost.",
                        "risk_score": "High OpEx",
                        "value": "manual_fix"
                    }
                ]
            }
        ]
    }

def generate_booking_questions_en(requirement: str, language: str) -> dict:
    return generate_generic_questions_en(requirement, language)

def generate_chat_questions_en(requirement: str, language: str) -> dict:
    return generate_generic_questions_en(requirement, language)

def generate_todo_questions_en(requirement: str, language: str) -> dict:
    return generate_generic_questions_en(requirement, language)

def generate_generic_questions_en(requirement: str, language: str) -> dict:
    return {
        "questions": [
            {
                "id": "q1_concurrency",
                "type": "single_choice",
                "text": "If multiple users operate the same data simultaneously, how to ensure consistency?",
                "options": [
                    {
                        "label": "A. Pessimistic Lock",
                        "description": "Absolutely safe, but terrible performance.",
                       "risk_score": "Low Risk, High Latency",
                        "value": "pessimistic"
                    },
                    {
                        "label": "B. Optimistic Lock",
                        "description": "Good performance, but many retry failures on conflict.",
                        "risk_score": "High Risk, Low Latency",
                        "value": "optimistic"
                    },
                    {
                        "label": "C. Distributed Lock (Redis)",
                        "description": "Extremely fast, but data inconsistency if Redis fails.",
                        "risk_score": "Depends on External Service",
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


# ===== 其他場景 =====

def generate_video_questions(requirement: str, language: str) -> dict:
    return generate_generic_questions(requirement, language)

def generate_payment_questions(requirement: str, language: str) -> dict:
    return generate_generic_questions(requirement, language)

def generate_user_auth_questions(requirement: str, language: str) -> dict:
    return generate_generic_questions(requirement, language)

def generate_search_questions(requirement: str, language: str) -> dict:
    return generate_generic_questions(requirement, language)

def generate_file_storage_questions(requirement: str, language: str) -> dict:
    return generate_generic_questions(requirement, language)


def generate_mixed_scenario_questions(scenarios: List[str], count: int, language: str) -> dict:
    """
    多場景混合問題生成
    
    當檢測到多個場景時，從每個場景中選取最核心的問題
    """
    all_questions = []
    
    # 場景優先級
    scenario_map = {
        '部落格': 'blog',
        '電商': 'ecommerce',
        '預約': 'booking',
        '聊天': 'chat',
        '支付': 'payment',
        '會員': 'user_auth',
    }
    
    generators = {
        'blog': generate_blog_questions,
        'ecommerce': generate_ecommerce_questions,
        'booking': generate_booking_questions,
        'chat': generate_chat_questions,
        'user_auth': generate_user_auth_questions,
    }
    
    # 從每個場景收集第一個問題
    for scenario in scenarios[:count]:
        scenario_key = scenario_map.get(scenario)
        if scenario_key and scenario_key in generators:
            gen = generators[scenario_key]
            result = gen('', language)
            if 'questions' in result and len(result['questions']) > 0:
                # 取第一個最重要的問題
                all_questions.append(result['questions'][0])
    
    # 補充到目標數量
    while len(all_questions) < count and len(all_questions) < 5:
        # 從第二優先級問題補充
        for scenario in scenarios[:count]:
            if len(all_questions) >= count:
                break
            scenario_key = scenario_map.get(scenario)
            if scenario_key and scenario_key in generators:
                gen = generators[scenario_key]
                result = gen('', language)
                if 'questions' in result and len(result['questions']) > 1:
                    all_questions.append(result['questions'][1])
        break  # 避免無限循環
    
    return {
        'questions': all_questions[:count]
    }

