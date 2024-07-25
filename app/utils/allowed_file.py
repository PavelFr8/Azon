def allowed_file(filename):
    """
    Check that fileformat is correct
    :param filename:
    :return: bool
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp'}