import json

def output(nucleotide_count: dict[str, int], format: str, file_location):
    file = build_file(format, nucleotide_count)
    file_path = file_location + "." + format

    with open(file_path, 'w') as fp:
        fp.write(file)

def build_file(format, nucleotide_count):
    match format:
        case "json":
            return json_output(nucleotide_count)
        case "csv":
            return csv_output(nucleotide_count)
        case "txt":
            return txt_output(nucleotide_count)
        
def json_output(nucleotide_count):
    return json.dumps(nucleotide_count, indent=4)

def csv_output(nucleotide_count):
    return ""

def txt_output(nucleotide_count):
    return ""