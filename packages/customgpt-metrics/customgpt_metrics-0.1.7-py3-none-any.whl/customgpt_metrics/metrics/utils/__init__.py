def convert_to_class_name(string):
    words = string.split('_')
    capitalized_words = [word.capitalize() for word in words]
    class_name = ''.join(capitalized_words)
    return class_name