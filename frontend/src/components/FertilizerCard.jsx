import React from 'react';

export default function FertilizerCard({ result, onReset }) {
  if (!result) return null;

  const { prediction, model_version, created_at, input_summary } = result;

  return (
    <div className="bg-white rounded-xl border border-emerald-200 shadow-md p-6 mt-8">
      <div className="flex items-center justify-between border-b border-gray-100 pb-4">
        <div>
          <span className="text-xs uppercase tracking-wider font-semibold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-full">
            Recommended Fertilizer Category
          </span>
          <h2 className="text-3xl font-extrabold text-gray-900 mt-2 flex items-center">
            🧪 {prediction}
          </h2>
        </div>
        <button
          onClick={onReset}
          className="text-sm font-medium text-gray-500 hover:text-emerald-700 bg-gray-50 hover:bg-emerald-50 px-3 py-1.5 rounded-lg border border-gray-200 transition"
        >
          New Recommendation ↻
        </button>
      </div>

      <div className="mt-6">
        <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Evaluation Context (Input Parameters)</h4>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-3">
          <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
            <span className="text-xs text-gray-500 block">Soil Type</span>
            <span className="text-sm font-bold text-gray-800">{input_summary?.soil_type || '—'}</span>
          </div>
          <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
            <span className="text-xs text-gray-500 block">Crop Type</span>
            <span className="text-sm font-bold text-gray-800">{input_summary?.crop_type || '—'}</span>
          </div>
          <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
            <span className="text-xs text-gray-500 block">Nitrogen (N)</span>
            <span className="text-sm font-bold text-gray-800">{input_summary?.nitrogen}</span>
          </div>
          <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
            <span className="text-xs text-gray-500 block">Phosphorous (P)</span>
            <span className="text-sm font-bold text-gray-800">{input_summary?.phosphorous}</span>
          </div>
          <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
            <span className="text-xs text-gray-500 block">Potassium (K)</span>
            <span className="text-sm font-bold text-gray-800">{input_summary?.potassium}</span>
          </div>
          <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
            <span className="text-xs text-gray-500 block">Temperature</span>
            <span className="text-sm font-bold text-gray-800">{input_summary?.temperature}°C</span>
          </div>
          <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
            <span className="text-xs text-gray-500 block">Humidity</span>
            <span className="text-sm font-bold text-gray-800">{input_summary?.humidity}%</span>
          </div>
          <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
            <span className="text-xs text-gray-500 block">Moisture</span>
            <span className="text-sm font-bold text-gray-800">{input_summary?.moisture}%</span>
          </div>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap justify-between items-center text-xs text-gray-400 border-t border-gray-100 pt-3">
        <span>Model Version: {model_version}</span>
        <span>Generated: {new Date(created_at).toLocaleString()}</span>
      </div>
    </div>
  );
}
