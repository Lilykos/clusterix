from clusterix.affiliations.models import Affiliation


# noinspection PyClassHasNoInit
class AffiliationProperties():

    @staticmethod
    def get_country_code(affiliations):
        return [i.country_code for i in affiliations]

    @staticmethod
    def get_region(affiliations):
        return [i.region for i in affiliations]

    @staticmethod
    def get_settlement(affiliations):
        return [i.settlement for i in affiliations]

    @staticmethod
    def get_institution(affiliations):
        return [i.institution for i in affiliations]

    @staticmethod
    def get_department(affiliations):
        return [i.department for i in affiliations]

    @staticmethod
    def get_laboratory(affiliations):
        return [i.laboratory for i in affiliations]

    @staticmethod
    def get_all_affiliations():
        return Affiliation.query.all()