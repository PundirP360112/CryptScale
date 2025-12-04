# CryptScale 

CryptScale is a lightweight, web-based password strength auditing tool. It analyzes password complexity in real-time against standard security criteria (length, casing, digits, and symbols) and provides immediate, visual feedback to the user.

⚡ Features

Complexity Algorithms: Checks for lowercase, uppercase, numeric, and special character inclusion.

Visual Strength Meter: Displays a color-coded progress bar (Red/Yellow/Green) indicating password robustness.

Actionable Feedback: Tells the user exactly what is missing (e.g., "Missing numbers").

Secure UI: "Dark Mode" interface with a toggle button to show/hide the password input.

🛠️ Tech Stack

Backend: Python (Flask)

Frontend: HTML5, CSS3, JavaScript (Jinja2 Templates)

Logic: Python Regular Expressions (re module)

🚀 Installation & Setup

Clone the repository:

git clone [https://github.com/yourusername/cryptscale.git](https://github.com/yourusername/cryptscale.git)
cd cryptscale


Install Flask:

pip install flask


Run the application:

python app.py


Access the Audit Tool:
Open your web browser and navigate to:

[http://127.0.0.1:5001](http://127.0.0.1:5001)


🧠 Scoring Logic

The application evaluates passwords based on the following:

Critical Fail: Length < 8 characters (Automatic "WEAK" rating).

Points System:

+1 Base score (Length >= 8)

+1 Length Bonus (Length >= 12)

+1 Lowercase present

+1 Uppercase present

+1 Digit present

+1 Special Character present

Ratings:

0-3: WEAK (Red)

4-5: MODERATE (Yellow)

6+: STRONG (Green)

📄 License

This project is open-source and available under the MIT License.
