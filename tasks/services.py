from config.firebase import db
from firebase_admin import firestore


def create_task(

        title,

        description,

        project_id,

        project_name,

        assigned_to,

        assigned_to_name,

        assigned_by,

        priority,

        deadline
):

    db.collection(
        'tasks'
    ).add({

        'title':
        title,

        'description':
        description,

        'project_id':
        project_id,

        'project_name':
        project_name,

        'assigned_to':
        assigned_to,

        'assigned_to_name':
        assigned_to_name,

        'assigned_by':
        assigned_by,

        'priority':
        priority,

        'status':
        'Pendiente',

        'deadline':
        deadline,

        'created_at':
        firestore.SERVER_TIMESTAMP
    })