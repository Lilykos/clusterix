from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
items_to_metadata = db.Table('item_metadata_connection',
                             db.Column('input_id', db.Integer, db.ForeignKey('input_item.id')),
                             db.Column('input_item_metadata_id', db.Integer, db.ForeignKey('input_item_metadata.id'))
                             )


class InputItem(db.Model):
    __tablename__ = 'input_item'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    raw_string = db.Column(db.Text, index=True)
    timestamp = db.Column(db.Text)
    # raw_string_unicode = db.Column(db.Text)
    # grobid_xml = db.Column(db.Text)
    # language = db.Column(db.Text)

    # Metadata relationship
    input_item_metadata = db.relationship("InputItemMetadata",
                                          secondary="item_metadata_connection",
                                          cascade="all, delete-orphan",
                                          single_parent=True)


class InputItemMetadata(db.Model):
    __tablename__ = 'input_item_metadata'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text)
    value = db.Column(db.Text)
    type = db.Column(db.Text)
