from chalice import Chalice
import schemarecomb as sr
from Bio import SeqIO
import boto3
import json

app = Chalice(app_name='schemarecomb_serverless')

@app.route('/run', methods=['POST'], cors=True)
def run():
    # TODO: write dummy output to dynamodb database or S3 bucket
    request = app.current_request
    body = json.loads(request._body)
    parent_sequences = json.dumps(body['parent_sequences'])
    parents = sr.ParentSequences.from_json(parent_sequences)
    # TODO: skip this section if the user provides aligned FASTA sequences and a .pdb file
    parents.obtain_seqs(body['num_final_seqs'], body['desired_identity'])
    parents.align()
    parents.get_PDB()
    
    libraries = sr.generate_libraries(parents, body['num_blocks'])
    best_lib = max(libraries, key=lambda x: x.mutation_rate - x.energy)
    # TODO: write output to dynamodb database or S3 bucket
    return json.dumps(best_lib.dna_blocks)

# TODO: get status from dynamodb database or S3 bucket
@app.route('/check_progress', methods=['POST'], cors=True)
def check_progress():
    return None