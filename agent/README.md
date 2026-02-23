# Saitama VC Sourcing Automated Agent

This project contains a daily automated agent that searches for startup funding and founding information (focusing on Saitama prefecture, young founders, and specific "social/well-being" domains) as specified in `rules.md`.
It uses an LLM to evaluate the startups and then saves the results to a Google Spreadsheet and sends an email report via Gmail.

## Prerequisites

1. **Python 3.9+**
2. **Google Cloud Project**:
   - Enable **Google Sheets API** and **Gmail API**.
   - Create an **OAuth 2.0 Client ID** (Desktop Application) and download it as `credentials.json` into the `agent/` directory.
3. **LLM API Key**: Gemini API key (`GOOGLE_API_KEY`) is required for evaluation.

## Setup Instructions

1. Install dependencies:
   ```bash
   cd agent
   pip install -r requirements.txt
   ```

2. Set environment variables. Create a `.env` file in `agent/`:
   ```env
   GOOGLE_API_KEY="your-gemini-api-key"
   SPREADSHEET_ID="your-google-spreadsheet-id"
   EMAIL_TO="your-email@example.com"
   ```

3. First Time Run (Authentication):
   Run the Google Clients script once to authorize the app and generate a `token.json` file.
   ```bash
   python src/google_clients.py
   ```
   *This will open a browser window asking you to log in to your Google Account and grant permissions.*

## Running the Agent

To run the sourcing agent manually:
```bash
python src/sourcing_agent.py
```

## GitHub Actions (定期実行) のセットアップ

毎週金曜日の18:00に自動でエージェントを動かすには、以下の手順でGitHubリポジトリの設定を行います。

### 1. 認証ファイルのBase64エンコード
GitHub Secretsにはファイルの中身を直接貼ることができないため、Base64という形式の文字列に変換します。
ターミナルで以下のコマンドを実行し、出力された長い文字列をコピーしてください。

```bash
# credentials.json のエンコード
base64 -i agent/credentials.json | tr -d '\n' | pbcopy
# (クリップボードにコピーされるので、どこかにメモしてください)

# token.json のエンコード
base64 -i agent/token.json | tr -d '\n' | pbcopy
# (同様にコピーしてメモしてください)
```

### 2. GitHubリポジトリの作成とプッシュ
1. [GitHub](https://github.com/)上で新しい空のリポジトリを作成します。
2. ターミナルで初期化してプッシュします：
   ```bash
   git init
   git add .
   # .env や credentils.json、token.json は直接アップロードしないよう .gitignore に設定することをお勧めします。
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git
   git push -u origin main
   ```

### 3. GitHub Secrets の登録
GitHubリポジトリの画面で、`Settings` > `Secrets and variables` > `Actions` を開き、「New repository secret」から以下の5つの変数を登録します。

1. **`GOOGLE_API_KEY`**: GeminiのAPIキー (`.env`に書いたもの)
2. **`SPREADSHEET_ID`**: シートのID (`.env`に書いたもの)
3. **`EMAIL_TO`**: メール送信先 (`.env`に書いたもの)
4. **`GOOGLE_CREDENTIALS_B64`**: 先ほどBase64エンコードした `credentials.json` の文字列
5. **`GOOGLE_TOKEN_B64`**: 先ほどBase64エンコードした `token.json` の文字列

### 4. 実行の確認
金曜日の18時になれば自動的に `Actions` タブで処理が走ります。
手動でテストしたい場合は、`Actions` タブ -> `Weekly Automated Sourcing` -> `Run workflow` ボタンから実行可能です。
