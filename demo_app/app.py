from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

VALID_EMAIL = "valid_email@example.com"
VALID_PASSWORD = "valid_password"

LOGIN_HTML = """
<html>
<head><title>Login</title></head>
<body>
<h2>Login Page</h2>

<form method="post" action="/login">
    <input data-test="login-email" name="email" placeholder="Email"><br><br>
    <input data-test="login-password" name="password" placeholder="Password" type="password"><br><br>
    <button data-test="login-submit" type="submit">Login</button>
</form>

<div data-test="login-error" style="color:red;">
{error}
</div>

</body>
</html>
"""

DASHBOARD_HTML = """
<html>
<body>
<h2>Dashboard</h2>
<p>Login successful</p>
</body>
</html>
"""


@app.get("/login", response_class=HTMLResponse)
def login_page():
    return LOGIN_HTML.format(error="")


@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    if email == VALID_EMAIL and password == VALID_PASSWORD:
        return RedirectResponse("/dashboard", status_code=302)
    else:
        return HTMLResponse(LOGIN_HTML.format(error="Invalid credentials"))


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return DASHBOARD_HTML