from argparse import ArgumentParser
import parser
import compiler
import sys

def read_args():
    parser = ArgumentParser()
    parser.add_argument("file", help="Data file to read")

    # Optional arguments
    parser.add_argument("--mode", choices=["dna", "rna"], default="dna", help="Analysis mode (dna/rna)")
    parser.add_argument("--format", choices=["json", "csv", "txt"], default="json", help="Output format (json/csv/txt)")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--gc", action="store_true", help="Calculate and include GC content percentage in the analysis")
    parser.add_argument("--transcribe", action="store_true", help="Transcribe DNA to RNA (replaces T with U) instead of printing the summary")
    
    return parser.parse_args()

def main():
    args = read_args()

    if args.transcribe and args.mode == "rna":
        print("Error: --transcribe requires --mode dna (RNA sequences are already transcribed).", file=sys.stderr)
        sys.exit(1)

    try:
        nucleic_acid_string = parser.read_file(args.file)
    except FileNotFoundError:
        print(f"Error: The file '{args.file}' could not be found.", file=sys.stderr)
        sys.exit(1)

    if args.transcribe:
        transcribed = parser.transcribe(nucleic_acid_string)
        if args.output:
            file_path = args.output + "." + "txt"
            with open(file_path, "w") as fp:
                fp.write(transcribed)
        else:
            print(transcribed)
        return

    nucleotide_counts = parser.count_nucleotides(nucleic_acid_string)
    
    if args.gc:
        nucleotide_counts["GC"] = parser.calculate_gc(nucleotide_counts)

    if args.mode == "dna":
        nucleotide_counts.pop("U", None)
    else:
        nucleotide_counts.pop("T", None)

    dot_count = nucleotide_counts.pop(".", None) or 0
    dash_count = nucleotide_counts.pop("-", None) or 0
    nucleotide_counts["Gap"] = dot_count + dash_count

    if args.output:
        compiler.output(nucleotide_counts, args.format, args.output)
    else:
        TABLE_WIDTH = 38

        print("=" * TABLE_WIDTH)
        print(f"{'Genomic Summary':^38}")
        print("=" * TABLE_WIDTH)

        print(f"Sequence Type: {args.mode.upper():>23}")
        print(f"Bases Count:   {sum(nucleotide_counts.values()):>23}")
        print("=" * TABLE_WIDTH)
        labels = {
            "A": "Adenine", "G": "Guanine", "C": "Cytosine", "T": "Thymine", "U": "Uracil",
            "R": "A or G", "Y": "C or T/U", "S": "G or C", "W": "A or T/U", "K": "G or T/U",
            "M": "A or C", "B": "C or G or T/U", "D": "A or G or T/U", "H": "A or C or T/U",
            "V": "A or C or G", "N": "Any base", "Gap": "Gap"
        }

        total = sum(nucleotide_counts.values())

        for symbol, label in labels.items():
            count = nucleotide_counts.get(symbol, 0)
            percent = (count / total * 100) if total else 0
            
            # Formatting Breakdown:
            # {label:<15}  -> Left-align label in a 15-character column
            # {symbol:^3}   -> Center-align symbol in a 3-character column
            # {count:>5}    -> Right-align count in a 5-character column
            # {percent:>5.1f} -> Right-align percentage with 1 decimal place in a 5-character column
            print(f"{label:<15} ({symbol:^3}): {count:>5}  ({percent:>5.1f}%)")

        if args.gc:
            print("=" * TABLE_WIDTH)
            print(f"GC:\t\t{nucleotide_counts['GC']:>5.2f}%")

if  __name__ == "__main__":
    main()