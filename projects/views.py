from django.shortcuts import (
    render,
    redirect
)

from django.contrib import messages

from config.firebase import db


def project_list(request):

    uid = request.jwt_user[
        'uid'
    ]

    role = request.jwt_user[
        'role'
    ]

    if role != 'admin':

        return redirect(
            'home_dashboard'
        )

    projects = []

    docs = db.collection(
        'projects'
    ).stream()

    for doc in docs:

        project = doc.to_dict()

        if project.get(
            'created_by'
        ) == uid:

            project['id'] = doc.id

            projects.append(
                project
            )

    return render(

        request,

        'projects/list.html',

        {

            'projects':
            projects
        }
    )


def create_project_view(request):

    if request.method == 'POST':

        uid = request.jwt_user[
            'uid'
        ]

        title = request.POST.get(
            'title'
        )

        description = request.POST.get(
            'description'
        )

        status = request.POST.get(
            'status'
        )

        db.collection(
            'projects'
        ).add({

            'title':
            title,

            'description':
            description,

            'status':
            status,

            'created_by':
            uid
        })

        messages.success(
            request,
            'Proyecto creado'
        )

        return redirect(
            'project_list'
        )

    return render(
        request,
        'projects/create.html'
    )


def edit_project_view(
        request,
        project_id
):

    project_doc = db.collection(
        'projects'
    ).document(
        project_id
    ).get()

    project = (
        project_doc.to_dict()
    )

    if request.method == 'POST':

        title = request.POST.get(
            'title'
        )

        description = request.POST.get(
            'description'
        )

        status = request.POST.get(
            'status'
        )

        db.collection(
            'projects'
        ).document(
            project_id
        ).update({

            'title':
            title,

            'description':
            description,

            'status':
            status
        })

        messages.success(
            request,
            'Proyecto actualizado'
        )

        return redirect(
            'project_list'
        )

    return render(

        request,

        'projects/edit.html',

        {

            'project':
            project,

            'project_id':
            project_id
        }
    )


def delete_project(
        request,
        project_id
):

    db.collection(
        'projects'
    ).document(
        project_id
    ).delete()

    messages.success(
        request,
        'Proyecto eliminado'
    )

    return redirect(
        'project_list'
    )