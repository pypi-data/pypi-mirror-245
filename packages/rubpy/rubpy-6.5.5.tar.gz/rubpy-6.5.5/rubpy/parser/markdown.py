def Bold(text: str) -> str:
    return f'**{text}**'

def Italic(text: str) -> str:
    return f'__{text}__'

def Underline(text: str) -> str:
    return f'--{text}--'

def Strike(text: str) -> str:
    return f'~~{text}~~'

def Spoiler(text: str) -> str:
    return f'||{text}||'

def Code(text: str):
    return f'`{text.strip()}`'

def Mention(text: str, object_guid: str) -> str:
    return f'[{text.strip()}]({object_guid})'

def HyperLink(text: str, link: str) -> str:
    return f'[{text.strip()}]({link})'