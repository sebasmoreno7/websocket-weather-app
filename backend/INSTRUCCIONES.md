# INSTRUCCIONES PARA EJECUTAR EL SERVIDOR MODULAR

## Pasos para ejecutar el servidor:

1. **Verificar que estés en el directorio correcto:**
   ```bash
   cd /home/sebas525/Desktop/arduron-ws-test/backend
   pwd  # Debe mostrar: /home/sebas525/Desktop/arduron-ws-test/backend
   ```

2. **Activar el entorno virtual (ejecutar manualmente en la terminal):**
   ```bash
   source venv/bin/activate
   ```
   
3. **Verificar que el entorno esté activo:**
   ```bash
   which python  # Debe mostrar una ruta que incluya 'venv'
   which uvicorn # Debe mostrar una ruta que incluya 'venv'
   ```

4. **Instalar dependencias (si es necesario):**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar el servidor:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Si hay problemas con el entorno virtual:

### Recrear el entorno virtual:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ejecutar sin entorno virtual (usando Python del sistema):
```bash
pip3 install fastapi uvicorn aiohttp python-dotenv
python3 main.py
```

## Verificar que el servidor esté funcionando:

1. **Abrir en el navegador:**
   - http://localhost:8000 (información del servidor)
   - http://localhost:8000/status (estado del servidor)

2. **Probar WebSocket con el frontend:**
   - El frontend debe conectarse a ws://localhost:8000/ws/observer

## Estructura modular implementada:

✅ **Configuración centralizada:** `app/core/settings.py`
✅ **Modelos de datos:** `app/models/weather.py`  
✅ **Servicios de negocio:** `app/services/`
✅ **Rutas de API:** `app/api/`
✅ **Utilidades:** `app/utils/helpers.py`
✅ **Aplicación principal:** `main.py`

## Beneficios de la arquitectura modular:

- **Mantenibilidad:** Código organizado en módulos específicos
- **Testabilidad:** Cada componente puede ser testado independientemente  
- **Escalabilidad:** Fácil agregar nuevas funcionalidades
- **Reutilización:** Componentes reutilizables
- **Configurabilidad:** Configuración centralizada en `settings.py`
