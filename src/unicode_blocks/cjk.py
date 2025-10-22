from .unicodeBlock import UnicodeBlock
from .charNormaliser import CharNormaliser
from .blocks import IDEO_BLOCKS, JPAN_BLOCKS, KORE_BLOCKS, PUNC_BLOCKS

CJK_BLOCKS = IDEO_BLOCKS + JPAN_BLOCKS + KORE_BLOCKS + PUNC_BLOCKS

### Individual character checks ###


def is_in_blocks(char: str | int | bytes, blocks: list[UnicodeBlock]) -> bool:
    unidec = CharNormaliser.to_codepoint(char)
    return any(unidec in block for block in blocks)


def is_ideographic_zero(char: str | int | bytes) -> bool:
    """Check if a character is ideographic zero (U+3007).
    May be a str, int, or bytes. Bytes are decoded to str using utf-8.
    """
    return CharNormaliser.to_codepoint(char) == 0x3007


def is_ideographic(char: str | int | bytes) -> bool:
    """Check if a character is ideographic (hanzi/kanji/hanja/漢字/汉字).
    May be a str, int, or bytes. Bytes are decoded to str using utf-8.
    """
    return is_ideographic_zero(char) or is_in_blocks(char, IDEO_BLOCKS)


def is_japanese_kana(char: str | int | bytes) -> bool:
    """Check if a character is Japanese kana (ひらがな/カタカナ).
    May be a str, int, or bytes. Bytes are decoded to str using utf-8.
    """
    return is_in_blocks(char, JPAN_BLOCKS)


def is_japanese(char: str | int | bytes) -> bool:
    """Check if a character is Japanese (kanji + kana).
    May be a str, int, or bytes. Bytes are decoded to str using utf-8.
    """
    return is_japanese_kana(char) or is_ideographic(char)


def is_korean_hangul(char: str | int | bytes) -> bool:
    """Check if a character is Korean hangul (한글).
    May be a str, int, or bytes. Bytes are decoded to str using utf-8.
    """
    return is_in_blocks(char, KORE_BLOCKS)


def is_korean(char: str | int | bytes) -> bool:
    """Check if a character is Korean (hanja + hangul).
    May be a str, int, or bytes. Bytes are decoded to str using utf-8.
    """
    return is_korean_hangul(char) or is_ideographic(char)


def is_cjk_punctuation(char: str | int | bytes) -> bool:
    """Check if a character is CJK symbol or punctuation.
    May be a str, int, or bytes. Bytes are decoded to str using utf-8.
    """
    return is_in_blocks(char, PUNC_BLOCKS)


def is_cjk(char: str | int | bytes) -> bool:
    """Determine if a character is used in CJK (Chinese, Japanese, Korean) languages.
    May be a str, int, or bytes. Bytes are decoded to str using utf-8.
    """
    return is_ideographic_zero(char) or is_in_blocks(char, CJK_BLOCKS)


### Block checks ###


def is_ideographic_block(block: UnicodeBlock) -> bool:
    """Check if a block is used in ideographic (hanzi/kanji/hanja/漢字/汉字)."""
    return block in IDEO_BLOCKS


def is_japanese_kana_block(block: UnicodeBlock) -> bool:
    """Check if a block is used in Japanese kana (ひらがな/カタカナ)."""
    return block in JPAN_BLOCKS


def is_japanese_block(block: UnicodeBlock) -> bool:
    """Check if a block is used in Japanese (kanji + kana)."""
    return is_japanese_kana_block(block) or is_ideographic_block(block)


def is_korean_hangul_block(block: UnicodeBlock) -> bool:
    """Check if a block is used in Korean hangul (한글)."""
    return block in KORE_BLOCKS


def is_korean_block(block: UnicodeBlock) -> bool:
    """Check if a block is used in Korean (hanja + hangul)."""
    return is_korean_hangul_block(block) or is_ideographic_block(block)


def is_cjk_punctuation_block(block: UnicodeBlock) -> bool:
    """Check if a block is used in CJK symbol or punctuation."""
    return block in PUNC_BLOCKS


def is_cjk_block(block: UnicodeBlock) -> bool:
    """Determine if a block is used in used in CJK (Chinese, Japanese, Korean) languages."""
    return (
        is_ideographic_block(block)
        or is_japanese_block(block)
        or is_korean_block(block)
        or is_cjk_punctuation_block(block)
    )


### Block accessors ###


def get_ideographic_blocks() -> list[UnicodeBlock]:
    """Get all Unicode blocks used in ideographic (hanzi/kanji/hanja/漢字/汉字)."""
    return IDEO_BLOCKS


def get_japanese_kana_blocks() -> list[UnicodeBlock]:
    """Get all Unicode blocks used in Japanese kana (ひらがな/カタカナ)."""
    return JPAN_BLOCKS


def get_japanese_blocks() -> list[UnicodeBlock]:
    """Get all Unicode blocks used in Japanese (kanji + kana)."""
    return JPAN_BLOCKS + IDEO_BLOCKS


def get_korean_hangul_blocks() -> list[UnicodeBlock]:
    """Get all Unicode blocks used in Korean hangul (한글)."""
    return KORE_BLOCKS


def get_korean_blocks() -> list[UnicodeBlock]:
    """Get all Unicode blocks used in Korean (hanja + hangul)."""
    return KORE_BLOCKS + IDEO_BLOCKS


def get_cjk_punctuation_blocks() -> list[UnicodeBlock]:
    """Get all Unicode blocks used in CJK symbol or punctuation."""
    return PUNC_BLOCKS


def get_cjk_blocks() -> list[UnicodeBlock]:
    """Get all Unicode blocks used in used in CJK (Chinese, Japanese, Korean) languages."""
    return CJK_BLOCKS
