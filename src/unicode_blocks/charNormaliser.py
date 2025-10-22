class CharNormaliser:
    @staticmethod
    def to_codepoint(char: int | str | bytes) -> int:
        """Convert a character to its Unicode code point.
        May be a str, int, or bytes. Bytes are decoded to str using utf-8.
        Returns the Unicode code point as an integer.
        """
        if isinstance(char, int):
            unidec = char
        elif isinstance(char, bytes):
            unidec = ord(char.decode("utf-8")[0])
        elif isinstance(char, str):
            unidec = ord(char[0])
        else:
            raise TypeError(f"Expected str, int, or bytes, got {type(char).__name__}")
        assert 0 <= unidec < 0x110000, "Code point must be in the range [0, 0x10FFFF]"
        return unidec
