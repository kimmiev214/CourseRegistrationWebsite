from flask import Flask

app=Flask(__name__)

@app.route('/')
def homepage():
    return "Hello Universe"

if __name__ == '__main__':
    app.run(debug=True)


