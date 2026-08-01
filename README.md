# Sistema de Gestión de Posts

Sistema de gestión de Posts con frontend en React + Redux, backend en Python (FastAPI), base de datos SQL Server y almacenamiento de archivos en S3 (MinIO para desarrollo local).

---

## Arquitectura

```text
React + Redux
       │
       ▼
 FastAPI (Python)
       │
 ├──────────────► SQL Server
 │
 └──────────────► S3 / MinIO
```

---

## Requisitos

- Docker y Docker Compose
- Navegador web moderno

---

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/UnderWeb/post-management.git
cd post-management
```

### 2. Configurar variables de entorno

Copiar el archivo .env.example a .env:

```bash
cp .env.example .env
```

Las variables por defecto son suficientes para desarrollo local.

### 3. Levantar todos los servicios

```bash
docker compose up --build -d
```

Este comando:

- Construye las imágenes del backend y frontend
- Inicia SQL Server, MinIO (S3), backend y frontend
- Ejecuta migraciones de base de datos automáticamente
- Carga datos iniciales (5 posts de ejemplo)

### 4. Verificar el estado de los servicios

```bash
docker compose ps
```

Se debería desplegar 4 servicios en estado running o healthy.

---

## Acceso a la Aplicación

| Servicio | URL | Descripción |
| --- | --- | --- |
| Frontend | <http://localhost:3000> | Aplicación React |
| Backend API | <http://localhost:8000> | API REST (FastAPI) |
| API Docs | <http://localhost:8000/docs> | Documentación Swagger |
| MinIO Console | <http://localhost:9001> | Gestión de archivos S3 |
| MinIO API | <http://localhost:9000> | Endpoint S3 |

**Credenciales MinIO:**

- Usuario: minioadmin
- Password: minioadmin

---

## Estructura del Proyecto

```text
post-management/
├── backend/
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── alembic.ini
│   ├── app/
│   │   ├── application/
│   │   │   ├── ports/
│   │   │   │   ├── storage_service.py
│   │   │   │   └── summarizer_service.py
│   │   │   └── use_cases/
│   │   │       ├── create_post.py
│   │   │       ├── delete_post.py
│   │   │       └── list_posts.py
│   │   ├── core/
│   │   │   ├── config/
│   │   │   │   └── settings.py
│   │   │   ├── exceptions/
│   │   │   │   └── handlers.py
│   │   │   └── logging/
│   │   │       └── logger.py
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── post.py
│   │   │   └── interfaces/
│   │   │       └── post_repository.py
│   │   ├── infrastructure/
│   │   │   ├── database/
│   │   │   │   ├── models/
│   │   │   │   │   ├── base.py
│   │   │   │   │   └── post_model.py
│   │   │   │   └── session.py
│   │   │   ├── repositories/
│   │   │   │   └── post_repository.py
│   │   │   └── services/
│   │   │       ├── s3_storage_service.py
│   │   │       └── summarizer_service.py
│   │   ├── main.py
│   │   └── presentation/
│   │       ├── dependencies.py
│   │       ├── mappers/
│   │       │   └── post_mapper.py
│   │       ├── router.py
│   │       └── schemas.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── scripts/
│   │   ├── entrypoint.sh
│   │   └── seed.py
│   └── tests/
│       ├── conftest.py
│       ├── test_api_endpoints.py
│       ├── test_create_post.py
│       ├── test_delete_post.py
│       ├── test_list_posts.py
│       └── test_post_repository_contract.py
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── axios.ts
│   │   │   └── postsApi.ts
│   │   ├── app/
│   │   │   └── store.ts
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── EmptyState.tsx
│   │   │   ├── ErrorMessage.tsx
│   │   │   └── Loading.tsx
│   │   ├── features/
│   │   │   └── posts/
│   │   │       ├── components/
│   │   │       │   ├── CreatePostForm.tsx
│   │   │       │   ├── PostCard.tsx
│   │   │       │   └── PostList.tsx
│   │   │       ├── postsSelectors.ts
│   │   │       ├── postsSlice.ts
│   │   │       ├── postsThunks.ts
│   │   │       └── types.ts
│   │   ├── hooks/
│   │   │   ├── index.ts
│   │   │   ├── useAppDispatch.ts
│   │   │   └── useAppSelector.ts
│   │   ├── index.css
│   │   ├── main.tsx
│   │   ├── pages/
│   │   │   ├── index.ts
│   │   │   └── PostsPage.tsx
│   │   ├── test/
│   │   │   └── setup.ts
│   │   └── types/
│   │       └── post.ts
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml     # Orquestación de servicios
├── .env.example           # Variables de entorno de ejemplo
└── AWS_PROPOSAL.md        # Propuesta de despliegue en AWS
```

---

## Funcionalidades

### Frontend

- Crear posts con título, descripción y archivo opcional
- Listar posts con resumen generado automáticamente
- Eliminar posts (incluyendo archivo asociado en S3)
- Filtrar posts por título (búsqueda local en tiempo real)

### Backend

- GET /api/posts - Listar todos los posts
- POST /api/posts - Crear post con resumen automático (multipart/form-data)
- DELETE /api/posts/{id} - Eliminar post y archivo asociado
- Generación automática de resumen y palabras clave
- Almacenamiento de archivos en S3 (MinIO local / AWS S3 producción)

### Base de Datos

- Migraciones automáticas con Alembic
- Seeders con 5 posts de ejemplo
- SQL Server 2022

### Tests Backend

```bash
docker compose exec posts_backend pytest
```

### Tests Frontend

```bash
docker compose exec posts_frontend npm run test
```

---

## Tecnologías Utilizadas

### Backend

- Python 3.14
- FastAPI 0.141.1
- SQLAlchemy 2.0.51
- Alembic 1.18.5
- PyODBC 5.3.0
- Boto3 1.35.0 (AWS S3 SDK)
- Pytest 9.1.1

### Frontend

- React 19.2.8
- Redux Toolkit 2.12.0
- TypeScript 6.0.2
- Vite 8.2.0
- Axios 1.19.0
- Vitest 4.1.10

### Infraestructura

- Docker & Docker Compose
- SQL Server 2022
- MinIO (S3-compatible)
- Nginx 1.30.4

---

## Documentación Adicional

- [Propuesta de Despliegue en AWS](AWS_PROPOSAL.md)
- [Documentación de la API (Swagger)](http://localhost:8000/docs)

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
