from flask import Flask


# web 
app = Flask(__name__)
@app.route('/')
def web_main():
    return "hello world"

if __name__ == "__main__":
    app.run()


