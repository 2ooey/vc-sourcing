import os
import json
import urllib.parse
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from google_clients import GoogleClients
from evaluator import SourcingEvaluator

load_dotenv()

class SourcingAgent:
    def __init__(self):
        self.evaluator = SourcingEvaluator()
        self.google_clients = GoogleClients()
        self.spreadsheet_id = os.environ.get("SPREADSHEET_ID")
        self.email_to = os.environ.get("EMAIL_TO")

    def run_daily_sourcing(self):
        print("Starting daily sourcing...")
        
        # 1. Fetch raw data (Simulation of Web Scraping for Saitama startups)
        # In a real scenario, this would scrape PR TIMES keyword search for "埼玉 スタートアップ 資金調達" 
        # For demonstration, we use some dummy scraped data that matches the new rules
        raw_startups = self._scrape_startups()
        
        if not raw_startups:
            print("No new startups found today.")
            return

        evaluated_results = []
        for startup in raw_startups:
            print(f"Evaluating {startup['name']}...")
            eval_json_str = self.evaluator.evaluate_startup(
                company_name=startup["name"], 
                description=startup["description"],
                url=startup["url"]
            )
            try:
                eval_data = json.loads(eval_json_str)
            except:
                eval_data = {}
                
            evaluated_results.append({
                "name": eval_data.get("企業名", startup["name"]),
                "url": eval_data.get("企業URL", startup["url"]),
                "location": eval_data.get("所在地", ""),
                "founded_year": eval_data.get("設立年", ""),
                "description": eval_data.get("事業概要", startup["description"]),
                "domain": eval_data.get("領域分類", ""),
                "social_impact": eval_data.get("社会性・課題意識", ""),
                "tech_uniqueness": eval_data.get("技術／独自性", ""),
                "stage": eval_data.get("想定ステージ", ""),
                "funding": eval_data.get("資本・調達状況", ""),
                "score": eval_data.get("評価", "C"),
                "reason": eval_data.get("評価コメント", "解析エラー")
            })

        # 2. Append to Google Sheets
        self._write_to_sheets(evaluated_results)
        
        # 3. Send Summary Email
        self._send_summary_email(evaluated_results)
        
        print("Daily sourcing completed successfully.")

    def _scrape_startups(self):
        # 実際のリサーチ結果をモックとして注入（埼玉県・設立3年以内・AI/DX関連・若手起業家）
        return [
            {
                "name": "株式会社AI共創総研",
                "url": "https://controudit.ai/",
                "description": "2024年9月設立（埼玉県さいたま市岩槻区）。AIリスクアセスメントやAI戦略構築などのコンサルティングを提供。LLMセキュリティやISO/IEC 42001取得支援事業を展開。スタートアッププログラムSCAP採択。代表取締役CEO 藤井 涼氏（SNS: LinkedInにて発信あり）。"
            },
            {
                "name": "株式会社デジタルツール研究所",
                "url": "https://digitool-lab.com/",
                "description": "2024年7月設立（埼玉県比企郡・行田市）。地域の中小企業向けに「月額制DX顧問サービス」や「AI/SNS研修プログラム」を提供し、生成AI普及によるDX格差の解消を目指す。代表：松岡 鉄平氏。"
            },
            {
                "name": "株式会社nekonata",
                "url": "https://saitama-u.ac.jp/ (所属大学発)",
                "description": "2025年2月設立。埼玉大学の学生起業家である田原 大輔氏が立ち上げた埼玉大学認定ベンチャー（所在地: 埼玉）。学生向けの情報可視化・DXモバイルアプリ「埼大アプリ」などを開発・運営。"
            }
        ]

    def _write_to_sheets(self, results):
        if not self.spreadsheet_id:
            print("SPREADSHEET_ID not set. Skipping sheets append.")
            return
            
        # Format for sheets: 13 columns
        # ['日付', '企業名', '企業URL', '所在地', '設立年', '事業概要', '領域分類', '社会性・課題意識', '技術／独自性', '想定ステージ', '資本・調達状況', '評価', '評価コメント']
        from datetime import datetime
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        values = []
        for r in results:
            values.append([
                today_str,
                r["name"],
                r["url"],
                r["location"],
                r["founded_year"],
                r["description"],
                r["domain"],
                r["social_impact"],
                r["tech_uniqueness"],
                r["stage"],
                r["funding"],
                r["score"],
                r["reason"]
            ])
            
        # Write to "List" (needs to exist)
        self.google_clients.append_to_sheet(self.spreadsheet_id, "List!A:M", values)

    def _send_summary_email(self, results):
        if not self.email_to:
            print("EMAIL_TO not set. Skipping email send.")
            return

        subject = "[Daily Report] Saitama Sourcing Agent"
        body = "本日のソーシング結果（埼玉・若手・ソーシャル領域）のご報告です：\n\n"
        
        for r in results:
            body += f"■ {r['name']} (評価: {r['score']})\n"
            body += f"URL: {r['url']}\n"
            body += f"概要: {r['description']}\n"
            body += f"理由: {r['reason']}\n\n"
            
        self.google_clients.send_email(self.email_to, subject, body)

if __name__ == "__main__":
    agent = SourcingAgent()
    agent.run_daily_sourcing()
