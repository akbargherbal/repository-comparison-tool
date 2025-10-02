# Repository Comparison Tool

This web application provides a visual comparison of a Git repository's file structure at two different points in time. It uses pre-processed historical data from the [TandoorRecipes/recipes](https://github.com/TandoorRecipes/recipes) repository to display an interactive file tree for commits closest to the selected dates.

![Screenshot of the Repository Comparison Tool](./screenshot.png)  
_(Note: You would typically add a screenshot of the application here.)_

## Features

- **Side-by-Side View**: Compare two versions of the repository structure simultaneously.
- **Date-Based Selection**: Choose any two dates to find the earliest commit on or after that day.
- **Interactive File Trees**: Expand and collapse directories to explore the repository's layout, powered by Wunderbaum.js.
- **Commit Metadata**: View the exact commit date and hash for each snapshot.
- **Direct GitHub Links**: Easily navigate to the corresponding commit on GitHub.
- **Responsive Design**: The interface adapts to various screen sizes, from desktops to tablets.

## Tech Stack

- **Backend**: Python 3, Flask, Pandas
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Data Format**: Apache Parquet for efficient data storage and retrieval.
- **Tree Visualization**: [Wunderbaum.js](https://github.com/mar10/wunderbaum) library.

## How It Works

The application operates in a straightforward manner:

1.  **Data Loading**: On startup, the Flask server loads a Parquet file (`recipes_json_trees.parquet`) into a Pandas DataFrame. This file contains the commit history, metadata, and a JSON representation of the file tree for each commit.
2.  **Frontend Request**: When a user selects two dates and clicks "Compare," the browser sends asynchronous JavaScript requests to the backend API for each date.
3.  **Backend Logic**: The Flask API endpoint (`/tree/<year>/<month>`) receives the request. It uses the pre-sorted DataFrame to efficiently find the first commit that occurred on or after the requested date.
4.  **JSON Response**: The backend returns a JSON object containing the file tree structure, commit hash, exact commit date, and a direct link to the commit on GitHub.
5.  **Frontend Rendering**: The JavaScript on the frontend parses the JSON response and uses the Wunderbaum.js library to render the interactive file tree in the corresponding panel.

## Project Structure

```
.
├── app.py                  # Main Flask application, routes, and logic
├── helpers.py              # Helper function to query the DataFrame
├── recipes_json_trees.parquet # The dataset containing repository snapshots
├── templates/
│   └── index.html          # The single HTML page for the user interface
└── README.md               # This file
```

## Setup and Installation

To run this project locally, follow these steps:

**Prerequisites:**

- Python 3.8+
- pip package manager

**1. Clone the Repository**

```bash
git clone <repository-url>
cd <repository-directory>
```

**2. Create and Activate a Virtual Environment**
It's highly recommended to use a virtual environment to manage dependencies.

- **Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

**3. Install Dependencies**
Create a `requirements.txt` file with the following content:

```
Flask
pandas
pyarrow
```

Then, install the packages:

```bash
pip install -r requirements.txt
```

_(Note: `pyarrow` is required by Pandas to read Parquet files.)_

**4. Run the Application**

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000` in your web browser.

## API Endpoints

The application exposes a simple API to fetch repository data.

- **`GET /`**

  - **Description**: Renders the main HTML page.
  - **Response**: `text/html`

- **`GET /tree/<year>/<month>`**
  - **Description**: Fetches the repository tree and metadata for the first commit on or after the specified year and month.
  - **URL Parameters**:
    - `year` (integer): The four-digit year (e.g., `2020`).
    - `month` (integer): The one or two-digit month (e.g., `1` or `12`).
  - **Success Response** (`200 OK`):
    ```json
    {
      "tree": [
        {"title": "src", "folder": true, "children": [...]}
      ],
      "commit_hash": "a1b2c3d4e5f6g7h8i9j0...",
      "date": "2020-01-15T10:30:05+00:00",
      "github_link": "https://github.com/TandoorRecipes/recipes/tree/a1b2c3d..."
    }
    ```
  - **Error Response** (`500 Internal Server Error`):
    ```json
    {
      "error": "No data found for or after 2023-01"
    }
    ```
