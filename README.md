# Project Directory Structure

This project uses a modular directory structure to separate code, configuration, data, and documentation. Here is an overview of the main directories:

| Directory                | Purpose                                                                                 |
|--------------------------|-----------------------------------------------------------------------------------------|
| ./backend/               | Python FastAPI backend application source code and Docker build context.                 |
| ./data/                  | Persistent data and configuration for services (databases, observability, etc).         |
| ./data/database/         | MySQL database data (persisted between container restarts).                             |
| ./data/loki/             | Loki log storage and configuration.                                                     |
| ./data/loki/config/      | Loki configuration files (e.g., loki-config.yaml).                                      |
| ./data/loki/wal/         | Loki Write-Ahead Log (WAL) directory (must be writable by Loki container).              |
| ./data/prometheus/       | Prometheus configuration files (e.g., prometheus.yaml).                                 |
| ./data/grafana/          | Grafana persistent data (dashboards, users, etc).                                       |
| ./docs/                  | Project documentation, including observability setup steps.                             |
| ./grafana/               | Grafana provisioning (data sources, dashboards) and custom configuration.                |
| ./grafana/provisioning/  | Grafana provisioning root directory.                                                     |
| ./grafana/provisioning/datasources/ | Data source configuration files for Grafana (e.g., Loki, Prometheus).         |
| ./helm/                  | Helm charts and scripts for Kubernetes-based deployments (if used).                     |

> **Note:**
> - All configuration files use the `.yaml` extension for consistency.
> - Data directories are mounted as Docker volumes for persistence and configuration.

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>
# tic-tac-toe
Tic Tac Toe with N number of players and a bot

<a name="readme-top"></a>

<!-- [![Contributors][contributors-shield]][contributors-url] -->
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/vyavasthita/tic-tac-toe">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Tic Tac Toe</h3>
</div>

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

# About the project
To play Tic Tac Toe Game.

This includes:
* MySql 8
* MySql Workbench
* Phpmyadmin

Details:
* This project has been implemented using Python and FastAPI web framework.

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

## Built With

Softwares/libraries used in this project.

* [![Python][Python]][Python-url]
* [![Docker][Docker]][Docker-url]
* [![DockerCompose][DockerCompose]][Docker-Compose-url]
* [![Makefile][Makefile]][Makefile-url]

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

## :hammer: Testing
### System Environment
- Docker Compose version v2.31.0-desktop.2
- Docker version 27.4.0
- GNU Make 3.81
- Python 3.13.1

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

### :pencil: Notes
TBD

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

### Validations done
TBD

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>


# Feature added
TBD

<!-- Prerequisites -->
## :bangbang: Prerequisites

1. Docker
2. Docker Compose
3. Git Version Control
4. GNU Make

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Installation -->
## :gear: Installation

1. Clone the repo
   ```sh
   git clone https://github.com/vyavasthita/tic-tac-toe.git
   ```

2. Go to root directory 'mysql-learning'.
   ```sh
   cd tic-tac-toe
   ```

3. Checkout master branch
   ```sh
   git checkout master
   ```

<!-- Run -->
### :running: Start Containers

Now you are ready to start the application

1. You must be in root directory 'tic-tac-toe'.

2. Start containers

```bash
  make all
```

This will start multiple docker containers.

#### :eyes: Usage
#### Starting Application

##### FastAPI App
To Open Tic Tac Toe backend App go to following url; -
(This is FastAPI openapi client)

```bash
  http://127.0.0.1:5000/docs
```

#### Phpmyadmin gets connected automatically with MySql DB

##### Phpmyadmin
```bash
  http://0.0.0.0:8081/
```

#### MySqlWorkbench gets connected automatically with MySql DB

##### MySqlWorkbench
```bash
  http://0.0.0.0:3000/
```

##### Create Connection in MySql Workbench
hostname: database
port: 3306
username: root
password: root

##### :pencil: There is no password is used for MySql (Empty Password).

### :pencil:
- Both MySql workbench and phpmyadmin can be used as GUI for Mysql.

# Observability
Ref: https://github.com/iam-veeramalla/observability-zero-to-hero/

##### Prometheus
```sh
   http://localhost:9090/
```
##### Grafana
```sh
   http://localhost:8080/
```
Grafana UI: username is admin
Grafana UI: password is admin

Add Prometheus connection:
Use URL: http://prometheus:9090

# Using Helm

## Observability
Ref: https://github.com/iam-veeramalla/observability-zero-to-hero/
     https://www.cncf.io/blog/2022/04/22/opentelemetry-and-python-a-complete-instrumentation-guide/
     https://last9.io/blog/integrating-opentelemetry-with-fastapi/


### Setup
1. Start Minikube
   ```sh
      minikube start --memory=4098
   ```
2. Run
   ```sh
      make helm
   ```

## Prometheus
```sh
   http://localhost:9090/
```

## Grafana
```sh
   http://localhost:8080/
```
Grafana UI: username is admin
Grafana UI: password is prom-operator

Add Prometheus connection:
Use URL: http://monitoring-kube-prometheus-prometheus.monitoring:9090

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Stop containers -->
### :test_tube: Stop Containers

To stop all running containers, run the following command

```bash
  make stop
```

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Clean containers -->
### :test_tube: Clean Containers

To clean all running containers, run the following command

```bash
  make clean
```

<!-- Deployment -->
# :triangular_flag_on_post: Deployment

TBD

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Roadmap -->
# :compass: Roadmap

It has some limitations;-
- [ ] TBD

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Contributing -->
## :wave: Contributing

<a href="https://github.com/vyavasthita/grhakarya/graphs/contributors">
  Contribution
</a>

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Code of Conduct -->
### :scroll: Code of Conduct

TBD

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

Ref:
https://dev.to/ken_mwaura1/getting-started-monitoring-a-fastapi-app-with-grafana-and-prometheus-a-step-by-step-guide-3fbn


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/-contributors-red?logo=github&logoColor=white&style=for-the-badge
[contributors-url]: https://github.com/vyavasthita/grhakarya/graphs/contributors
[forks-shield]: https://img.shields.io/badge/-forks-pink?logo=github&logoColor=white&style=for-the-badge
[forks-url]: https://github.com/vyavasthita/tiny-url/network/members
[stars-shield]: https://img.shields.io/badge/-stars-yellow?logo=github&logoColor=white&style=for-the-badge
[stars-url]: https://github.com/vyavasthita/tiny-url/stargazers
[license-shield]: https://img.shields.io/badge/-license-blue?logo=license&logoColor=white&style=for-the-badge
[license-url]: https://github.com/vyavasthita/tiny-url/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/diliplakshya/
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Docker]: https://img.shields.io/badge/Docker-4A4A55?style=for-the-badge&logo=docker&logoColor=FF3E00
[Docker-url]: https://www.docker.com/
[linkedin-url]: https://www.linkedin.com/in/diliplakshya/
[DockerCompose]: https://img.shields.io/badge/-Docker%20Compose-blue?logo=docker&logoColor=white&style=for-the-badge
[Docker-Compose-url]: https://docs.docker.com/compose/
[Makefile]: https://img.shields.io/badge/-makefile-red?logo=gnu&logoColor=white&style=for-the-badge
[Makefile-url]: https://www.gnu.org/software/make/