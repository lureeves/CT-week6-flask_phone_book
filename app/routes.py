from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/information_entry', methods =["GET", "POST"])
def information_entry():
    # Create an instance of the form (in the context of the current request)
    form = SignUpForm()
    # Check if the form was submitted and that all of the fields are valid 
    if form.is_submitted():
        # If so, get the data from the form fields
        print("Input Received!")
        first_name = form.first_name.data
        last_name = form.last_name.data
        number = form.number.data
        address = form.address.data
        print(first_name, last_name, number, address)
        flash(f"Thank you, {first_name} for entering information!", "success")
        return redirect(url_for('index'))
    return render_template('information_entry.html', form=form)