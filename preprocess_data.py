import json

from create_app import app
from nksc2c.models import NKS, db, StatusEnum


IMAGES_JSON = "images.json";

try:
    with open(IMAGES_JSON, "r") as fd:
        json_data = json.load(fd)

    # Insert data into the database
    with app.app_context():
        records = []

        for page_name, pixels in json_data.items():
            nks = NKS.query.filter_by(page_name=page_name).first()
            pixel_to_string = json.dumps(pixels)
            if not nks:
                nks = NKS(pixel_data=pixel_to_string, page_name=page_name)
            else:
                nks.pixel_data = pixel_to_string
            records.append(nks)
        db.session.bulk_save_objects(records)
        db.session.commit()
        print("Data inserted successfully!")

except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
    print(f"Error at line {e.lineno}, column {e.colno}, position {e.pos}")

