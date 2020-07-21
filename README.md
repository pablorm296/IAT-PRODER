# IAT (Proyecto sobre Discriminación Étnico-Racial en México)

This is an Implicit Association Test (IAT) designed to measure the strength of stereotypes on skin tones. This test was created for the [Ethnoracial Discrimination in Mexico Research Project](https://discriminacion.colmex.mx/) at [El Colegio de México](https://www.colmex.mx/en).

## Overview :mag:

This IAT is based on the [Stereotype Content Model](https://en.wikipedia.org/wiki/Stereotype_content_model) (SCM). It measures the strength of associations between two target categories (dark skin, white skin) and implicit stereotypes.

The server side implementation uses Python (mainly [Flask](https://flask.palletsprojects.com/en/1.1.x/)), to process user interaction, serve dynamic pages, and manage sessions. It also uses [MongoDB](https://www.mongodb.com/) as the main storage service. The Python application exposes a [Public REST API](https://en.wikipedia.org/wiki/Representational_state_transfer) as the main way of communication with the client side (a basic mix of plain JS, SASS, and HTML) and other software.

To compute the IAT effect, we implemented the scoring algorithm proposed by A. G. Greenwald and B. A. Nosek in ["Understanding and Using the Implicit Association Test: I. An ImprovedScoring Algorithm"](https://psycnet.apa.org/record/2003-05897-003), which at its core uses a 

### Collaborators

**IAT design:** Stephanie Posadas Narvaéz.

**IAT implementation:** Pablo Reyes Moctezuma.

**Content review:** Elisa Marcela Cheng Oviedo, Patricio Solís Gutiérrez.

## Deployment and Configuration Instructions :package:

First of all, if you're deploying this IAT on a remote server, make sure that you have ssh access to it and that your user is in the _sudoers_ group.

You can deploy the IAT using [Docker](https://www.docker.com/) (recommended) or by directly installing it on your server (only advanced users). Please, keep it mind that **this application was designed to be deployed in GNU/Linux systems**. We have not tested it on Windows Servers.

### Deploy with Docker :whale:

To deploy this app using Docker, you need to have Docker installed in your system. If you don't have it, please follow the instructions provided in [this link](https://docs.docker.com/engine/install/). 

#### 1. Clone the repository

Start by cloning this repository.

```bash
git clone https://github.com/pablorm296/IAT-PRODER.git
```

This will create a new directory with a copy of the repository inside it. Next, we just simply move to the cloned repository folder.

```bash
cd IAT-PRODER
```

### Native Installation

#### Configuration

#### Testing & Debugging

## IAT Results :bar_chart:

## Build Info :construction_worker:

## Security :police_car:

## License :page_with_curl:

See LICENSE for more information on licensing.
