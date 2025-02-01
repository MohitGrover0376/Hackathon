import lighthouse from '@lighthouse-web3/sdk';

// Function to retrieve content
async function getDreamContent(cid) {
    try {
        const response = await fetch(`https://gateway.lighthouse.storage/ipfs/${cid}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching from Lighthouse:", error);
    }
}

// Usage
const dreamContent = await getDreamContent(lighthouseCID);
console.log("Dream content:", dreamContent);