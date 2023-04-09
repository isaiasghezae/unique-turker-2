from flask import Blueprint, render_template, request, flash, redirect, url_for, flash, session
from . import db, Uniqueid, Worker
import random  # for randomly generating unique identifier
import string  # for randomly generating unique identifier


# function to randomly generate Unique Identifier
def execute():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(12))
    return password


# function to check if the worker exists in the database for the given unique ID
def worker_exists(worker_id, unique_id):
    unique_id_entry = Uniqueid.query.filter_by(identifier=unique_id).first()
    if unique_id_entry:
        worker_entry = Worker.query.filter_by(
            workerid=worker_id, unique_id=unique_id_entry.id).first()
        return worker_entry is not None
    return False


# function to insert the worker ID into the database when the worker does not exist
def add_worker(worker_id, unique_id):
    unique_id_entry = Uniqueid.query.filter_by(identifier=unique_id).first()
    if not unique_id_entry:
        unique_id_entry = Uniqueid(identifier=unique_id)
        db.session.add(unique_id_entry)
        db.session.commit()

    new_worker = Worker(workerid=worker_id, unique_id=unique_id_entry.id)
    db.session.add(new_worker)
    db.session.commit()


views = Blueprint('views', __name__)

# 3 views
# home page = where you input the unique identifier + survey  link
# output page = outputs the html code for the HIT
# check_worker_eligibility = container for POST requests to check worker ID against the database


@views.route('/', methods=['GET', 'POST'])
def home():
    output = execute()  # Generate a unique ID for users to enter

    if request.method == 'POST':
        identifier = request.form.get('identifier')
        survey_link = request.form.get('survey_link')

        if identifier:
            if len(identifier) < 12:
                flash(
                    'Unique Identifier needs to be at least 12 characters long.', category='error')
            else:
                # Check for duplicate unique IDs
                existing_id = Uniqueid.query.filter_by(
                    identifier=identifier).first()

                if existing_id:
                    flash(
                        'This unique identifier is already in use. Please enter a different unique identifier.', category='error')
                else:
                    new_id = Uniqueid(identifier=identifier, workers=[])
                    db.session.add(new_id)
                    db.session.commit()

                    # Store identifier and survey_link the user entered in the session before redirecting
                    session['identifier'] = identifier
                    session['survey_link'] = survey_link
                    return redirect(url_for('views.output'))

    return render_template("home.html", output=output)


@views.route('/output', methods=['GET', 'POST'])
def output():
    # Retrieve identifier and survey_link from the session
    identifier = session.get('identifier')
    survey_link = session.get('survey_link')

    if request.method == 'POST':
        return redirect(url_for('views.home'))

    return render_template("output.html", identifier=identifier, survey_link=survey_link)


@views.route('/check_worker_eligibility', methods=['POST'])
def check_worker_eligibility():
    data = request.get_json()
    worker_id = data.get('workerId')
    unique_id = data.get('uniqueId')

    if worker_exists(worker_id, unique_id):
        return '0'  # worker does exist in the database
    else:
        add_worker(worker_id, unique_id)  # add worker ID to the database
        return '1'  # worker does not exist in the database
