import json
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Udajemy prawdziwego użytkownika
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        
        # Ten link prowadzi bezpośrednio do JSONa z propsami
        url = "https://www.bovada.lv/services/sports/event/v2/events/A/description/basketball/nba?marketFilterId=def&includeDirectAncestors=true"
        
        print(f"Pobieram dane z: {url}")
        page.goto(url, wait_until="networkidle")
        time.sleep(5) # Czekamy na załadowanie danych
        
        # Wyciągamy czysty tekst JSON
        content = page.locator("body").inner_text()
        
        try:
            # Sprawdzamy czy to poprawny JSON
            data = json.loads(content)
            with open("nba_data.json", "w") as f:
                json.dump(data, f)
            print("SUKCES: Dane zapisane.")
        except:
            print("BŁĄD: Nie udało się sparsować JSONa.")
            with open("nba_data.json", "w") as f:
                f.write(content)

        browser.close()

if __name__ == "__main__":
    run()
