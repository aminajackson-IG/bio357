from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SeqIO
import json


def run_ncbi_blast_to_json(query, query_type="sequence", database="nr", program="blastn",
                           output_file="blast_results.json"):
    """
    Runs NCBI BLAST with the given query (sequence or accession ID) and parameters,
    then writes the output as a JSON file.

    Args:
        query (str): The query sequence or accession ID.
        query_type (str): Specifies whether the 'query' is a 'sequence' or 'accession'. Defaults to 'sequence'.
        database (str): The NCBI database to search against (default: "nr").
        program (str): The BLAST program to use (default: "blastn").
        output_file (str): The name of the JSON file to write the results to (default: "blast_results.json").
    """
    try:
        if query_type == "sequence":
            print(f"Running NCBI BLAST with sequence: '{query[:20]}...'")
            result_handle = NCBIWWW.qblast(program, database, query)
        elif query_type == "accession":
            print(f"Running NCBI BLAST with accession ID: '{query}'")
            result_handle = NCBIWWW.qblast(program, database, query)
        else:
            raise ValueError("Invalid query_type. Must be 'sequence' or 'accession'.")

        print("BLAST search completed successfully.")

        blast_records = NCBIXML.parse(result_handle)
        results_list = []

        for blast_record in blast_records:
            record_dict = {
                "query": blast_record.query,
                "query_id": blast_record.query_id,
                # "description": blast_record.description,
                "alignments": []
            }
            for alignment in blast_record.alignments:
                alignment_dict = {
                    "title": alignment.title,
                    "hit_id": alignment.hit_id,
                    "hit_def": alignment.hit_def,
                    # "hit_accession": alignment.hit_accession,
                    "length": alignment.length,
                    "hsps": []
                }
                for hsp in alignment.hsps:
                    hsp_dict = {
                        "align_length": hsp.align_length,
                        "bits": hsp.bits,
                        "expect": hsp.expect,
                        "frame": hsp.frame,
                        "gaps": hsp.gaps,
                        "identities": hsp.identities,
                        "positives": hsp.positives,
                        "query": hsp.query,
                        "query_end": hsp.query_end,
                        "query_start": hsp.query_start,
                        "sbjct": hsp.sbjct,
                        "sbjct_end": hsp.sbjct_end,
                        "sbjct_start": hsp.sbjct_start,
                        "score": hsp.score,
                        "strand": hsp.strand
                    }
                    alignment_dict["hsps"].append(hsp_dict)
                record_dict["alignments"].append(alignment_dict)
            results_list.append(record_dict)

        with open(output_file, "w") as f:
            json.dump(results_list, f, indent=4)

        print(f"BLAST results written to: {output_file}")

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    print("Choose the query type:")
    print("1. Enter sequence directly")
    print("2. Provide a FASTA file")
    print("3. Enter an NCBI Accession ID")

    choice = input("Enter your choice (1, 2, or 3): ")

    query_sequence = None

    if choice == "1":
        query_sequence = input("Enter the query sequence: ").strip()
        query_type = "sequence"
    elif choice == "2":
        fasta_file = input("Enter the path to the FASTA file: ").strip()
        try:
            record = next(SeqIO.parse(fasta_file, "fasta"))
            query_sequence = str(record.seq)
            query_type = "sequence"
        except FileNotFoundError:
            print(f"Error: File not found at {fasta_file}")
            exit()
        except Exception as e:
            print(f"Error reading FASTA file: {e}")
            exit()
    elif choice == "3":
        accession_id = input("Enter the NCBI Accession ID: ").strip()
        query_sequence = accession_id
        query_type = "accession"
    else:
        print("Invalid choice.")
        exit()

    if query_sequence:
        # Specify the database and program (optional)
        database_name = "nr"
        blast_program = "blastn"

        # Specify the output JSON file name (optional)
        output_filename = "blast_results.json"

        # Run the BLAST search and save results to JSON
        run_ncbi_blast_to_json(query_sequence, query_type, database_name, blast_program, output_filename)
