from django import template

register = template.Library()

censore = [
    'блять',
    'бля',
    'сука',
    'сейчас',
]

@register.filter()
def censored(text):
    for word in censore:
        text = text.replace(word, word[0] + '*' * (len(word) - 1))
    return text
