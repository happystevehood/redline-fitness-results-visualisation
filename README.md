# Redline Fitness Results Analyzer

This application allows users to analyze past Redline Fitness Games results, view visualizations, and gain insights for training and race strategy.

I embarked on this developement to expirement with some of the python mathplotlib based visualisation which I had learned.

This module was developed to create visualisation of the results below.

2023 redline fitness games scraped from - Day 1 results.
https://runnersunite.racetecresults.com/results.aspx?CId=16634&RId=1216

2023 redline fitness games scraped from - Day 2 results.
https://runnersunite.racetecresults.com/results.aspx?CId=16634&RId=1217

2024 redline fitness games scraped from - Day 1 results.
https://runnersunite.racetecresults.com/results.aspx?CId=16634&RId=1251

2024 redline fitness games scraped from - Day 2 results.
https://runnersunite.racetecresults.com/results.aspx?CId=16634&RId=1252

Results from abvove were cut and paste into excel file and saved as csv files per competition.

This intial development is based on the format for 2023, The events/formats were different for 2024 so this code will need to be updated.

Here are some examples of the  output that can be produced....
![MensDoubles2024Bar](https://github.com/user-attachments/assets/9b87357c-8ac4-4931-a882-a88e27a8e5da)

![MensSinglesCompetitive2024Hist](https://github.com/user-attachments/assets/035317a0-b424-427e-b0eb-667b8a56c36b)

![MixedDoubles2024Corr](https://github.com/user-attachments/assets/35b0822b-6cd5-40dd-bf77-f979fa5a5c7d)

![TeamRelayMixed2024Pie](https://github.com/user-attachments/assets/4047b102-6092-456d-8fac-7e12cd07c539)

![MixedDoubles2024SkiScat](https://github.com/user-attachments/assets/601d7629-aaae-485d-93d5-8a45cff5ed94)

## Table of Contents

1.  [Features](#features)
2.  [Tech Stack](#tech-stack)
3.  [Prerequisites](#prerequisites)
4.  [Environment Setup](#environment-setup)
    *   [Option 1: Using Docker (Recommended for Reproducibility)](#option-1-using-docker-recommended-for-reproducibility)
    *   [Option 2: Local Setup with Miniconda3 (Manual)](#option-2-local-setup-with-miniconda3-manual)
5.  [Running the Application](#running-the-application)
    *   [Running with Docker](#running-with-docker)
    *   [Running Locally (without Docker)](#running-locally-without-docker)
6.  [Environment Variables](#environment-variables)
7.  [Deployment (Google Cloud Run)](#deployment-google-cloud-run)
    *   [Building the Deploy Image](#building-the-deploy-image)
    *   [Pushing to Google Container Registry (GCR)](#pushing-to-google-container-registry-gcr)
    *   [Deploying to Cloud Run](#deploying-to-cloud-run)
    *   [GCloud Setup Notes](#gcloud-setup-notes)
8.  [Scripts Overview](#scripts-overview)
9.  [Contributing](#contributing) (Optional)
10. [License](#license) (Optional)

## Features

*   Deep Dive Data Analysis of Past Redline Fitness Games Events.
*   Searchable database of athletes and their results.
*   Generation of various performance visualizations (Pie charts, Bar charts, Violin plots, Radar charts, Scatter plots, Heatmaps).
*   Competitor comparison tools.
*   Pacing table generation.
*   Downloadable reports (CSV, PDF).
*   Athlete/Trainer focused design.
*   All free, no hidden charges.

## Tech Stack

*   **Backend:** Python, Flask
*   **Data Handling:** Pandas, NumPy
*   **Visualization:** Matplotlib, Seaborn
*   **PDF Generation:** PyMuPDF
*   **Containerization:** Docker, Docker Compose
*   **Deployment (Optional):** Google Cloud Platform (GCP) - Cloud Run, Container Registry (GCR)
*   **Development Environment:** VSCode, Miniconda3 (for local non-Docker setup)

## Prerequisites

*   **Git:** For cloning the repository.
*   **Docker Desktop:** Required if you choose the Docker setup (recommended). Ensure it's running.
*   **Miniconda3 (or Anaconda):** Required only if you choose the local non-Docker setup for managing Python environments.
*   **Google Cloud SDK (`gcloud` CLI):** Required only if you intend to deploy to Google Cloud Platform.
*   **Bash-like terminal:** For running the `.sh` scripts (Git Bash on Windows, or native terminal on Linux/macOS).

## Environment Setup

You have two primary options for setting up the development environment:

### Option 1: Using Docker (Recommended for Reproducibility)

This is the easiest way to ensure a consistent environment.

1.  **Clone the repository:**
    ```bash
    git clone redline-fitness-results-visualisation
    cd redline-fitness-results-visualisation
    ```
2.  **Ensure Docker Desktop is running.**
3.  **Copy Environment Files:** The application uses `.env` files for configuration. You will need to create them based on the provided examples:
    *   Copy `.env.development.example` to `.env.development` for local Docker development.
    *   Copy `.env.production.example` to `.env.production` for local Docker production simulation.
    *   Copy `.env.deploy.example` to `.env.deploy` if you plan to build for deployment.
    Adjust any necessary variables within these files (e.g., `SECRET_KEY`, database URIs if applicable, though your current scripts suggest environment variables passed via scripts).
4.  **Build & Run:** Use the provided scripts (see [Running with Docker](#running-with-docker)).

### Option 2: Local Setup with Miniconda3 (Manual)

This method was used for initial development and requires manual Python environment setup.

1.  **Clone the repository:** (Same as above)
2.  **Install Miniconda3 (64-bit):** If you don't have it, download and install it from the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html).
3.  **Create a Conda Environment:**
    Open your terminal (Anaconda Prompt or terminal where `conda` is in PATH).
    ```bash
    # It's good practice to create an environment from an environment.yml file if you have one.
    # If not, you can create one manually and install packages.
    # Assuming you have a requirements.txt or will create one:
    conda create --name redline_results python=3.x # Replace 3.x with your Python version
    conda activate redline_results
    # Install dependencies (assuming requirements.txt exists or you install them manually)
    pip install -r requirements.txt 
    # Or: conda install pandas numpy matplotlib seaborn flask flask-wtf PyMuPDF python-slugify gunicorn waitress etc.
    ```
4.  **Set Environment Variables:** You'll need to set `ENV_MODE` (e.g., `development` or `production`) in your terminal before running the app, or the scripts will handle this.
5.  **Copy `.env` files:** Similar to the Docker setup, ensure you have the appropriate `.env` files (e.g., `.env.development`) in the project root, as `python app.py` might load variables from them depending on your Flask app's configuration loading.

## Running the Application

All run scripts are located in the `./run-scripts/` directory and should typically be executed from the project's root directory (the scripts `cd` into the correct locations).

### Running with Docker

Ensure Docker Desktop is running.

*   **Development Mode (Docker):**
    ```bash
    ./run-scripts/run-docker-dev.sh
    ```
    This uses `docker-compose-local.yml` and sets `ENV_MODE=development`, typically running on `http://localhost:5000`.

*   **Production Mode (Docker):**
    ```bash
    ./run-scripts/run-docker-prod.sh
    ```
    This also uses `docker-compose-local.yml` but sets `ENV_MODE=production`, typically running on `http://localhost:8080`.

### Running Locally (without Docker)

Ensure you have activated your Conda environment (`conda activate redline_results`).

*   **Development Mode (Local):**
    ```bash
    ./run-scripts/run-local-dev.sh
    ```
    This sets `ENV_MODE=development` and runs `python app.py` from the `src` directory.

*   **Production Mode (Local):**
    ```bash
    ./run-scripts/run-local-prod.sh
    ```
    This sets `ENV_MODE=production` and runs `python app.py` from the `src` directory. For a true local production test, consider using a WSGI server like Gunicorn or Waitress instead of Flask's built-in server.

## Environment Variables

The application uses environment variables for configuration. These are typically set by the run scripts or loaded from `.env` files. Key variables include:

*   `ENV_MODE`: Can be `development`, `production`, or `deploy`. Controls Flask settings, logging levels, etc.
*   `FLASK_APP`: Should be set to `app.py` (or your main Flask app file).
*   `FLASK_DEBUG`: Set to `1` for development mode.
*   `SECRET_KEY`: A secret key for session management and CSRF protection. **Ensure this is strong and unique for production.**
*   `PORT`: The port the application will run on (used by Docker scripts).
*   *(Add any other environment variables your application relies on, e.g., database URLs, API keys, paths to static directories if not relative)*

Refer to `.env.example` (you should create this) for a template of necessary environment variables.

## Deployment (Google Cloud Run)

These scripts assist in deploying the application to Google Cloud Run using Google Container Registry (GCR).

### Building the Deploy Image

This script builds a Docker image specifically for deployment, using `Dockerfile_deploy`.
```bash
./run-scripts/build-deploy-prod.sh

#redlinefitnessgames #redlinefitness
