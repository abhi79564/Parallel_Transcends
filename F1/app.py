from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the scholarship data from CSV
scholarships = pd.read_csv('certificates.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    state_filter = request.form.get('state_filter', None)
    if state_filter:
        filtered_scholarships = scholarships[scholarships['State'] == state_filter]
    else:
        filtered_scholarships = scholarships

    return render_template('index.html', scholarships=filtered_scholarships)

if __name__ == '__main__':
    app.run(debug=True)
