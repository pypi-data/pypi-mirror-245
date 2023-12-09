def is_image(filename:str):
    img_extensions = ["jpg", "jpeg", "png", "webp"]
    extension = filename.split(".")[-1]
    return extension in img_extensions
