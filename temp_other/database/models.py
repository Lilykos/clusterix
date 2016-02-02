from flask.ext.sqlalchemy import SQLAlchemy

"""
The 3 tables used allow for a flexible saving of the data through relationships. An example would be:
    input_item:
         id |           raw_string            |   timestamp
        ----+---------------------------------+---------------
          1 | John,Software Dev.,Paris        | 1456237151829
          2 | Tom,Painter,Chicago             | 1456237151829

    item_metadata_connection:
         input_id | input_item_metadata_id
        ----------+------------------------
                1 |                      1
                1 |                      2
                1 |                      3
                2 |                      4
                2 |                      5
                2 |                      6

    input_item_metadata:
         id | name |         value         | type
        ----+------+-----------------------+------
          1 | Name | John                  | text
          2 | Job  | Software Dev.         | text
          3 | City | Paris                 | text
          4 | Name | Tom                   | text
          5 | Job  | Painter               | text
          6 | City | Chicago               | text
"""
db = SQLAlchemy()
items_to_metadata = db.Table('item_metadata_connection',
                             db.Column('input_id', db.Integer, db.ForeignKey('input_item.id')),
                             db.Column('input_item_metadata_id', db.Integer, db.ForeignKey('input_item_metadata.id'))
                             )


class InputItem(db.Model):
    """The input table, containing the raw input."""
    __tablename__ = 'input_item'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    raw_string = db.Column(db.Text)
    timestamp = db.Column(db.Text)

    # Metadata relationship
    input_item_metadata = db.relationship("InputItemMetadata",
                                          lazy='subquery',
                                          secondary="item_metadata_connection",
                                          cascade="all, delete-orphan",
                                          single_parent=True)


class InputItemMetadata(db.Model):
    """The metadata table, which has a relationship with the main input."""
    __tablename__ = 'input_item_metadata'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text)
    value = db.Column(db.Text)
    type = db.Column(db.Text)
