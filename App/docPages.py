from flask import Blueprint, render_template, redirect, url_for, request, flash

from flask_login import login_required,current_user
from .models import Document, User
from . import db
from datetime import datetime
from .main import active_required

docPages = Blueprint('docPages', __name__)


@docPages.route('/documents')
#@login_required
@active_required
def documents():
    all_documents = Document.query.all()
    unsigned_documents = Document.query.filter(Document.status==0).all()
    signed_documents = Document.query.filter(Document.status > 0).all()
    user_names = {}
    for i in all_documents:
        _user = User.query.filter(User.id==i.user_id).first()
        user_names[i.id] = f'{_user.name} {_user.lastname}'

    time_now = datetime.utcnow().strftime('Серверное время %H:%M:%S')
    return render_template('documents.html', docs = all_documents, unsigned_documents = unsigned_documents, signed_documents = signed_documents, \
                           user_names = user_names, time = time_now)

@docPages.route('/documentCreate')
@login_required
@active_required
def documentCreate():
    return render_template('document_create.html')

@docPages.route('/documentCreate', methods=['POST'])
@login_required
def signup_post():
    title = request.form.get('title')
    description = request.form.get('description')
    duedate = d = datetime.strptime(request.form.get('duedate'), "%Y-%m-%d")
    minPrice = request.form.get('minPrice')
    maxPrice = request.form.get('maxPrice')

    user_id = current_user.id
    dateCreate = datetime.now()
    dateUpdate = datetime.now()
    status = 0

    new_document = Document(title=title, description=description, duedate=duedate,minPrice=minPrice, \
                   maxPrice=maxPrice,dateCreate=dateCreate,dateUpdate=dateUpdate,status=status,user_id=user_id)
    db.session.add(new_document)
    db.session.commit()
    
    return redirect(url_for('docPages.documents'))

@docPages.route('/documents/delete/<document_id>')
@active_required
def delete_post(document_id):
    document_id = int(document_id)
    Document.query.filter(Document.id == document_id).delete()
    db.session.commit()
    return redirect("/documents")

@docPages.route('/documents/confirm/<document_id>')
@active_required
def confirm_post(document_id):
    document_id = int(document_id)
    doc = Document.query.filter(Document.id == document_id).first()
    doc.status = 2
    db.session.commit()
    return redirect("/documents")

@docPages.route('/documents/reject/<document_id>')
@active_required
def reject_post(document_id):
    document_id = int(document_id)
    doc = Document.query.filter(Document.id == document_id).first()
    doc.status = 1
    db.session.commit()
    return redirect("/documents")