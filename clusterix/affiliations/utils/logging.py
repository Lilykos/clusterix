from pprint import PrettyPrinter
from lxml import etree


class MyPrettyPrinter(PrettyPrinter):
    def format(self, obj, context, max_levels, level):
        if isinstance(obj, unicode):
            return obj.encode('utf8'), True, False

        return PrettyPrinter.format(self, object, context, max_levels, level)

pp = MyPrettyPrinter(indent=8)


def get_printer():
    return pp \
        if pp is not None \
        else MyPrettyPrinter(indent=8)


def log_txt(title, text):
    get_printer().pprint('***** {}:'.format(title))
    get_printer().pprint(text)


def log_xml(title, xml_str):
    grobid = etree.fromstring(xml_str)

    get_printer().pprint('----- {}:'.format(title))
    get_printer().pprint(etree.tostring(grobid, pretty_print=True))


def log_dict(title, dictionary):
    get_printer().pprint('----- {}:'.format(title))
    get_printer().pprint(dictionary)