import React from 'react';

const LoadingDots: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-black text-white">
      <div className="flex space-x-2">
        <div className="w-3 h-3 bg-white rounded-full animate-bounce"></div>
        <div className="w-3 h-3 bg-white rounded-full animate-bounce [animation-delay:0.2s]"></div>
        <div className="w-3 h-3 bg-white rounded-full animate-bounce [animation-delay:0.4s]"></div>
      </div>
      <p className="mt-4 text-lg font-semibold">Extracting Information...</p>
    </div>
  );
};

export default LoadingDots;