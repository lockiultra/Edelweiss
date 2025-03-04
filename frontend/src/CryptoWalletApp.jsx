import React, { useState, useEffect } from 'react';
import { LoadingScreen } from './components/LoadingScreen';
import { BottomNavigation } from './components/BottomNavigation';
import { WalletPage } from './pages/WalletPage';
import { StakingPage } from './pages/StakingPage';
import { ProfilePage } from './pages/ProfilePage';
import { SettingsPage } from './pages/SettingsPage';

// Main App Component
const CryptoWalletApp = () => {
  const [activePage, setActivePage] = useState('wallet');
  const [isLoading, setIsLoading] = useState(true);

  // Simulating initial loading
  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
    }, 1500);
  }, []);

  // Page transitions animation
  const getPageStyle = (pageName) => {
    return {
      opacity: activePage === pageName ? 1 : 0,
      transform: `translateX(${activePage === pageName ? 0 : 100}px)`,
      position: 'absolute',
      width: '100%',
      height: 'calc(100% - 60px)',
      transition: 'all 0.3s ease-in-out',
      display: activePage === pageName ? 'block' : 'none'
    };
  };

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <div className="h-screen w-full bg-gray-50 overflow-hidden relative font-sans">
      <div className="h-full w-full relative overflow-hidden pb-16">
        {/* Wallet Page */}
        <div style={getPageStyle('wallet')}>
          <WalletPage />
        </div>

        {/* Staking Page */}
        <div style={getPageStyle('staking')}>
          <StakingPage />
        </div>

        {/* Profile Page */}
        <div style={getPageStyle('profile')}>
          <ProfilePage />
        </div>

        {/* Settings Page */}
        <div style={getPageStyle('settings')}>
          <SettingsPage />
        </div>
      </div>

      {/* Bottom Navigation */}
      <BottomNavigation activePage={activePage} setActivePage={setActivePage} />
    </div>
  );
};

export default CryptoWalletApp;
