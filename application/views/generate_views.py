from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

from application.forms import JournalForm
from application.utils.open_ai_handler import OpenAIHandler
from application.utils.db_handler import DBHandler

gen = Blueprint("gen", __name__)


@login_required
@gen.route("/journal_response", methods=["POST"])
def journal_response():
    form = JournalForm()
    if form.validate_on_submit():
        ai = OpenAIHandler()
        ai_response = ai.create_journal_entry_response(form.journal_entry.data)
        if ai_response:
            dbh = DBHandler()
            profile_id = current_user.profile.profile_id
            entry = form.journal_entry.data
            print(ai_response)
            dbh.add_journal_entry(
                profile_id=profile_id, entry=entry, ai_response=ai_response
            )
            print(f"P- ID: {profile_id}, Entry: {entry}, Resp.: {ai_response}")
        else:
            print(f"Error: {ai_response['message']}")
    return redirect(url_for("user.journal")), 200
