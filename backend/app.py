from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome, you found the MusicMood backend!"

if __name__ == '__main__':
    app.run(debug=True)