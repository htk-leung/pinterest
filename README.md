# Pinterest Clone Full Stack App

This repository hosts the source code of a full stack app that emulates the functionalities of Pinterest.

The project is written in Python, build upon the Django app framework, and uses PostgreSQL as the backend database service provider. 

Supported features include and not limited to :

* Homepage displaying all pins available on site
* Search for pins by tag
* Creation of new accounts with email, password, name etc.
* Creation/Deletion of new pin, board, and streams of selected boards
* Adding friends whose posts you can see in a stream
* Commenting on and liking pins


---

## Project Structure

```
.
├── mysite/
│   ├── dbquery/            #  
│   ├── mysite/             # 
│   ├── db.sqlite3          # Database 
│   └── manage.py           # Code for running server
├── pclone/
│   ├── icons/              # 
│   ├── images/             # 
│   ├── media/              # 
│   ├── pclone/             # App src code
│   ├── pinsdbmigrate/      # DB migration files
│   ├── pinterest/          # App src code
│   └── manage.py           # 
├── requirements.txt        # pip install requirements.txt
└── README.md

```

---

## Build & Run

###  Build environment

```anaconda powershell prompt
conda env create -f environment.yml
conda list
conda activate pinenv
```

This creates a new Conda virtual environment with pip installed. Then you can proceed to activating the virtual environment, and installing the rest of the packages with pip. 


###  Run Server

```powershell
cd mysite
python manage.py runserver
```

Enter directory that hosts the root of the Django framework, then run 'runserver' to get link for html preview.


<!-- | Target          | Description                                     |
| --------------- | ----------------------------------------------- |
| `run_hnsw`      | Runs HNSW or Grasp-based search                 |
| `run_vamana`    | Runs Vamana search                              |
| `run_graph`     | Runs the abstract graph (for Efanna, NSG, etc.) |
| `run_data_type`  | Runs HNSW while logging every pop/push from datasets   | -->


---


##  TODO

* file description, DB description, connection from DB to Django, take from paper, sample algo, frontend code, image ![alt text](image-url)
