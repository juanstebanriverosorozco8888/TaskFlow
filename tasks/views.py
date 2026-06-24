from django.shortcuts import (
    render,
    redirect
)

from django.contrib import messages

from config.firebase import db

from .services import (
    create_task
)


def task_list(request):

    uid = request.jwt_user[
        'uid'
    ]

    role = request.jwt_user[
        'role'
    ]

    tasks = []

    docs = db.collection(
        'tasks'
    ).stream()

    for doc in docs:

        task = doc.to_dict()

        task['id'] = doc.id

        if role == 'admin':

            if task.get(
                'assigned_by'
            ) == uid:

                tasks.append(
                    task
                )

        else:

            if task.get(
                'assigned_to'
            ) == uid:

                tasks.append(
                    task
                )

    return render(

        request,

        'tasks/list.html',

        {

            'tasks':
            tasks,

            'role':
            role
        }
    )


def user_task_list(request):

    uid = request.jwt_user[
        'uid'
    ]

    tasks = []

    docs = db.collection(
        'tasks'
    ).where(
        'assigned_to',
        '==',
        uid
    ).stream()

    for doc in docs:

        task = doc.to_dict()

        task['id'] = doc.id

        tasks.append(
            task
        )

    return render(

        request,

        'tasks/user_tasks.html',

        {

            'tasks':
            tasks
        }
    )

def create_task_view(request):

    role = request.jwt_user[
        'role'
    ]

    uid = request.jwt_user[
        'uid'
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

    users = []

    users_docs = db.collection(
        'users'
    ).stream()

    for doc in users_docs:

        user = doc.to_dict()

        if user.get(
            'role'
        ) == 'usuario':

            users.append(user)

    if request.method == 'POST':

        title = request.POST.get(
            'title'
        )

        description = request.POST.get(
            'description'
        )

        project_id = request.POST.get(
            'project_id'
        )

        assigned_to = request.POST.get(
            'assigned_to'
        )

        priority = request.POST.get(
            'priority'
        )

        deadline = request.POST.get(
            'deadline'
        )

        project_doc = db.collection(
            'projects'
        ).document(
            project_id
        ).get()

        project = (
            project_doc.to_dict()
        )

        user_data = None

        users_query = db.collection(
            'users'
        ).where(
            'uid',
            '==',
            assigned_to
        ).stream()

        for user_doc in users_query:

            user_data = (
                user_doc.to_dict()
            )

        create_task(

            title,

            description,

            project_id,

            project[
                'title'
            ],

            assigned_to,

            user_data[
                'name'
            ],

            uid,

            priority,

            deadline
        )

        messages.success(
            request,
            'Tarea creada'
        )

        return redirect(
            'task_list'
        )

    return render(

        request,

        'tasks/create.html',

        {

            'projects':
            projects,

            'users':
            users
        }
    )


def edit_task_view(
        request,
        task_id
):

    task_doc = db.collection(
        'tasks'
    ).document(
        task_id
    ).get()

    task = (
        task_doc.to_dict()
    )

    users = []

    users_docs = db.collection(
        'users'
    ).stream()

    for doc in users_docs:

        user = doc.to_dict()

        if user.get(
            'role'
        ) == 'usuario':

            users.append(user)

    if request.method == 'POST':

        db.collection(
            'tasks'
        ).document(
            task_id
        ).update({

            'title':
            request.POST.get(
                'title'
            ),

            'description':
            request.POST.get(
                'description'
            ),

            'priority':
            request.POST.get(
                'priority'
            ),

            'deadline':
            request.POST.get(
                'deadline'
            ),

            'status':
            request.POST.get(
                'status'
            ),

            'assigned_to':
            request.POST.get(
                'assigned_to'
            )
        })

        messages.success(
            request,
            'Tarea actualizada'
        )

        return redirect(
            'task_list'
        )

    return render(

        request,

        'tasks/edit.html',

        {

            'task':
            task,

            'task_id':
            task_id,

            'users':
            users
        }
    )


def delete_task(
        request,
        task_id
):

    db.collection(
        'tasks'
    ).document(
        task_id
    ).delete()

    messages.success(
        request,
        'Tarea eliminada'
    )

    return redirect(
        'task_list'
    )


def update_status(
        request,
        task_id
):

    status = request.POST.get(
        'status'
    )

    db.collection(
        'tasks'
    ).document(
        task_id
    ).update({

        'status':
        status
    })

    return redirect(
        'task_list'
    )

def user_update_status(request, task_id):

    task_ref = db.collection("tasks").document(task_id)

    task_doc = task_ref.get()

    if not task_doc.exists:
        return redirect("user_task_list")

    task = task_doc.to_dict()

    # Si ya está completada no permitir más cambios
    if task.get("status") == "Completada":
        messages.error(
            request,
            "Esta tarea ya fue completada y no puede modificarse."
        )
        return redirect("user_task_list")

    nuevo_estado = request.POST.get("status")

    task_ref.update({
        "status": nuevo_estado
    })

    messages.success(
        request,
        "Estado actualizado correctamente."
    )

    return redirect("user_task_list")