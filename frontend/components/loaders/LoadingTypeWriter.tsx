import React, { useState, useEffect } from 'react';

const LoadingTypewriter: React.FC = () => {
  const [text, setText] = useState('');
  const fullText = "Extracting Information...";

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      if (index <= fullText.length) {
        setText(fullText.slice(0, index));
        index++;
      } else {
        clearInterval(interval);
      }
    }, 50);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-black text-white">
      <p className="text-lg font-semibold">{text}</p>
      <div className="w-4 h-4 bg-white rounded-full mt-4 animate-pulse"></div>
    </div>
  );
};

export default LoadingTypewriter;