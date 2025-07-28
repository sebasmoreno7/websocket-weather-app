# 🔐 Configuración Google OAuth

## 📋 **Pasos para configurar Google OAuth**

### **1. Crear proyecto en Google Cloud Console**

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+ 

### **2. Configurar OAuth 2.0**

1. Ve a **APIs & Services > Credentials**
2. Clic en **"+ CREATE CREDENTIALS" > "OAuth client ID"**
3. Selecciona **"Web application"**
4. Configura:
   - **Name**: Weather Monitor App
   - **Authorized JavaScript origins**:
     - `http://localhost:3000`
     - `http://127.0.0.1:3000`
   - **Authorized redirect URIs**:
     - `http://localhost:3000/oauth/callback`
     - `http://127.0.0.1:3000/oauth/callback`

### **3. Configurar variables de entorno**

Copia tu **Client ID** y agrégalo al archivo `.env`:

```env
# WebSocket Server Configuration
REACT_APP_WS_URL=ws://localhost:8000/ws/observer

# Google OAuth Configuration
REACT_APP_GOOGLE_CLIENT_ID=1234567890-abcdefghijklmnop.apps.googleusercontent.com
```

### **4. Para modo DEMO (sin configurar Google)**

Si quieres probar sin configurar Google OAuth, puedes:

1. Usar el Client ID de demo en `.env`:
```env
REACT_APP_GOOGLE_CLIENT_ID=demo-client-id
```

2. El sistema mostrará un usuario demo automáticamente.

---

## 🌟 **Características del Login**

✅ **Popup OAuth**: Ventana emergente para autenticación  
✅ **Persistencia**: Sesión guardada en localStorage  
✅ **Perfil de usuario**: Muestra foto, nombre y email  
✅ **Logout**: Botón para cerrar sesión  
✅ **Responsive**: Funciona en móvil y desktop  
✅ **Loading states**: Indicadores de carga  
✅ **Error handling**: Manejo de errores OAuth  

---

## 🔄 **Flujo de autenticación**

1. Usuario hace clic en "Continuar con Google"
2. Se abre popup con OAuth de Google
3. Usuario autoriza la aplicación
4. Callback procesa la respuesta
5. Usuario autenticado accede al dashboard
6. WebSocket se conecta automáticamente

---

## 🛡️ **Seguridad**

- OAuth 2.0 estándar de Google
- Client ID público (normal para SPAs)
- No se almacenan contraseñas
- Token de acceso temporal
- Cierre de sesión local

---

## 🚀 **Para iniciar la app**

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend (nueva terminal)
cd frontend
npm start
```

La aplicación estará disponible en: `http://localhost:3000`
