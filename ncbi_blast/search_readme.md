# NCBI BLAST to JSON Script

This Python script allows you to run NCBI BLAST searches directly from the command line and save the results in a structured JSON format. It leverages the Biopython library to interact with NCBI's BLAST server and parse the XML output.

## Features

* **Flexible Query Input:** Supports three ways to provide the query:
    * Directly entering a sequence.
    * Providing a path to a FASTA file.
    * Entering an NCBI Accession ID.
* **Configurable BLAST Parameters:** Allows you to specify the database (`-db`) and program (`-program`) for the BLAST search. Defaults to `nr` (non-redundant protein database) and `blastn` (nucleotide BLAST), respectively.
* **Structured JSON Output:** Saves the BLAST results in a human-readable and easily parsable JSON format, including details about the query, alignments, and high-scoring segment pairs (HSPs).
* **Error Handling:** Includes basic error handling for network issues, invalid query types, and file-related errors.

## Prerequisites

* **Python 3.x** installed on your system.
* **Biopython library** installed. You can install it using pip:
    ```bash
    pip install biopython
    ```
* **Internet Connection:** The script requires an active internet connection to communicate with the NCBI BLAST server.

## Usage

1.  **Save the script:** Save the Python code (provided earlier) as a `.py` file (e.g., `run_blast.py`).

2.  **Run from the command line:** Open your terminal or command prompt, navigate to the directory where you saved the script, and run it using:
    ```bash
    python bio357_run_blast.py
    ```

3.  **Follow the prompts:** The script will present you with a menu to choose how you want to provide your query:
    ```
    Choose the query type:
    1. Enter sequence directly
    2. Provide a FASTA file
    3. Enter an NCBI Accession ID
    Enter your choice (1, 2, or 3):
    ```
    * **Option 1:** Enter your nucleotide or protein sequence when prompted.
    * **Option 2:** Enter the full path to your FASTA-formatted file. The script will read the first sequence from the file.
    * **Option 3:** Enter a valid NCBI Accession ID (e.g., NP\_001785, M10051).

4.  **BLAST execution:** Once you provide the query, the script will initiate the BLAST search on the NCBI server. You will see messages indicating the progress.

5.  **JSON output:** Upon successful completion of the BLAST search, the results will be saved in a JSON file named `blast_results.json` (by default) in the same directory where you ran the script.

## Optional Arguments (within the script)

You can modify the following variables within the `if __name__ == "__main__":` block of the script to customize the BLAST search:

* `database_name`: Change the NCBI database to search against (e.g., `"nt"` for nucleotide database, `"swissprot"` for Swiss-Prot). Refer to the NCBI BLAST documentation for a list of available databases.
* `blast_program`: Specify the BLAST program to use (e.g., `"blastp"` for protein-protein BLAST, `"blastx"` for translated nucleotide vs. protein). Refer to the NCBI BLAST documentation for available programs.
* `output_filename`: Change the name of the JSON file where the results will be saved.

**Example modifications within the script:**

```python
if __name__ == "__main__":
    # ... (query input section) ...

    if query_sequence:
        # Specify the database and program
        database_name = "nt"  # Search against the nucleotide database
        blast_program = "blastx" # Translated nucleotide vs. protein

        # Specify the output JSON file name
        output_filename = "translated_blast_results.json"

        # Run the BLAST search and save results to JSON
        run_ncbi_blast_to_json(query_sequence, query_type, database_name, blast_program, output_filename)
