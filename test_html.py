class HTML:
    def __init__(self, output=None):
        self.output = output 
        self.children = []

    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None: 
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)

    def __str__(self): 
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "</html>"
        return html

class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __iadd__(self, other): 
        self.children.append(other)
        return self

    def __enter__(self):  
        return self

    def __exit__(self, *args, **kwargs): 
        pass

    def __str__(self): 
        html = "<%s>\n" % self.tag
        for child in self.children:
            html += str(child)
        html += "</%s>\n" % self.tag
        return html

class Tag:
    def __init__(self, tag, klass=None, is_single=False, **attrs):
        self.tag = tag
        self.is_single = is_single
        self.text = ""
        self.attributes = attrs
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)
    
    def __enter__(self):  
        return self

    def __exit__(self, *args, **kwargs): 
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.is_single:
            return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
        
        if self.children:
            text = "<{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
            for child in self.children:
                text += str(child)
            text += "\n</{tag}>\n".format(tag=self.tag)
            return text
                   
        else: 
            return "<{tag} {attrs}>{text}</{tag}>\n".format(
                tag=self.tag, attrs=attrs, text=self.text
            )
            
def main(output=None):
    with HTML(output) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body


if __name__ == "__main__":
    main("test.html")


