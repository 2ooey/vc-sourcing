import schedule
import time
from sourcing_agent import SourcingAgent

def job():
    print("Running scheduled sourcing job...")
    agent = SourcingAgent()
    agent.run_daily_sourcing()

schedule.every().day.at("09:00").do(job)

if __name__ == "__main__":
    print("Runner started. Waiting for scheduled time (09:00 daily)...")
    while True:
        schedule.run_pending()
        time.sleep(60)
