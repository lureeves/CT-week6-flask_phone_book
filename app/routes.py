from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import NumberEntry, SignUpForm, LoginForm
from app.models import User, PhoneNumber
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    phone_number = PhoneNumber.query.all()
    return render_template('index.html', phone_number=phone_number)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    # Create an instance of the form (in the context of the current request)
    form = SignUpForm()
    # Check if the form was submitted and that all of the fields are valid
    if form.validate_on_submit():
        # If so, get the data from the form fields
        print('Hooray our form was validated!!')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        # Check to see if there is already a user with either username or email
        check_user = db.session.execute(db.select(User).filter((User.username == username) | (User.email == email))).scalars().all()
        if check_user:
            # Flash a message saying that user with email/username already exists
            flash("A user with that username and/or email already exists", "warning")
            return redirect(url_for('signup'))
        # If check_user is empty, create a new record in the user table
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f"Thank you {new_user.username} for signing up!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/number_entry', methods =["GET", "POST"])
@login_required
def number_entry():
    # Create an instance of the form (in the context of the current request)
    form = NumberEntry()
    # Check if the form was submitted and that all of the fields are valid 
    if form.validate_on_submit():
        # If so, get the data from the form fields
        print("Input Received!")
        first_name = form.first_name.data
        last_name = form.last_name.data
        number = form.number.data
        address = form.address.data
        print(first_name, last_name, number, address)
        # If check_user is empty, create a new record in the user table
        new_number = PhoneNumber(first_name=first_name, last_name=last_name, number=number, address=address, user_id=current_user.id)
        flash(f"{new_number.first_name} {new_number.last_name} has been added to the phonebook!", "success")
        return redirect(url_for('index'))
    return render_template('number_entry.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated :)')
        username = form.username.data
        password = form.password.data
        print(username, password)
        # Check if there is a user with username and that password
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
             # If the user exists and has the correct password, log them in
            login_user(user)
            flash(f'You have successfully logged in as {username}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect(url_for('index'))

@app.route('/edit/<phone_number_id>', methods=["GET", "POST"])
@login_required
def edit_number(phone_number_id):
    form = NumberEntry()
    number_to_edit = PhoneNumber.query.get_or_404(phone_number_id)
    print("\n", number_to_edit.id, "\n")
    # Make sure that the number  is the current user
    if number_to_edit.user_id != current_user.id:
        flash("You do not have permission to edit this number", "danger")
        return redirect(url_for('index'))

    # If form submitted, update number
    if form.validate_on_submit():
        # update the number with the form data
        number_to_edit.first_name = form.first_name.data
        number_to_edit.last_name = form.last_name.data
        number_to_edit.number = form.number.data
        number_to_edit.address = form.address.data
        # Commit that to the database
        db.session.commit()
        flash(f"{number_to_edit.first_name} {number_to_edit.last_name}'s number/address has been edited!", "success")
        return redirect(url_for('index'))

    # Pre-populate the form with number To Edit's values
    form.first_name.data = number_to_edit.first_name
    form.last_name.data = number_to_edit.last_name
    form.number.data = number_to_edit.number
    form.address.data = number_to_edit.address
    return render_template('edit.html', form=form, number=number_to_edit)


@app.route('/delete/<phone_number_id>')
@login_required
def delete_number(phone_number_id):
    number_to_edit = PhoneNumber.query.get_or_404(phone_number_id)
    if number_to_edit.user_id != current_user.id:
        flash("You do not have permission to delete this post", "danger")
        return redirect(url_for('index'))

    db.session.delete(number_to_edit)
    db.session.commit()
    flash(f"{number_to_edit.first_name} {number_to_edit.last_name} has been deleted", "info")
    return redirect(url_for('index'))