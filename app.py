from flask import Flask, render_template, send_file
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Read the CSV file downloaded
    with open('table1.csv', 'r') as file:
        csv_data = file.read()
    
    # Load the CSV file for calculations
    df = pd.read_csv('table1.csv', index_col='Index #')

    # Calculate Table 2
    try:
        alpha = df.loc['A5', 'Value'] + df.loc['A20', 'Value']
        beta = df.loc['A15', 'Value'] / df.loc['A7', 'Value']
        charlie = df.loc['A13', 'Value'] * df.loc['A12', 'Value']
    except KeyError as e:
        print(f"KeyError: {e}")
        return "An error occurred while processing the table.", 500

    table2_data = {
        'Category': ['Alpha', 'Beta', 'Charlie'],
        'Value': [int(alpha), int(beta), int(charlie)]
    }
    table2_df = pd.DataFrame(table2_data)
    table2_html = table2_df.to_html(classes='table table-striped', index=False)

    # Render the template with CSV data and Table 2
    return render_template('web.html', csv_data=csv_data, table2=table2_html)

# Route to download Table 1
@app.route('/download')
def download():
    return send_file('table1.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)