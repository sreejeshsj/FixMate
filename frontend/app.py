import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from flask import Flask, render_template, request, session, redirect, url_for
from backend.core import FixMate
from backend.llm.llm_client import LLMClient
from backend.auth import auth_bp  # Import authentication

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Change this for security
app.register_blueprint(auth_bp)  # Register authentication routes

# Initialize FixMate with LLM client
llm_client = LLMClient()
fixmate = FixMate(llm_client)

@app.route('/')
def index():
    if "user" not in session:
        return redirect(url_for("auth.login"))  # Redirect to login if not authenticated
    return render_template('index.html', username=session["user"])

@app.route('/repair', methods=['POST'])
def repair():
    if "user" not in session:
        return redirect(url_for("auth.login"))  # Restrict repair to logged-in users

    code = request.form['code']
    objective = request.form['objective']
    
    corrected_code, errors = fixmate.repair_code(code, objective)
    
    return render_template('result.html',
                         original_code=code,
                         obj=objective,
                         corrected_code=corrected_code,
                         errors=errors)

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))

if __name__ == '__main__':
    app.run(debug=True)
