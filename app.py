from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# HTML templates
home_page = '''
<!doctype html>
<html>
<head><title>Search Form</title></head>
<body>
    <h1>Enter a search term</h1>
    <form method="post">
        <input type="text" name="search_term" required>
        <input type="submit" value="Search">
    </form>
    {% if error %}
    <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

result_page = '''
<!doctype html>
<html>
<head><title>Search Result</title></head>
<body>
    <h1>Search Result</h1>
    <p>Your search term is: {{ search_term }}</p>
    <form action="/">
        <input type="submit" value="Return to Home">
    </form>
</body>
</html>
'''

# Home page with the search form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_term = request.form['search_term']
        validation_result = validate_search_term(search_term)
        if validation_result != "valid":
            return render_template_string(home_page, error=validation_result)
        return redirect(url_for('result', search_term=search_term))
    return render_template_string(home_page)

# Result page
@app.route('/result')
def result():
    search_term = request.args.get('search_term', '')
    return render_template_string(result_page, search_term=search_term)

# Function to validate search term against XSS and SQL injection
def validate_search_term(search_term):
    if "<" in search_term or ">" in search_term or "'" in search_term or '"' in search_term:
        return "Input validated to be XSS attack. Please try again."
    if "SELECT" in search_term.upper() or "INSERT" in search_term.upper() or "DELETE" in search_term.upper() or "UPDATE" in search_term.upper():
        return "Input validated to be SQL injection attack. Please try again."
    return "valid"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
