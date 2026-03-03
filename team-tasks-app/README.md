# Team Tasks App

Estructura base del proyecto. Incluye API construida con FastAPI y PostgreSQL.

## Endpoints principales

- **/users/**: CRUD de usuarios.
- **/tasks/**: CRUD de tareas.
- **/tasks/filters/search?q=<texto>**: Buscar tareas por título o descripción.
- **/tasks/filters/filter?user_id=<id>&status=<estado>**: Filtrar tareas por usuario y/o estado.

> Nota: los endpoints de filtros usan el subpath `/tasks/filters` para evitar
> colisiones con `/tasks/{task_id}` que generaban errores HTTP 422 cuando
> la palabra `search` o `filter` se interpretaba como `task_id`.

## Probar en Swagger

Levanta el contenedor con `docker compose up --build` y abre
[http://localhost:8000/docs](http://localhost:8000/docs). Busca la sección
"Filters" y utiliza los campos de consulta (`q`, `user_id`, `status`) para
realizar búsquedas y filtrados.
