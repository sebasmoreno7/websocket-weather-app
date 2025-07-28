# Advanced WebSocket Server - Arquitectura Modular

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación principal FastAPI
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuración centralizada
│   │   └── logging.py         # Setup de logging
│   ├── models/
│   │   ├── __init__.py
│   │   ├── message.py         # Modelo de mensajes
│   │   ├── connection.py      # Modelo de conexiones
│   │   └── room.py           # Modelo de salas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── room_manager.py    # Gestor de salas
│   │   ├── websocket_service.py # Servicio WebSocket
│   │   └── heartbeat_service.py # Servicio de heartbeat
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── websocket.py       # Rutas WebSocket
│   │   └── api.py            # Rutas REST API
│   └── utils/
│       ├── __init__.py
│       └── auth.py           # Utilidades de autenticación
├── main_new.py               # Punto de entrada
├── requirements.txt
└── README.md
```

## Características

### 🏗️ Arquitectura Modular
- **Separación de responsabilidades**: Cada módulo tiene una función específica
- **Inyección de dependencias**: Servicios globales reutilizables
- **Configuración centralizada**: Todas las configuraciones en un solo lugar

### 🔐 Seguridad
- **Autenticación por token**: Validación de tokens para conexiones WebSocket
- **Validación de client_id**: Evita duplicados y formatos inválidos
- **Manejo de errores**: Códigos de error específicos para diferentes situaciones

### 📊 Gestión Avanzada
- **Historial de mensajes**: Últimos 50 mensajes por sala (configurable)
- **Estadísticas detalladas**: Tiempo de conexión, actividad, etc.
- **Heartbeat automático**: Verificación de estado cada 20 segundos

### 🚀 APIs REST
- `GET /api/v1/` - Información del servidor
- `GET /api/v1/status` - Estado detallado de todas las salas
- `GET /api/v1/messages/{room_id}` - Historial de mensajes
- `POST /api/v1/broadcast/{room_id}` - Enviar mensaje desde servidor
- `GET /api/v1/rooms` - Lista de salas activas
- `GET /api/v1/rooms/{room_id}/connections` - Conexiones de una sala

### 🔌 WebSocket
- `WS /ws/{room_id}?client_id=xxx&token=xxx` - Conexión WebSocket

## Uso

### Iniciar el servidor
```bash
python main_new.py
```

### Conectar por WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/robots?client_id=RobotA&token=abc123');
```

### Obtener historial
```bash
curl http://localhost:8000/api/v1/messages/robots
```

### Enviar mensaje desde servidor
```bash
curl -X POST "http://localhost:8000/api/v1/broadcast/robots?token=abc123" \
     -H "Content-Type: application/json" \
     -d "Test message from server"
```

## Configuración

Edita `app/core/config.py` para modificar:
- Tokens válidos
- Intervalo de heartbeat
- Máximo de mensajes por sala
- Configuración de CORS
- Puertos y hosts

## Logs

El sistema incluye logging detallado con:
- 🏠 Creación/eliminación de salas
- ✅ Conexiones/desconexiones
- 📨 Mensajes enviados/recibidos
- 💓 Heartbeats automáticos
- ⚠️ Errores y advertencias
