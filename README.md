# Intelligent Document Manager

The Intelligent Document Manager is a Flask-based web application that helps users manage their documents efficiently. It offers features such as document uploading, sorting, moving, renaming, deletion, and intelligent tagging using OpenAI's GPT-4 model.

## Features

- **Document Uploading**: Upload files and directories.
- **Document Viewing**: Browse and view documents and directories.
- **Intelligent Tagging**: Automatically tag documents using OpenAI's GPT-4 model.
- **Sorting**: Sort documents by various criteria.
- **Moving and Renaming**: Move and rename documents.
- **Search**: Search documents based on tags and content.
- **Database Management**: Manage the document database, including removing unused records.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip
- Node.js and npm

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/intelligent-document-manager.git
   cd intelligent-document-manager

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required Python packages**

   ```bash
   pip install -r requirements.txt

4. **Set up environment variables**

   Create a .env file in the root directory and add:
   ```bash
   FLASK_APP=app
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=sqlite:///site.db
   OPENAI_API_KEY=your_openai_api_key

5. **Initialize the database**

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade


### Usage

1. **Run the Flask application**
   
   ```bash
   flask run

2. Open your web browser and go to http://127.0.0.1:5000/.



### License
This project is licensed under the MIT License.






   
