# TaskFlow 📋

## Descripción del Proyecto

**TaskFlow** es una aplicación web de gestión de tareas y proyectos construida con **Django** que permite a los usuarios y administradores organizar, asignar y monitorear tareas de manera eficiente. La plataforma proporciona un dashboard intuitivo, sistema de autenticación seguro basado en Firebase, y características avanzadas como gestión de proyectos, seguimiento de tareas, y consulta de información climática.

### Características Principales:
- 📊 **Dashboard**: Panel de control personalizado para usuarios y administradores
- 📝 **Gestión de Tareas**: Crear, editar y monitorear tareas asignadas
- 🏢 **Gestión de Proyectos**: Organizar tareas dentro de proyectos específicos
- 👥 **Gestión de Usuarios**: Control de roles (Admin, Usuarios)
- 🌤️ **Información Climática**: Integración de datos meteorológicos
- 💬 **Sistema de Comentarios**: Colaboración mediante comentarios en tareas
- 🔐 **Autenticación Segura**: Autenticación basada en Firebase Authentication y JWT

---

## Modelo de Base de Datos

La aplicación utiliza **Google Cloud Firestore** (Firebase) como base de datos NoSQL. La estructura de colecciones es la siguiente:

### Colecciones Principales:

#### 1. **tasks**
```
{
  id: string,
  title: string,
  description: string,
  status: string (pendiente, en_progreso, completada),
  priority: string (baja, media, alta),
  assigned_to: string (UID del usuario asignado),
  assigned_by: string (UID del usuario que asignó),
  project_id: string,
  created_at: timestamp,
  due_date: timestamp,
  comments: array
}
```

#### 2. **projects**
```
{
  id: string,
  title: string,
  description: string,
  status: string (activo, completado, archivado),
  created_by: string (UID del administrador),
  tasks: array (referencias a IDs de tareas),
  created_at: timestamp,
  updated_at: timestamp
}
```

#### 3. **users**
```
{
  uid: string (Firebase UID),
  email: string,
  nombre: string,
  apellido: string,
  role: string (admin, usuario),
  departamento: string,
  created_at: timestamp,
  updated_at: timestamp
}
```

#### 4. **comments**
```
{
  id: string,
  task_id: string,
  user_id: string (UID del usuario),
  content: string,
  created_at: timestamp,
  updated_at: timestamp
}
```

#### 5. **weather**
```
{
  id: string,
  user_id: string,
  location: string,
  temperature: number,
  description: string,
  humidity: number,
  wind_speed: number,
  updated_at: timestamp
}
```

### Relaciones:
- **Tasks → Projects**: Una tarea pertenece a un proyecto
- **Tasks → Users**: Una tarea es asignada a un usuario por otro usuario
- **Comments → Tasks**: Un comentario está asociado a una tarea
- **Weather → Users**: Un registro climático está asociado a un usuario

---

## Tecnologías Utilizadas

### Backend
- **Django 5.2.6**: Framework web Python
- **Django REST Framework 3.17.1**: API REST
- **Django CORS Headers 4.9.0**: Gestión de CORS
- **Gunicorn 26.0.0**: Servidor WSGI

### Autenticación y Seguridad
- **Firebase Admin SDK 7.4.0**: Autenticación y almacenamiento en la nube
- **PyJWT 2.13.0**: Tokens JWT
- **django-rest-framework-simplejwt**: Autenticación JWT para DRF
- **cryptography 49.0.0**: Funciones criptográficas
- **google-auth 2.54.0**: Autenticación Google

### Base de Datos
- **Google Cloud Firestore 2.27.0**: Base de datos NoSQL en la nube
- **SQLParse 0.5.5**: Parser SQL

### Frontend
- **HTML5/CSS3**: Maquetación y estilos
- **JavaScript**: Interactividad del cliente

### Infraestructura y Despliegue
- **Vercel**: Plataforma de despliegue
- **WhiteNoise**: Servicio de archivos estáticos
- **ASGI/WSGI**: Servidores de aplicación

### Otros
- **python-dotenv 1.2.2**: Gestión de variables de entorno
- **Requests 2.34.2**: Peticiones HTTP
- **Protobuf 7.35.1**: Serialización de datos

### Stack de Desarrollo
```
Python 3.13
Django 5.2
Firebase/Firestore
JWT Authentication
REST API
HTML/CSS/JavaScript
```

---

## URL del Sistema Desplegado

La aplicación está desplegada en **Vercel** y se puede acceder a través de:

```
https://task-flow-steel-chi.vercel.app/
```

### Ambiente de Desarrollo
- **Local**: `http://localhost:8000`

### Endpoints Principales
- Dashboard: `/dashboard/`
- Tareas: `/tasks/`
- Proyectos: `/projects/`
- Usuarios: `/users/`
- Admin: `/admin/`
- API REST: `/api/`

---

## Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Firebase Project configurado

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd TaskFlow
```

2. **Crear un ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crear archivo `.env` en la raíz del proyecto:
```
SECRET_KEY=tu_clave_secreta
DEBUG=True
FIREBASE_CREDENTIALS=tu_json_firebase
DATABASE_URL=tu_url_firebase
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Recopilar archivos estáticos**
```bash
python manage.py collectstatic --noinput
```

7. **Ejecutar el servidor de desarrollo**
```bash
python manage.py runserver
```

---

## Estructura del Proyecto

```
TaskFlow/
├── api/                    # Endpoints de API
├── comments/               # App de comentarios
├── config/                 # Configuración principal
├── dashboard/              # App del dashboard
├── projects/               # App de gestión de proyectos
├── tasks/                  # App de gestión de tareas
├── users/                  # App de gestión de usuarios
├── weather/                # App de información climática
├── templates/              # Plantillas HTML
├── staticfiles/            # Archivos estáticos (CSS, JS, imágenes)
├── manage.py               # Utilidad de línea de comandos de Django
├── requirements.txt        # Dependencias del proyecto
├── vercel.json            # Configuración de Vercel
└── build.sh               # Script de construcción
```

---

## Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo `LICENSE` para detalles.


