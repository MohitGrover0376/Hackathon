# Install required packages:
# pip install python-ethers lighthouse-web3 aiohttp

from ethers import Contract, JsonRpcProvider, Wallet
import lighthouse
import json
import asyncio
import aiohttp
from datetime import datetime

class DreamChainService:
    def _init_(self):
        # Initialize provider (Infura, Alchemy, etc.)
        INFURA_API_KEY = "989c9a51fc8e4cbb97dfa5d1cd5ab317"
        self.provider = JsonRpcProvider(f"https://sepolia.infura.io/v3/{INFURA_API_KEY}")
        
        # Contract setup
        self.contract_address = "0x70F45d6FC98B035C448b507d772ad0591b0e5083"
        
        # Load contract ABI
        self.contract_abi = [
            "function storeDream(string memory cid, bool isPublic) public",
            "function getDreams() public view returns (string[] memory)"
        ]
        
        # Setup wallet
        self.wallet = Wallet("YOUR_PRIVATE_KEY", self.provider)
        
        # Initialize contract with signer
        self.contract = Contract(
            self.contract_address,
            self.contract_abi,
            self.wallet
        )
        
        # Lighthouse API key
        self.lighthouse_token = "YOUR_LIGHTHOUSE_API_TOKEN"
        self.lighthouse = lighthouse.Lighthouse(
            token=self.lighthouse_token,
            network="testnet"  # or "mainnet"
        )

    async def upload_to_lighthouse(self, dream_data: dict) -> str:
        """
        Upload dream data to Lighthouse and return CID
        """
        try:
            # Convert dream data to JSON string
            json_str = json.dumps(dream_data)
            
            # Upload to Lighthouse
            upload_response = await self.lighthouse.upload_text(
                text=json_str,
                name=f"dream_{int(datetime.now().timestamp())}"
            )
            
            return upload_response.data.Hash
            
        except Exception as e:
            print(f"Lighthouse upload failed: {e}")
            raise

    async def store_dream_in_contract(self, cid: str):
        """
        Store CID in smart contract
        """
        try:
            # Get current gas price
            gas_price = await self.provider.get_gas_price()
            
            # Estimate gas
            gas_estimate = await self.contract.estimate_gas.storeDream(
                cid,
                True  # isPublic parameter
            )
            
            # Prepare and send transaction
            tx = await self.contract.storeDream(
                cid,
                True,
                {
                    'gasLimit': gas_estimate,
                    'gasPrice': gas_price
                }
            )
            
            # Wait for transaction confirmation
            receipt = await tx.wait()
            return receipt
            
        except Exception as e:
            print(f"Contract storage failed: {e}")
            raise

    async def process_dream(self, dream_content: str):
        """
        Main function to process dream: upload to Lighthouse and store in contract
        """
        try:
            # Prepare dream data
            dream_data = {
                "content": dream_content,
                "timestamp": int(datetime.now().timestamp()),
                "metadata": {
                    "source": "python_backend"
                }
            }
            
            # Upload to Lighthouse
            print("Uploading to Lighthouse...")
            cid = await self.upload_to_lighthouse(dream_data)
            print(f"Uploaded to Lighthouse with CID: {cid}")
            
            # Store in smart contract
            print("Storing in smart contract...")
            receipt = await self.store_dream_in_contract(cid)
            print(f"Stored in contract. Transaction hash: {receipt.transaction_hash.hex()}")
            
            return {
                "status": "success",
                "cid": cid,
                "transaction_hash": receipt.transaction_hash.hex()
            }
            
        except Exception as e:
            print(f"Dream processing failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

# Example usage
async def main():
    # Initialize service
    dream_service = DreamChainService()
    
    # Example dream content
    dream_content = "I was flying over a crystal city filled with light..."
    
    # Process dream
    result = await dream_service.process_dream(dream_content)
    
    if result["status"] == "success":
        print("\nDream successfully processed!")
        print(f"IPFS CID: {result['cid']}")
        print(f"Transaction Hash: {result['transaction_hash']}")
    else:
        print(f"\nError processing dream: {result['error']}")

# Run the example
if _name_ == "_main_":
    asyncio.run(main())

# FastAPI Integration Example
from fastapi import FastAPI, HTTPException

app = FastAPI()
dream_service = DreamChainService()

@app.post("/submit-dream")
async def submit_dream(dream_content: str):
    result = await dream_service.process_dream(dream_content)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
        return result