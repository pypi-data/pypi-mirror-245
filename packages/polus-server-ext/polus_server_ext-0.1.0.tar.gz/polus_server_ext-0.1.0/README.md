# Polus-Server-Extension
Jupyter Server Extension used serve files and provides a static build of Polus Render.

Please note that [render-server-ext](https://github.com/PolusAI/jupyterlab-extensions/tree/master/jupyterlab_polus_render/render-server-ext) is the improved version of this package.

# Installation
```
pip install "git+https://github.com/PolusAI/polus-prototypes.git#egg=polus-server-ext&subdirectory=polus-server-ext"
```
You will need to restart Jupyter Server for `polus-server-ext` endpoints to take effect.

# Adding a static build of Polus Render
- Remove all existing files in `~/serve/static/render-ui/`.
- Run `npx nx build render-ui` in the root of your Polus Render folder
- Transfer generated files from `~/Polus Render/dist/apps/render-ui/` into `~/serve/static/render-ui/`.

# API Endpoints
- `/serve/`: Help on usage of extension
- `/static/serve/render-ui/index.html`: Serves local version of Polus Render Web Application
- `/serve/file/(.+)`: Serves files at a specfied  directory. Does not serve directories.

After installation, you will need to restart the notebook server for changes to take effect.
