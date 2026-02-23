import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class SourcingEvaluator:
    def __init__(self, rules_path="../rules.md"):
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"})
        self.rules_path = rules_path
        self.rules_text = self._load_rules()

    def _load_rules(self):
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "Rules file not found."

    def evaluate_startup(self, company_name, description, url=""):
        prompt = f"""
あなたはVC（ベンチャーキャピタル）の優秀なソーシング・エージェントです。
以下のルール（投資候補選定・探索ガイドライン）に基づき、提示されたスタートアップ企業を評価してください。

【ルール】
{self.rules_text}

【評価対象スタートアップ】
- 企業名: {company_name}
- URL: {url}
- 概要/ニュース: {description}

【タスク】
この情報を元に、評価と各項目を抽出・推測して埋めてください。
出力は以下のJSONフォーマットのみに整えてください（Markdownなどの修飾は不要です）。

{{
  "企業名": "企業名",
  "企業URL": "URL",
  "所在地": "わかる範囲の所在地（例：埼玉県さいたま市）",
  "設立年": "設立年（例：2024年）",
  "事業概要": "2〜3文で要約した事業概要（代表者のSNS情報があれば含める）",
  "領域分類": "事業領域のラベル（SaaS, 生成AI, Vertical AI 等）",
  "社会性・課題意識": "解決しようとしている社会課題やペインポイントについて",
  "技術／独自性": "AI/DX関連の技術的な強みや独自性について",
  "想定ステージ": "シード, シリーズA等（不明な場合はシード前〜シード等）",
  "資本・調達状況": "資金調達の情報があれば記載",
  "評価": "A, B, C のいずれか",
  "評価コメント": "評価の推論・根拠を記述"
}}
"""
        try:
            response = self.model.generate_content(prompt)
            result_json = response.text
            return result_json
        except Exception as e:
            print(f"Error evaluating {company_name}: {e}")
            return '{{"evaluation_score": "Error", "reason": "Failed to evaluate via LLM"}}'
