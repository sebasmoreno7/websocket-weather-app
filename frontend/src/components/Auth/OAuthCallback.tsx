// src/components/Auth/OAuthCallback.tsx
import React, { useEffect, useState } from 'react';

const OAuthCallback: React.FC = () => {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Procesando autenticación...');

  useEffect(() => {
    const handleOAuthCallback = async () => {
      try {
        setStatus('loading');
        setMessage('Procesando autenticación...');

        // En lugar de buscar código en query params, buscar tokens en el hash (flujo implícito)
        console.log('Full URL:', window.location.href);
        console.log('Hash:', window.location.hash);
        console.log('Search params:', window.location.search);
        
        // Intentar obtener tokens del hash primero (flujo implícito)
        const hashParams = new URLSearchParams(window.location.hash.substring(1));
        let accessToken = hashParams.get('access_token');
        let idToken = hashParams.get('id_token');
        let error = hashParams.get('error');
        
        // Si no hay tokens en el hash, intentar con query parameters (por si acaso)
        if (!accessToken && !error) {
          console.log('No tokens in hash, checking query params...');
          const queryParams = new URLSearchParams(window.location.search);
          accessToken = queryParams.get('access_token');
          idToken = queryParams.get('id_token');
          error = queryParams.get('error');
          
          // También verificar si hay un código de autorización (flujo de código)
          const authCode = queryParams.get('code');
          if (authCode && !accessToken) {
            console.log('Found authorization code, but we need access token for implicit flow');
            throw new Error('Received authorization code instead of access token. Please check OAuth configuration.');
          }
        }

        console.log('Access token:', accessToken);
        console.log('ID token:', idToken);
        console.log('Error:', error);

        if (error) {
          throw new Error(`OAuth error: ${error}`);
        }

        if (!accessToken) {
          throw new Error('No access token received. Hash: ' + window.location.hash + ' Search: ' + window.location.search);
        }

        // ID token es opcional para obtener información básica del usuario
        console.log('Proceeding with access token:', accessToken?.substring(0, 20) + '...');

        setMessage('Obteniendo información del usuario...');

        // Obtener información del usuario usando el access token
        const userResponse = await fetch(`https://www.googleapis.com/oauth2/v2/userinfo?access_token=${accessToken}`);

        if (!userResponse.ok) {
          const errorData = await userResponse.text();
          console.error('User info request failed:', errorData);
          throw new Error('Failed to get user information');
        }

        const userInfo = await userResponse.json();
        console.log('User info from Google:', userInfo);

        const user = {
          id: userInfo.id,
          name: userInfo.name,
          email: userInfo.email,
          picture: userInfo.picture,
          accessToken: accessToken
        };

        setStatus('success');
        setMessage('¡Autenticación exitosa! Redirigiendo...');

        // Enviar datos al parent
        if (window.opener) {
          console.log('Sending success message to parent with user:', user);
          window.opener.postMessage({
            type: 'GOOGLE_OAUTH_SUCCESS',
            user
          }, window.location.origin);
          
          // Delay más largo para asegurar que el mensaje se procese
          setTimeout(() => {
            console.log('Closing OAuth popup window');
            window.close();
          }, 2000);
        } else {
          console.error('No window.opener found');
          setTimeout(() => {
            window.close();
          }, 3000);
        }

      } catch (error) {
        console.error('OAuth callback error:', error);
        setStatus('error');
        setMessage(`Error: ${error instanceof Error ? error.message : 'Error desconocido'}`);

        if (window.opener) {
          console.log('Sending error message to parent:', error);
          window.opener.postMessage({
            type: 'GOOGLE_OAUTH_ERROR',
            error: error instanceof Error ? error.message : 'Error desconocido'
          }, window.location.origin);
          
          setTimeout(() => {
            console.log('Closing OAuth popup window after error');
            window.close();
          }, 3000);
        } else {
          console.error('No window.opener found for error handling');
          setTimeout(() => {
            window.close();
          }, 3000);
        }
      }
    };

    handleOAuthCallback();
  }, []);

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      backgroundColor: '#f0f2f5',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        backgroundColor: 'white',
        padding: '40px',
        borderRadius: '12px',
        boxShadow: '0 4px 16px rgba(0,0,0,0.1)',
        textAlign: 'center',
        maxWidth: '400px',
        width: '100%'
      }}>
        {status === 'loading' && (
          <>
            <div style={{
              width: '40px',
              height: '40px',
              border: '4px solid #f3f3f3',
              borderTop: '4px solid #4285f4',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              margin: '0 auto 20px'
            }} />
            <h2 style={{ color: '#333', marginBottom: '10px' }}>Autenticando...</h2>
          </>
        )}
        
        {status === 'success' && (
          <>
            <div style={{ fontSize: '48px', marginBottom: '20px' }}>✅</div>
            <h2 style={{ color: '#4CAF50', marginBottom: '10px' }}>¡Éxito!</h2>
          </>
        )}
        
        {status === 'error' && (
          <>
            <div style={{ fontSize: '48px', marginBottom: '20px' }}>❌</div>
            <h2 style={{ color: '#f44336', marginBottom: '10px' }}>Error</h2>
          </>
        )}
        
        <p style={{ color: '#666', fontSize: '14px' }}>{message}</p>
      </div>

      <style dangerouslySetInnerHTML={{
        __html: `
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `
      }} />
    </div>
  );
};

export default OAuthCallback;