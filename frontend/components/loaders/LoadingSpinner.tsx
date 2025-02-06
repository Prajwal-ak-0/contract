import React from 'react';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="fixed inset-0 bg-transparent z-50">
      <div className="flex flex-col items-center justify-center min-h-screen">
        <div className="relative">
          {/* Outer ring */}
          <div className="w-16 h-16 border-4 border-gray-200 rounded-full animate-spin">
          </div>
          {/* Inner ring */}
          <div className="absolute top-0 left-0 w-16 h-16 border-4 border-t-gray-900 rounded-full animate-spin" 
               style={{ animationDuration: '0.6s' }}>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;