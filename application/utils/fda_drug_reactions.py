import requests
from sentence_transformers import SentenceTransformer
from application.utils.extensions import db

from application.db.models import Medications
from application.app import app


class PopulateMedicationTable:
    def __init__(self, medication_name: str):
        self.medication_name = medication_name
        self.med_id = None
        self.side_effects_embeddings = None
        self.side_effects_str = ""

    def is_medication_in_db(self) -> bool:
        with app.app_context():
            return self.medication_name in [
                m[0] for m in db.session.query(Medications.name).all()
            ]

    def get_medication_id(self) -> str:
        with app.app_context():
            return (
                db.session.query(Medications.id)
                .filter(Medications.name == self.medication_name)
                .scalar()
            )

    def get_side_effects_for_drug(self) -> str:
        url = "https://api.fda.gov/drug/event.json"
        params = {
            "search": f"patient.drug.medicinalproduct:{self.medication_name}",
            "limit": 5,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "results" in data:

            for result in data["results"]:
                for reaction in result["patient"]["reaction"]:
                    self.side_effects_str += (
                        ", " + reaction["reactionmeddrapt"]
                        if self.side_effects_str
                        else reaction["reactionmeddrapt"]
                    )

            self.side_effects_embeddings = self.generate_embedding(
                self.side_effects_str
            )
            print(f"{self.medication_name=} - {self.side_effects_str=}")
            print(f"{self.side_effects_embeddings=}")

        else:
            print("No data found.")

    def generate_embedding(self, side_effects: str) -> list:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return model.encode(side_effects).tolist()

    def store_medication_data(
        self, medication_name: str, side_effects_embeddings: list
    ) -> str:
        if self.side_effects_embeddings:
            medication = Medications(
                name=self.medication_name,
                description="",
                side_effects=side_effects_embeddings,
            )
            with app.app_context():
                try:
                    db.session.add(medication)
                    db.session.commit()
                    print(f"Added {self.medication_name} to the database.")
                except Exception as e:
                    db.session.rollback()
                    print(f"Error committing to the database: {e}")
            return self.get_medication_id()


if __name__ == "__main__":
    p = PopulateMedicationTable("Viagra")
    print(p.is_medication_in_db())
    if not p.is_medication_in_db():
        p.get_side_effects_for_drug()
        p.store_medication_data(p.medication_name, p.side_effects_embeddings)
        print(p.get_medication_id())

    print(p.get_medication_id())
