<p align="center">
      <img src="https://github.com/serj-goa/todolist_project/blob/main/logo.png" alt="Project Logo" width="200">

[//]: # (<img src="https://www.seekpng.com/png/detail/1012-10120478_the-to-do-list-graphic-design.png" )
[//]: # (alt="The To Do List - Graphic Design@seekpng.com" width="726">)
</p>

[//]: # (<kbd>)

[//]: # (    <img src="https://github.com/serj-goa/todolist_project/blob/main/logo.png" alt="Project Logo">)

[//]: # (</kbd>)

[//]: # ()
[//]: # (![Project logo]&#40;https://github.com/serj-goa/todolist_project/blob/main/logo.png&#41;)

# ToDoList

<b>_ToDoList_ _Project_</b> — task planner that allows you to work with goals and track progress towards achieving them.

---

### Built with:

[<img src="https://img.shields.io/badge/python-3.10%20%7C%203.11-blue?style=for-the-badge&logo=Python">](https://www.python.org/)
[<img src="https://img.shields.io/badge/Django-4.1.17-blue?style=for-the-badge&logo=Django">](https://docs.djangoproject.com/en/4.1/)
[<img src="https://img.shields.io/badge/PostgreSQL-grey?style=for-the-badge&logo=PostgreSQL">](https://www.postgresql.org/)
[<img src="https://img.shields.io/badge/Docker-grey?style=for-the-badge&logo=Docker">](https://docs.docker.com/)
---

### Functionality:

* Login/registration/authentication via VK.
* Goal creation.
* Selection:
    * Goal time frame with display of number of days to goal completion;
    * category of the goal (personal, work, development, sport, etc.) with possibility to add/delete/update categories;
    * goal priority (static list of minor, major, critical, etc.);
    * goal completion status (in progress, completed, overdue, archived).
* Change:
    * targets;
    * target description;
    * status;
    * priority and category of the goal.
* Deleting a goal.
    * When a target is deleted, its status changes to "in the archive".
* Search by target name.
* Filtering by status, category, priority, year.
* Unloading of targets to CSV/JSON.
* Notes on goals.

### Local launch:

#### - Running a project with Docker

In the project directory, run the command:

```python
make up-d
```

#### - Running in a virtual environment

1. Clone the repository.

    While in the code folder, create a virtual environment 

    ```python
    python -m venv venv
    ```

2. Activate it:

    `venv\scripts\activate.bat` - Windows

    `source venv/bin/activate`  - Linux/Mac


3. Install dependencies 
    ```python
    python -m pip install -r requirements.txt
   ```

4. Rename `.env.example` to `.env` and populate it.


5. To run it locally, while in the project directory, execute the commands:

    ```python
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```
