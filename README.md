# 學前幼兒生活島 — 完整網站架構 (新版)

## 🆕 本版本架構變化

從「一整段 mp3 + timeline JSON」改為「**每句一個 mp3**」。優點:
- **字幕跟語音 100% 同步** (不再需要 timeline)
- **未來換真人錄音只要覆蓋檔案**,不用動程式碼
- **句子結尾自動含 150ms 靜音**,銜接自然且給瀏覽器預載時間

## 📁 目錄結構

```
preschool/                          ← 拖整包到 Cloudflare Pages
│
├── index.html                      ← 首頁:列出所有 18 個主題
├── build_all_audio.bat             ← 一鍵批次產生所有語音
│
├── parents/                        ← 主題:新時代的父母
│   ├── index.html                  ← 主題頁
│   ├── 06/                         ← 情境6
│   │   ├── index.html              ← 情境播放頁
│   │   ├── lines.json              ← 字幕資料 (已預產)
│   │   ├── generate_audio.py       ← 語音產生腳本
│   │   ├── README.txt              ← 提醒要放圖片
│   │   ├── image.png               ← (你放) 情境圖片
│   │   ├── line_01_zh.mp3          ← (腳本產生) 第1句中文
│   │   ├── line_02_zh.mp3          ← 第2句
│   │   ├── ... 
│   │   ├── line_16_zh.mp3
│   │   ├── line_01_en.mp3          ← 英文檔案
│   │   ├── line_02_en.mp3
│   │   └── ...
│   └── ...
├── traits/ ...  (其他主題)
```

**總計:18 主題,82 情境**

## 🚀 一次跑完所有語音

### 前置:安裝套件

```
pip install edge-tts pydub
```

**Windows 還要裝 ffmpeg** (pydub 讀寫 mp3 需要):
1. 下載 https://www.gyan.dev/ffmpeg/builds/ (選 ffmpeg-release-essentials.zip)
2. 解壓縮到 `C:\ffmpeg`
3. 把 `C:\ffmpeg\bin` 加到系統 PATH
4. 開新的 cmd 視窗,打 `ffmpeg -version` 確認

### 執行

雙擊 `build_all_audio.bat`,它會自動跑完 82 個情境的語音。

⏱ 全部約需 20-30 分鐘。

## 📸 放圖片

每個情境資料夾都有 `README.txt` 提醒你要放圖片。把對應的圖片**改名為 `image.png`**,放進去。

## 🚀 部署到 Cloudflare

1. 所有圖片放好、語音產生完成
2. 把整個 `preschool` 資料夾拖到 Cloudflare Pages
3. 部署完成

## 🎙️ 未來換真人錄音

真人錄音師只要按照這個檔名規則錄音:

```
line_01_zh.mp3  ← 第1句中文 (長度: 唸完句子就好,結尾不用留靜音)
line_02_zh.mp3  ← 第2句
...
line_01_en.mp3  ← 第1句英文
...
```

**建議在每句結尾保留 100~200ms 的自然收尾氣音**,聽起來會比較自然。或是用音訊軟體後處理加 150ms 靜音。

把檔案直接覆蓋進資料夾,**不用改任何程式碼**,重新部署就好。

## 🎨 主題 ↔ 路徑對照表

| # | 主題 | 路徑 | 情境數 |
|---|---|---|---|
| 1 | 孩童的生活和行為特徵 | `traits` | 6 |
| 2 | 給孩子的想像空間 | `imagine` | 4 |
| 3 | 不要成為孩子的奴隸 | `notslave` | 3 |
| 4 | 關於管教的種種 | `discipline` | 4 |
| 5 | 新時代的父母 | `parents` | 6 |
| 6 | 單親問題面面觀 | `singleparent` | 3 |
| 7 | 透過藝術的孩童教育 | `art` | 2 |
| 8 | 怎樣幫助孩子學習說話 | `speech` | 6 |
| 9 | 孩童的活動與遊戲 | `activity` | 5 |
| 10 | 如何培養孩子適應群體生活 | `social` | 4 |
| 11 | 要不要提早入學 | `earlyschool` | 2 |
| 12 | 孩童睡覺學問大 | `sleep` | 4 |
| 13 | 怎樣訓練孩童大小便 | `toilet` | 9 |
| 14 | 孩子注意力不集中怎麼辦 | `focus` | 5 |
| 15 | 孩子說謊怎麼辦 | `lying` | 5 |
| 16 | 如何幫助孩子克服害羞 | `shy` | 3 |
| 17 | 跟嫉妒說再見 | `jealousy` | 6 |
| 18 | 如何改變孩子過度依賴 | `dependency` | 5 |

## 💡 調整提示

### 想改停頓時間?
編輯個別情境的 `generate_audio.py`,改這一行:
```python
TARGET_TAIL_SILENCE_MS = 150
```
然後重跑該情境的腳本。

### 想換語音?
改這兩行:
```python
ZH_VOICE = "zh-TW-HsiaoChenNeural"   # 或 zh-TW-HsiaoYuNeural, zh-TW-YunJheNeural
EN_VOICE = "en-US-AriaNeural"        # 或 en-US-JennyNeural, en-US-GuyNeural
```
