"""Seed file to make sample data for Posts db."""

from models import Pet, db
from app import app


with app.app_context():

    db.drop_all()
    db.create_all()

    Pet.query.delete()

    first_pet = Pet(name="Snowball",species="dog",photo_url="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQVaICBnTl1DaP8w_QIUQQ7O3DRcFWEZC6SbwytzcjFtYWYGf40"
                    , age = 2 , notes="likes the outdoors", available = True)
    second_pet = Pet(name="Spots",species="dog",photo_url="https://i.ebayimg.com/images/g/0SwAAOSwTLtihlY-/s-l1200.jpg"
                    , age = 1 , notes="family friendly", available = True)

    db.session.add_all([first_pet,second_pet])
    db.session.commit()