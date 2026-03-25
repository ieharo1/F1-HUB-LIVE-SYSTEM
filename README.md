# 🏎️ F1 Hub Live System

<p align="center">
  <img src="https://img.icons8.com/color/200/racing-helmet.png" alt="F1 Hub Logo" width="200"/>
</p>

---

## 📱 Descripción

**F1 Hub Live System** es una plataforma web full stack construida con **Django + PostgreSQL + Docker** y frontend 100% **Bootstrap 5** (sin CSS custom), inspirada en la experiencia visual de Formula 1.

> El sistema centraliza datos reales de F1 en un solo dashboard: noticias, standings de pilotos, standings de constructores, calendario, resultados y sesiones live/recentes.

---

## ✨ Características

### Funcionalidades Implementadas ✅

- ✅ **Dashboard F1 completo** con diseño responsive estilo dark + acentos racing
- ✅ **Clasificación de Pilotos (real)** desde API externa
- ✅ **Clasificación de Constructores (real)** desde API externa
- ✅ **Calendario del campeonato** por rondas
- ✅ **Resultados de la última carrera**
- ✅ **Noticias de Formula 1** vía feed RSS oficial
- ✅ **Módulo Live Sessions** con datos de sesiones recientes/live
- ✅ **API interna JSON (`/api/live/`)** para refresco parcial
- ✅ **Polling cada 30 segundos** (mínimo JS)
- ✅ **Caché en PostgreSQL** para optimizar consumo de APIs
- ✅ **Docker + Docker Compose** listo para producción/entorno local

### Próximamente 🔄

- 🔄 Login de usuarios + favoritos de equipos/pilotos
- 🔄 Gráficos históricos por piloto/constructor
- 🔄 Alertas push de cambios de standings
- 🔄 Integración de telemetry avanzada por vuelta

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Backend | Django | 5.1.6 |
| Lenguaje | Python | 3.12 |
| Base de datos | PostgreSQL | 16 |
| Frontend | Bootstrap | 5.3.3 |
| Contenedores | Docker + Compose | latest |
| HTTP Client | requests | 2.32.3 |

---

## 📁 Estructura del Proyecto

```text
__React/
├── dashboard/
│   ├── migrations/
│   ├── templates/dashboard/
│   │   └── home.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── services.py
│   └── views.py
├── f1hub/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 Cómo Ejecutar el Proyecto

### 1) Clonar
```bash
git clone <tu-repo>
cd __React
```

### 2) Levantar con Docker (recomendado)
```bash
docker compose up --build
```

La aplicación quedará en:
- 🌐 http://localhost:8000

### 3) Ejecutar sin Docker (opcional)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export POSTGRES_DB=f1hub
export POSTGRES_USER=f1hub
export POSTGRES_PASSWORD=f1hub
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
python manage.py migrate
python manage.py runserver
```

---

## 🌍 Fuentes de Datos Reales

- **Jolpica / Ergast compatible API**: standings, calendario, resultados.
- **OpenF1 API**: sesiones live/recentes.
- **Formula1.com RSS**: noticias oficiales.

> Si una API externa falla, el sistema no se cae: mantiene resiliencia con fallback y cacheo.

---

## 📡 API Interna

### Endpoint live
```http
GET /api/live/
```

Respuesta:
- `driver_standings`
- `constructor_standings`
- `live_sessions`
- `updated_at`

---

## 📱 Responsive Design

- Mobile-first con grid Bootstrap 5
- Tablas responsivas (`table-responsive`)
- Cards adaptativas para noticias y módulos live
- Navbar sticky para navegación rápida

---

## 🧠 Arquitectura de Actualización “Casi Tiempo Real”

1. El backend consulta fuentes reales.
2. Guarda snapshot en PostgreSQL (`ApiSnapshot`).
3. El frontend refresca bloques críticos cada 30s con JS mínimo.
4. Se evita sobrecargar APIs gracias al TTL de caché.

---

## 🐳 Docker

### Servicios
- `web`: Django app
- `db`: PostgreSQL 16

### Comandos útiles
```bash
docker compose up --build
docker compose down
docker compose logs -f web
docker compose exec web python manage.py createsuperuser
```

---

## 👨‍💻 Desarrollado por Isaac Esteban Haro Torres

**Ingeniero en Sistemas · Full Stack Developer · Automatización · Data**

### 📞 Contacto

- 📧 **Email:** zackharo1@gmail.com
- 📱 **WhatsApp:** [+593 988055517](https://wa.me/593988055517)
- 💻 **GitHub:** [ieharo1](https://github.com/ieharo1)
- 🌐 **Portafolio:** [ieharo1.github.io](https://ieharo1.github.io/portafolio-isaac.haro/)

---

## 📄 Licencia

© 2026 Isaac Esteban Haro Torres - Todos los derechos reservados.

---

⭐ Si te gustó el proyecto, ¡dame una estrella en GitHub!
