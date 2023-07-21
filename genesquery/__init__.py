import requests
import sys
import click
import pandas as pd






@click.command()# is used to define the command line
@click.argument("genes", nargs=-1, required=True)# Is used to specify the command line argument for the command defined by the function , 
# the nargs = 1  is allowing the the argument genes to accept multiple genes
def main(genes):# we insert the genes as an  argument which will help pass the gene names to be able to give us the elements in t
    """
    Process and lookup information for the given list of genes.

    Arguments:
        genes: One or more gene names to lookup.
    """
    # Process the genes as per your requirements
    for gene in genes:
        results = lookup(gene)
        if not results.ok:
            results.raise_for_status()
            sys.exit()
        decoded = results.json()
        extracted_ids = extract_ids(decoded)

        keys = {
            'hgnc_id': 'HGNC',
            'ena': 'ENA',
            'entrez_id': 'Entrez_id',
            'mgd_id': 'MGD',
            'refseq_accession': 'RefSeq',
            'vega_id': 'Vega',
            'ensembl_gene_id': 'Ensembl',
            'ccds_id': 'CCDS',
            'omim_id': 'OMIM',
            'uniprot_ids': 'UniProt',
            'ucsc_id': 'UCSC',
            'rgd_id': 'RGD',
            'agr': 'AGR',
            'mane_select': 'MANE'
        }

        rows = []
        for key, value in extracted_ids.items():
            if isinstance(value, list):
                for element in value:
                    rows.append([key, element])
            else:
                rows.append([key, value])

        df = pd.DataFrame(rows, columns=["Genes", "Identifier"])
        df["Gene_id"] = df["Genes"].replace(keys)

        filename = f"geneticsds_{gene}.csv"
        df.to_csv(filename, index=False)
        print("Data saved:", filename)


def lookup(genes):
    server = "https://rest.genenames.org/"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    ext = f"/fetch/symbol/{genes}"
    http = server + ext

    r = requests.get(http, headers=headers)
    return r


def extract_ids(response):
    response = response["response"]
    docs = response["docs"]
    gene_info = docs[0]
    keys = [
        'hgnc_id', 'ena', 'entrez_id', 'mgd_id', 'refseq_accession',
        'vega_id', 'ensembl_gene_id', 'ccds_id', 'omim_id',
        'uniprot_ids', 'ucsc_id', 'rgd_id', 'agr', 'mane_select'
    ]
    ids = {}

    for key in keys:
        if key in gene_info:
            ids[key] = gene_info[key]
        else:
            ids[key] = None

    return ids


if __name__ == "__main__":
    main()  #here we calling the main function with an empty parentheses becasue it will execute the genes and identifiers because we are not reffering to a particular genes buy multiple genes

