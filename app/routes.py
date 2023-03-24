from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import NumberEntry, SignUpForm, LoginForm
from app.models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/number_entry', methods =["GET", "POST"])
def number_entry():
    # Create an instance of the form (in the context of the current request)
    form = NumberEntry()
    # Check if the form was submitted and that all of the fields are valid 
    if form.is_submitted():
        # If so, get the data from the form fields
        print("Input Received!")
        first_name = form.first_name.data
        last_name = form.last_name.data
        number = form.number.data
        address = form.address.data
        print(first_name, last_name, number, address)
        # If check_user is empty, create a new record in the user table
        new_contact = User(first_name=first_name, last_name=last_name, number=number, address=address)
        flash(f"{new_contact.first_name} {new_contact.last_name} has been added to the phonebook!", "success")
        return redirect(url_for('index'))
    return render_template('number_entry.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    # Create an instance of the form (in the context of the current request)
    form = SignUpForm()
    # Check if the form was submitted and that all of the fields are valid
    if form.validate_on_submit():
        # If so, get the data from the fields
        print("Field was validated!")
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        flash(f'You have successfully signed up as {username}.', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)



@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated :)')
        username = form.username.data
        password = form.password.data
        print(username, password)
        # TODO: Check if there is a user with username and that password
        # Fake an invalid log in
        if password == 'abc':
            flash('Invalid username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

        flash(f'You have successfully logged in as {username}.', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)
