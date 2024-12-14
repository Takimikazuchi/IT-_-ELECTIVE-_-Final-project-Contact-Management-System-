from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(15), nullable=False)

# Route to show all contacts
@app.route('/')
def home():
    contacts = Contact.query.all()  # Get all contacts
    return render_template('index.html', contacts=contacts)  # Pass contacts to index.html

# Route to add a new contact
@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        # Get form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        age = request.form['age']
        address = request.form['address']
        contact = request.form['contact']

        # Create a new contact and add it to the database
        new_contact = Contact(
            firstname=firstname,
            lastname=lastname,
            gender=gender,
            age=age,
            address=address,
            contact=contact
        )

        db.session.add(new_contact)
        db.session.commit()

        return redirect(url_for('home'))  # Redirect to home page after adding contact

    return render_template('add_contact.html')  # Show the form to add a new contact

# Route to edit an existing contact
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)  # Get the contact to edit

    if request.method == 'POST':
        # Update the contact fields
        contact.firstname = request.form['firstname']
        contact.lastname = request.form['lastname']
        contact.gender = request.form['gender']
        contact.age = request.form['age']
        contact.address = request.form['address']
        contact.contact = request.form['contact']

        db.session.commit()  # Commit the changes to the database

        return redirect(url_for('home'))  # Redirect to home page after editing contact

    return render_template('edit_contact.html', contact=contact)  # Show edit form with contact data

# Route to delete a contact
@app.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)  # Get the contact to delete
    db.session.delete(contact)  # Delete the contact
    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('home'))  # Redirect to home page after deleting contact

if __name__ == "__main__":
    app.run(debug=True)
