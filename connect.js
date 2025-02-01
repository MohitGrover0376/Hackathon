// Using ethers.js
const dreamChainAddress = "0xb27A31f1b0AF2946B7F582768f03239b1eC07c2c";
const dreamChainABI = [
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "dreamer",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "ipfsHash",
				"type": "string"
			},
			{
				"indexed": false,
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
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "userDreams",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
] ;

// Connect to the contract
const provider = new ethers.providers.Web3Provider(window.ethereum);
const signer = provider.getSigner();
const dreamChainContract = new ethers.Contract(dreamChainAddress, dreamChainABI, signer);

// Your Lighthouse CID
const lighthouseCID = "bafkreic37sp67hloqxxcae2j353ecfnkv4s5ufdut44oxmt3bv7wvwpjk4";

// Submit the dream with the CID
try {
    const tx = await dreamChainContract.submitDream(lighthouseCID);
    await tx.wait();
    console.log("Dream submitted successfully!");
} catch (error) {
    console.error("Error submitting dream:", error);
}