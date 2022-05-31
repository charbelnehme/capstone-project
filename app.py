import os
import json
import pandas as pd
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./contracts/compiled/certificate_abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return contract

################################################################################
# Test Code to create a database of product hashes to authenticate against
################################################################################

# Static database for testing, A csv to be generated and used subsequently

# Our application will be connected with oracles that read data from the companies database, for testing we use csv.
csv_path = Path("./Data_files/Encoded_Data_Adidas.csv")
hashes_df = pd.read_csv(csv_path)

st.write(hashes_df)
################################################################################
# Award Certificate
################################################################################
# Load the contract
contract = load_contract()

accounts = w3.eth.accounts
account = accounts[0]
student_account = st.selectbox("Select Account", options=accounts)


customer_hash = st.text_input("Enter the product hashcode from the box:")

#if customer_hash in hashes_df.Hashcode:
st.write(customer_hash)




if st.button("Award Certificate"): 

    #st.write(customer_hash)
# json.dumps(dict)
    for hashes in hashes_df.Hashcode:
      if customer_hash in hashes:
         
   # if new_hash in product_hashes.database:
         contract.functions.awardCertificate(student_account, json.dumps(customer_hash)).transact({'from': account, 'gas': 1000000})
         st.write("True")
################################################################################
# Display Certificate
################################################################################
certificate_id = st.number_input("Enter a Certificate Token ID to display", value=0, step=1)

if st.button("Display Certificate"):
    # Get the certificate owner
    certificate_owner = contract.functions.ownerOf(certificate_id).call()
    st.write(f"The certificate was awarded to {certificate_owner}")

    # Get the certificate's metadata
    certificate_uri = contract.functions.tokenURI(certificate_id).call()
    st.write(f"The certificate's tokenURI metadata is {certificate_uri}")
