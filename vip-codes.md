# VIP 登錄碼 & 每週單字管理

> 此檔案供作者管理使用，勿公開。

---

## 新增 VIP 帳號（兩步驟）

### 步驟 1：在 `index.html` 加碼

找到：
```javascript
const VIP_CODES = [
  '1010609',
];
```
加一行：
```javascript
const VIP_CODES = [
  '1010609',
  '新的7位數碼',
];
```

### 步驟 2：建立該 VIP 的資料檔

複製 `weekly/data/1010609.json`，重新命名為 `weekly/data/{新碼}.json`，並修改 `name` 欄位。

---

## 每週更新單字（兩步驟）

### 檔案命名規則

```
weekly/data/{vip_code}.{起始日YYYYMMDD}.{終止日YYYYMMDD}.json
```

例：`weekly/data/1010609.20260522.20260528.json`

舊週次檔案**永久保留**，不刪除。

---

### 步驟 1：建立新週次資料檔

新增 `weekly/data/{vip_code}.{起始}.{終止}.json`，內容如下：

```json
{
  "vip": "1010609",
  "name": "小名",
  "week": "第 X 週",
  "start": "2026-05-22",
  "end": "2026-05-28",
  "words": [
    { "word": "ambitious", "zh": "有抱負的；有野心的", "syllables": "am·bi·tious" }
  ]
}
```

**單字欄位說明：**
- `word`：英文單字（必填）
- `zh`：中文解釋（必填）
- `syllables`：音節分隔，用 `·` 隔開（選填）

### 步驟 2：更新索引檔

開啟 `weekly/data/{vip_code}.json`，將 `current` 改為新檔名：

```json
{
  "current": "1010609.20260529.20260604.json"
}
```

---

---

## 登錄碼清單

| 碼號 | 持有者 | 啟用日期 | 備註 |
|------|--------|----------|------|
| 1010609 | 爸爸(作者) | 2026-05-22 | 首筆測試碼 |
