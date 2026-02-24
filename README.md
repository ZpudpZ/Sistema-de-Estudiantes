# (DESACTUALIZADO)
# SIGA - Sistema Integrado de Gestión Académica

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Docker](https://img.shields.io/badge/container-docker-blue)
![Python](https://img.shields.io/badge/backend-FastAPI-009688)
![Streamlit](https://img.shields.io/badge/frontend-Streamlit-FF4B4B)

## Descripción General
Este repositorio contiene el código fuente y la documentación técnica del Sistema Integrado de Gestión Académica (SIGA). El proyecto consiste en una solución de software diseñada para la administración de información estudiantil, implementada bajo una arquitectura de microservicios containerizados.

El sistema integra un flujo de trabajo DevOps completo, utilizando prácticas de Integración Continua y Despliegue Continuo (CI/CD) para automatizar la puesta en producción en infraestructura On-Premise.

## Arquitectura del Sistema
El diseño del software sigue el patrón arquitectónico **Modelo-Vista-Controlador (MVC)** distribuido, garantizando el desacoplamiento de componentes y la escalabilidad modular.

### Componentes Principales
1.  **Frontend (Capa de Presentación):**
    * Implementado con **Streamlit (Python)**.
    * Responsable de la interacción con el usuario final.
    * Incluye lógica de validación de entrada (Input Validation) estricta en el lado del cliente.
    * Comunicación asíncrona con el Backend mediante peticiones HTTP.

2.  **Backend (Capa de Negocio):**
    * API RESTful desarrollada con **FastAPI**.
    * Gestiona la lógica de negocio, transacciones y seguridad.
    * Utiliza **Pydantic** para la validación de esquemas de datos.

3.  **Persistencia de Datos:**
    * Motor de base de datos **MySQL 8.0**.
    * Configuración mediante volúmenes de Docker para garantizar la integridad y persistencia de la información entre reinicios del sistema.

4.  **Orquestación:**
    * **Docker Compose** administra el ciclo de vida de los contenedores, la red interna virtualizada y la inyección de variables de entorno.

---

## Especificaciones Tecnológicas

| Componente | Tecnología | Versión | Descripción |
| :--- | :--- | :--- | :--- |
| Lenguaje | Python | 3.10 | Lenguaje base para Backend y Frontend. |
| API Framework | FastAPI | 0.95+ | Framework de alto rendimiento para APIs. |
| Interfaz | Streamlit | Latest | Librería para renderizado de UI de datos. |
| Base de Datos | MySQL | 8.0 | Sistema de gestión de bases de datos relacional. |
| ORM | SQLAlchemy | 2.0 | Mapeo objeto-relacional. |
| Contenedores | Docker | 24.0+ | Plataforma de containerización. |
| CI/CD | GitHub Actions | - | Automatización del pipeline de despliegue. |

---

## Estructura del Proyecto

```text
sistema-gestion-oti/
├── .github/workflows/    # Definición de pipelines CI/CD
├── app/                  # Código fuente del Backend (Microservicio API)
│   ├── main.py           # Punto de entrada de la API
│   ├── models.py         # Modelos de base de datos (SQLAlchemy)
│   ├── schemas.py        # Esquemas de validación (Pydantic)
│   └── crud.py           # Capa de acceso a datos
├── frontend/             # Código fuente del Frontend (Microservicio UI)
│   ├── assets/           # Recursos estáticos y hojas de estilo
│   ├── components/       # Módulos de interfaz reutilizables
│   └── app.py            # Punto de entrada de la aplicación visual
├── docker-compose.yml    # Archivo de orquestación de servicios
└── README.md             # Documentación técnica
```
---

## Guía de Instalación y Despliegue

### Prerrequisitos
* Sistema Operativo: Windows 10/11, Linux (Ubuntu 20.04+) o macOS.
* Docker Desktop instalado y en ejecución.
* Git instalado.

### Procedimiento de Despliegue Local

**1. Clonar el repositorio**
```bash
git clone https://github.com/ZpudpZ/Sistema-de-Estudiantes.git
cd Sistema-de-Estudiantes
```

**2. Configuración de Entorno**
Crear un archivo llamado .env en la raíz del directorio del proyecto con las siguientes credenciales:
```bash
COMPOSE_PROJECT_NAME=sistema
DB_NAME=db_estudiantes
DB_USER=user
DB_PASSWORD=user_pass
DB_HOST=db
DB_PORT=3306
MYSQL_ROOT_PASSWORD=root_admin
```
**3. Construcción y Ejecución**
Ejecutar el siguiente comando para compilar las imágenes y levantar los servicios en modo detached:
```bash
docker compose up -d --build
```
## Manual de Uso

Una vez desplegada la infraestructura, los servicios estarán accesibles en los siguientes puertos locales:

### Aplicación Web (Frontend)
**URL:** http://localhost:8501

* **Módulo Directorio:** Visualización tabular de estudiantes activos en el sistema.
* **Módulo Inscripción:** Formulario de registro con validación de integridad (Código de matrícula de 6 dígitos numéricos).
* **Módulo Gestión:** Funcionalidad de búsqueda por Código de Matrícula, edición de datos y eliminación lógica/física de registros.

### Documentación API (Swagger UI)
**URL:** http://localhost:8000/docs

* Interfaz técnica autogenerada para pruebas de endpoints, verificación de esquemas JSON y códigos de estado HTTP.

---

## Flujo de Integración y Despliegue Continuo (CI/CD)

El proyecto implementa un pipeline automatizado mediante **GitHub Actions** y un **Self-Hosted Runner**.

1.  **Source Control:** El código es versionado en la rama `main`.
2.  **Continuous Integration (CI):** Al detectar un `push`, GitHub Actions inicia el flujo de trabajo.
3.  **Continuous Deployment (CD):** El Runner local, configurado en el servidor de destino:
    * Descarga la última versión del código.
    * Reconstruye las imágenes de Docker si se detectan cambios en las dependencias.
    * Reinicia los contenedores garantizando "Zero-Downtime" en la base de datos (gracias a los volúmenes persistentes).

---

## Autor
**Wilder P.**
*Estudiante de Ingeniería de Sistemas*
* Universidad Nacional del Altiplano (UNAP)
* [ZpudpZ](https://github.com/ZpudpZ)
