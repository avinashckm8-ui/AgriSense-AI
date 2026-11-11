import React from 'react';
import Navbar from './components/Navbar';
import FertilizerPage from './pages/FertilizerPage';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-between">
      <div>
        <Navbar />
        <FertilizerPage />
      </div>

      <footer className="bg-white border-t border-gray-200 py-6 text-center text-xs text-gray-500">
        <p>AgriSense AI – Intelligent Agricultural Prediction and Decision Support System &copy; 2026</p>
        <p className="mt-1 text-gray-400">Team: Sujay (Crop) | Chetan (Yield) | Avinash (Fertilizer) | Dhyan (Platform)</p>
      </footer>
    </div>
  );
}
