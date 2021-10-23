# .\venv\Scripts\activate
from flask import Flask, render_template, request, redirect
from matrix import *


app = Flask(__name__)


# Routing do define url
@app.route('/')
def index():
    return render_template('matrix.html')

# Post json
@app.route('/get-json', methods=['GET', 'POST'])
def get_json():
    # Import Data
    list_brand, df_ordbr, df_con, df_rec = order_brand(PATH_IN)

    df_nodes = create_nodes(df_con, 6)

    df_links = create_links(df_rec, df_ordbr, list_brand)    

    json_to = create_json(df_nodes, df_links)

    return json_to    


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True, port=5000)


