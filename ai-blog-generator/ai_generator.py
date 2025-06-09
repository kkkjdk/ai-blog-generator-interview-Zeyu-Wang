import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

AFFILIATE_LINKS = {
    "AFF_LINK_1": "https://example.com/affiliate/product1",
    "AFF_LINK_2": "https://example.com/affiliate/product2",
    "AFF_LINK_3": "https://example.com/affiliate/product3"
}


def generate_blog_content(keyword, seo_data):
    """
    Generate blog contents by using deepseek API.
    :param keyword: target keyword
    :param seo_data: SEO data dictionary
    :return: contents of generated blogs (Markdown format)
    """
    prompt = f"""
    As a professional SEO contents author, please write a comprehensive and professional blog post for 
    keyword"{keyword}"
    Requirements:
    1. The headline of this blog should include primary keyword"{keyword}", and attract reader to click simultaneously 
    2. The structure of this article
       - compelling introductions (about 100 words)
       - 3-5 primary content parts, each of which has a sub-headline
       - product recommendation using placeholders {{AFF_LINK_1}}, {{AFF_LINK_2}}, {{AFF_LINK_3}}
       - conclusion part including action proposals
    3. integrate SEO data naturally
       - search volume in a month: {seo_data['search_volume']}
       - keyword difficulty: {seo_data['keyword_difficulty']}/100
       - average CPC: ${seo_data['avg_cpc']}
    4. include 3 internal link suggestions (using [link texts](internal link) format)
    5. output format: use Markdown format, including headlines, sub-headlines, paragraphs and lists
    6. The length of this article: 1000-1200 words
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-r1",
            messages=[
                {"role": "system",
                 "content": "You are an experienced SEO author who focuses on high-quality and "
                            "well-designed blog contents"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        content_response = response.choices[0].message.content.strip()
        for placeholder, link in AFFILIATE_LINKS.items():
            content_response = re.sub(r"\{+\s*%s\s*\}+|%s" % (placeholder, placeholder), link, content_response)
        return content_response
    except Exception as e:
        print(f"deepseek API Error: {e}")
        return f"# Failed to generate contents\n\nerror: {str(e)}"


if __name__ == "__main__":
    mock_seo = {
        "search_volume": 8500,
        "keyword_difficulty": 65,
        "avg_cpc": 2.35
    }
    content = generate_blog_content("university", mock_seo)
    print("Generated Content:\n")
    print(content)
