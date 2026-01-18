import json
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Uruchamiamy przeglądarkę
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        
        url = "https://www.bovada.lv/services/sports/event/v2/events/A/description/basketball/nba?marketFilterId=def&includeDirectAncestors=true"
        
        print(f"Wchodzę na: {url}")
        page.goto(url, wait_until="networkidle")
        
        # Pobieramy czystą treść strony (JSON)
        content = page.locator("pre").inner_text()
        
        try:
            data = json.loads(content)
            with open("nba_data.json", "w") as f:
                json.dump(data, f)
            print("Sukces! Dane zapisane do nba_data.json")
        except:
            # Jeśli Bovada nie wyświetliła JSONa w <pre>, bierzemy całą treść
            body = page.inner_text("body")
            with open("nba_data.json", "w") as f:
                f.write(body)
            print("Zapisano surową treść body.")

        browser.close()

if __name__ == "__main__":
    run()
