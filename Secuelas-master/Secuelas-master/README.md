# SQL Detective Game

This project is a Flask application that simulates a game where you play as a data analyst. You will be given missions that require you to write SQL queries to find information and solve objectives.

## How to Run the Project

There are two ways to run this project:

**1. Using the main application (Secuelas):**

This is the primary version of the application.

*   **Prerequisites:**
    *   Python 3.x
    *   Flask
    *   Flask-SQLAlchemy
*   **Setup:**
    1.  Clone the repository.
    2.  Navigate to the `Secuelas` directory: `cd Secuelas`
    3.  Install the required dependencies (you might want to use a virtual environment):
        ```bash
        pip install Flask Flask-SQLAlchemy
        ```
*   **Running the application:**
    1.  Ensure you are in the `Secuelas` directory.
    2.  Run the `app.py` file:
        ```bash
        python app.py
        ```
    3.  Open your web browser and go to `http://0.0.0.0:5001` or `http://localhost:5001`.

**2. Using the standalone demo (sql_game_demo.py):**

This is a single-file version of the game, useful for quick demos.

*   **Prerequisites:**
    *   Python 3.x
    *   Flask
    *   Flask-SQLAlchemy
*   **Setup:**
    1.  Clone the repository.
    2.  Install the required dependencies (you might want to use a virtual environment):
        ```bash
        pip install Flask Flask-SQLAlchemy
        ```
*   **Running the application:**
    1.  Navigate to the root directory of the project.
    2.  Run the `sql_game_demo.py` file:
        ```bash
        python sql_game_demo.py
        ```
    3.  Open your web browser and go to `http://0.0.0.0:5001` or `http://localhost:5001`.

## Project Structure

Here's a brief overview of the main files and directories:

*   **`Secuelas/`**: This directory contains the main Flask application.
    *   **`app.py`**: The main entry point for the Flask application. It creates and configures the Flask app instance.
    *   **`views.py`**: Defines the routes and view functions for the application (handling web requests and rendering HTML).
    *   **`models.py`**: Contains the SQLAlchemy database models (e.g., `Employee`, `DocumentAccessLog`, `Archive`).
    *   **`config.py`**: Holds configuration settings for the application, most importantly the mission definitions. This includes the mission briefings, conditions for successful completion (`solution_check`), and hints.
    *   **`extensions.py`**: Sets up Flask extensions, like SQLAlchemy.
    *   **`init_db.py`**: Contains logic to initialize the database with schema and initial data.
    *   **`templates/`**: Contains the HTML templates used for rendering web pages (e.g., `index.html`).
    *   **`notas_*.txt`**: Text files with notes and ideas related to different parts of the project.
*   **`sql_game_demo.py`**: A standalone Python script that runs a demo version of the game. It includes the Flask app, database models, and game logic in a single file.
*   **`README.md`**: This file, providing information about the project.

## How to Play

The game interface presents you with missions from your "Coordinator." Each mission will require you to retrieve specific information from a simulated database by writing SQL queries.

1.  **Read the Mission Briefing:** Carefully read the title, subject, and body of the message from your coordinator. This will explain your objective.
2.  **Write SQL Queries:** In the "ENTRADA DE CONSULTA SQL" text area, write the SQL query you believe will satisfy the mission's requirements.
3.  **Execute Query:** Click the "EJECUTAR CONSULTA" button.
4.  **Review Results:**
    *   If your query is syntactically correct, the results will be displayed in a table.
    *   If there's an error in your SQL, an error message will be shown.
    *   The game will check if your query results correctly solve the mission.
5.  **Mission Progression:**
    *   If your solution is correct, you will receive a success message and automatically advance to the next mission.
    *   If your solution is incorrect, you'll receive a warning, and you might get a hint to help you refine your query.
6.  **Archived Findings:** Some missions might have you uncover information that gets "archived" for future reference. These will be listed under "HALLAZGOS ARCHIVADOS."
7.  **Reset Progress:** If you want to start over from the beginning, you can click the "REINICIAR SIMULACIÓN" button.

**Objective:** Successfully complete all assigned missions by applying your SQL knowledge.

## Future Improvements

This project has potential for further development. Some ideas include:

*   **New Missions:** Designing and implementing more complex and diverse missions.
*   **Enhanced Storyline:** Developing a more intricate narrative that unfolds as the player progresses.
*   **Database Schema Enhancements:**
    *   Refining table relationships (e.g., explicitly linking `document_access_logs` to a dedicated `documents` table).
    *   Adding new tables and fields to support more complex query scenarios.
*   **Advanced SQL Challenges:** Introducing missions that require more advanced SQL features like JOINs, subqueries, window functions, etc.
*   **User Authentication:** Adding user accounts to save progress.
*   **Improved UI/UX:** Enhancing the visual design and user experience of the terminal interface.

Many of these ideas are inspired by the notes found in `Secuelas/notas_generales.txt`.
