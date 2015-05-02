from flask import Flask, render_template
from search_engine import driver
import urllib


app = Flask(__name__, template_folder='web/templates')


@app.route("/")
def hello():
    return render_template('main.html')

@app.route('/search/<search_query>', methods=['POST'])
def query_processor(search_query):
    decoded_query = urllib.unquote(search_query).decode('utf8')
    return driver.process_search(decoded_query, limit=8)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
