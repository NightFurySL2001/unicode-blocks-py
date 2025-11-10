from .unicodeBlock import UnicodeBlock
from .charNormaliser import CharNormaliser
from .blocks import ALL_BLOCKS, NO_BLOCK
from .errors import InvalidUnicodeBlockNameError


def all() -> list[UnicodeBlock]:
    """
    Get all Unicode blocks.
    """
    return ALL_BLOCKS


def for_name(name: str) -> UnicodeBlock:
    """
    Get the Unicode block for a given name.
    """
    blocks = all()
    for block in blocks:
        if block.normalised_name == UnicodeBlock.normalise_name(name):
            return block
        if UnicodeBlock.normalise_name(name) in block.aliases:
            return block
    raise InvalidUnicodeBlockNameError(name)


def of(char: str | int | bytes) -> UnicodeBlock:
    """
    Get the name of the Unicode block for a given character.
    May be a str, int, or bytes. Bytes are decoded to str using utf-8.
    """
    unidec = CharNormaliser.to_codepoint(char)
    blocks = all()
    low, high = 0, len(blocks) - 1
    while low <= high:
        mid = (low + high) // 2
        block = blocks[mid]
        if unidec in block:
            return block
        elif unidec < block.start:
            high = mid - 1
        else:
            low = mid + 1
    return NO_BLOCK
