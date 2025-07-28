# 🌦️ WebSocket Weather App

Sistema de monitoreo meteorológico en tiempo real para Bogotá y Medellín con chat inteligente, autenticación OAuth y diseño responsivo.

## 🌐 Demo en Vivo

**🚀 Prueba la aplicación aquí:** [https://websocket-weather-app-lqpu.vercel.app/](https://websocket-weather-app-lqpu.vercel.app/)

- **Frontend**: Desplegado en **Vercel**
- **Backend**: Desplegado en **Render**
- **Datos**: Simulados en tiempo real (sin necesidad de APIs)

## ✨ Características

- **📡 Datos en tiempo real**: OpenWeatherMap API con fallback a datos simulados
- **🤖 Chat inteligente**: Asistente meteorológico con 15+ tipos de preguntas
- **🔐 Autenticación**: Google OAuth integrada
- **📱 Responsive**: Interfaz adaptable a móviles y desktop
- **⚡ WebSocket**: Comunicación bidireccional en tiempo real
- **🏗️ Arquitectura modular**: Backend organizado con mejores prácticas

## 🚀 Instalación y Ejecución Local

### Prerrequisitos

- **Python 3.8+** (recomendado 3.11+)
- **Node.js 16+** y **npm**
- **Git**

### 📋 Paso a Paso

#### 1. Clonar el repositorio
```bash
git clone https://github.com/sebasmoreno7/websocket-weather-app.git
cd websocket-weather-app
```

#### 2. Configurar el Backend (FastAPI + Python)

```bash
# Ir al directorio del backend
cd backend

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo de variables de entorno (opcional)
echo "OPENWEATHER_API_KEY=tu_api_key_aqui" > .env
```

#### 3. Configurar el Frontend (React + TypeScript)

```bash
# Abrir nueva terminal y ir al directorio del frontend
cd frontend

# Instalar dependencias
npm install
```

#### 4. Ejecutar la aplicación

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
python main.py
```
El backend estará disponible en: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```
La aplicación web estará disponible en: http://localhost:3000

### 🌐 URLs Importantes

**🌍 Producción:**
- **Aplicación en vivo**: https://websocket-weather-app-lqpu.vercel.app/

**🏠 Desarrollo local:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws/observer

## 🚀 Despliegue

### Producción Actual
- **Frontend**: Desplegado en **Vercel** (automático desde GitHub)
- **Backend**: Desplegado en **Render** (automático desde GitHub)
- **CI/CD**: Despliegue automático en cada push a `main`

### Desplegar tu propia versión

#### Frontend en Vercel
1. Fork este repositorio
2. Conecta tu GitHub a [Vercel](https://vercel.com)
3. Importa el proyecto
4. Configura el directorio raíz como `frontend`
5. Deploy automático ✅

#### Backend en Render
1. Conecta tu GitHub a [Render](https://render.com)
2. Crea un nuevo Web Service
3. Configura el directorio raíz como `backend`
4. Comando de build: `pip install -r requirements.txt`
5. Comando de inicio: `python main.py`
6. Deploy automático ✅

## 🔧 Configuración Opcional

### API Key de OpenWeatherMap

Para datos meteorológicos reales (opcional):

1. Regístrate en [OpenWeatherMap](https://openweathermap.org/api)
2. Obtén tu API Key gratuita
3. Crea el archivo `.env` en `backend/`:
```env
OPENWEATHER_API_KEY=tu_api_key_aqui
```

**Nota**: Sin API key, la aplicación usa datos simulados automáticamente.

### Google OAuth (opcional)

Para habilitar autenticación:

1. Configura un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilita Google+ API
3. Crea credenciales OAuth 2.0
4. Agrega `http://localhost:3000` a orígenes autorizados

## 💬 Uso del Chat Inteligente

Prueba estos comandos en el chat:

### 🌡️ Clima
- "¿Qué temperatura hace en Bogotá?"
- "¿Cómo está el clima en Medellín?"
- "¿Qué temperatura hace?" (ambas ciudades)

### 💧 Humedad
- "¿Cuál es la humedad en Bogotá?"
- "¿Está muy húmedo?"

### 📊 Comparaciones
- "Compara el clima de ambas ciudades"
- "¿Dónde hace más calor?"

### 👕 Recomendaciones
- "¿Qué me recomiendas llevar?"
- "¿Cómo debo vestirme para Bogotá?"

### 🏃 Actividades
- "¿Es buen día para hacer ejercicio?"
- "¿Puedo salir a correr?"

### ❓ Ayuda
- "ayuda" o "help" (lista completa de comandos)

## 🏗️ Arquitectura del Proyecto

```
websocket-weather-app/
├── backend/                 # FastAPI + Python
│   ├── app/
│   │   ├── core/           # Configuración
│   │   ├── services/       # Lógica de negocio
│   │   ├── api/            # Rutas y WebSockets
│   │   ├── models/         # Modelos Pydantic
│   │   └── utils/          # Utilidades
│   ├── main.py             # Punto de entrada
│   └── requirements.txt    # Dependencias Python
├── frontend/               # React + TypeScript
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── hooks/          # Custom hooks
│   │   └── types/          # Tipos TypeScript
│   └── package.json        # Dependencias Node.js
└── README.md
```

## 🛠️ Tecnologías

### Backend
- **FastAPI**: Framework web moderno y rápido
- **WebSockets**: Comunicación en tiempo real
- **Pydantic**: Validación de datos
- **aiohttp**: Cliente HTTP asíncrono
- **python-dotenv**: Variables de entorno

### Frontend
- **React 18**: Biblioteca de interfaz de usuario
- **TypeScript**: JavaScript con tipos
- **CSS3**: Estilos responsivos
- **WebSocket API**: Comunicación en tiempo real

## 🔍 Solución de Problemas

### Backend no inicia
```bash
# Verificar que el entorno virtual esté activado
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt

# Verificar imports
python -c "from app.core.settings import settings; print('✅ OK')"
```

### Frontend no carga
```bash
# Limpiar cache y reinstalar
rm -rf node_modules package-lock.json
npm install
npm start
```

### WebSocket no conecta
- Verificar que el backend esté ejecutándose en puerto 8000
- Revisar la consola del navegador para errores
- Verificar que no haya firewall bloqueando el puerto

## 📝 Licencia

MIT License - consulta el archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

---

**¿Necesitas ayuda?** Abre un [issue](https://github.com/sebasmoreno7/websocket-weather-app/issues) en GitHub.
