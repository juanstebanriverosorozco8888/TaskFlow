from config.firebase import db
from firebase_admin import firestore


def create_project(
        title,
        description,
        created_by,
):

    db.collection(
        'projects'
    ).add({

        'title':
        title,

        'description':
        description,

        'created_by':
        created_by,

        'status':
        'Activo',

        'created_at':
        firestore.SERVER_TIMESTAMP
    })


def get_all_projects():

    projects = []

    docs = db.collection(
        'projects'
    ).stream()

    for doc in docs:

        data = doc.to_dict()

        data['id'] = doc.id

        projects.append(data)

    return projects


def delete_project(
        project_id
):

    db.collection(
        'projects'
    ).document(
        project_id
    ).delete()