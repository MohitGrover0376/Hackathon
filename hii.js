import React, { useState } from "react";
import { ethers } from "ethers";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

// Replace these with your deployed contract details
const scholarshipContractAddress = "YOUR_CONTRACT_ADDRESS";
const scholarshipContractABI = [
  // Your ABI goes here
];

const App = () => {
  const [walletConnected, setWalletConnected] = useState(false);
  const [provider, setProvider] = useState(null);
  const [contract, setContract] = useState(null);
  const [amount, setAmount] = useState("");
  const [studentAddress, setStudentAddress] = useState("");

  const connectWallet = async () => {
    try {
      if (!window.ethereum) {
        alert("Please install MetaMask to use this app.");
        return;
      }

      const web3Provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = web3Provider.getSigner();
      const contractInstance = new ethers.Contract(
        scholarshipContractAddress,
        scholarshipContractABI,
        signer
      );

      await web3Provider.send("eth_requestAccounts", []);
      setProvider(web3Provider);
      setContract(contractInstance);
      setWalletConnected(true);
    } catch (error) {
      console.error("Error connecting wallet:", error);
    }
  };

  const donateFunds = async () => {
    if (!amount || !contract) {
      alert("Please enter a valid amount.");
      return;
    }

    try {
      const tx = await contract.donate({
        value: ethers.utils.parseEther(amount),
      });
      await tx.wait();
      alert("Donation successful!");
      setAmount("");
    } catch (error) {
      console.error("Error donating funds:", error);
    }
  };

  const addStudent = async () => {
    if (!studentAddress || !contract) {
      alert("Please enter a valid student address.");
      return;
    }

    try {
      const tx = await contract.addStudent(studentAddress);
      await tx.wait();
      alert("Student added successfully!");
      setStudentAddress("");
    } catch (error) {
      console.error("Error adding student:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10">
      <h1 className="text-3xl font-bold mb-6">Scholarship Distribution Platform</h1>
      {!walletConnected ? (
        <Button onClick={connectWallet} className="bg-blue-500 text-white">
          Connect Wallet
        </Button>
      ) : (
        <div className="grid gap-6 w-full max-w-3xl">
          <Card>
            <CardContent>
              <h2 className="text-xl font-semibold mb-2">Donate Funds</h2>
              <Input
                type="number"
                placeholder="Enter amount in ETH"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="mb-4"
              />
              <Button onClick={donateFunds} className="bg-green-500 text-white">
                Donate
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <h2 className="text-xl font-semibold mb-2">Add Student</h2>
              <Input
                type="text"
                placeholder="Enter student wallet address"
                value={studentAddress}
                onChange={(e) => setStudentAddress(e.target.value)}
                className="mb-4"
              />
              <Button onClick={addStudent} className="bg-purple-500 text-white">
                Add Student
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default App;
