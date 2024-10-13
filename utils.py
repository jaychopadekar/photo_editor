def validate_file_format(filename):
    allowed_extensions = ['jpg', 'jpeg', 'png']
    extension = filename.split('.')[-1].lower()
    return extension in allowed_extensions
