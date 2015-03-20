from io import StringIO
from subprocess import check_output
from flask import Flask, request, jsonify, render_template
from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class CliForm(Form):
    path = StringField('path', validators=[DataRequired()])
    index = IntegerField('index', validators=[DataRequired()])
    record_type = StringField('record_type', validators=[DataRequired()])

app = Flask(__name__)
app.secret_key = 'Super secret'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CliForm(request.form)
    if form.validate_on_submit():
        
        stdout = check_output([form.data['path'], form.data['record_type']])
        return render_template('results.html', out = stdout)


    return render_template('index.html', form = form)

@app.route('/api', methods=['POST'])
def api():
    data = request.json

    stdout = check_output([data['path']])
    return jsonify({'out': stdout.decode('utf8')})

if __name__ == "__main__":
    app.debug = True
    app.run()
