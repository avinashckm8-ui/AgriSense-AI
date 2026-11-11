import React, { useState } from 'react';
import { predictFertilizer } from '../services/api';
import FertilizerDisclaimer from '../components/FertilizerDisclaimer';
import FertilizerCard from '../components/FertilizerCard';

const SOIL_TYPES = ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey'];
const CROP_TYPES = [
  'Maize',
  'Sugarcane',
  'Cotton',
  'Tobacco',
  'Paddy',
  'Barley',
  'Wheat',
  'Millets',
  'Oil seeds',
  'Pulses',
  'Ground Nuts',
];

const INITIAL_FORM = {
  temperature: 26,
  humidity: 52,
  moisture: 38,
  soil_type: 'Sandy',
  crop_type: 'Maize',
  nitrogen: 37,
  potassium: 0,
  phosphorous: 0,
};

export default function FertilizerPage() {
  const [formData, setFormData] = useState(INITIAL_FORM);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'number' ? (value === '' ? '' : parseFloat(value)) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const response = await predictFertilizer(formData);
      setResult(response);
    } catch (err) {
      setError(err.message || 'Failed to generate recommendation. Check if backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Title Header */}
      <div className="mb-8 text-center sm:text-left">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 tracking-tight">
          Fertilizer Recommendation System
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          Intelligent precision agriculture assistant: Predict the optimal fertilizer category by entering soil chemical
          metrics (N, P, K) and localized climate parameters.
        </p>
      </div>

      {/* Main Form Container */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sm:p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Soil & Crop Categories */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4 border-b pb-2">
              1. Soil & Crop Classification
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="soil_type" className="block text-sm font-medium text-gray-700">
                  Soil Type
                </label>
                <select
                  id="soil_type"
                  name="soil_type"
                  value={formData.soil_type}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm bg-gray-50 border p-2.5"
                  required
                >
                  {SOIL_TYPES.map((soil) => (
                    <option key={soil} value={soil}>
                      {soil} Soil
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="crop_type" className="block text-sm font-medium text-gray-700">
                  Target Crop
                </label>
                <select
                  id="crop_type"
                  name="crop_type"
                  value={formData.crop_type}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm bg-gray-50 border p-2.5"
                  required
                >
                  {CROP_TYPES.map((crop) => (
                    <option key={crop} value={crop}>
                      {crop}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Soil Nutrient Indicators */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4 border-b pb-2">
              2. Primary Soil Nutrients (NPK)
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label htmlFor="nitrogen" className="block text-sm font-medium text-gray-700">
                  Nitrogen (N)
                </label>
                <div className="mt-1 relative rounded-md shadow-sm">
                  <input
                    type="number"
                    step="any"
                    min="0"
                    max="300"
                    id="nitrogen"
                    name="nitrogen"
                    value={formData.nitrogen}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm border p-2.5"
                    required
                  />
                  <span className="absolute inset-y-0 right-0 pr-3 flex items-center text-xs text-gray-400">ratio</span>
                </div>
              </div>

              <div>
                <label htmlFor="phosphorous" className="block text-sm font-medium text-gray-700">
                  Phosphorous (P)
                </label>
                <div className="mt-1 relative rounded-md shadow-sm">
                  <input
                    type="number"
                    step="any"
                    min="0"
                    max="300"
                    id="phosphorous"
                    name="phosphorous"
                    value={formData.phosphorous}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm border p-2.5"
                    required
                  />
                  <span className="absolute inset-y-0 right-0 pr-3 flex items-center text-xs text-gray-400">ratio</span>
                </div>
              </div>

              <div>
                <label htmlFor="potassium" className="block text-sm font-medium text-gray-700">
                  Potassium (K)
                </label>
                <div className="mt-1 relative rounded-md shadow-sm">
                  <input
                    type="number"
                    step="any"
                    min="0"
                    max="300"
                    id="potassium"
                    name="potassium"
                    value={formData.potassium}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm border p-2.5"
                    required
                  />
                  <span className="absolute inset-y-0 right-0 pr-3 flex items-center text-xs text-gray-400">ratio</span>
                </div>
              </div>
            </div>
          </div>

          {/* Environmental Conditions */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4 border-b pb-2">
              3. Environmental & Soil Moisture Conditions
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label htmlFor="temperature" className="block text-sm font-medium text-gray-700">
                  Temperature
                </label>
                <div className="mt-1 relative rounded-md shadow-sm">
                  <input
                    type="number"
                    step="any"
                    min="-10"
                    max="60"
                    id="temperature"
                    name="temperature"
                    value={formData.temperature}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm border p-2.5"
                    required
                  />
                  <span className="absolute inset-y-0 right-0 pr-3 flex items-center text-xs text-gray-400">°C</span>
                </div>
              </div>

              <div>
                <label htmlFor="humidity" className="block text-sm font-medium text-gray-700">
                  Relative Humidity
                </label>
                <div className="mt-1 relative rounded-md shadow-sm">
                  <input
                    type="number"
                    step="any"
                    min="0"
                    max="100"
                    id="humidity"
                    name="humidity"
                    value={formData.humidity}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm border p-2.5"
                    required
                  />
                  <span className="absolute inset-y-0 right-0 pr-3 flex items-center text-xs text-gray-400">%</span>
                </div>
              </div>

              <div>
                <label htmlFor="moisture" className="block text-sm font-medium text-gray-700">
                  Soil Moisture
                </label>
                <div className="mt-1 relative rounded-md shadow-sm">
                  <input
                    type="number"
                    step="any"
                    min="0"
                    max="100"
                    id="moisture"
                    name="moisture"
                    value={formData.moisture}
                    onChange={handleChange}
                    className="block w-full rounded-md border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm border p-2.5"
                    required
                  />
                  <span className="absolute inset-y-0 right-0 pr-3 flex items-center text-xs text-gray-400">%</span>
                </div>
              </div>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="rounded-md bg-red-50 p-4 border border-red-200 text-sm text-red-700 flex items-center space-x-2">
              <span className="text-red-500 font-bold">✕</span>
              <span>{error}</span>
            </div>
          )}

          {/* Action Button */}
          <div>
            <button
              type="submit"
              disabled={loading}
              className={`w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-base font-semibold text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition ${
                loading ? 'opacity-70 cursor-wait' : ''
              }`}
            >
              {loading ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Processing Agricultural Model...
                </>
              ) : (
                'Generate Recommendation'
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Prediction Output Section */}
      <FertilizerCard result={result} onReset={handleReset} />

      {/* Mandatory Agricultural Disclaimer */}
      <FertilizerDisclaimer />
    </main>
  );
}
