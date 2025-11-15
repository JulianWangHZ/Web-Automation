# Web 自動化測試套件

_[英文說明請見此](README.md)_

這是一套為 Inline 訂餐體驗打造的端對端自動化框架。  
除了既有的 Selenium + pytest-bdd 回歸腳本，也可透過 Playwright MCP 進行即時探索與除錯。

---

## 📑 目錄

1. [Playwright MCP 安裝與使用](#-playwright-mcp-安裝與使用)
2. [專案概覽](#-專案概覽)
3. [主要功能](#-主要功能)
4. [快速開始](#-快速開始)
5. [Headless 模式](#headless-模式)
6. [平行執行範例](#-平行執行範例)
7. [開發指南](#-開發指南)
8. [常見問題](#-常見問題)

---

## 🎭 Playwright MCP 安裝與使用

雖然正式測試由 Selenium 驅動，但我們透過 MCP 控制 Playwright 進行快速 UI 驗證與偵錯。

### 安裝

```bash
pnpm add -D @playwright/mcp
# 或
npm install --save-dev @playwright/mcp
```

並在 `~/.cursor/mcp.json` 中加入：

```json
"playwright": {
  "command": "npx",
  "args": ["@playwright/mcp@latest"]
}
```

### 使用原則

1. 在 `playwright_navigate` 之前先說明目標網址與操作目的。
2. 嚴格依照 feature/BDD 步驟順序執行。
3. 每個關鍵操作後記錄畫面狀態（例如地址卡、Edit 按鈕）。
4. 結果以 `Navigate ➜ Actions ➜ Verification` 形式回報。

### 官方資源

- [Playwright Docs](https://playwright.dev/)
- [Playwright GitHub](https://github.com/microsoft/playwright)
- [Cursor MCP Guide](https://cursor.sh/docs/mcp)

---

## 🎯 專案概覽

| 項目         | 說明                                                                |
|--------------|---------------------------------------------------------------------|
| 架構         | Page Object Model + pytest-bdd                                      |
| 目標流程     | Inline 餐廳外帶/外送訂單                                            |
| 多裝置支援   | 透過 `config/devices/*` 切換桌機/手機視窗                          |
| 入口點       | `pytest`（搭配 `order_page`, `payment` 等 marker）                |
| CI 友善程度  | 可 headless、可平行，整合 `pytest-xdist`                           |

---

## ✨ 主要功能

### 1. 多設備模擬
- 裝置設定集中在 `config/devices/`，皆繼承 `BaseDevice`。
- 透過 `--device iphone17`、`--device pixel9pro` 即可切換。

### 2. 跨瀏覽器測試
- 支援 Chrome / Firefox / Safari（使用 `--browser`）。
- 可加上 `--headless` 進行無頭模式（Safari 不支援，見 FAQ）。

### 3. 傳統測試優勢
- BDD 腳本位於 `features/`，邏輯清楚。
- 同時整合 `pytest-html`、`allure-pytest`、rerunfailures。
- Selector 由 `locators/` 單一入口管理，`BaseAction` 提供統一等待/點擊邏輯。

---

## 🚀 快速開始

### 前置需求
- Python 3.13+
- Node.js 18+（用於 MCP/工具鏈）
- 本機已安裝 Chrome / Firefox / Safari
- （選用）Android SDK – 若需啟動 Appium MCP

### 安裝步驟

```bash
git clone https://github.com/<your-org>/web-automation.git
cd web-automation
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 執行測試

#### 1️⃣ 基本執行
```bash
pytest -m "order_page"
```

#### 2️⃣ 設備切換
```bash
pytest -m "order_page" --device=iphone17
```

#### 3️⃣ 進階選項
```bash
pytest -m "order_page" \
  --browser=firefox \
  --device=pixel9pro \
  --headless \
  --reruns=1 \
  -n 3
```

#### Headless 模式
加上 `--headless` 即可；預設使用 Chrome headless（可搭配 `--browser` 覆寫）。

---

## 🧭 平行執行範例

| 情境                              | 指令示例                                                               |
|-----------------------------------|------------------------------------------------------------------------|
| 依 marker 執行                    | `pytest -m "order_page" -n 3`                                          |
| 針對特定檔案                      | `pytest tests/test_order_page.py -n 3`                                 |
| 使用關鍵字過濾                    | `pytest -k "delivery and not payment" -n 2`                            |
| 指定瀏覽器/裝置組合               | `pytest -m "order_page" --browser chrome --device iphone17 -n 2`       |
| 僅重跑失敗案例                    | `pytest --last-failed --reruns 2`                                      |

> ⚠️ **注意事項**  
> - 執行前請確認 Inline staging 網站可連線。  
> - Safari 需在 Develop 選單啟用「Allow Remote Automation」。  
> - Safari 使用 `--device` 時僅支援桌面視窗。

---

## 📚 開發指南

### 1. 新增裝置
1. 在 `config/devices/` 新建類別並繼承 `BaseDevice`。
2. 覆寫 `name`, `width`, `height`, `pixel_ratio`, `user_agent`。
3. 在 `config/config.py#get_device_class` 登記裝置代稱。

### 2. 新增頁面
1. 建立對應 locator（例：`locators/payment_page_locators.py`）。
2. 在 `pages/` 建立 page object，繼承 `BaseAction`。
3. 重用 `BaseAction` 內的等待/點擊等工具，避免重複 Selenium 程式碼。

### 3. 新增測試
1. 在 `features/*.feature` 撰寫情境。
2. 在 `tests/test_<feature>.py` 加入步驟實作。
3. 需要共享狀態時使用 fixture（例如 `order_context`）。

---

## ❓ 常見問題

### Safari 限制
- 啟用 **Develop ▸ Allow Remote Automation** 後再執行。
- 建議使用 Safari Technology Preview 以獲得較穩定的 WebDriver。
- 行動裝置模擬有限，若需完整手機場景請使用 Chrome/Firefox。
- > ⚠️ **Safari 不支援 headless 模式，務必使用視窗模式執行。**

---

祝測試順利！若有新裝置或付款流程，歡迎擴充此套件並整合更多 MCP 工具。

