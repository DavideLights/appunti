
# `APIRouter`
**Struttura**: FastAPI mostra una struttura a piu cartelle
```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```
* `__init__.py`: la presenza di questo file permette di struttura il progetto in moduli `routers` ed `internal`. Python vede la cartella come un `Paccheto`, ossia una collezione di moduli.
* seprazione logica delle `path operations`


`httpx`

