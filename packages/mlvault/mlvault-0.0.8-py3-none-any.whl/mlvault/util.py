def is_image(filename:str):
    img_extensions = ["jpg", "jpeg", "png", "webp"]
    extension = filename.split(".")[-1]
    return extension in img_extensions

def find_args(args:list[str], arg:str):
    try:
        index = args.index(arg)
        return args[index + 1]
    except ValueError:
        return None
