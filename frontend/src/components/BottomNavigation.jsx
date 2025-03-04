import React from 'react';
import { Wallet, LineChart, User, Settings } from 'lucide-react';

// Bottom Navigation Component
export const BottomNavigation = ({ activePage, setActivePage }) => {
  const navItems = [
    { name: 'wallet', icon: <Wallet size={24} />, label: 'Wallet' },
    { name: 'staking', icon: <LineChart size={24} />, label: 'Staking' },
    { name: 'profile', icon: <User size={24} />, label: 'Profile' },
    { name: 'settings', icon: <Settings size={24} />, label: 'Settings' }
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 h-16 bg-white shadow-lg flex justify-around items-center z-50">
      {navItems.map((item) => (
        <button
          key={item.name}
          onClick={() => setActivePage(item.name)}
          className={`flex flex-col items-center justify-center w-20 h-full transition-all ${
            activePage === item.name ? 'text-blue-600 scale-110' : 'text-gray-500'
          }`}
        >
          <div className="transition-all duration-300">
            {item.icon}
          </div>
          <span className="text-xs mt-1">{item.label}</span>
        </button>
      ))}
    </div>
  );
};