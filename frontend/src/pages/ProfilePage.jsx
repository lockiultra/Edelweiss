import React from 'react';

// Profile Page Component
export const ProfilePage = () => {
  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      <header className="bg-gradient-to-r from-green-600 to-teal-600 text-white p-6 pb-20">
        <h1 className="text-xl font-bold">Profile</h1>
      </header>

      <section className="px-4 -mt-14">
        <div className="bg-white rounded-xl shadow-md p-5 animate-fadeIn text-center">
          <p className="text-gray-500 mb-3">This section is under development.</p>
          {/* TODO: Connect to backend API to fetch user profile data */}
          <button className="bg-green-600 text-white px-4 py-2 rounded-lg font-medium" disabled>
            Coming Soon
          </button>
        </div>
      </section>
    </div>
  );
};