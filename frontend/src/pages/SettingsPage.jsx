import React from 'react';

// Settings Page Component
export const SettingsPage = () => {
  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      <header className="bg-gradient-to-r from-gray-700 to-gray-800 text-white p-6">
        <h1 className="text-xl font-bold">Settings</h1>
      </header>

      <section className="p-4">
        <h2 className="text-lg font-bold mb-3 text-gray-800">App Preferences</h2>
        <div className="bg-white rounded-xl shadow-sm overflow-hidden animate-fadeIn text-center">
          <p className="text-gray-500 mb-3">This section is under development.</p>
          {/* TODO: Connect to backend API to fetch and update settings */}
          <button className="bg-gray-700 text-white px-4 py-2 rounded-lg font-medium" disabled>
            Coming Soon
          </button>
        </div>
      </section>
    </div>
  );
};