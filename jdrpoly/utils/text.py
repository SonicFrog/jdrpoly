import re

link_regex = re.compile("\[url=(.+)\].+\[/url\]", re.IGNORECASE)
img_regex = re.compile("\[img=(.+)\]", re.IGNORECASE)


def render_to_html(self, text):
    intermediate = link_regex.sub('<a href="\1">\2</a>', text)
    intermediate = img_regex.sub('<img src="\1" alt="" />', intermediate)
    return intermediate
