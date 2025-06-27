from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Study Planner Flask 앱 배포 성공!"

if __name__ == "__main__":
    app.run(debug=True)
