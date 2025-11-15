# Web Automation Test Suite

> 🌐 This guide is also available in [Mandarin](README.zh-TW.md).

A Python-based end-to-end automation suite for Inline’s ordering experience.  
It combines classic Selenium + pytest-bdd scenarios with Playwright MCP-powered exploratory runs so you can validate both scripted and ad-hoc flows.

---

## 📑 Table of Contents

1. [Playwright MCP Setup](#-playwright-mcp-setup)
2. [Project Overview](#-project-overview)
3. [Tech Stack](#-tech-stack)
4. [Key Features](#-key-features)
5. [Quick Start](#-quick-start)
6. [Headless Mode](#headless-mode)
7. [Parallel Execution Recipes](#-parallel-execution-recipes)
8. [Development Guide](#-development-guide)
9. [FAQ](#-faq)

---

## 🎭 Playwright MCP Setup

Although Selenium drives the formal regression suite, we also wire Playwright through MCP for rapid debugging / live UI checks.

### Installation

```bash
pnpm add -D @playwright/mcp
# or
npm install --save-dev @playwright/mcp
```

Ensure the MCP entry exists in `~/.cursor/mcp.json`:

```json
"playwright": {
  "command": "npx",
  "args": ["@playwright/mcp@latest"]
}
```

### Usage Guidelines

1. Describe the target URL + objective before invoking `playwright_navigate`.
2. Execute steps exactly as written in the feature file.
3. Capture state after each important action (address card text, Edit button visibility, etc.).
4. Report results in the format `Navigate ➜ Actions ➜ Verification`.

### Official Resources

- [Playwright Docs](https://playwright.dev/)
- [Playwright GitHub](https://github.com/microsoft/playwright)
- [Cursor MCP Guide](https://cursor.sh/docs/mcp) – for enabling MCP agents.

---

## 🎯 Project Overview

| Aspect            | Details                                                                 |
|-------------------|-------------------------------------------------------------------------|
| Architecture      | Page Object Model + pytest-bdd                                          |
| Target Flow       | Inline restaurant ordering (delivery/takeout)                           |
| Multi‑device      | Desktop + mobile viewports via `config/devices/*`                       |
| Entry Point       | `pytest` with markers (`order_page`, `payment`, etc.)                   |
| CI Readiness      | Headless-friendly, parallelizable via `pytest-xdist`                    |

---

## ✨ Key Features

### 1. Multi-device simulation
- Device profiles live under `config/devices/` and inherit from `BaseDevice`.
- Switch via `--device iphone17` / `--device pixel9pro`.

### 2. Cross-browser matrix
- Supported: Chrome, Firefox, Safari (`--browser` flag).
- Headless toggle using `--headless`.

### 3. Classic Test Characteristics
- BDD scenarios in `features/`.
- Rich reporting via `pytest-html`, `allure-pytest`, rerun support.
- Centralized selectors (`locators/`) and base actions with timeout + fallback clicks.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+ (for Playwright MCP / tooling)
- Chrome / Firefox / Safari installed locally
- Optional: Android SDK for Appium MCP

### Installation

```bash
git clone https://github.com/<your-org>/web-automation.git
cd web-automation
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Running Tests

#### 1️⃣ Basic run
```bash
pytest -m "order_page"
```

#### 2️⃣ Device selection
```bash
pytest -m "order_page" --device=iphone17
```

#### 3️⃣ Advanced options
```bash
pytest -m "order_page" \
  --browser=firefox \
  --device=pixel9pro \
  --headless \
  --reruns=1 \
  -n 3
```

#### Headless Mode
Append `--headless` to any command. Uses Chrome headless by default unless `--browser` overrides it.

---

## 🧭 Parallel Execution Recipes

| Use Case                         | Command                                                                 |
|---------------------------------|-------------------------------------------------------------------------|
| Marker-based selection          | `pytest -m "order_page" -n 3`                                          |
| Specific file                   | `pytest tests/test_order_page.py -n 3`                                 |
| Keyword filter                  | `pytest -k "delivery and not payment" -n 2`                            |
| Device/Browser matrix           | `pytest -m "order_page" --browser chrome --device iphone17 -n 2`       |
| Re-run fails                    | `pytest --last-failed --reruns 2`                                      |

> ⚠️ **Notes:**  
> - Ensure the Inline staging site is reachable before starting.  
> - Safari automation requires enabling “Allow Remote Automation” in Safari’s Develop menu.  
> - When using `--device` with Safari, only desktop viewport is supported.

---

## 📚 Development Guide

### 1. Add a New Device
1. Create a class under `config/devices/` inheriting `BaseDevice`.
2. Override `name`, `width`, `height`, `pixel_ratio`, `user_agent`.
3. Register the device alias in `config/config.py#get_device_class`.

### 2. Add a New Page
1. Create a locator file (e.g., `locators/payment_page_locators.py`).
2. Implement page actions in `pages/<page>.py`, inheriting `BaseAction`.
3. Reuse wait/click helpers; avoid duplicate Selenium logic.

### 3. Add a New Test
1. Describe the scenario in `features/*.feature`.
2. Add step definitions in `tests/test_<feature>.py`.
3. Use fixtures to share context where necessary (see `order_context` example).

---

## ❓ FAQ

### Safari Limitations
- Enable **Develop ▸ Allow Remote Automation** before running tests.
- Safari Technology Preview is recommended for more stable WebDriver support.
- Some mobile emulation modes are unavailable in Safari; use Chrome/Firefox for those flows.
- > ⚠️ **Safari does not support headless mode. Always run it in headed mode.**

---

Happy testing! Feel free to extend the suite with additional devices, payment scenarios, or MCP integrations as needed.

