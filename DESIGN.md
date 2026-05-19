# JuniorABC 設計文件

> 個性化國中會考學習輔助網站 — 截至 2026-05-18 的討論成果

---

## 一、專案概述

### 1.1 目標
為國中會考準備設計一套**個性化**學習輔助系統。「個性化」在此專案的明確定義:**所有練習題目皆來自學生自己上傳的素材**(實體考卷、講義、參考書影像),系統不自動產生題目。

### 1.2 使用者
- **最多 3 位**,皆為熟識的國中學生:
  - 開發者本人的女兒
  - 兩位同事的女兒
- 三位皆為**國二**(2026 年 5 月)
- 無公開註冊,無陌生使用者

### 1.3 學科優先順序
- **Phase 1**:英文(單字記憶 + 文法練習)
- **Phase 2+**:數學、英文閱讀、聽力等(時程未定)

### 1.4 近期里程碑
- **2026 年 9 月 國一全模擬考**(距 2026-05-18 約 16 週)
- **長期目標**:2027 年國中會考(約 1.5 年)

---

## 二、核心原則(不可妥協)

| # | 原則 | 理由 |
|---|---|---|
| 1 | **LLM 不得自行產生練習題** | 避免 LLM 在數學上產生幻覺答案;讓使用者用自己學校/補習班的真實素材 |
| 2 | **數學答案必由人工提供** | 數學題若上傳素材無解答,由父親手動補上;LLM 不負責解數學 |
| 3 | **英文答案需 LLM 二次審查** | 商業參考書答案會有錯,LLM 需在解析時對可疑答案標記、待人工確認 |
| 4 | **小範圍、緊密迭代** | 不為「將來可能用得到」做設計,只做當下要用的功能 |
| 5 | **學生即 co-designer** | 三位使用者皆可參與 UI 風格、命名、外觀決策,提升使用意願 |

---

## 三、進度區間 (Buckets)

### 3.1 固定六大區間
僅這六個,**不再向下細分**:

```
國一上 → 國一下 → 國二上 → 國二下 → 國三上 → 國三下
```

### 3.2 複合區間
上傳素材時可標記為複合區間,例如:`國一全`、`國一二`、`全國中`。

### 3.3 起點規則
- **全員從「國一上」起跑**,不論註冊時的實際年級
- 不可由使用者自選起點
- 想加速:透過下文「超前申請」機制

### 3.4 區間進展
- **不可越級**:必須依序 國一上 → 國一下 → ... → 國三下
- 升級觸發見「五、升級規則」

---

## 四、每週學習週期

### 4.1 基本參數
| 項目 | 值 |
|---|---|
| 週期長度 | 7 天(以個人滾動計算,非固定週一至週日) |
| 每週題量 | **100 題(總量,含新題 + 複習)** |
| 單字 : 文法比例 | **8 : 2**(80 單字 + 20 文法) |

### 4.2 自適應規則
**下週「新題比例 = 本週正確率」**,複習題補滿至 100:

| 本週正確率 | 下週新題數 | 下週複習數 |
|---|---|---|
| 80% | 80 | 20 |
| 50% | 50 | 50 |
| 30% | 30 | 70 |
| 100% | 100 | 0 |

此設計確保**弱者不被壓垮、強者持續挑戰**。

### 4.3 題目用完之處理
- 當前 bucket 在使用者上傳庫存中**題目用盡** → **循環出題**(舊題重抽,直至上傳新素材或晉級)
- **不會自動跨 bucket** 補題

---

## 五、升級規則(A + B 混合)

### 5.1 自動升級(B 路徑)
**觸發條件**:該使用者在當前 bucket 的所有「非過濾」題目,**每題至少答對 2 次**,且**無 stuck 標記**。

**行為**:當週期自然結束時,平緩進入下一 bucket。

### 5.2 主動超前(A 路徑)
**觸發條件**:使用者按下「申請超前」按鈕,且**連續 2 週 ≥80% 正確率**。

**行為**:**立即重置** 7 天 / 100 題週期,新題從下一 bucket 抽。

### 5.3 UI 提示
當「連續 2 週 ≥80%」條件達成時,網頁右上角顯示「🚀 你已可申請進入下一單元」紅點,引導使用者主動操作。

---

## 六、卡關 (Stuck) 處理

| 條件 | 行為 |
|---|---|
| 同一題連續 2 週答錯 | 標記為 `is_stuck = true` |
| 後續處理 | **暫不設計**,等真實使用一段時間後再決定 |

---

## 七、單字難度過濾

### 7.1 上限(過難排除)
**白名單**:大考中心七千字 **Level 1 ~ Level 4**(約涵蓋前 4500 字)。

凡不在此範圍內的單字 → `status = 'filtered_too_hard'`,**不進練習池**(但保留資料供未來使用)。

### 7.2 下限(過簡排除)
**黑名單**:約 200 個過於基本的單字,涵蓋:

| 類別 | 範例 |
|---|---|
| 人稱代名詞 | I, you, he, she, it, we, they, me, him, her, them |
| be 動詞與助動詞 | is, am, are, was, were, be, been, do, does, did, have, has, had, can, will |
| 冠詞 / 介系詞 | a, an, the, of, in, on, at, to, for, with, by, from |
| 指示 / 連接 | this, that, these, those, and, or, but, so |
| 基本疑問詞 | what, where, when, who, why, how |
| 1 ~ 20 數字 | one, two, three ... twenty |
| 顏色 / 星期 / 月份 | red, blue, ... / Monday ... / January ... |
| 其他超基本 | yes, no, hi, hello, bye, good, big, small |

凡命中黑名單 → `status = 'filtered_too_easy'`,**不進練習池**(可後台編輯黑名單)。

---

## 八、資料表 Schema(Phase 1)

### 8.1 主要資料表
```
┌─────────────────────────────────────────────────────────────────┐
│ users                                                            │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ line_user_id      LINE bot 對應 ID(從 webhook 取得)            │
│ display_name      例:"Amy"                                      │
│ current_bucket    default '國一上'                               │
│ cycle_start_date  本週期起算日(因超前可隨時重設)              │
│ created_at                                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ materials  (一張上傳的圖 = 一筆)                                │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ user_id (FK → users)                                             │
│ image_path        本機檔案路徑或 S3 key                          │
│ content_type      'vocab' | 'grammar'                            │
│ bucket            '國一上' / '國一下' / ...                      │
│ uploaded_at                                                      │
│ parse_status      'pending' | 'parsed' | 'confirmed' | 'rejected'│
│ parse_notes       Claude Vision 解析時的疑慮備註                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ vocab_items                                                      │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ material_id (FK → materials)                                     │
│ user_id (FK → users)         冗余,加速查詢                     │
│ bucket                        冗余                               │
│ word              英文單字,統一小寫                             │
│ pos               詞性: n. v. adj. ...                           │
│ meaning_zh        中譯,可多個用 ; 分隔                         │
│ example_en        例句(若有)                                    │
│ example_zh                                                       │
│ frequency_level   1~7,大考中心七千字級別;0 = 不在表內         │
│ audio_url_us      美式發音 mp3 本機路徑(Phase 1.5 新增)        │
│ sentence_audio_path  例句合成音檔路徑(Phase 1.5 新增)          │
│ mnemonic_zh       使用者自訂諧音(中文,Phase 1.5 新增)        │
│ mnemonic_updated_at                                              │
│ svg_path          SVG 圖檔路徑(Phase 1.5 新增)                 │
│ svg_generated_at                                                 │
│ svg_source        'ai_generated' | 'user_uploaded' | 'none'      │
│ status            'active' | 'filtered_too_easy'                 │
│                   | 'filtered_too_hard' | 'pending_human_review' │
│ created_at                                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ grammar_items                                                    │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ material_id (FK → materials)                                     │
│ user_id, bucket             冗余                                 │
│ question_text     題幹                                           │
│ options_json      [{key:'A', text:'...'}, ...]                   │
│ correct_key       'A' | 'B' | 'C' | 'D' | free-text              │
│ topic_tag         文法主題,例:'past_tense' (LLM 提標、人工確認)│
│ status            'active' | 'pending_human_review'              │
│ created_at                                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ weekly_sessions  (每週期一筆)                                    │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ user_id (FK → users)                                             │
│ started_at, ends_at (= started_at + 7 days)                      │
│ target_total      = 100                                          │
│ new_count, review_count                                          │
│ correctness_rate  本週期結束時計算                               │
│ status            'active' | 'completed' | 'reset_by_skip'       │
│ trigger           'regular' | 'skip_request' | 'auto_advance'    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ session_items  (本週期內每題一筆)                                │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ session_id (FK → weekly_sessions)                                │
│ item_id, item_type ('vocab' | 'grammar')                         │
│ is_new            true = 新題, false = 複習                     │
│ presented_at, answered_at                                        │
│ answer_given                                                     │
│ is_correct                                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ item_progress  (每使用者每題的長期狀態)                          │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ user_id, item_id, item_type     複合 unique                      │
│ times_seen, times_correct                                        │
│ last_seen, last_correct                                          │
│ consecutive_wrong_weeks  偵測 stuck 用                          │
│ is_stuck          true if consecutive_wrong_weeks ≥ 2            │
│ is_mastered       true if times_correct ≥ 2 AND last_correct     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ trivial_blacklist  (後台可編輯)                                  │
├─────────────────────────────────────────────────────────────────┤
│ word (PK, 小寫)                                                  │
│ added_by, added_at                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 九、每週週期演算法(虛擬碼)

```python
# Trigger: 上一週期結束 OR 使用者按下「申請超前」

def on_cycle_end_or_skip(user, trigger):

    # 1. 結算上週期
    last_session = get_last_active_session(user)
    if last_session:
        rate = correct / total of last_session.session_items
        last_session.correctness_rate = rate
        last_session.status = 'completed' if trigger=='regular' else 'reset_by_skip'

        for si in last_session.session_items:
            p = get_or_create_item_progress(user, si.item)
            p.times_seen += 1
            if si.is_correct:
                p.times_correct += 1
                p.last_correct = now()
                p.consecutive_wrong_weeks = 0
            else:
                p.consecutive_wrong_weeks += 1
                if p.consecutive_wrong_weeks >= 2:
                    p.is_stuck = True
            p.is_mastered = (p.times_correct >= 2 and p.last_correct == now())

    # 2. 升級判定
    new_bucket = user.current_bucket
    if trigger == 'skip_request':
        # A 路徑:主動超前
        assert eligible_for_skip(user)   # 連續 2 週 ≥80%
        new_bucket = next_bucket(user.current_bucket)
    elif trigger == 'regular':
        # B 路徑:自動晉級
        if all_items_mastered_in_bucket(user, user.current_bucket):
            new_bucket = next_bucket(user.current_bucket)
    user.current_bucket = new_bucket

    # 3. 算下週新題 / 複習比例
    rate = last_session.correctness_rate if last_session else 1.0
    new_target    = round(rate * 100)
    review_target = 100 - new_target

    # 4. 8:2 切割 vocab : grammar
    new_vocab      = round(new_target    * 0.8)
    new_grammar    = new_target - new_vocab
    review_vocab   = round(review_target * 0.8)
    review_grammar = review_target - review_vocab

    # 5. 抽題
    new_v = pick_new_vocab(user, new_bucket, n=new_vocab)
    new_g = pick_new_grammar(user, new_bucket, n=new_grammar)
    if len(new_v) < new_vocab:           # 新題池不足 → 循環
        new_v += pick_from_completed_pool(user, new_bucket, 'vocab', n=...)
    rev_v = pick_review_vocab(user, n=review_vocab)
    rev_g = pick_review_grammar(user, n=review_grammar)

    # 6. 建立新週期
    s = create_session(
        user=user,
        started_at=now(),
        ends_at=now() + 7*days,
        target_total=100,
        new_count=len(new_v) + len(new_g),
        review_count=len(rev_v) + len(rev_g),
        trigger=trigger,
        status='active',
    )
    enqueue_session_items(s, new_v + new_g + rev_v + rev_g)
    user.cycle_start_date = now()
    save(user)


def eligible_for_skip(user):
    last2 = last_n_completed_sessions(user, n=2)
    return len(last2) >= 2 and all(s.correctness_rate >= 0.8 for s in last2)
```

---

## 十、Phase 1.5 補充功能:單字小卡(發音 / 諧音 / SVG)

### 10.1 功能定義
讓使用者上傳的單字自動轉成**互動式小卡**,供學生**自我預習**(非測驗)。
小卡內含三個 AI 輔助學習區塊:**真人發音**、**中文諧音記憶**、**抽象 SVG 圖示**。

### 10.2 UX 規則(共通)
| 項目 | 決定 |
|---|---|
| 卡片單字池 | 只能瀏覽「當前 bucket 以下」的單字 |
| 是否影響成績 | **完全不影響** — 純預習,不寫入 `item_progress` |
| 預設發音 | 美式(台灣教學主流) |
| 卡片結構 | 正面:SVG 圖示 + 單字 + 音標 + 🔊 + 詞性;翻面:中譯 + 例句 + 例句 🔊 + 諧音 |

### 10.3 發音音訊策略(三層 fallback)

| 音訊類型 | 第一層 | 第二層 | 第三層 |
|---|---|---|---|
| 單字本身 | **Free Dictionary API** (api.dictionaryapi.dev) — 真人錄音 mp3,免費,無 auth | Azure Speech Neural TTS | 瀏覽器 Web Speech API |
| 例句 | **程式碼 TTS 合成**(預設 Azure Speech Neural) | 其他 TTS API | 瀏覽器 Web Speech API |

### 10.4 諧音記憶區塊
| 項目 | 決定 |
|---|---|
| 隱私 | **完全私有** — A 的諧音 B 看不到 |
| 預設值 | 空白(選填) |
| AI 輔助 | 使用者按下「✨ AI 建議」可請 LLM 給 2~3 個諧音候選,**使用者選用或改寫** |
| 編輯方式 | 卡片上 inline 編輯,不另開後台頁 |
| 範例 | `ambulance` → "俺不能死" / `apple` → "阿婆" |

### 10.5 抽象 SVG 圖示
| 項目 | 決定 |
|---|---|
| 生成時機 | 解析新單字、入庫時**背景生成**,非即時 |
| 適用範圍 | **僅具象名詞 / 動作**;抽象詞(however, although 等)由 LLM 判斷不適合即跳過,顯示「無圖」 |
| 風格規範 | Prompt 寫死:單色、無邊框、`viewBox="0 0 100 100"`、線寬固定,降低跳調 |
| 卡片占比 | **≤ 25%**(不可反客為主) |
| 學生重生 | **允許** — 卡片上「🎲 重新生成」按鈕,不滿意可換 |
| 使用者上傳替換 | **允許** — 學生可上傳手繪 / 自找的 SVG / PNG 取代 AI 圖 |
| 模型 | Claude Haiku(成本低,品質夠) |
| 預估成本 | 約 NT$0.05 / 圖;3 人 × 1500 字 ≈ NT$225 一次性 |

### 10.6 快取策略
- 所有下載 / 合成 / 生成的音檔與圖檔**永久存本機**
  - 音檔: `audio/{word}_us.mp3` / `audio/sentence/{item_id}.mp3`
  - SVG: `svg/{word}.svg`(系統生成);`svg/user/{user_id}/{word}.svg`(使用者上傳)
- 一次產出,後續直接讀檔
- 預估**音訊月費 NT$0**(Dictionary API 免費,Azure 免費 quota 三人用不完)
- SVG 生成為一次性費用(僅在解析新單字時觸發)

### 10.7 vocab_items 新增欄位

```
mnemonic_zh           TEXT, nullable        使用者自訂諧音記憶(中文)
mnemonic_updated_at   TIMESTAMP, nullable
svg_path              TEXT, nullable        SVG 圖檔本機路徑
svg_generated_at      TIMESTAMP, nullable
svg_source            'ai_generated' | 'user_uploaded' | 'none'
audio_url_us          TEXT, nullable        美式發音 mp3 本機路徑
sentence_audio_path   TEXT, nullable        例句合成音檔路徑
```

### 10.8 上線時機與工作量
- **Phase 1 核心測驗流程跑通後再追加**,不阻塞 Phase 0 / Phase 1
- **預估工作量約為 Phase 1 的 60~80%**(視 SVG 品質要求而定)
- Phase 1 上線後到 Phase 1.5 上線約再隔 2~3 週

---

## 十一、技術架構(待 Phase 0 後敲定)

### 11.1 雙通道輸入
- **LINE bot**:輕量上傳通道(拍照、簡短互動)
- **瀏覽器**:正式學習介面(較大畫面、座位式練習)

LINE 上傳需要**公開 HTTPS webhook**,意味著系統從 Phase 1 開始就必須部署到雲端(不可純 localhost)。

### 11.2 前後端分離
| 層級 | 內容 |
|---|---|
| 前端(UI) | 學生練習介面、爸爸後台介面 |
| 後端(API + DB) | 接 LINE webhook、解析調用、題目管理、週期演算 |
| 資料庫 | Phase 1 用 SQLite 即可(3 人,負擔極小) |

### 11.3 解析流程
```
LINE 上傳圖片
   ↓
存原圖 → 寫入 materials
   ↓
Claude Vision 解析
   ↓
   ├─ vocab → 抽 word/pos/meaning/example → 過難濾掉 / 過簡濾掉
   ├─ grammar → 抽 題幹/選項/答案 → 答案合理性審查
   ↓
寫入 vocab_items / grammar_items (status='pending_human_review')
   ↓
爸爸後台確認 → status='active' → 進入題目池
```

---

## 十二、分階段時程

| 階段 | 預估時程 | 內容 | 狀態 |
|---|---|---|---|
| **Phase 0** | 數天 | Claude Vision 在真實單字頁 / 文法頁的辨識能力驗證(門檻:vocab ≥ 95%,grammar ≥ 85%) | **進行中**(等待使用者提供測試照片) |
| **Phase 1** | 約 2~3 週 | MVP:LINE 上傳、Vision 解析、爸爸確認後台、學生網頁(單字測驗 + 文法測驗)、每週週期演算 | 未啟動 |
| **Phase 1.5** | (Phase 1 後) | 單字小卡 + 發音 | 未啟動 |
| **Phase 2+** | 待定 | 錯題本、弱點分析、儀表板、擴展至 3 位使用者、數學、閱讀、聽力 | 未啟動 |

---

## 十三、已明確「不做」的項目

避免將來重新爭論,以下項目**目前不在計畫內**:

- ❌ 多租戶帳號系統、付費機制
- ❌ 跨題目 AI 自由對話(「這個觀念再講一次」)
- ❌ 學生手寫答案 OCR 辨識
- ❌ 通知 / 提醒系統
- ❌ SVG 數學圖形重繪
- ❌ 數學、英文閱讀、英文聽力(Phase 2+)
- ❌ LLM 自動生成練習題
- ❌ 系統根據學生年級自動定位起點(全員從國一上)

---

## 十四、待處理項目

| 項目 | 觸發點 |
|---|---|
| Phase 0 測試照片提供 | 使用者方便時 |
| 過簡黑名單完整 ~200 字版本 | Phase 1 建 admin 後台前 |
| 例句 TTS 是否確定用 Azure(其他 TTS 提供商比較) | Phase 1.5 開工前 |
| 卡關 (stuck) 題的後續處理方式 | Phase 1 上線並累積一段使用資料後 |
| SVG 生成 prompt 模板敲定(視覺風格規範) | Phase 1.5 開工前 |
| 諧音 AI 建議 prompt 模板敲定 | Phase 1.5 開工前 |

---

*文件最後更新:2026-05-18(新增:Phase 1.5 諧音記憶 + SVG 圖示子功能)*
