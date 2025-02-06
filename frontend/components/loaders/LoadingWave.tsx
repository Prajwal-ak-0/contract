import React from 'react';

const LoadingWave: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-black text-white">
      <div className="relative w-64 h-4 bg-gray-800 rounded-full overflow-hidden">
        <div className="absolute top-0 left-0 h-full bg-white animate-wave"></div>
      </div>
      <p className="mt-4 text-lg font-semibold">Processing Document...</p>
    </div>
  );
};

export default LoadingWave;