import json
import uuid

import boto3
from chalice import Chalice

app = Chalice(app_name='schemarecomb_serverless')
s3_client = boto3.client('s3')


@app.route('/run', methods=['POST'], cors=True)
def run():
    run_params = app.current_request.json_body
    try:
        # Check that these params are in the json_body.
        run_params['parentsText']
        run_params['pdbText']
        run_params['numBlocks']
    except KeyError:
        return {'errorMsg': 'Message body was not formatted properly.'}

    # Unique key for request.
    run_uuid = uuid.uuid4()

    # TODO: Object expiration.
    # Put run object in S3. This will trigger s3_handler below.
    response = s3_client.put_object(
        Body=json.dumps(run_params).encode(),
        Bucket='schemarecomb-runs',
        Key=str(run_uuid),
        Metadata={'status': 'run raspp'}
    )

    print('started uuid:', str(run_uuid))
    return {'response': response, 'uuid': str(run_uuid)}


@app.on_s3_event(bucket='schemarecomb-runs')
def s3_handler(event):

    event_dict = event.to_dict()

    # Testing whether event happens correctly. It does, so we can remove this
    # in future development (TODO).
    s3_client.put_object(
        Body=str(event_dict).encode(),
        Bucket='schemarecomb-test',
        Key=event.key,
    )

    # TODO: Need to extract status from event Metadata. Handle cases:
    #   case 'run raspp': Add the event key (run_uuid) to SQS and initialize
    #                     ECS cluster to do RASPP.
    #   case 'obtain seqs': Same but obtain seqs. (Implement once we get RASPP
    #                       working.
    #   case 'get pdb': same but get PDB.
    #   case ...

    # TODO: All of this stuff now happens in ECS, so we don't need
    # schemarecomb as a dependency for the chalice app.
    '''
    try:
        pdb_f = StringIO(pdb_str)
        pdb = sr.PDBStructure.from_pdb_file(pdb_f)

        parents_f = StringIO(parents_str)
        parents_srs = list(SeqIO.parse(parents_f, 'fasta'))
        parents = sr.ParentSequences(parents_srs, pdb, prealigned=True)

        libraries = sr.generate_libraries(parents, num_blocks)
        lib = libraries[0]

        dna_file_str = StringIO()
        SeqIO.write(lib.dna_blocks, dna_file_str, 'fasta')
        dna_file_str.seek(0)
    except Exception as e:
        return {'error': repr(e)}

    return [f'Number of libraries: {len(libraries)}', dna_file_str.read()]
        '''


# TODO: get status S3 bucket
@app.route('/check_progress', methods=['POST'], cors=True)
def check_progress():
    return None
