// src/hooks/useResponsive.ts
import { useState, useEffect } from 'react';

interface BreakpointValues {
  mobile: boolean;
  tablet: boolean;
  desktop: boolean;
  width: number;
}

export const useResponsive = (): BreakpointValues => {
  const [screenSize, setScreenSize] = useState<BreakpointValues>({
    mobile: false,
    tablet: false,
    desktop: false,
    width: 0
  });

  useEffect(() => {
    const updateScreenSize = () => {
      const width = window.innerWidth;
      setScreenSize({
        mobile: width < 768,
        tablet: width >= 768 && width < 1024,
        desktop: width >= 1024,
        width
      });
    };

    // Initialize
    updateScreenSize();

    // Add event listener
    window.addEventListener('resize', updateScreenSize);

    // Cleanup
    return () => window.removeEventListener('resize', updateScreenSize);
  }, []);

  return screenSize;
};

// Utility functions for responsive values
export const responsive = {
  // Responsive spacing
  spacing: (mobile: string, tablet: string, desktop: string, currentWidth: number) => {
    if (currentWidth < 768) return mobile;
    if (currentWidth < 1024) return tablet;
    return desktop;
  },
  
  // Responsive font sizes
  fontSize: (base: number, currentWidth: number) => {
    const scale = Math.max(0.8, Math.min(1.2, currentWidth / 1200));
    return `${base * scale}px`;
  },
  
  // Grid columns
  gridColumns: (currentWidth: number) => {
    if (currentWidth < 768) return '1fr';
    if (currentWidth < 1024) return '1fr';
    return '1fr 1fr';
  }
};
