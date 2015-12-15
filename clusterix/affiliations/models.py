from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Affiliation(db.Model):
    """ The db model for affiliations."""
    __tablename__ = 'affiliations'

    # Autoincrement ids
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # Country/ Region related
    country = db.Column(db.Text)
    country_code = db.Column(db.Text)
    post_box = db.Column(db.Text)
    post_code = db.Column(db.Text)
    region = db.Column(db.Text)
    settlement = db.Column(db.Text)

    # Institution related
    institution = db.Column(db.Text)
    department = db.Column(db.Text)
    laboratory = db.Column(db.Text)

    # General info
    raw_string = db.Column(db.Text, index=True)
    raw_string_unicode = db.Column(db.Text, index=True)
    grobid_xml = db.Column(db.Text)
    language = db.Column(db.Text)

    def __init__(self, country, country_code, post_box, post_code, region, settlement,
                 institution, department, laboratory,
                 raw_string, raw_string_unicode, grobid_xml, language):
        self.country = country
        self.country_code = country_code
        self.post_box = post_box
        self.post_code = post_code
        self.region = region
        self.settlement = settlement
        self.institution = institution
        self.department = department
        self.laboratory = laboratory
        self.raw_string = raw_string
        self.raw_string_unicode = raw_string_unicode
        self.grobid_xml = grobid_xml
        self.language = language

    # def __repr__(self):
    #     return (
    #         """
    #         raw string - {}
    #         country - {}
    #         affiliation - {} {} {}
    #         """.format(self.raw_string, self.country,
    #                    self.institution, self.department, self.laboratory,)
    #     )


class BrokenAffiliation(db.Model):
    """ The db model for affiliations that could not be parsed correctly."""
    __tablename__ = 'broken_affiliations'

    # Autoincrement ids
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # General info
    raw_string = db.Column(db.Text)
    raw_string_unicode = db.Column(db.Text)
    grobid_xml = db.Column(db.Text)

    def __init__(self, raw_string, raw_string_unicode, grobid_xml):
        self.raw_string = raw_string
        self.raw_string_unicode = raw_string_unicode
        self.grobid_xml = grobid_xml

    # def __repr__(self):
    #     return (
    #         """
    #         raw string: {}
    #         GROBID: {}
    #         """.format(self.raw_string, self.grobid_xml)
    #     )