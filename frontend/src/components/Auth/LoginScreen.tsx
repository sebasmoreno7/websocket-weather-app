// src/components/Auth/LoginScreen.tsx
import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useResponsive } from '../../hooks/useResponsive';

const LoginScreen: React.FC = () => {
  const { loginWithGoogle, loading } = useAuth();
  const { mobile } = useResponsive();

  const handleGoogleLogin = () => {
    loginWithGoogle();
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      backgroundColor: '#f0f2f5',
      fontFamily: 'Arial, sans-serif',
      padding: mobile ? '10px' : '20px'
    }}>
      {/* Login Card */}
      <div style={{
        backgroundColor: 'white',
        padding: mobile ? '30px 20px' : '40px',
        borderRadius: '12px',
        boxShadow: '0 4px 16px rgba(0,0,0,0.1)',
        textAlign: 'center',
        maxWidth: mobile ? '350px' : '400px',
        width: '100%'
      }}>
        {/* Logo/Title */}
        <div style={{ marginBottom: mobile ? '25px' : '30px' }}>
          <h1 style={{ 
            margin: '0 0 10px 0', 
            color: '#1a73e8',
            fontSize: mobile ? 'clamp(24px, 6vw, 28px)' : '32px',
            fontWeight: 'bold'
          }}>
            🌦️ Weather Monitor
          </h1>
          <p style={{ 
            margin: '0', 
            color: '#666',
            fontSize: mobile ? 'clamp(14px, 3.5vw, 15px)' : '16px',
            lineHeight: '1.4'
          }}>
            Sistema de monitoreo meteorológico en tiempo real
          </p>
        </div>

        {/* Description */}
        <div style={{ marginBottom: '30px' }}>
          <p style={{ 
            color: '#333', 
            fontSize: '14px',
            lineHeight: '1.5',
            margin: '0'
          }}>
            Accede al sistema de monitoreo de clima para Bogotá y Medellín con datos en tiempo real.
          </p>
        </div>
        
        {/* Google Login Button */}
        <button
          onClick={handleGoogleLogin}
          disabled={loading}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '12px',
            width: '100%',
            padding: '14px 20px',
            backgroundColor: loading ? '#f8f9fa' : '#4285f4',
            color: loading ? '#666' : 'white',
            border: loading ? '1px solid #dadce0' : 'none',
            borderRadius: '8px',
            fontSize: '16px',
            fontWeight: '500',
            cursor: loading ? 'not-allowed' : 'pointer',
            transition: 'all 0.2s ease',
            boxShadow: loading ? 'none' : '0 2px 4px rgba(66,133,244,0.3)'
          }}
          onMouseOver={(e) => {
            if (!loading) {
              e.currentTarget.style.backgroundColor = '#3367d6';
              e.currentTarget.style.boxShadow = '0 4px 8px rgba(66,133,244,0.4)';
            }
          }}
          onMouseOut={(e) => {
            if (!loading) {
              e.currentTarget.style.backgroundColor = '#4285f4';
              e.currentTarget.style.boxShadow = '0 2px 4px rgba(66,133,244,0.3)';
            }
          }}
        >
          {/* Google Icon */}
          <svg width="20" height="20" viewBox="0 0 24 24">
            <path 
              fill={loading ? "#666" : "white"} 
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path 
              fill={loading ? "#666" : "white"} 
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path 
              fill={loading ? "#666" : "white"} 
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path 
              fill={loading ? "#666" : "white"} 
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          
          {loading ? 'Iniciando sesión...' : 'Continuar con Google'}
        </button>

        {/* Footer info */}
        <div style={{ 
          marginTop: '30px', 
          fontSize: '12px', 
          color: '#999',
          lineHeight: '1.4'
        }}>
          Al iniciar sesión, aceptas acceder al sistema de monitoreo meteorológico.
          <br />
          Tus datos están protegidos por Google OAuth 2.0.
        </div>
      </div>

      {/* Bottom info */}
      <div style={{ 
        marginTop: '20px', 
        fontSize: '14px', 
        color: '#666',
        textAlign: 'center'
      }}>
        <strong>Características:</strong>
        <br />
        📊 Datos en tiempo real • 🏔️ Bogotá • 🌺 Medellín • 💬 Chat interactivo
      </div>
    </div>
  );
};

export default LoginScreen;
