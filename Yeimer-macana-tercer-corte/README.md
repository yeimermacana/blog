# 📊 Blog de Analítica Avanzada con Jekyll

Blog profesional para análisis de datos con Apache Spark, construido con Jekyll y GitHub Pages.

## 🚀 Instalación y Configuración

### Prerrequisitos

```bash
# Instalar Ruby (Windows)
# Descargar desde: https://rubyinstaller.org/

# Verificar instalación
ruby -v
gem -v
```

### Paso 1: Instalar dependencias

```bash
# Instalar Bundler
gem install bundler jekyll

# Instalar dependencias del proyecto
bundle install
```

### Paso 2: Generar gráficas

```bash
# Instalar librerías Python necesarias
pip install matplotlib pandas numpy seaborn

# Crear carpeta para imágenes si no existe
mkdir -p assets/images

# Generar las gráficas
python generate_graphs.py
```

### Paso 3: Ejecutar el servidor local

```bash
# Iniciar servidor Jekyll
bundle exec jekyll serve

# O con live reload
bundle exec jekyll serve --livereload
```

Visita: **http://localhost:4000**

## 📁 Estructura del Proyecto

```
blog-analytics/
│
├── _config.yml                 # Configuración principal
├── _includes/                  # Componentes reutilizables
│   ├── head.html              # Meta tags y CSS
│   └── footer.html            # Pie de página
│
├── _layouts/                   # Plantillas
│   ├── default.html           # Layout base
│   └── post.html              # Layout para artículos
│
├── _posts/                     # Artículos del blog
│   └── 2025-10-29-analisis-clickstream-spark.md
│
├── assets/                     # Recursos estáticos
│   ├── css/
│   │   └── style.css          # Estilos personalizados
│   ├── images/                # Gráficas generadas
│   │   ├── top_users_chart.png
│   │   ├── temporal_analysis.png
│   │   ├── clicks_vs_sessions.png
│   │   ├── user_distribution.png
│   │   └── activity_heatmap.png
│   └── data/
│       └── clickstream_data.csv
│
├── _site/                      # Sitio generado (no editar)
├── index.md                    # Página principal
├── generate_graphs.py          # Script para gráficas
├── Gemfile                     # Dependencias Ruby
└── README.md                   # Este archivo
```

## 🎨 Personalización

### Cambiar información del blog

Edita `_config.yml`:

```yaml
title: Tu Título
description: Tu Descripción
author: Tu Nombre
baseurl: ""
url: "https://tu-usuario.github.io"
```

### Agregar nuevo artículo

1. Crea un archivo en `_posts/` con formato: `YYYY-MM-DD-titulo.md`

```markdown
---
layout: post
title: "Título del Artículo"
date: 2025-10-29
author: Tu Nombre
categories: analytics spark
---

# Tu contenido aquí
```

2. Ejecuta: `bundle exec jekyll serve`

### Modificar estilos

Edita `assets/css/style.css` con tus colores y estilos preferidos.

## 📊 Generar Nuevas Gráficas

El script `generate_graphs.py` crea 5 visualizaciones:

1. **top_users_chart.png** - Top 15 usuarios por actividad
2. **temporal_analysis.png** - Análisis temporal de clicks
3. **clicks_vs_sessions.png** - Relación clicks vs sesiones
4. **user_distribution.png** - Distribución de usuarios
5. **activity_heatmap.png** - Mapa de calor de actividad

Para personalizar:

```python
# Edita generate_graphs.py con tus propios datos
users = ['User_001', 'User_002', ...]
clicks = [94, 93, 87, ...]
```

## 🚀 Despliegue en GitHub Pages

### Opción 1: Repositorio Personal

```bash
# 1. Crear repo: username.github.io
# 2. Subir archivos
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/username.github.io.git
git push -u origin main

# 3. Tu sitio estará en: https://username.github.io
```

### Opción 2: Repositorio de Proyecto

```bash
# 1. Crear repo cualquiera
# 2. Actualizar _config.yml:
baseurl: "/nombre-repo"
url: "https://username.github.io"

# 3. Habilitar Pages en Settings > Pages > Branch: main
# 4. Tu sitio: https://username.github.io/nombre-repo
```

## 🔧 Comandos Útiles

```bash
# Servidor local
bundle exec jekyll serve

# Construir sitio
bundle exec jekyll build

# Limpiar archivos generados
bundle exec jekyll clean

# Ver versión
bundle exec jekyll -v

# Actualizar dependencias
bundle update
```

## 📝 Formato de Posts

### Front Matter

```yaml
---
layout: post
title: "Título"
date: 2025-10-29
author: Nombre
categories: categoria1 categoria2
---
```

### Incluir imágenes

```markdown
![Descripción]({{ "/assets/images/imagen.png" | relative_url }})
```

### Código

````markdown
```python
# Tu código aquí
print("Hola mundo")
```
````

### Tablas

```markdown
| Columna 1 | Columna 2 |
|-----------|-----------|
| Dato 1    | Dato 2    |
```

## 🐛 Solución de Problemas

### Error: "Could not find gem 'jekyll'"

```bash
gem install jekyll bundler
bundle install
```

### Error: "Address already in use"

```bash
# Cambiar puerto
bundle exec jekyll serve --port 4001
```

### Las gráficas no aparecen

```bash
# Verificar que existan
ls assets/images/

# Regenerar
python generate_graphs.py
```

### Cambios no se reflejan

```bash
# Limpiar y reconstruir
bundle exec jekyll clean
bundle exec jekyll serve --livereload
```

## 📚 Recursos Adicionales

- [Documentación Jekyll](https://jekyllrb.com/docs/)
- [GitHub Pages](https://pages.github.com/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Apache Spark](https://spark.apache.org/docs/latest/)

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👤  Autor
maria Fernanda herazo escobar 


- Curso: Analítica Avanzada 2025
- Proyecto: Análisis de Clickstream con Spark
