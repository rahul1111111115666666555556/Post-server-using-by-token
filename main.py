from flask import Flask, request, flash, redirect, url_for, render_template_string
import requests
import time
import threading
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
FACEBOOK_GRAPH_URL = "https://graph.facebook.com/{}/comments/"

def post_comments(fb_token, post_id, commenter_name, comments, delay):
    for comment in comments:
        time.sleep(delay)
        comment_with_name = f"{commenter_name}: {comment}"
        data = {'message': comment_with_name, 'access_token': fb_token}
        res = requests.post(FACEBOOK_GRAPH_URL.format(post_id), data=data).json()
        if 'error' in res:
            print(f"❌ Failed: {comment_with_name} - {res['error'].get('message', 'Unknown error')}")
        else:
            print(f"✅ Comment posted: {comment_with_name}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            fb_token = request.form['fb_token']
            post_id = request.form['post_id']
            commenter_name = request.form['commenter_name']
            delay = int(request.form['delay'])
            comments_file = request.files['comments_file']

            if not comments_file:
                flash("❌ No file uploaded!", "danger")
                return redirect(url_for('index'))

            comments_content = comments_file.read().decode('utf-8').strip()
            if not comments_content:
                flash("❌ Uploaded file is empty!", "danger")
                return redirect(url_for('index'))

            comments = comments_content.splitlines()

            thread = threading.Thread(target=post_comments, args=(fb_token, post_id, commenter_name, comments, delay))
            thread.start()

            flash("✅ Comments are being posted in the background!", "success")
            return redirect(url_for('index'))

        except Exception as e:
            flash(f"❌ Error: {str(e)}", "danger")
            return redirect(url_for('index'))

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>AL3X POST SERVER</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0; padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            body {
                background: #121212;
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                min-height: 100vh;
                padding: 20px;
            }
            h2 {
                color: #ff4d4d;
                margin-bottom: 20px;
                font-size: 2em;
                text-shadow: 1px 1px 3px #000;
            }
            form {
                background: #1e1e1e;
                padding: 30px;
                border-radius: 10px;
                width: 100%;
                max-width: 500px;
                box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
            }
            label {
                font-weight: bold;
                color: #ff4d4d;
            }
            input[type="text"],
            input[type="number"],
            input[type="file"],
            button {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 20px;
                border-radius: 5px;
                border: none;
                font-size: 16px;
            }
            input, select {
                background-color: #2e2e2e;
                color: white;
            }
            button {
                background-color: #ff4d4d;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }
            button:hover {
                background-color: #e60000;
            }
            .flash {
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: center;
            }
            .success {
                background-color: #145214;
                color: #a4f3a4;
            }
            .danger {
                background-color: #5a0000;
                color: #ffb3b3;
            }
            .footer {
                margin-top: 40px;
                color: #aaa;
                font-size: 14px;
            }
            .whatsapp-button {
                display: inline-block;
                margin-top: 20px;
                background-color: #25D366;
                color: white;
                padding: 15px 25px;
                text-decoration: none;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
            }
            .whatsapp-button:hover {
                background-color: #1cba56;
            }
        </style>
    </head>
    <body>
        <h2>🔥 AL3X AUTO COMMENT TOOL 🔥</h2>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="post" enctype="multipart/form-data">
            <label>Facebook Token:</label>
            <input type="text" name="fb_token" required>

            <label>Post ID (numeric only):</label>
            <input type="text" name="post_id" required>

            <label>Commenter Name (e.g., AL3X):</label>
            <input type="text" name="commenter_name" required>

            <label>Delay (in seconds):</label>
            <input type="number" name="delay" required min="1">

            <label>Upload File (1 comment per line):</label>
            <input type="file" name="comments_file" required>

            <button type="submit">🚀 Start Posting</button>
        </form>

        <a class="whatsapp-button" href="https://wa.me/+9779824204204" target="_blank">💬 Contact on WhatsApp</a>

        <div class="footer">2025 © Developed by Alex Khan | All Rights Reserved.</div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
