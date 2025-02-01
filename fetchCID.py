from web3 import Web3
from web3.exceptions import ContractLogicError, ABIFunctionNotFound
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Blockchain (Use Infura/Alchemy or Local RPC)
INFURA_API_KEY = "989c9a51fc8e4cbb97dfa5d1cd5ab317"
rpc_url = f"https://sepolia.infura.io/v3/{INFURA_API_KEY}"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Verify connection
if not web3.is_connected():
    raise Exception("Failed to connect to Ethereum network")

# Define the smart contract address & ABI
contract_address = "0x70F45d6FC98B035C448b507d772ad0591b0e5083"
contract_abi = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "dreamer",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "ipfsHash",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "name": "DreamLogged",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_ipfsHash",
                "type": "string"
            }
        ],
        "name": "submitDream",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "dreams",
        "outputs": [
            {
                "internalType": "address",
                "name": "dreamer",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "ipfsHash",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAllDreams",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "dreamer",
                        "type": "address"
                    },
                    {
                        "internalType": "string",
                        "name": "ipfsHash",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct DreamChain.Dream[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "user",
                "type": "address"
            }
        ],
        "name": "getDreamsByUser",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "dreamer",
                        "type": "address"
                    },
                    {
                        "internalType": "string",
                        "name": "ipfsHash",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct DreamChain.Dream[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Initialize contract
try:
    contract = web3.eth.contract(
        address=web3.to_checksum_address(contract_address),
        abi=contract_abi
    )
except Exception as e:
    raise Exception(f"Failed to initialize contract: {str(e)}")

def format_dream_data(dreams):
    """Format dream data into a readable format"""
    formatted_dreams = []
    for dream in dreams:
        formatted_dream = {
            'dreamer': dream[0],
            'ipfsHash': dream[1],
            'timestamp': datetime.fromtimestamp(dream[2]).strftime('%Y-%m-%d %H:%M:%S')
        }
        formatted_dreams.append(formatted_dream)
    return formatted_dreams

def get_dream_cids(user_address):
    """Get dreams for a specific user"""
    try:
        # Ensure proper address formatting
        user_address = web3.to_checksum_address(user_address)
        
        # Call the contract function
        dreams = contract.functions.getDreamsByUser(user_address).call()
        
        # Format the results
        formatted_dreams = format_dream_data(dreams)
        return formatted_dreams
    
    except ContractLogicError as e:
        print(f"Contract logic error: {str(e)}")
        return None
    except ABIFunctionNotFound as e:
        print(f"Function not found in contract ABI: {str(e)}")
        return None
    except ValueError as e:
        print(f"Invalid address format: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def main():
    # Example: Fetch stored dreams for a user
    user_address = "0x37dC3933E0f9a1d624136A945905D08550eb9C58"
    dreams = get_dream_cids(user_address)
    
    if dreams:
        print("\nFetched Dreams:")
        for i, dream in enumerate(dreams, 1):
            print(f"\nDream {i}:")
            print(f"Dreamer: {dream['dreamer']}")
            print(f"IPFS Hash: {dream['ipfsHash']}")
            print(f"Timestamp: {dream['timestamp']}")
    else:
        print("No dreams found or error occurred")

if __name__ == "__main__":
    main()