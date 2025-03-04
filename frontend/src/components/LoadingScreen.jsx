import React from 'react';

// Loading Screen Component
export const LoadingScreen = () => {
  return (
    <div className="h-screen w-full flex flex-col items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-24 h-24 mb-8 relative">
        <div className="absolute w-full h-full border-8 border-white rounded-full opacity-30"></div>
        <div className="absolute w-full h-full border-8 border-t-blue-300 rounded-full animate-spin"></div>
      </div>
      <h1 className="text-white text-2xl font-bold">CryptoWallet</h1>
    </div>
  );
};
