from flask import Blueprint, render_template
from flask_login import login_required
from flask_login import current_user
from application.forms import JournalForm
from application.db.models import Journal
from application.utils.extensions import db
import json

user = Blueprint("user", __name__)


@login_required
@user.route("/profile")
def profile():

    # You can now directly access current_user in the template
    return render_template("profile.html", user=current_user)


@login_required
@user.route("/journal", methods=["GET", "POST"])
def journal():
    journal_entries = (
        db.session.query(Journal)
        .filter_by(profile_id=current_user.profile.profile_id)
        .all()
    )
    for entry in journal_entries:
        if entry.ai_response:  # Ensure it's not None
            entry.ai_response = json.loads(entry.ai_response)
    journal_form = JournalForm()

    return render_template(
        "journal.html",
        form=journal_form,
        journal_entries=journal_entries,
        user=current_user,
    )
