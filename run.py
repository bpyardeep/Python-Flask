from project import app
from project.models import db

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()
