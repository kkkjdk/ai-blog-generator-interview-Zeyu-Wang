import os
import re
import pytz
from flask import Flask, request, jsonify
from datetime import datetime
from flask_apscheduler import APScheduler
from seo_fetcher import get_seo_data
from ai_generator import generate_blog_content

app = Flask(__name__)

if not os.path.exists('posts'):
    os.makedirs('posts')


def generate_and_save_post(keyword):
    """
    Generate blog posts and store them.
    :param keyword: target keyword
    :return: a path to store files
    """
    try:
        seo_data = get_seo_data(keyword)
        content = generate_blog_content(keyword, seo_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_keyword = re.sub(r'[^a-zA-Z0-9]+', '_', keyword)
        filename = f"posts/{timestamp}_{safe_keyword}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Generated post for '{keyword}' saved to {filename}")
        return filename

    except Exception as e:
        print(f"Error generating post for '{keyword}': {str(e)}")
        return None


@app.route('/')
def home():
    return '<h1 style="font-weight: bold; font-size: 24px;">AI-Powered Blog Post Generator with Daily Automation</h1>'


@app.route('/generate', methods=['GET'])
def generate_post():
    """
    Generate blog posts.
    """
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({
            "status": "error",
            "message": "Missing 'keyword' parameter"
        }), 400

    file_path = generate_and_save_post(keyword)

    if file_path:
        return jsonify({
            "status": "success",
            "message": f"Blog post generated for '{keyword}'",
            "file_path": file_path
        })
    else:
        return jsonify({
            "status": "error",
            "message": f"Failed to generate post for '{keyword}'"
        }), 500


def scheduled_job():
    """
    Generate a new post for a predefined keyword once per day.
    """
    keyword = "software engineering"
    print(f"Starting scheduled job for keyword: {keyword}")
    file_path = generate_and_save_post(keyword)
    if file_path:
        print(f"Scheduled job completed: {file_path}")
    else:
        print(f"Scheduled job failed for {keyword}")


class Config(object):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = pytz.timezone('America/New_York')


app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.add_job(id='scheduled_blog_post', func=scheduled_job, trigger='cron', hour=0, minute=0)
if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler.start()

if __name__ == '__main__':
    print("Starting Flask app...")
    print("Scheduled jobs:", scheduler.get_jobs())
    app.run(host='0.0.0.0', port=5000, debug=True)
