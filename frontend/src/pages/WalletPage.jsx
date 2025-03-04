import React, { useState, useEffect } from 'react';
import { ArrowUpDown } from 'lucide-react';
import { AssetCard } from '../components/AssetCard'; // Import AssetCard
import { fetchWalletData } from '../services/api'; // API service

// Wallet Page Component
export const WalletPage = () => {
  const [cryptoData, setCryptoData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadWalletData = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchWalletData(); // Call API service
        setCryptoData(data);
      } catch (err) {
        setError(err);
        console.error("Error fetching wallet data:", err);
      } finally {
        setLoading(false);
      }
    };

    loadWalletData();
  }, []);

  if (loading) return <div className="p-4">Loading wallet data...</div>;
  if (error) return <div className="p-4 text-red-500">Error loading wallet data. Please try again.</div>;
  if (!cryptoData) return <div className="p-4">No wallet data available.</div>;

  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      <header className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-b-3xl shadow-md">
        <h1 className="text-xl font-bold mb-2">Your Balance</h1>
        <div className="flex items-baseline">
          <p className="text-3xl font-bold">${cryptoData.totalBalance.toLocaleString()}</p>
          <span className="ml-2 text-green-300">+3.2%</span> {/* TODO: Connect to backend for real-time change */}
        </div>
        <div className="flex mt-6 gap-4">
          <button className="flex-1 bg-white text-blue-600 rounded-full py-2 font-medium flex items-center justify-center">
            <ArrowUpDown size={16} className="mr-1" /> Send/Receive {/* TODO: Implement Send/Receive functionality */}
          </button>
          <button className="flex-1 bg-blue-500 text-white rounded-full py-2 font-medium border border-blue-400">
            Buy {/* TODO: Implement Buy functionality */}
          </button>
        </div>
      </header>

      <section className="p-4">
        <h2 className="text-lg font-bold mb-3 text-gray-800">Your Assets</h2>
        <div className="space-y-3">
          {cryptoData.assets.map(asset => (
            <AssetCard key={asset.id} asset={asset} /> // Use AssetCard component
          ))}
        </div>
      </section>

      <section className="p-4">
        <h2 className="text-lg font-bold mb-3 text-gray-800">Recent Transactions</h2>
        <div className="bg-white rounded-xl p-4 shadow-sm">
          {/* TODO: Connect to backend API to fetch transaction history */}
          <p className="text-gray-500 text-center py-4">No recent transactions</p>
        </div>
      </section>
    </div>
  );
};