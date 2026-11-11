import React from 'react';

export default function Navbar() {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center space-x-3">
            <span className="text-3xl">🌱</span>
            <div>
              <span className="text-xl font-bold text-gray-900 tracking-tight">AgriSense <span className="text-emerald-600">AI</span></span>
              <span className="hidden sm:inline-block ml-2 text-xs font-medium px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded-full">
                Decision Support System
              </span>
            </div>
          </div>

          <nav className="flex space-x-1 sm:space-x-4 text-sm font-medium text-gray-600">
            <a
              href="#fertilizer"
              className="px-3 py-2 text-emerald-700 bg-emerald-50 rounded-md font-semibold border-b-2 border-emerald-600"
            >
              Fertilizer Recommendation
            </a>
            <span className="hidden md:inline-flex items-center px-3 py-2 text-gray-400 cursor-not-allowed" title="Coordinated by Sujay">
              Crop Recommendation
            </span>
            <span className="hidden md:inline-flex items-center px-3 py-2 text-gray-400 cursor-not-allowed" title="Coordinated by Chetan">
              Crop Yield
            </span>
            <span className="hidden lg:inline-flex items-center px-3 py-2 text-gray-400 cursor-not-allowed" title="Coordinated by Dhyan">
              Dashboard
            </span>
          </nav>
        </div>
      </div>
    </header>
  );
}
