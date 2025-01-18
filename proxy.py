from urllib import parse

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import or_

from nksc2c.s3_client import S3Client
from nksc2c.models import NKS, db, StatusEnum
from create_app import app

migrate = Migrate(app, db)


@app.route('/')
@app.route('/index')
def index():
    return """
        <div style='text-align: center; margin-top: 3em;'>
            <h1>
                Hello friend! Welcome! This is the NKS Click to Copy code Project.
            </h1>
        </div>
    """

@app.route('/nksc2c_notebook', methods=['POST'])
def nksc2c_notebook():
    data = request.get_json()
    if not data:
        return jsonify({{'error': 'Invalid input'}}), 400

    name = data.get('name')
    if name and len(name) > 50:
        return jsonify({'error': {'name': 'Name too long.'}}), 400

    page_name = data.get('page_name')
    social_link = data.get('social_link')
    notebook_name = data.get('notebook_name', 'new_notebook')
    notebook_chapter = data.get('notebook_chapter')
    notebook_link = f"https://tccup.s3.amazonaws.com/{parse.quote(notebook_name)}.nb" 
    status = StatusEnum.PENDING
    name_args = {}
    if name:
        name_args = {"name": name}

    nks = NKS.query.filter_by(page_name=page_name).first()
    if nks:
        nks.social_link = social_link
        nks.notebook_name = notebook_name
        nks.notebook_link = notebook_link
        nks.notebook_chapter = notebook_chapter
        nks.name = name
        nks.status = status
        new_nks = nks
    else:
        new_nks = NKS(
            **name_args,
            social_link=social_link,
            notebook_name=notebook_name,
            notebook_link=notebook_link,
            notebook_chapter=notebook_chapter,
            page_name=page_name,
            status=status
        )
    new_nks.upload_token = new_nks.generate_upload_token()
    db.session.add(new_nks)
    db.session.commit()
    return jsonify({'data': {**new_nks.to_dict(), "token": new_nks.upload_token}}), 201

@app.route('/nksc2c_notebooks/<int:nksc2c_id>', methods=['POST'])
def update_nksc2c_notebook(nksc2c_id):
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    nks = NKS.query.get_or_404(nksc2c_id)
    if not nks:
        return jsonify({'error': 'No data for this nksc2c notebook id.'})

    try:
        db.session.commit()
        return jsonify({'message': 'Updated successfully', 'nks': nks.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/nksc2c_notebooks', methods=['GET'])
def nksc2c_notebooks():
    pages = request.args.get("pages")
    page_names = pages.split(",")
    nks = NKS.query.order_by(NKS.created_at.desc()).filter(NKS.page_name.in_(page_names)).all()
    allnks = [t.to_dict() for t in nks]
    return jsonify({'data': allnks})

@app.route('/uploadnksnotebook', methods=['POST'])
def uploadnksnotebook():
    file = request.files.get("file")
    token = request.form.get('token')
    notebook_name = request.form.get('notebook_name')
    if not file:
        return jsonify({"error": "File is required for upload."})

    if not token:
        return jsonify({"error": "Token is required for upload."})
    
    nksc2cnotebook = NKS.query.filter_by(notebook_name=notebook_name).first()
    if token != nksc2cnotebook.upload_token:
        return jsonify({"error": "The upload token provided is not correct. Please contact asheuh49@gmail.com for assistance."})

    # Upload to the cloud
    s3_client = S3Client()
    resource_url = s3_client.upload_file_to_s3(f"{notebook_name}.nb", file)
    nksc2cnotebook.status = StatusEnum.GOOD
    db.session.add(nksc2cnotebook)
    db.session.commit()
    return jsonify({'data': nksc2cnotebook.to_dict()})
