# My great planning app

docker compose up -d

docker compose restart

# Run migrations for the new models
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Restart to pick up code changes
docker compose restart web

user
admin nopassword


mermaid class diagram
https://mermaid.live/edit

```

classDiagram
    class User {
        <<Django Auth>>
        +int id
        +str username
        +str email
        +str password
        +bool is_active
        +bool is_staff
    }

    class Plan {
        +int id
        +str title
        +text description
    }

    class Task {
        +int id
        +str title
        +text description
        +str status "pending|in_progress|completed"
        +datetime created_at
        +datetime completed_at
        +property duration()
    }

    class FlashCardCollection {
        +int id
        +str title
    }

    class FlashCard {
        +int id
        +str title
        +text front_side
        +text back_side
    }

    class Timer {
        +int id
        +str title
        +datetime created_at
        +datetime completed_at
        +property is_running()
    }

    User "1" --> "0..*" Plan : owns
    Plan "1" --> "0..*" Task : contains
    User "1" --> "0..*" FlashCardCollection : owns
    FlashCardCollection "1" --> "0..*" FlashCard : contains
    User "1" --> "0..*" Timer : owns

```