import React, { useState, useEffect } from 'react';

const CircularProgress: React.FC = () => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) return 100;
        return prev + 1;
      });
    }, 30);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-black text-white">
      <svg className="w-24 h-24 transform -rotate-90">
        <circle
          cx="48"
          cy="48"
          r="44"
          fill="none"
          stroke="gray"
          strokeWidth="4"
        ></circle>
        <circle
          cx="48"
          cy="48"
          r="44"
          fill="none"
          stroke="white"
          strokeWidth="4"
          strokeDasharray="276.46"
          strokeDashoffset={276.46 - (276.46 * progress) / 100}
          className="transition-all duration-300"
        ></circle>
      </svg>
      <p className="mt-4 text-lg font-semibold">{progress}% Uploaded</p>
    </div>
  );
};

export default CircularProgress;