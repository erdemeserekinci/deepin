"""Customer names kept confidential for now.

When HIDE is on, a customer name never reaches the page: it is replaced by a
blurred placeholder of neutral text (the real name is not in the HTML, so it
cannot be read from the source or indexed). Switch off with
"proof": {"hide_names": false} in src/data.<lang>.json.
"""
import html

HIDE = True
LABEL = {"tr": "Gizli referans", "en": "Confidential reference"}
_SHAPES = ["Xxxxx Xxxxxx", "Xxxxxxx", "Xxxxx", "Xxxxxx Xxxxx Xxx", "Xxxxxxxxx", "Xxxx Xxxxxxx"]
_lang = "tr"
_n = 0


def set_lang(lang):
    global _lang, _n
    _lang, _n = lang, 0


def name(real, tag="span"):
    """The customer name, or a blurred stand-in when names are hidden."""
    global _n
    if not HIDE:
        return f"<{tag}>{html.escape(real, quote=True)}</{tag}>" if tag != "span" else html.escape(real, quote=True)
    shape = _SHAPES[_n % len(_SHAPES)]
    _n += 1
    return (f'<{tag} class="redact" role="img" aria-label="{LABEL[_lang]}" title="{LABEL[_lang]}">'
            f'<span aria-hidden="true">{shape}</span></{tag}>')
