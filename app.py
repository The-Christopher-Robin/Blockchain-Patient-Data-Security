from flask import Flask, render_template, request, redirect, url_for,jsonify
from web3 import Web3
from datetime import datetime
import json
import sqlite3

app = Flask(__name__)
blocknum=0
# Initialize Web3 instance
web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))  # Connect to local Ganache instance

# Load smart contract ABI from file
with open('C:\\Users\\Chris\\Desktop\\bda\\Health.abi', 'r') as f:
    contract_abi = json.load(f)

# Address of deployed smart contract
contract_address = '0x7F51F06b911D70d5509ABAaBA1527e0fbf36fAC5'  # Replace with your actual contract address

# Account address that will be used to send transactions
from_address = '0x4baa221dD96AB3e5577506D8cEd64B20178F5932'  # Replace with your actual Ethereum address

# Initialize smart contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
def is_valid_usn(usn):
    valid_usns = [str(i) for i in range(1, 101)]
    return usn in valid_usns

@app.route('/', methods=['GET', 'POST'])
def index():
    global blocknum
    if request.method == 'POST':
        blocknum+=1
        selected_organization = request.form['organization']
        entered_usn = request.form['voter_id']
        entered_name = request.form['name']
        print(f"{selected_organization},{entered_usn},{entered_name}")
        # Check if the entered USN is valid
        if is_valid_usn(entered_usn):
            # Perform additional validation if needed
            # For example, check if the entered name matches any records
            tx_hash = contract.functions.vote(selected_organization,entered_usn,entered_name).transact({'from': from_address})
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# Check if the transaction was successful
            if tx_receipt.status == 1:
                print("Vote function executed successfully!")
            else:
                print("Vote function failed!")
        # Wait for transaction receipt
           #receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            # tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
            # logs = tx_receipt['logs']
            # for log in logs:
            #     print(log)


        
        # Insert vote details into the SQLite database
            record_vote(selected_organization, entered_usn, entered_name)
            # Redirect to the thank you page if credentials are valid
            return redirect(url_for('thank_you', organization=selected_organization, usn=entered_usn, name=entered_name))
        else:
            # Return an error message
            return jsonify({'error': 'Invalid age, please enter a valid age'}), 400
    else:
        # Render the index page with the organization options
        organizations = ["NSS", "NCC", "BDC"]  # Replace with actual organization list
        return render_template('index.html', organizations=organizations)

# def record_vote(id,name,org):
#     try:
#         # Connect to the database
#         conn = sqlite3.connect('votes.db')
#         print("Connected to SQLite database")

#         # Create a cursor object
#         c = conn.cursor()
#         if id in ['23', '27', '29', '42', '47']:
#         # Execute the INSERT statement
#             c.execute('''INSERT INTO votes (id, name, org) VALUES (?, ?, ?)''', (id,name,org))

#             # Commit the changes
#             conn.commit()
#             print("Vote recorded successfully")

#     except sqlite3.Error as e:
#         print("SQLite error:", e)

#     finally:
#         # Close the connection
#         conn.close()
def record_vote(name, age, blood_group):
    try:
        # Connect to the database
        conn = sqlite3.connect('C:\\Users\\Chris\\Desktop\\bda\\votes.db')
        print("Connected to SQLite database")

        # Create a cursor object
        c = conn.cursor()

        # Create the votes table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS info (
                            name TEXT PRIMARY KEY,
                            age TEXT,
                            blood_group TEXT
                    )''')

        # Check if the ID is not empty and valid
        
        # Execute the INSERT statement
        c.execute('''INSERT INTO info (name, age, blood_group) VALUES (?, ?, ?)''', (name, age, blood_group))
        # c.execute('''SELECT * FROM info''')
        # Commit the changes
        conn.commit()
        print("Vote recorded successfully")

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        # Close the connection
        conn.close()



@app.route('/thank-you')
def thank_you():
    selected_candidate = request.args.get('organization', 1)
    voter_id = request.args.get('voter_id', 2)
    return render_template('thank_you.html', selected_candidate=selected_candidate, voter_id=voter_id)

@app.route('/block/<int:voter_id>')
def block_details(voter_id):
    # Retrieve block details based on voter ID from smart contract or blockchain
    # Example: block = contract.functions.getBlockByVoterId(voter_id).call()
    block = {
        'number': blocknum,  # Example block number
        'hash': '0x358AA13c52544ECCEF6B0ADD0f801012ADAD5eE3',  # Example block hash
        'timestamp': datetime.now(),  # Example timestamp
        'parentHash': '0x59Be6Ca4CDD745927C0EAa085d348a0cE7D15A3D'  # Example parent hash
        # Add more block details as needed
    }
    return render_template('block_details.html', block=block)


if __name__ == '__main__':
    app.run(debug=True)