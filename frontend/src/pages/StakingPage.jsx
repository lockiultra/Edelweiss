import React from 'react';

// Staking Page Component
export const StakingPage = () => {
  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      <header className="bg-gradient-to-r from-purple-600 to-purple-700 text-white p-6">
        <h1 className="text-xl font-bold">Staking</h1>
        <p className="opacity-80">Earn passive income on your crypto</p>
      </header>

      <section className="p-4">
        <h2 className="text-lg font-bold mb-3 text-gray-800">Your Active Stakes</h2>
        <div className="bg-white rounded-xl p-6 shadow-sm text-center">
          <p className="text-gray-500 mb-3">This section is under development.</p>
          {/* TODO: Connect to backend API to fetch active stakes */}
          <button className="bg-purple-600 text-white px-4 py-2 rounded-lg font-medium" disabled>
            Coming Soon
          </button>
        </div>
      </section>

      <section className="p-4">
        <h2 className="text-lg font-bold mb-3 text-gray-800">Staking Opportunities</h2>
        <div className="bg-white rounded-xl p-6 shadow-sm text-center">
          <p className="text-gray-500 mb-3">This section is under development.</p>
          {/* TODO: Connect to backend API to fetch staking opportunities */}
          <button className="bg-purple-600 text-white px-4 py-2 rounded-lg font-medium" disabled>
            Coming Soon
          </button>
        </div>
      </section>
    </div>
  );
};