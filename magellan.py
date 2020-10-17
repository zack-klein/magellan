from magellan import create_app
from magellan.app.database import db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
