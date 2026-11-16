# 星燈港冒險者公會｜D&D 冒險委託布告欄

Repository 名稱：`vibe-dnd`。

## 專案簡介

星燈港是一座原創的奇幻港城。玩家從公會布告欄挑選短篇冒險，閱讀委託、報酬與第一條線索；主持人展開專屬筆記後，可查看真相、人物動機與不同選擇的後果。現有委託為〈鐘樓第十三聲〉、〈失蹤的渡船〉與五星委託〈無星之夜的燈塔〉。

## 閱讀與維護

下載專案後開啟 `index.html` 即可閱讀。維護規則見 [AGENTS.md](AGENTS.md)。網站採用靜態 HTML、CSS 與 JavaScript，產生器只需要 Python 3，沒有額外套件或 API 金鑰。GitHub Pages 發布方式見下方。

## 網站特色

- 動漫奇幻公會場景、臺灣時間時鐘、錯落釘貼的委託書。
- 紙條顯示地點與一至五星難度；懸停顯示標題及簡介，點擊整張紙開啟完整卷軸。
- 主持人筆記預設收合，展開時延續卷軸動畫。
- 每面最多五張，只有中間公告板翻轉；最後一面接回第一面，只有一面時不顯示翻頁按鈕。
- 五星與特別委託優先排列；五星滿面後，後續頁面套用相同規則。完整規則見 AGENTS.md。
- 從委託返回時保留原本的公告板分面。

## 專案結構

| 路徑 | 用途 |
|---|---|
| `AGENTS.md` | AI 必須遵循的內容、視覺、排序與開發規則 |
| `quests/*.json` | 每張委託的原始內容；新增委託時修改這裡 |
| `build.py` | 檢查資料、產生首頁與委託內頁 |
| `style.css` | 全站字體、配色、紙張、卷軸與動畫 |
| `board.js`、`flip.js`、`return-board.js` | 時鐘、紙條互動、翻面與返回位置 |
| `assets/` | 插畫、紙紋、飾框與字型授權 |
| `flip-preview.html`（選用） | 執行 `python build.py --preview` 產生的本機預覽，不包含在上傳包 |
| `publish.py` | 檢查生成頁面並整理正式網站到 `_site/` |
| `.github/workflows/pages.yml` | 推送 main 後發布 GitHub Pages |

## 如何新增委託

1. 複製 `quests/lost-ferry.json`，改成唯一英文小寫檔名，例如 `moonlit-caravan.json`。
2. `number` 使用現有最大值加一，建立後不更改。填寫故事欄位，設定 `difficulty` 為 1～5；特別委託才把 `special` 設成 `true`。
3. 在專案目錄執行：

```sh
python build.py
python build.py --check
```

4. 開啟首頁，確認地點、星數、懸停預覽、完整委託及主持人筆記；若超過五張，再確認翻面與返回位置。
5. 將 JSON 與生成的 HTML 一起提交。不要只改生成的 HTML，下次重建會覆蓋它。

可以這樣請 AI 新增內容：

> 請先閱讀 AGENTS.md，新增一張發生在月影商道的三星委託。沿用既有格式，包含具體線索、人物動機、至少兩條調查路線與不同結局。使用下一個 number，重建並檢查網站，保持既有視覺及排序規則。

## 發布到 GitHub Pages

1. 將此專案的內容放在 GitHub 儲存庫根目錄，使用 `main` 分支。
   使用上傳包時先解壓縮，上傳裡面的檔案與資料夾（包含 `.github`），不要只上傳 ZIP，也不要在儲存庫根目錄多包一層 `vibe-dnd` 資料夾。
2. 到儲存庫 **Settings → Pages → Build and deployment → Source** 選擇 **GitHub Actions**。
3. 推送至 `main`，或在 **Actions → Publish guild board → Run workflow** 啟動發布。
4. 工作流程會檢查資料與 HTML 一致，將正式頁面及資源打包發布；測試頁、原始 JSON 與開發文件保留在儲存庫，不包含在網站成品。
5. 以 Pages 顯示的網址為準，確認首頁、三張委託、字體圖片與返回功能後再繳交。

本機可執行 `python publish.py` 檢查發布成品。`_site/` 為自動產生的目錄，不需提交。網站支援儲存庫子路徑，沒有後端服務。

## 規則如何幫助 AI 延伸內容

AGENTS.md 指定資料夾、命名方式、必填欄位、劇透放置位置與驗收步驟。AI 新增一份委託 JSON 後，執行 `python build.py` 就會同步產生內頁並更新首頁。〈失蹤的渡船〉依照這個流程新增，沿用第一張委託的版型，保有自己的線索與結局。執行 `python build.py --check` 可核對資料與生成頁面。

## 字型

全站使用 LXGW 的霞鶩文楷 TC，Regular 與 Medium 字檔隨網站提供；標題較重的樣式對應 Medium。來源為 [LXGW WenKai TC](https://github.com/lxgw/LxgwWenkaiTC)，授權見 [WenKai-OFL.txt](assets/fonts/WenKai-OFL.txt)。公會場景與裝飾插畫由 AI 生成，故事為本專案創作；D&D 為主題參考，本網站為非官方課堂作品。
