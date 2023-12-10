from html.parser import HTMLParser

class HTMLToMarkdownParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.in_code_block = False

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.result.append('\n\n')
        elif tag == 'br':
            self.result.append('\n')
        elif tag == 'code':
            self.in_code_block = True
            self.result.append("`")
        elif tag == 'pre':
            self.in_code_block = True
            self.result.append("```\n")
        elif tag == 'strong' or tag == 'b':
            self.result.append('**')
        elif tag == 'em' or tag == 'i':
            self.result.append('__')
        elif tag == 'u':
            self.result.append('--')
        elif tag == 'del':
            self.result.append('~~')
        elif tag == 'span':
            if any(attr[0] == 'style' and 'text-decoration: underline' in attr[1] for attr in attrs):
                self.result.append('__')

    def handle_endtag(self, tag):
        if tag == 'li':
            self.result.append('\n')
        elif tag == 'ul':
            self.result.append('\n\n')
        elif tag == 'code':
            self.in_code_block = False
            self.result.append("`")
        elif tag == 'pre':
            self.in_code_block = False
            self.result.append("```\n")
        elif tag == 'strong' or tag == 'b':
            self.result.append('**')
        elif tag == 'em' or tag == 'i':
            self.result.append('__')
        elif tag == 'u':
            self.result.append('--')
        elif tag == 'del':
            self.result.append('~~')
        elif tag == 'span':
            self.result.append('__')

    def handle_data(self, data):
        if self.in_code_block:
            self.result.append(data)
        else:
            self.result.append(data.replace('\n', ' '))

def html_to_markdown(html_content: str):
    parser = HTMLToMarkdownParser()
    parser.feed(html_content)
    return ''.join(parser.result)