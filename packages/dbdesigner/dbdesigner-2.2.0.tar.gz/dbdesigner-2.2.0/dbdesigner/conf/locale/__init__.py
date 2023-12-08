"""
LANG_INFO is a dictionary structure to provide meta information about languages.

About name_local: capitalize it as if your language name was appearing
inside a sentence in your language.
The 'fallback' key can be used to specify a special fallback logic which doesn't
follow the traditional 'fr-ca' -> 'fr' fallback logic.
"""

LANG_INFO = {
    'en': {
        'bidi': False,
        'code': 'en',
        'name': 'English',
        'name_local': 'English',
    },
    'zh-hans': {
        'bidi': False,
        'code': 'zh-hans',
        'name': 'Simplified Chinese',
        'name_local': '简体中文',
    }
}
