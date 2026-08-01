# Propuesta de Despliegue en AWS

## 1. Frontend

**S3 + CloudFront**: El frontend es una SPA generada con Vite, por lo que solo produce archivos estáticos. S3 permite alojarlos de forma económica y CloudFront distribuirlos mediante CDN (Content Delivery Network), mejorando el rendimiento y la disponibilidad.

## 2. Base de Datos

**RDS for SQL Server**: El proyecto ya usa SQL Server 2022 en desarrollo, así que tiene sentido mantenerlo en producción. RDS quita la carga de administrar backups, parches de seguridad y cambios manuales.

## 3. IAM

Implementaría estas reglas:

- **Rol para el backend (ECS)** con permisos mínimos: solo `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject` sobre el bucket de archivos. El acceso a la base de datos estaría restringido mediante **Security Groups** para que solo el backend pueda conectarse a la instancia RDS.
- **Bucket S3 con Block Public Access** activado: Los archivos solo son accesibles vía el backend autenticado, no directamente desde internet.
- **Bucket Policy**: Restricción de acceso a la VPC del backend.
- **SSE-S3 obligatorio**: Encriptación de todos los archivos en reposo.
- **Secrets Manager**: Almacenaría las credenciales de SQL Server y el acceso a S3, permitiendo su rotación automática. El backend las consumiría mediante un IAM Role, evitando credenciales hardcodeadas o almacenadas en variables de entorno.

## 4. Otros Servicios Útiles

**ECS con Fargate**: Para orquestar los contenedores del backend. Al ser Fargate serverless, no es necesario gestionar instancias EC2. Se integra nativamente con Application Load Balancer y autoescala basado en CPU/memoria.
**Secrets Manager**: Para manejar credenciales de SQL Server y S3 con rotación automática. Elimina el riesgo de credenciales en código o variables de entorno.
**CloudWatch**: Para centralizar logs del backend, métricas de RDS (CPU, conexiones) y ECS (uso de memoria). Configuraría alarmas para errores 5xx y latencia alta.
