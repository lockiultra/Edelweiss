import React from 'react';

export const AssetCard = ({ asset }) => {
  return (
    <div
      className="bg-white p-4 rounded-xl shadow-sm flex justify-between items-center animate-fadeIn"
    >
      <div className="flex items-center">
        <div className={`w-10 h-10 rounded-full mr-3 flex items-center justify-center ${
          asset.symbol === 'BTC' ? 'bg-orange-100 text-orange-600' :
          asset.symbol === 'ETH' ? 'bg-purple-100 text-purple-600' :
          'bg-blue-100 text-blue-600'
        }`}>
          {asset.symbol.charAt(0)}
        </div>
        <div>
          <h3 className="font-medium">{asset.name}</h3>
          <p className="text-sm text-gray-500">{asset.amount} {asset.symbol}</p>
        </div>
      </div>
      <div className="text-right">
        <p className="font-medium">${asset.value.toLocaleString()}</p>
        <p className={`text-sm ${asset.change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
          {asset.change >= 0 ? '+' : ''}{asset.change}%
        </p>
      </div>
    </div>
  );
};