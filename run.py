# from app.routes import create_app
# from app.models import db
#
# if __name__ == "__main__":
#     app = create_app()
#     with app.app_context():
#         db.init_app(app)
#         db.create_all()
#         app.run()

from app.models import db
from app.routes import create_app

app = create_app()

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    app.run()
