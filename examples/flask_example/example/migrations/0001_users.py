from flask.ext.evolution import BaseMigration

from example.models.user import User


class Migration(BaseMigration):
    def up(self):
        User.__table__.create()

    def down(self):
        User.__table__.drop()
