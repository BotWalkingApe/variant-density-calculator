import argparse, yaml  # Importa os módulos necessários: argparse para lidar com argumentos da linha de comando e yaml para manipular arquivos YAML.

class Feature:  # Define uma classe para representar uma região de interesse (feature) no genoma.
    def __init__(self, feature_id, start, end):  # Inicializa um objeto Feature com ID, posição inicial e posição final.
        self.feature_id = feature_id  # Identificador único da feature.
        self.start = start  # Posição inicial da feature.
        self.end = end  # Posição final da feature.
        self.length = end - start + 1  # Calcula o comprimento da feature (número de bases).
        self.variants = []  # Inicializa uma lista para armazenar variantes associadas a esta feature.

    def add_variant(self, variant_pos):  # Método para adicionar a posição de uma variante à lista de variantes da feature.
        self.variants.append(variant_pos)

    def calculate_density(self):  # Método para calcular a densidade de variantes por kilobase.
        return len(self.variants) / (self.length / 1000)

class Variant:  # Define uma classe para representar uma variante genética.
    def __init__(self, chrom, pos, ref, alt):  # Inicializa um objeto Variant com cromossomo, posição, alelo de referência e alelo alternativo.
        self.chrom = chrom  # Cromossomo onde a variante está localizada.
        self.pos = pos  # Posição da variante no cromossomo.
        self.ref = ref  # Alelo de referência.
        self.alt = alt  # Alelo alternativo.

def parse_gff(file_path, feature_types):  # Função para analisar um arquivo GFF e extrair features com base em seus tipos.
    features = []  # Lista para armazenar as features extraídas.
    with open(file_path, 'r') as file:  # Abre o arquivo GFF para leitura.
        for line in file:  # Lê o arquivo linha por linha.
            if line.startswith("#"):  # Ignora linhas de comentário.
                continue
            columns = line.strip().split('\t')  # Divide a linha em colunas separadas por tabulação.
            if columns[2] in feature_types:  # Verifica se o tipo da feature está na lista de tipos desejados.
                attributes = columns[8]  # Obtém os atributos da feature (última coluna).
                feature_id = attributes.split(";")[0].split("=")[1]  # Extrai o ID da feature dos atributos.
                features.append(Feature(feature_id, int(columns[3]), int(columns[4])))  # Cria um objeto Feature e adiciona à lista.
    return features  # Retorna a lista de features.

def parse_vcf(file_path):  # Função para analisar um arquivo VCF e extrair variantes.
    variants = []  # Lista para armazenar as variantes extraídas.
    with open(file_path, 'r') as file:  # Abre o arquivo VCF para leitura.
        for line in file:  # Lê o arquivo linha por linha.
            if line.startswith("#"):  # Ignora linhas de cabeçalho.
                continue
            columns = line.strip().split('\t')  # Divide a linha em colunas separadas por tabulação.
            chrom = columns[0]  # Obtém o cromossomo da variante.
            pos = int(columns[1])  # Obtém a posição da variante no cromossomo.
            ref = columns[3]  # Obtém o alelo de referência.
            alt = columns[4]  # Obtém o alelo alternativo.
            variants.append(Variant(chrom, pos, ref, alt))  # Cria um objeto Variant e adiciona à lista.
    return variants  # Retorna a lista de variantes.

def filter_variants(features, variants):  # Função para filtrar variantes que estão dentro das regiões definidas pelas features.
    filtered_variants = []  # Lista para armazenar variantes filtradas.
    for variant in variants:  # Itera sobre todas as variantes.
        for feature in features:  # Itera sobre todas as features.
            if feature.start <= variant.pos <= feature.end:  # Verifica se a posição da variante está dentro da região da feature.
                feature.add_variant(variant.pos)  # Adiciona a posição da variante à lista de variantes da feature.
                filtered_variants.append(variant)  # Adiciona a variante à lista de variantes filtradas.
    return filtered_variants  # Retorna a lista de variantes filtradas.

def write_filtered_vcf(output_file, variants):  # Função para escrever as variantes filtradas em um arquivo VCF.
    with open(output_file, 'w') as file:  # Abre o arquivo de saída para escrita.
        file.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")  # Escreve o cabeçalho do VCF.
        for variant in variants:  # Itera sobre as variantes filtradas.
            file.write(f"{variant.chrom}\t{variant.pos}\t.\t{variant.ref}\t{variant.alt}\t.\t.\t.\n")  # Escreve cada variante no arquivo.

def write_yaml_report(output_file, features, feature_type):  # Função para gerar um relatório YAML com informações sobre features e variantes.
    total_features = len(features)  # Conta o número total de features.
    total_variants = sum(len(feature.variants) for feature in features)  # Conta o número total de variantes associadas às features.
    variants_per_feature = [  # Cria uma lista com informações detalhadas sobre cada feature.
        {
            "FeatureID": feature.feature_id,  # ID da feature.
            "Length": feature.length,  # Comprimento da feature.
            "VariantCount": len(feature.variants),  # Número de variantes associadas.
            "Density": feature.calculate_density()  # Densidade de variantes por kilobase.
        }
        for feature in features
    ]

    report = {  # Estrutura o dicionário do relatório.
        "DensityReport": {
            "FilteringReport": {
                "Feature_Type": feature_type,  # Tipo(s) de feature analisado(s).
                "TotalFeatures": total_features,  # Número total de features.
                "TotalVariants": total_variants,  # Número total de variantes.
                "VariantsPerFeature": variants_per_feature  # Lista de informações detalhadas das features.
            }
        }
    }

    with open(output_file, 'w') as file:  # Abre o arquivo YAML para escrita.
        yaml.dump(report, file, sort_keys=False)  # Escreve o relatório no arquivo em formato YAML.

def main():  # Função principal que coordena a execução do programa.
    parser = argparse.ArgumentParser(description="Variant Density Calculator")  # Define o parser para os argumentos da linha de comando.
    parser.add_argument("-gff", required=True, help="Input GFF file")  # Argumento para o arquivo GFF de entrada.
    parser.add_argument("-vcf", required=True, help="Input VCF file")  # Argumento para o arquivo VCF de entrada.
    parser.add_argument("-var", required=True, help="Output filtered VCF file")  # Argumento para o arquivo VCF filtrado de saída.
    parser.add_argument("-rep", required=True, help="Output report YAML file")  # Argumento para o arquivo de relatório YAML de saída.
    parser.add_argument("-ftr", required=True, help="Feature types to analyze (comma-separated)")  # Argumento para os tipos de features.
    args = parser.parse_args()  # Analisa os argumentos da linha de comando.

    feature_types = args.ftr.split(",")  # Divide os tipos de features em uma lista.
    features = parse_gff(args.gff, feature_types)  # Analisa o arquivo GFF para obter as features.
    variants = parse_vcf(args.vcf)  # Analisa o arquivo VCF para obter as variantes.
    filtered_variants = filter_variants(features, variants)  # Filtra as variantes que estão dentro das features.

    write_filtered_vcf(args.var, filtered_variants)  # Escreve as variantes filtradas no arquivo de saída VCF.
    write_yaml_report(args.rep, features, ", ".join(feature_types))  # Gera o relatório YAML com as informações das features e variantes.

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente.
    main()  # Executa a função principal.