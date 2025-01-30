import hashlib

def calculate_hash(output_file_path, algoritimo="sha256"):

    h = hashlib.new(algoritimo)

    with open(output_file_path, "rb") as f:
        while chunk := f.read(4096):
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()