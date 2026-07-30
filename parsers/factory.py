from parsers.generic import GenericParser
from parsers.rss import RSSParser


class ParserFactory:

    @staticmethod
    def get_parser(parser_type, keywords):

        parser_type = parser_type.lower()

        if parser_type == "generic":
            return GenericParser(keywords)

        elif parser_type == "rss":
            return RSSParser(keywords)

        raise ValueError(f"Unsupported parser type: {parser_type}")