from typing import Optional, List, Dict

import googlesearch
import requests

from bs4 import BeautifulSoup


class WikipediaScraper:
    
    def __init__(self, query: str):
        self.query = query
    
    def get_sanitized_wiki(self) -> List[Dict[str, str]]:
        pass
        html = requests.get(self.get_target_page(self.query)).text
        
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.find(name="div", attrs={"id": "mw-content-text"})
        soup = soup.findAll(name=["p", "h2", "h3", "h4"])
        
        sanitized_content = []
        for tag in soup:
            if tag.name == 'p':
                raw_string = "".join(tag.strings).strip()
                if raw_string and raw_string != '\n':
                    sanitized_content.append({"type": "paragraph", "content": raw_string})
            else:
                raw_string = "".join(tag.strings).strip()
                sanitized_string = raw_string.replace("[edit]", "")
                # omit notes and references section
                if [word for word in ["Notes", "References"] if word in sanitized_string]:
                    break
                sanitized_content.append({"type": "heading", "content": sanitized_string})
        return sanitized_content
    
    @staticmethod
    def get_target_page(query: str) -> Optional[str]:
        # takes a query string and returns the associated wiki page.
        for item in googlesearch.search(query, stop=5):
            if "wikipedia" in item:
                return item
        
        return None
