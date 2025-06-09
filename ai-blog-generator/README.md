# AI-Powered Blog Post Generator with Daily Automation

A Flask-based tool for generating blog posts on-demand or automatically via manual scheduling.

---

## 1. Installation
- Clone the repository or download the code to your local machine.
- Install Python dependencies (Python 3.11 recommended):

   ```bash
   pip install -r requirements.txt

---

## 2. Running the Application
### 2.1 Start the Server
```bash
python app.py
```
- The service will run by default at `http://127.0.0.1:5000`.

### 2.2 Verify the Service
- Open your browser and visit `http://127.0.0.1:5000`, and you should see the homepage title:  **"AI-Powered Blog Post Generator with Daily Automation"**.

### 2.3 Generate a Blog Post
- To generate a post on-demand, visit the following URL in your browser and replace `KEYWORD` with your target topic:  

  ```
  http://localhost:5000/generate?keyword=KEYWORD
  ```

- The generated Markdown file will be saved in the `posts` directory.

---

## 3. Scheduler Configuration
- The scheduler is set to run **daily at 00:00 (midnight) EST** by default.  
- To customize the schedule, modify the `scheduler.add_job()` line in `app.py`:  

  ```python
  scheduler.add_job(
      id='scheduled_blog_post',
      func=scheduled_job,
      trigger='cron',
      hour=0,  # Change this to adjust the hour (24-hour format)
      minute=0  # Change this to adjust the minute
  )
  ```

  - Example: Set `hour=6` to run at 6 AM EST daily.

---

## 4. Notes
1. The generated posts are saved as Markdown files in the `posts` directory (created automatically if it doesn’t exist).  