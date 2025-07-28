// src/hooks/useAuth.ts
import { useState, useEffect, useCallback } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  picture: string;
  accessToken: string;
}

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true); // Cambiar a true para mostrar loading inicial

  // Check if user is already logged in (from localStorage)
  useEffect(() => {
    // Check for existing user in localStorage
    const savedUser = localStorage.getItem('googleUser');
    if (savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        console.log('Restored user from localStorage:', userData);
        setUser(userData);
      } catch (error) {
        console.error('Error parsing saved user data:', error);
        localStorage.removeItem('googleUser');
      }
    }
    setLoading(false);
  }, []);

  // Additional effect to log user state changes
  useEffect(() => {
    console.log('User state changed:', user ? `Logged in as ${user.name}` : 'Not logged in');
  }, [user]);

  const loginWithGoogle = useCallback(() => {
    setLoading(true);
    
    // Google OAuth configuration - usando flujo implícito para frontend
    const CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID || ''; 
    const REDIRECT_URI = window.location.origin + '/oauth/callback';
    const SCOPE = 'openid email profile';
    
    console.log('Starting OAuth with:', {
      CLIENT_ID: CLIENT_ID.substring(0, 20) + '...',
      REDIRECT_URI,
      SCOPE
    });
    
    // Usar response_type=token para flujo implícito (más simple)
    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?` +
      `client_id=${CLIENT_ID}&` +
      `redirect_uri=${encodeURIComponent(REDIRECT_URI)}&` +
      `response_type=token&` +
      `scope=${encodeURIComponent(SCOPE)}`;
    
    console.log('Auth URL:', authUrl);
    
    // Open Google OAuth in popup
    const popup = window.open(
      authUrl,
      'google-oauth',
      'width=500,height=600,scrollbars=yes,resizable=yes'
    );

    // Listen for popup messages
    const handleMessage = (event: MessageEvent) => {
      if (event.origin !== window.location.origin) return;
      
      if (event.data.type === 'GOOGLE_OAUTH_SUCCESS') {
        const userData = event.data.user;
        console.log('OAuth Success - User data received:', userData);
        
        // Actualizar estado inmediatamente
        setUser(userData);
        localStorage.setItem('googleUser', JSON.stringify(userData));
        setLoading(false);
        
        // Cerrar popup después de un breve delay
        setTimeout(() => {
          popup?.close();
        }, 500);
        
        window.removeEventListener('message', handleMessage);
        
        // Forzar recarga de página después de login exitoso
        setTimeout(() => {
          console.log('Reloading page after successful login...');
          window.location.reload();
        }, 1000);
        
      } else if (event.data.type === 'GOOGLE_OAUTH_ERROR') {
        console.error('OAuth Error:', event.data.error);
        setLoading(false);
        popup?.close();
        window.removeEventListener('message', handleMessage);
      }
    };

    window.addEventListener('message', handleMessage);

    // Handle popup closed manually
    const checkClosed = setInterval(() => {
      if (popup?.closed) {
        setLoading(false);
        clearInterval(checkClosed);
        window.removeEventListener('message', handleMessage);
      }
    }, 1000);
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem('googleUser');
  }, []);

  return {
    user,
    loading,
    loginWithGoogle,
    logout,
    isAuthenticated: !!user
  };
};
