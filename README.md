# Professor Dashboard

## Project Overview

**Professor Dashboard** is a full-stack project designed to display and manage professor data. The project consists of three main parts:

- **Frontend**: An interactive dashboard built with Angular (using standalone components) to display, create, edit, and delete professor records.
- **Backend**: A RESTful API built with Flask that integrates with a MongoDB database, implements JWT user authentication, and automatically generates API documentation using Flasgger.
- **Data Analysis**: A component that uses Python's Pandas, Matplotlib, and ReportLab to perform exploratory data analysis on professor data and generate a PDF report.

## Tech Stack

- **Frontend**: Angular, HTML, CSS, JavaScript
- **Backend**: Python, Flask, Flask-CORS, PyMongo, Flasgger, Flask-JWT-Extended
- **Database**: MongoDB
- **Data Analysis**: Python, Pandas, Matplotlib, ReportLab

## Project Structure

```
professor-dashboard/
├── src/
│   ├── app/
│   │   ├── app.component.html
│   │   ├── app.component.ts
│   │   ├── app.routes.ts
│   │   ├── professor.service.ts
│   │   ├── professor-list/
│   │   │   ├── professor-list.component.html
│   │   │   └── professor-list.component.ts
│   │   ├── professor-detail/
│   │   │   ├── professor-detail.component.html
│   │   │   └── professor-detail.component.ts
│   │   └── professor-form/
│   │       ├── professor-form.component.html
│   │       └── professor-form.component.ts
│   ├── assets/
│   │   └── data/
│   │       └── professors.json
│   ├── index.html
│   ├── main.ts
│   └── styles.css
├── app.py                  # Flask backend application
├── data_analysis.py        # Data analysis script
├── requirements.txt        # Python backend dependencies
├── package.json            # Frontend dependencies
└── README.md

```

## Installation and Running Instructions

### Frontend

1. **Clone the Repository**

    ```
    git clone <repository_url>
    cd professor-dashboard
    ```

2. **Install Frontend Dependencies**

    ```
    git clone <repository_url>
    cd professor-dashboard
    ```

3. **Start the Frontend Development Server**

    ```
    git clone <repository_url>
    cd professor-dashboard
    ```

After starting, open http://localhost:4200 in your browser to view the frontend interface.

### Backend

1. **Create and Activate a Virtual Environment**

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Backend Dependencies**

   ```
   pip install -r requirements.txt
   ```

   Example `requirements.txt` contents:

   ```
   Flask==2.2.2
   flask-cors==3.0.10
   pymongo==4.3.3
   flasgger==0.9.5
   flask-jwt-extended==4.4.4
   ```

3. **Start MongoDB**

   - If using local MongoDB, install and start it via Homebrew:

     ```
     brew tap mongodb/brew
     brew install mongodb-community@5.0
     brew services start mongodb/brew/mongodb-community
     ```

4. **Start the Flask Backend**

   ```
   python app.py
   ```

   The backend will run at http://127.0.0.1:5000.

5. **View API Documentation** Open http://127.0.0.1:5000/apidocs/ in your browser to view the Swagger-generated API documentation.

### Data Analysis

1. **Install Data Analysis Dependencies**

   ```
   pip install pandas matplotlib reportlab
   ```

2. **Run the Data Analysis Script**

   ```
   python data_analysis.py
   ```

   This script will generate chart images and a PDF report (e.g., `Professor_Data_Analysis_Report.pdf`).

## User Authentication

- The backend implements a simple JWT-based user authentication system.

- **Login Endpoint**: `POST /login`
   Request body example:

  ```
  {
    "username": "admin",
    "password": "password"
  }
  ```

- Upon successful login, an `access_token` is returned. For protected endpoints, include the token in the request header:

  ```
  Authorization: Bearer <access_token>
  ```

- Protected endpoints include: `POST /professors`, `PUT /professors/<id>`, and `DELETE /professors/<id>`.

## Git Version Control

1. **Initialize the Repository** If not already initialized, run:

   ```
   git init
   ```

2. **Create a .gitignore File** Create a `.gitignore` file with contents such as:

   ```
   # Python
   __pycache__/
   *.pyc
   venv/
   
   # Node.js
   node_modules/
   
   # Environment files
   .env
   
   # Build artifacts
   dist/
   build/
   
   # Generated PDF reports
   *.pdf
   ```

3. **Common Git Commands** After making changes, run:

   ```
   git add .
   git commit -m "Implemented [feature] - description of changes"
   git push
   ```

   Keep your commit history clear and detailed to document the development process.

## Additional Information

- **Future Improvements**:
  - Add more data analysis charts and a more sophisticated user authentication system.
  - Enhance API security, error handling, and logging.
- **License**: Please specify an open-source license (e.g., MIT, Apache 2.0) here.
- **Contact**: For any questions or suggestions, please contact chenzhu4@illinois.edu.