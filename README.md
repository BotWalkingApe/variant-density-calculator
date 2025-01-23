# Variant Density Calculator

## Program Description
The **Variant Density Calculator** is a Python program designed to analyze genomic data from GFF and VCF files. It calculates the density of genetic variants within specified genomic features and generates both a filtered VCF file and a YAML report summarizing the results.

## Program Structure
- **`variant_density_calculator.py`**: The main script containing all the logic for parsing, filtering, and generating outputs.

## Features
1. Parses a GFF file to extract genomic features of specified types (e.g., `exons`, `genes`).
2. Parses a VCF file to extract variant information.
3. Identifies variants that overlap with the specified genomic features.
4. Calculates the density of variants per kilobase for each feature.
5. Generates:
   - A filtered VCF file containing only overlapping variants.
   - A YAML report summarizing the results, including:
     - Feature type
     - Total number of features
     - Total number of variants
     - Detailed information for each feature (ID, length, variant count, density).

## Usage
The program is executed via the command line. Below are the required arguments:

```bash
python variant_density_calculator.py -gff <input.gff> -vcf <input.vcf> -var <output.vcf> -rep <output.yaml> -ftr <feature_types>
```

### Arguments:
- `-gff`: Path to the input GFF file.
- `-vcf`: Path to the input VCF file.
- `-var`: Path to the output filtered VCF file.
- `-rep`: Path to the output YAML report file.
- `-ftr`: Comma-separated list of feature types to analyze (e.g., `exon,gene`).

### Example Command:
python variant_density_calculator.py -gff example.gff -vcf example.vcf -var filtered.vcf -rep report.yaml -ftr gene


## Outputs
1. **Filtered VCF File**:
   - Contains only variants that overlap with the specified features.
   - Example:
    #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
      Y	276322	.	G	A	.	.	.
      Y	276323	.	T	C	.	.	.
      Y	276324	.	G	A	.	.	.
      Y	276330	.	G	A,C	.	.	.

2. **YAML Report**:
   - Summarizes feature and variant statistics.
   - Example:
     ```yaml
     DensityReport:
      FilteringReport:
        Feature_Type: gene
        TotalFeatures: 63
        TotalVariants: 512036
        VariantsPerFeature:
        - FeatureID: gene:ENSG00000292344
          Length: 27035
          VariantCount: 15390
          Density: 569.2620676900315
     ```

## Requirements
- Python 3
- Standard Python libraries (`argparse`, `yaml`)