import argparse, yaml

class Feature:
    def __init__(self, feature_id, start, end):
        self.feature_id = feature_id
        self.start = start
        self.end = end
        self.length = end - start + 1
        self.variants = []

    def add_variant(self, variant_pos):
        self.variants.append(variant_pos)

    def calculate_density(self):
        return len(self.variants) / (self.length / 1000)

class Variant:
    def __init__(self, chrom, pos, ref, alt):
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt

def parse_gff(file_path, feature_types):
    features = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            columns = line.strip().split('\t')
            if columns[2] in feature_types:
                attributes = columns[8]
                feature_id = attributes.split(";")[0].split("=")[1]
                features.append(Feature(feature_id, int(columns[3]), int(columns[4])))
    return features

def parse_vcf(file_path):
    variants = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            columns = line.strip().split('\t')
            chrom = columns[0]
            pos = int(columns[1])
            ref = columns[3]
            alt = columns[4]
            variants.append(Variant(chrom, pos, ref, alt))
    return variants

def filter_variants(features, variants):
    filtered_variants = []
    for variant in variants:
        for feature in features:
            if feature.start <= variant.pos <= feature.end:
                feature.add_variant(variant.pos)
                filtered_variants.append(variant)
    return filtered_variants

def write_filtered_vcf(output_file, variants):
    with open(output_file, 'w') as file:
        file.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
        for variant in variants:
            file.write(f"{variant.chrom}\t{variant.pos}\t.\t{variant.ref}\t{variant.alt}\t.\t.\t.\n")

def write_yaml_report(output_file, features, feature_type):
    total_features = len(features)
    total_variants = sum(len(feature.variants) for feature in features)

    variants_per_feature = []
    for feature in features:
        variants_per_feature.append({
            "FeatureID": feature.feature_id,
            "Length": feature.length,
            "VariantCount": len(feature.variants),
            "Density": feature.calculate_density()
        })

    report = {
        "DensityReport": {
            "FilteringReport": {
                "Feature_Type": feature_type,
                "TotalFeatures": total_features,
                "TotalVariants": total_variants,
                "VariantsPerFeature": variants_per_feature
            }
        }
    }

    with open(output_file, 'w') as file:
        yaml.dump(report, file, sort_keys=False)

def main():
    parser = argparse.ArgumentParser(description="Variant Density Calculator")
    parser.add_argument("-gff", required=True, help="Input GFF file")
    parser.add_argument("-vcf", required=True, help="Input VCF file")
    parser.add_argument("-var", required=True, help="Output filtered VCF file")
    parser.add_argument("-rep", required=True, help="Output report YAML file")
    parser.add_argument("-ftr", required=True, help="Feature types to analyze (comma-separated)")
    args = parser.parse_args()

    feature_types = args.ftr.split(",")
    features = parse_gff(args.gff, feature_types)
    variants = parse_vcf(args.vcf)
    filtered_variants = filter_variants(features, variants)

    write_filtered_vcf(args.var, filtered_variants)
    write_yaml_report(args.rep, features, ", ".join(feature_types))

if __name__ == "__main__":
    main()
