from FourthDimension.docstore.file import File


def process_file(
        file: File,
        loader_class
):
    file.compute_documents(loader_class)
    return file
