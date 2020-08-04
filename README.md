# IAT (Proyecto sobre Discriminación Étnico-Racial en México)

This is an Implicit Association Test (IAT) designed to measure the strength of stereotypes on skin tones. This test was created for the [Ethnoracial Discrimination in Mexico Research Project](https://discriminacion.colmex.mx/) at [El Colegio de México](https://www.colmex.mx/en).

### Table of Contents

<!-- TOC -->

- [Overview :mag:](#overview-mag)
    - [Collaborators](#collaborators)
- [Deployment and Configuration Instructions :package:](#deployment-and-configuration-instructions-package)
    - [Deploy with Docker :whale:](#deploy-with-docker-whale)
        - [1. Clone the Repository](#1-clone-the-repository)
        - [2. Set Up](#2-set-up)
            - [2.1. Main App Configuration](#21-main-app-configuration)
            - [2.2. Mongo Container Configuration](#22-mongo-container-configuration)
    - [Native Installation](#native-installation)
        - [Configuration](#configuration)
        - [Testing & Debugging](#testing--debugging)
- [IAT Results :bar_chart:](#iat-results-bar_chart)
- [Build Info :construction_worker:](#build-info-construction_worker)
- [Security :police_car:](#security-police_car)
- [License :page_with_curl:](#license-page_with_curl)

<!-- /TOC -->

## Overview :mag:

This IAT is based on the [Stereotype Content Model](https://en.wikipedia.org/wiki/Stereotype_content_model) (SCM). It measures the strength of associations between two target categories (dark skin, white skin) and implicit stereotypes.

The server side implementation uses Python (mainly [Flask](https://flask.palletsprojects.com/en/1.1.x/)), to process user interaction, serve dynamic pages, and manage sessions. It also uses [MongoDB](https://www.mongodb.com/) as the main storage service. The Python application exposes a [Public REST API](https://en.wikipedia.org/wiki/Representational_state_transfer) as the main way of communication with the client side (a basic mix of plain JS, SASS, and HTML) and other software.

To compute the IAT effect, we implemented the scoring algorithm proposed by A. G. Greenwald and B. A. Nosek in ["Understanding and Using the Implicit Association Test: I. An ImprovedScoring Algorithm"](https://psycnet.apa.org/record/2003-05897-003), which at its core uses [Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d) to compare the user latency.

### Collaborators

**IAT design:** Stephanie Posadas Narvaéz.

**IAT implementation:** Pablo Reyes Moctezuma.

**Content review:** Elisa Marcela Cheng Oviedo, Patricio Solís Gutiérrez.

## Deployment and Configuration Instructions :package:

First of all, if you're deploying this IAT on a remote server, make sure that you have ssh access to it and that your user is in the _sudoers_ group.

You can deploy the IAT using [Docker](https://www.docker.com/) (recommended) or by directly installing it on your server (only advanced users). Please, keep it mind that **this application was designed to be deployed in GNU/Linux systems**. We have not tested it on Windows Servers.

### Deploy with Docker :whale:

To deploy this app using Docker, you need to have Docker installed in your system. If you don't have it, please follow the instructions provided [here](https://docs.docker.com/engine/install/). 

#### 1. Clone the Repository

Start by cloning this repository.

```bash
git clone https://github.com/pablorm296/IAT-PRODER.git
```
#### 2. Set Up

##### 2.1. Main App Configuration

Move to the `Config/` directory in the cloned repository. Inside, you'll see two configuration files: `app-sample.config.json` and  `stimuli.config.json`. The first is an example of how the main configuration file should look like. The second file contains the stimuli to be used during the IAT. 

Edit `app-sample.config.json` as required and save it as `app.config.json`. 

Make sure that the Mongo database name, username, and passwords match your Mongo container configuration (see below). You will also need Google reCaptcha keys. You can sign up to Google reCaptcha and get them [here](https://www.google.com/recaptcha).

Please, **use a strong secret app key**. The key defined in `secret_key` will be used to sign the session cookies used by the web app. **A weak key can be cracked, allowing users to freely modify the session cookie**.

##### 2.2. Mongo Container Configuration

Move to the `Docker/Mongo/Config` directory in the cloned repository. Inside, you'll see two files: `db_secrets-example` and `root_secret-example`. Both are examples of the configurations files that define Mongo credentials and the container's root password, respectively.

Edit `db_secrets-example`. You'll need to define an username and password for the DB admin and the App reader/writer. You'll also need to specify the name of the DB for the app. Please, make sure that the Mongo fields in `app.config.json` (see above) match the credentials and DB name defined in this file. After editing, save it as `db_secrets`.

Edit `root_secret-example` and save it as `root_secret`. In this file you need to define the container's root password.

Please, **use strong passwords**. The Mongo container was configured to allow only authenticated users to perform read/write operations. However, **if you use weak passwords, DB info can be easily compromised**.

### Native Installation

#### Configuration

#### Testing & Debugging

## IAT Results :bar_chart:

## Build Info :construction_worker:

## Security :police_car:

## License :page_with_curl:

See LICENSE for more information on licensing.
