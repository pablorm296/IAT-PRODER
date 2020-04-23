# Prueba de Asociaciones Implícitas

Este repositorio contiene una prueba de asociaciones implícitas (IAT, por sus siglas en inglés) diseñada por miembros del Proyecto de Discriminación Étnico Racial en México, adscrito a El Colegio de México, y programada por Pablo Reyes Moctezuma.

## Estructura del repositorio

1. __api/__: Back-end REST API for data processing and session management. Python Flask.
2. __science/__: Folder containing R scripts, data input, and data output to analyse Harvard's Skin Color IAT (only Mexican subset). Partially included in GitHub repo.
3. __ssh/__: SSH Authetication keys for GitHub, Server, and FTP. Not included in GitHub repo.
4. __static/__: Front-end app. HTML, PHP, and Vanilla JS.
    1. __html/__: Static html files.
    2. __imgs/__: Image files.
        1. __stimuli/__: Stimuli images for IAT.
        2. __theme/__: Misc images for app theme.
    3. __js/__: JS files.
    4. __libs/__: Vendor PHP libraries.
        1. __Mobile-Detect/__: Mobile-Detect PHP implementation (source: [repo @ serbanghita/Mobile-Detect](https://github.com/serbanghita/Mobile-Detect))
    5. __src/__: PHP files.
    6. __style/__: SASS (compiled and source) files.
        1. __fonts/__: TTF files for app theme.
    7. __*index.php*__: Landing php file. Redirects to the proper PHP file in src/.
5. __*.htaccess*__: Apache server configuration file. Not included in GitHub repo.
6. __*api.wsgi*__: WSGI script. Configures Back-end REST API. Not included in GitHub repo.
