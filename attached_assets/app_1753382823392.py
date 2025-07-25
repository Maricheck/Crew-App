from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
crew_data = []

status_stages = ["Registered", "Screening", "Documents Verified", "Approved"]

@app.route('/')
def dashboard():
    return render_template('dashboard.html', crew=crew_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_crew = {
            'name': request.form['name'],
            'rank': request.form['rank'],
            'passport': request.form['passport'],
            'status': 0
        }
        crew_data.append(new_crew)
        return render_template('thankyou.html', crew=new_crew)
    return render_template('register.html')

@app.route('/update_status/<int:index>')
def update_status(index):
    if crew_data[index]['status'] < len(status_stages) - 1:
        crew_data[index]['status'] += 1
    return redirect(url_for('dashboard'))

@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        passport = request.form['passport']
        for crew in crew_data:
            if crew['passport'] == passport:
                return render_template('tracker.html', crew=crew, stages=status_stages)
        return render_template('tracker.html', crew=None, not_found=True)
    return render_template('tracker.html', crew=None)

if __name__ == '__main__':
    app.run(debug=True)