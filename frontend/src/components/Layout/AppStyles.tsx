// src/components/Layout/AppStyles.tsx
import React from 'react';

const AppStyles: React.FC = () => {
  return (
    <style>{`
      @keyframes slideIn {
        from {
          transform: translateX(100%);
          opacity: 0;
        }
        to {
          transform: translateX(0);
          opacity: 1;
        }
      }
    `}</style>
  );
};

export default AppStyles;
