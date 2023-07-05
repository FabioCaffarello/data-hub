import inflection

def to_camel_case(raw_text):
    return inflection.camelize(raw_text, False)
