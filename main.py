def main(fileName):
    # Read file
    with open(fileName, "r") as f:
        dna_string: str = f.read()

    # Parse and Count
    count_file(dna_string)

def count_file(dna_string: str):
    nucleotide_counts = {
        "A": 0,
        "G": 0,
        "C": 0,
        "T": 0,
    }

    for c in dna_string.upper():
        if c in nucleotide_counts:
            nucleotide_counts[c] += 1

    print(nucleotide_counts)

if __name__ == "__main__":
    main("data/example_string.txt")