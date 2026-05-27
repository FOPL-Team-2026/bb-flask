# bb-flask — Boolean Boyz Backend

The Boolean Boyz backend server, built to support the **Friends of the Poway Library (FOPL)** web application. This is a Python Flask API server forked from the [Open Coding Society Flask starter](https://github.com/open-coding-society/flask) and customized for our class project.

## About This Project

This backend was built by the Boolean Boyz team as part of an AP Computer Science Principles capstone project. It powers the FOPL website, providing APIs for volunteer management, book cataloging, interactive library games, and more. Future class cohorts are welcome and encouraged to build on this foundation.

## FOPL Features

The following features were built specifically for the Friends of the Poway Library:

- **Volunteer Applications** — Submit, review, and manage volunteer sign-ups with status tracking (`new`, `reviewed`, `contacted`, `accepted`, `rejected`)
- - **Book Scanner** — Scan and look up books to manage the library catalog
  - - **Book Catalog** — Browse and manage library book listings
    - - **Book Trivia** — A trivia game using the library's book collection
      - - **Calendar** — View and manage FOPL events
        - - **Face Match** — AI-assisted facial recognition feature for library use
          - - **Cover Guesser** — A game where users guess books from their covers
            - - **Library Dodge / Library Shelf Run** — Interactive library-themed mini games
              - - **Word Scramble / Puzzles / Network Stack Game / OSI Layers RPG** — Educational games tied to library and CS themes
                - - **Chat** — A chat feature for library community interaction
                  - - **Newsletters** — Manage and display FOPL newsletters
                    - - **Admin Panel** — FOPL-specific admin dashboard for managing the site
                      - - **User Authentication** — Login and session management for FOPL users
                       
                        - ## Project Structure
                       
                        - ```
                          bb-flask/
                          ├── api/
                          │   ├── fopl_volunteer_api.py   # Volunteer application management
                          │   ├── fopl_book_api.py        # Book scanner and catalog
                          │   ├── fopl_calendar_api.py    # Events calendar
                          │   ├── fopl_chat_api.py        # Community chat
                          │   ├── fopl_facematch_api.py   # AI face matching
                          │   ├── fopl_puzzle_api.py      # Puzzles and games
                          │   ├── fopl_admin_api.py       # Admin panel
                          │   ├── fopl_auth_api.py        # FOPL user authentication
                          │   └── fopl_ai_service.py      # AI service integrations
                          ├── model/                      # SQLAlchemy database models
                          ├── scripts/                    # Database init and migration scripts
                          ├── instance/                   # Generated SQLite database
                          ├── main.py                     # App entry point
                          └── requirements.txt
                          ```

                          ## Getting Started

                          ### Prerequisites

                          - Python 3.9 or later
                         
                          - ### Setup
                         
                          - 1. Clone the repository:
                            2.    ```bash
                                     git clone https://github.com/Boolean-Boyz/bb-flask.git
                                     cd bb-flask
                                     ```

                                  2. Create and activate a virtual environment:
                                  3.    ```bash
                                           python -m venv venv
                                           source venv/bin/activate
                                           ```

                                        3. Install dependencies:
                                        4.    ```bash
                                                 pip install -r requirements.txt
                                                 ```

                                              4. Create a `.env` file in the project root with your local secrets.
                                          
                                              5. 5. Initialize the database:
                                                 6.    ```bash
                                                          python scripts/db_init.py
                                                          ```

                                                       6. Run the server:
                                                       7.    ```bash
                                                                python main.py
                                                                ```

                                                             ## Contributing

                                                         This repo is designed to be picked up by future Boolean Boyz cohorts. To contribute:

                                                   1. Branch off `main` for your feature
                                                   2. 2. Make your changes with clear comments
                                                      3. 3. Open a pull request describing what you added or changed
                                                        
                                                         4. ## License
                                                        
                                                         5. MIT License — see [LICENSE](LICENSE) for details.
