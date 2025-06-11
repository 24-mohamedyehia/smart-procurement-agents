from flask import Flask, render_template, request, send_file, redirect, flash
from crew import procurement_crew
from src.utils import clean_report
import time
import os
OUTPUT_FOLDER = 'src/ai-agent-output'

app = Flask(__name__)
app.secret_key = 'supersecretkey'

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# clean output folder
for filename in os.listdir(OUTPUT_FOLDER):
    path = os.path.join(OUTPUT_FOLDER, filename)
    try:
        os.remove(path)
    except:
        print("Failed to remove file:", path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form fields
        product_name = request.form.get('product_name')
        top_recommendations_no = request.form.get('top_recommendations_no')
        language = request.form.get('language')

        try:
            # Prepare input for procurement_crew
            output_dir = OUTPUT_FOLDER
            os.makedirs(output_dir, exist_ok=True)
            # You may want to update the below with additional fields as needed
            procurement_crew.kickoff(inputs={
                'product_name': product_name,
                'no_keywords': 3,
                'websites_list': ['www.amazon.eg', 'www.jumia.com.eg', 'www.noon.com/egypt-en'],
                'language': language,
                'score_th': 0.5,
                'top_recommendations_no': int(top_recommendations_no),
                'country_name': 'Egypt',
                'search_results': os.path.join(output_dir, 'step_2_search_results.json'),
                'products_file': os.path.join(output_dir, 'step_3_products_file.json')
            })
            print("Procurement crew kickoff completed")

            time.sleep(3.0)  # Wait for the report to be generated
            result_html = os.path.join(output_dir, 'step_4_procurement_report.html')
            clean_report(result_html)
            if os.path.exists(result_html):
                return render_template('result.html', website_file='step_4_procurement_report.html')
            else:
                flash('Error: Report not generated. Please try again.')
                return redirect(request.url)
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(request.url)
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

@app.route('/preview/<filename>')
def preview_file(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

if __name__ == '__main__':
    app.run(debug=True)