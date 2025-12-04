from flask import Flask, request, render_template_string
import re
import string

app = Flask(__name__)

def assess_password(password):
    score = 0
    feedback = []
    
    length_criteria = len(password) >= 8
    length_bonus = len(password) >= 12
    has_lower = re.search(r"[a-z]", password)
    has_upper = re.search(r"[A-Z]", password)
    has_digit = re.search(r"\d", password)
    has_special = re.search(f"[{re.escape(string.punctuation)}]", password)

    if not length_criteria:
        return {
            "rating": "WEAK",
            "color": "#ff4d4d",
            "width": "20%",
            "feedback": ["CRITICAL: Password is too short (Must be 8+ characters)."]
        }

    score += 1
    if length_bonus: score += 1
    if has_lower: score += 1
    if has_upper: score += 1
    if has_digit: score += 1
    if has_special: score += 1

    if not has_lower: feedback.append("Missing lowercase letters (a-z)")
    if not has_upper: feedback.append("Missing uppercase letters (A-Z)")
    if not has_digit: feedback.append("Missing numbers (0-9)")
    if not has_special: feedback.append("Missing symbols (!@#$...)")
    if not length_bonus and score > 2: feedback.append("Tip: Make it 12+ chars for max security")

    if score <= 3:
        return {"rating": "WEAK", "color": "#ff4d4d", "width": "30%", "feedback": feedback}
    elif score <= 5:
        return {"rating": "MODERATE", "color": "#ffc107", "width": "60%", "feedback": feedback}
    else:
        return {"rating": "STRONG", "color": "#00ff9d", "width": "100%", "feedback": ["Perfect! This is a solid password."]}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CryptScale // Password Audit</title>
    <style>
        :root { --bg: #0d1117; --card: #161b22; --text: #c9d1d9; --accent: #58a6ff; }
        body {
            background-color: var(--bg); color: var(--text);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; margin: 0;
        }
        .container {
            background-color: var(--card); padding: 2.5rem;
            border-radius: 12px; border: 1px solid #30363d;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            width: 400px;
        }
        h1 { margin-top: 0; color: white; font-size: 1.5rem; display: flex; align-items: center; gap: 10px;}
        .shield-icon { font-size: 1.5rem; }
        
        .input-group { position: relative; margin-top: 20px; }
        input {
            width: 100%; padding: 15px; padding-right: 50px;
            background: #0d1117; border: 1px solid #30363d;
            color: white; border-radius: 8px; font-size: 1.1rem;
            box-sizing: border-box; outline: none; transition: 0.2s;
        }
        input:focus { border-color: var(--accent); }
        
        .toggle-btn {
            position: absolute; right: 15px; top: 15px;
            cursor: pointer; font-size: 1.2rem; user-select: none;
        }

        button {
            width: 100%; padding: 12px; margin-top: 15px;
            background-color: var(--accent); color: #0d1117;
            border: none; border-radius: 8px; font-weight: bold;
            font-size: 1rem; cursor: pointer; transition: 0.2s;
        }
        button:hover { opacity: 0.9; }

        .result-box {
            margin-top: 25px; padding: 20px;
            background: #0d1117; border-radius: 8px;
            border-left: 5px solid transparent;
        }
        .rating-title { font-weight: bold; font-size: 1.2rem; margin-bottom: 10px; display: block;}
        
        .progress-bar-bg {
            background: #30363d; height: 8px; border-radius: 4px;
            margin-bottom: 15px; overflow: hidden;
        }
        .progress-bar-fill { height: 100%; transition: width 0.5s ease; }
        
        ul { margin: 0; padding-left: 20px; font-size: 0.9rem; color: #8b949e; }
        li { margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1><span class="shield-icon">🛡️</span> CRYPTSCALE</h1>
        <p style="color: #8b949e; font-size: 0.9rem;">Advanced Password Complexity Audit</p>
        
        <form method="POST">
            <div class="input-group">
                <input type="password" id="passInput" name="password" placeholder="Enter password to audit..." required value="{{ original_input if original_input else '' }}">
                <span class="toggle-btn" onclick="togglePass()">👁️</span>
            </div>
            <button type="submit">ANALYZE STRENGTH</button>
        </form>

        {% if result %}
        <div class="result-box" style="border-color: {{ result.color }}">
            <span class="rating-title" style="color: {{ result.color }}">{{ result.rating }}</span>
            
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {{ result.width }}; background-color: {{ result.color }}"></div>
            </div>

            <ul>
                {% for tip in result.feedback %}
                <li>{{ tip }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
    </div>

    <script>
        function togglePass() {
            var x = document.getElementById("passInput");
            if (x.type === "password") { x.type = "text"; } 
            else { x.type = "password"; }
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    original_input = ""
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        original_input = password
        result = assess_password(password)
        
    return render_template_string(HTML_TEMPLATE, result=result, original_input=original_input)

if __name__ == '__main__':
    print("------------------------------------------------")
    print("   CRYPTSCALE PASSWORD AUDIT RUNNING")
    print("   OPEN BROWSER TO: http://127.0.0.1:5001")
    print("------------------------------------------------")
    app.run(port=5001, debug=True)