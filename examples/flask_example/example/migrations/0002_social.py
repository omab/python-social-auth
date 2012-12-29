from flask.ext.evolution import BaseMigration

from example import social_storage


class Migration(BaseMigration):
    def up(self):
        social_storage.user.__table__.create()
        social_storage.nonce.__table__.create()
        social_storage.association.__table__.create()

    def down(self):
        social_storage.user.__table__.drop()
        social_storage.nonce.__table__.drop()
        social_storage.association.__table__.drop()
