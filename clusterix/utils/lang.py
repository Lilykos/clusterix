def strip_accents_from_str(string):
    """
    Strip accents in the input phrase X (assumed in UTF-8) by replacing
    accented characters with their unaccented cousins.

    :param string: The raw input string.
    :type string: str

    :return: The unaccented string.
    :rtype: str
    """
    from unidecode import unidecode
    try:
        import chardet
        CHARDET_AVAILABLE = True
    except ImportError:
        CHARDET_AVAILABLE = False

    def _guess_minimum_encoding(text, charsets=('ascii', 'latin1', 'utf8')):
        """Try to guess the minimum charset that is able to represent the given
        text using the provided charsets. More info:
        https://github.com/inveniosoftware/invenio/blob/legacy/modules/miscutil/lib/textutils.py#L542
        """
        text_in_unicode = text.decode('utf8', 'replace')
        for charset in charsets:
            try:
                return text_in_unicode.encode(charset), charset
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
        return text_in_unicode.encode('utf8'), 'utf8'

    def _decode_to_unicode(text, default_encoding='utf-8'):
        """
        Decode input text into Unicode representation by first using the default
        encoding utf-8. More info:
        https://github.com/inveniosoftware/invenio/blob/legacy/modules/miscutil/lib/textutils.py#L429
        """
        if not text:
            return ""
        try:
            return text.decode(default_encoding)
        except (UnicodeError, LookupError):
            pass
        detected_encoding = None
        if CHARDET_AVAILABLE:
            # We can use chardet to perform detection
            res = chardet.detect(text)
            if res['confidence'] >= 0.8:
                detected_encoding = res['encoding']
        if detected_encoding == None:
            # No chardet detection, try to make a basic guess
            dummy, detected_encoding = _guess_minimum_encoding(text)
        return text.decode(detected_encoding)

    def _translate_to_ascii(values):
        """
        Transliterate the string contents of the given sequence into ascii representation.
        More info:
        https://github.com/inveniosoftware/invenio/blob/legacy/modules/miscutil/lib/textutils.py#L542
        """
        if not values and not type(values) == str:
            return values

        if type(values) == str:
            values = [values]
        for index, value in enumerate(values):
            if not value:
                continue
            unicode_text = _decode_to_unicode(value)
            if u"[?]" in unicode_text:
                decoded_text = []
                for unicode_char in unicode_text:
                    decoded_char = unidecode(unicode_char)
                    # Skip unrecognized characters
                    if decoded_char != "[?]":
                        decoded_text.append(decoded_char)
                ascii_text = ''.join(decoded_text).encode('ascii')
            else:
                ascii_text = unidecode(unicode_text).replace(u"[?]", u"").encode('ascii')
            values[index] = ascii_text
        return values

    try:
        return _translate_to_ascii(string)[0]
    except (TypeError, UnicodeEncodeError):
        return _translate_to_ascii(string.encode('utf-8'))[0]