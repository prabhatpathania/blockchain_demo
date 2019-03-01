# Module 1 - Create a Blockchain

# Importing libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

## Part 1 -- Building a Blockchain [class]

class Blockchain:
    
    def __init__(self):
        self.chain = []                                     # List of blocks
        self.create_block(proof = 1, previous_hash = '0')   # Genesis block
            
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()), # str for JSON compatibility
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() # Encoded for SHA256
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof                        # Nonce value
    
    def hash(self, block):                      # Returns hash of the block
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest() # Encode of SHA256
            if hash_operation[:4] == '0000':
                return True
            previous_block = block
            block_index += 1
        return True
        
    
## Part 2 -- Mining
        
# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain [object]
blockchain = Blockchain()

# Mining a new Block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Block mined successfully!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200


# Get the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Check the validity of the Blockchain
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    bValid = blockchain.is_chain_valid(blockchain.chain)
    if bValid == True:
        response = {'message': 'Chain is valid'}
    else:
        response = {'message': 'Chain is not valid'}
    return jsonify(response), 200


# Running the app
app.run(host = '0.0.0.0', port = 5000 )
