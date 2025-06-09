import random
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_seo_data(keyword):
    """
    Get SEO data of the keyword.
    :param keyword: target keyword
    :return: a dictionary containing SEO data
    """
    try:
        with open('mock_keywords.json') as f:
            data = json.load(f)
            for item in data['keywords']:
                if item['name'].lower() == keyword.lower():
                    return {
                        "keyword": keyword,
                        "search_volume": item['search_volume'],
                        "keyword_difficulty": item['difficulty'],
                        "avg_cpc": item['cpc'],
                        "source": "json_mock"
                    }
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return {
        "keyword": keyword,
        "search_volume": random.randint(1000, 10000),
        "keyword_difficulty": random.randint(1, 100),
        "avg_cpc": round(random.uniform(0.2, 5.0), 2),
        "source": "random_mock"
    }


if __name__ == "__main__":
    print("Mock SEO Data:", get_seo_data("wireless earbuds"))
