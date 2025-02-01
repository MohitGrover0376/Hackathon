import lighthouse from '@lighthouse-web3/sdk';

async function getDataFromLighthouse(bafkreic37sp67hloqxxcae2j353ecfnkv4s5ufdut44oxmt3bv7wvwpjk4) {
    try {
        // Direct gateway access
        const response = await fetch(`https://gateway.lighthouse.storage/ipfs/${bafkreic37sp67hloqxxcae2j353ecfnkv4s5ufdut44oxmt3bv7wvwpjk4}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching from Lighthouse:", error);
    }
}

// Function to process data and send to AI model
async function processDataWithAI(data) {
    try {
        // Assuming your AI model is accessible via an API endpoint
        const aiResponse = await fetch('https://language.googleapis.com/v1/documents:annotateText', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await aiResponse.json();
        return result;
    } catch (error) {
        console.error("Error processing with AI:", error);
    }
}

// Main function to orchestrate the process
async function main() {
    // Your Lighthouse CID
    const cid = "bafkreic37sp67hloqxxcae2j353ecfnkv4s5ufdut44oxmt3bv7wvwpjk4";
    
    // 1. Get data from Lighthouse
    const data = await getDataFromLighthouse(cid);
    console.log("Retrieved data:", data);
    
    // 2. Process with AI model
    const aiResult = await processDataWithAI(data);
    console.log("AI processing result:", aiResult);
}

main();