// Define API base URLs - adjust these based on your docker-compose setup
const AUTH_API_BASE_URL = 'http://localhost:8001'; // Change to auth service name in docker-compose
const WALLET_API_BASE_URL = 'http://localhost:8002'; // Change to wallet service name in docker-compose

// Function to handle API requests (you can expand this)
const handleResponse = async (response) => {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(`HTTP error! status: ${response.status}, message: ${message}`);
  }
  return await response.json();
};

// Wallet API calls
export const fetchWalletData = async () => {
  // Placeholder - replace with actual API endpoint and authentication if needed
  // For now, using mock data as before, you'll need to implement actual backend endpoint for wallet data
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        totalBalance: 24850.75,
        fiatValue: 24850.75,
        assets: [
          { id: 1, name: 'Bitcoin', symbol: 'BTC', amount: 0.55, value: 16500, change: 2.4 },
          { id: 2, name: 'Ethereum', symbol: 'ETH', amount: 4.2, value: 7560, change: -1.2 },
          { id: 3, name: 'Solana', symbol: 'SOL', amount: 27.5, value: 790.75, change: 5.6 }
        ]
      });
    }, 500); // Simulate network latency
  });
  // Example of actual API call (adjust endpoint and headers as needed):
  // const response = await fetch(`${WALLET_API_BASE_URL}/wallets/`, {
  //   headers: {
  //     'Authorization': `Bearer YOUR_ACCESS_TOKEN` // If authentication is required
  //   }
  // });
  // return handleResponse(response);
};

// Auth API calls (example for login - adapt for register etc.)
export const loginUser = async (credentials) => {
  const response = await fetch(`${AUTH_API_BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded', // Or application/json if backend expects JSON
    },
    body: new URLSearchParams(credentials) // For form-urlencoded, adjust if backend expects JSON
  });
  return handleResponse(response);
};

export const registerUser = async (userData) => {
    const response = await fetch(`${AUTH_API_BASE_URL}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });
    return handleResponse(response);
};


// Add more API service functions as needed (e.g., for staking, profile, settings, transactions)