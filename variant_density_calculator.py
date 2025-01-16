import argparse

# Classes


# Functions

def main():
    parser = argparse.ArgumentParser(description="Variant Density Calculator")
    parser.add_argument("-gff", required=True, help="Input GFF file")
    parser.add_argument("-vcf", required=True, help="Input VCF file")
    parser.add_argument("-var", required=True, help="Output filtered VCF file")
    parser.add_argument("-rep", required=True, help="Output TSV report file")
    parser.add_argument("-ftr", required=True, help="Feature types to analyze (comma-separated)")

    args = parser.parse_args()




if __name__ == "__main__":
    main()
