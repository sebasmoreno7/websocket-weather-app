"""
Chat service for handling intelligent question processing
"""
import logging
from typing import Dict, Any
from app.models.weather import ChatResponse
from app.services.weather_service import WeatherService
from app.utils.helpers import (
    get_colombia_time, 
    get_humidity_description,
    get_detailed_clothing_advice,
    get_activity_suggestions
)
from app.core.settings import settings

logger = logging.getLogger(__name__)

class ChatService:
    """Service for intelligent chat message processing"""
    
    @staticmethod
    async def handle_chat_message(content: str) -> Dict[str, Any]:
        """Sistema inteligente de procesamiento de preguntas con múltiples categorías"""
        content_lower = content.lower().strip()
        colombia_time = get_colombia_time()
        
        # === 1. PREGUNTAS SOBRE CLIMA ===
        if any(word in content_lower for word in ["temperatura", "temperature", "clima", "weather", "calor", "frio", "frío", "grados"]):
            return await ChatService._handle_weather_questions(content_lower, colombia_time)
        
        # === 2. PREGUNTAS SOBRE TIEMPO/HORA ===
        elif any(word in content_lower for word in ["hora", "time", "qué hora", "que hora", "horario"]):
            return {
                "type": "chat_response",
                "message": f"🕐 **Hora actual en Colombia:** {colombia_time.strftime('%H:%M:%S')}\n📍 Zona horaria: UTC-5 (Bogotá/Medellín)",
                "timestamp": colombia_time.isoformat()
            }
        
        # === 3. PREGUNTAS SOBRE FECHA ===
        elif any(word in content_lower for word in ["fecha", "date", "día", "dia", "hoy", "calendario"]):
            return ChatService._handle_date_questions(colombia_time)
        
        # === 4. PREGUNTAS SOBRE HUMEDAD ===
        elif any(word in content_lower for word in ["humedad", "humidity", "húmedo", "humedo", "vapor"]):
            return await ChatService._handle_humidity_questions(content_lower, colombia_time)
        
        # === 5. PREGUNTAS COMPARATIVAS ===
        elif any(word in content_lower for word in ["comparar", "compare", "diferencia", "más calor", "mas calor", "más frío", "mas frio", "versus", "vs", "entre"]):
            return await ChatService._handle_comparison_questions(content_lower, colombia_time)
        
        # === 6. PREGUNTAS DE SALUDO ===
        elif any(word in content_lower for word in ["hola", "hello", "hi", "hey", "buenos días", "buenas tardes", "buenas noches", "saludos"]):
            return ChatService._handle_greeting(colombia_time)
        
        # === 7. PREGUNTAS SOBRE AYUDA/COMANDOS ===
        elif any(word in content_lower for word in ["ayuda", "help", "que puedes hacer", "qué puedes hacer", "comandos", "opciones", "menu", "menú"]):
            return ChatService._get_help_message(colombia_time)
        
        # === 8. PREGUNTAS SOBRE UBICACIÓN ===
        elif any(word in content_lower for word in ["donde", "dónde", "ubicación", "location", "lugar", "ciudad", "coordenadas"]):
            return ChatService._get_location_info(colombia_time)
        
        # === 9. CONSEJOS DE VESTIMENTA ===
        elif any(word in content_lower for word in ["consejo", "recomendación", "que llevar", "qué llevar", "vestir", "ropa", "outfit"]):
            return await ChatService._handle_clothing_advice(content_lower, colombia_time)
        
        # === 10. PREGUNTAS SOBRE EL SISTEMA ===
        elif any(word in content_lower for word in ["robot", "sistema", "como funciona", "cómo funciona", "tecnología", "api"]):
            return ChatService._get_system_info(colombia_time)
        
        # === 11. PREGUNTAS SOBRE SALUD/ACTIVIDADES ===
        elif any(word in content_lower for word in ["ejercicio", "deporte", "correr", "caminar", "salir", "actividad"]):
            return await ChatService._handle_activity_suggestions(content_lower, colombia_time)
        
        # === 12. PREGUNTAS SOBRE PRONÓSTICO ===
        elif any(word in content_lower for word in ["pronóstico", "pronostico", "mañana", "después", "luego", "futuro"]):
            return {
                "type": "chat_response",
                "message": "🔮 **Pronóstico:** Actualmente solo proporciono datos en tiempo real. Para pronósticos, consulta:\n• IDEAM (Colombia): www.ideam.gov.co\n• Weather.com\n• AccuWeather\n\n¿Te ayudo con el clima actual?",
                "timestamp": colombia_time.isoformat()
            }
        
        # === 13. PREGUNTAS MATEMÁTICAS SIMPLES ===
        elif any(word in content_lower for word in ["suma", "resta", "diferencia de temperatura", "cuanto es", "cuánto es", "calcular"]):
            return await ChatService._handle_weather_calculations(content_lower, colombia_time)
        
        # === 14. PREGUNTAS SOBRE RECORD/EXTREMOS ===
        elif any(word in content_lower for word in ["máximo", "maximo", "mínimo", "minimo", "record", "récord", "extremo"]):
            return {
                "type": "chat_response",
                "message": f"🌡️ **Temperaturas históricas:**\n🏔️ **Bogotá**: Promedio {settings.CITIES['bogota']['avg_temp_range']} (altitud {settings.CITIES['bogota']['altitude']}m)\n🌺 **Medellín**: Promedio {settings.CITIES['medellin']['avg_temp_range']} (altitud {settings.CITIES['medellin']['altitude']}m)\n\n📊 Para datos históricos detallados, consulta IDEAM.\n¿Te ayudo con las temperaturas actuales?",
                "timestamp": colombia_time.isoformat()
            }
        
        # === 15. RESPUESTA POR DEFECTO INTELIGENTE ===
        else:
            return ChatService._get_default_response_with_suggestions(content, colombia_time)

    # === MÉTODOS PRIVADOS PARA MANEJAR CADA TIPO DE PREGUNTA ===
    
    @staticmethod
    async def _handle_weather_questions(content_lower: str, colombia_time) -> dict:
        """Maneja preguntas específicas sobre clima"""
        if "bogota" in content_lower or "bogotá" in content_lower:
            weather = await WeatherService.get_weather_data("bogota")
            return {
                "type": "chat_response",
                "message": f"""🏔️ **Clima en Bogotá:**
🌡️ **Temperatura:** {weather.temperature}°C
🌤️ **Condición:** {weather.description}
💧 **Humedad:** {weather.humidity}%
🕐 **Actualizado:** {weather.time}
📡 **Fuente:** {weather.source}
🏔️ **Altitud:** {weather.altitude} metros sobre el nivel del mar""",
                "timestamp": colombia_time.isoformat()
            }
        elif "medellin" in content_lower or "medellín" in content_lower:
            weather = await WeatherService.get_weather_data("medellin")  
            return {
                "type": "chat_response",
                "message": f"""🌺 **Clima en Medellín:**
🌡️ **Temperatura:** {weather.temperature}°C
🌤️ **Condición:** {weather.description}
💧 **Humedad:** {weather.humidity}%
🕐 **Actualizado:** {weather.time}
📡 **Fuente:** {weather.source}
🌸 **Altitud:** {weather.altitude} metros sobre el nivel del mar""",
                "timestamp": colombia_time.isoformat()
            }
        else:
            bogota = await WeatherService.get_weather_data("bogota")
            medellin = await WeatherService.get_weather_data("medellin")
            return {
                "type": "chat_response",
                "message": f"""🌤️ **Reporte climático completo:**

🏔️ **BOGOTÁ:**
   🌡️ {bogota.temperature}°C - {bogota.description}
   💧 Humedad: {bogota.humidity}%

🌺 **MEDELLÍN:**
   🌡️ {medellin.temperature}°C - {medellin.description}
   💧 Humedad: {medellin.humidity}%

🕐 **Actualizado:** {bogota.time} (Colombia)""",
                "timestamp": colombia_time.isoformat()
            }

    @staticmethod
    def _handle_date_questions(colombia_time) -> dict:
        """Maneja preguntas sobre fecha"""
        dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        
        dia_semana = dias[colombia_time.weekday()]
        mes = meses[colombia_time.month - 1]
        fecha_completa = f"{dia_semana}, {colombia_time.day} de {mes} de {colombia_time.year}"
        
        return {
            "type": "chat_response",
            "message": f"📅 **Fecha actual:** {fecha_completa}\n🇨🇴 Colombia (UTC-5)",
            "timestamp": colombia_time.isoformat()
        }

    @staticmethod
    async def _handle_humidity_questions(content_lower: str, colombia_time) -> dict:
        """Maneja preguntas específicas sobre humedad"""
        if "bogota" in content_lower or "bogotá" in content_lower:
            weather = await WeatherService.get_weather_data("bogota")
            humidity_level = get_humidity_description(weather.humidity)
            return {
                "type": "chat_response",
                "message": f"💧 **Humedad en Bogotá:** {weather.humidity}%\n📊 **Nivel:** {humidity_level}\n🌡️ **Temperatura:** {weather.temperature}°C",
                "timestamp": colombia_time.isoformat()
            }
        elif "medellin" in content_lower or "medellín" in content_lower:
            weather = await WeatherService.get_weather_data("medellin")
            humidity_level = get_humidity_description(weather.humidity)
            return {
                "type": "chat_response",
                "message": f"💧 **Humedad en Medellín:** {weather.humidity}%\n📊 **Nivel:** {humidity_level}\n🌡️ **Temperatura:** {weather.temperature}°C",
                "timestamp": colombia_time.isoformat()
            }
        else:
            bogota = await WeatherService.get_weather_data("bogota")
            medellin = await WeatherService.get_weather_data("medellin")
            return {
                "type": "chat_response",
                "message": f"""💧 **Comparación de humedad:**
🏔️ **Bogotá:** {bogota.humidity}% - {get_humidity_description(bogota.humidity)}
🌺 **Medellín:** {medellin.humidity}% - {get_humidity_description(medellin.humidity)}""",
                "timestamp": colombia_time.isoformat()
            }

    @staticmethod
    async def _handle_comparison_questions(content_lower: str, colombia_time) -> dict:
        """Maneja preguntas comparativas entre ciudades"""
        bogota = await WeatherService.get_weather_data("bogota")
        medellin = await WeatherService.get_weather_data("medellin")
        
        temp_diff = abs(bogota.temperature - medellin.temperature)
        humidity_diff = abs(bogota.humidity - medellin.humidity)
        
        warmer_city = "Medellín 🌺" if medellin.temperature > bogota.temperature else "Bogotá 🏔️"
        more_humid_city = "Medellín 🌺" if medellin.humidity > bogota.humidity else "Bogotá 🏔️"
        
        return {
            "type": "chat_response",
            "message": f"""📊 **Comparación climática detallada:**

🌡️ **Temperatura:**
   • {warmer_city} está {temp_diff}°C más caliente
   • Bogotá: {bogota.temperature}°C | Medellín: {medellin.temperature}°C

💧 **Humedad:**
   • {more_humid_city} es {humidity_diff}% más húmeda
   • Bogotá: {bogota.humidity}% | Medellín: {medellin.humidity}%

🏔️ **Diferencia de altitud:** 1,145 metros
🕐 **Actualizado:** {bogota.time}""",
            "timestamp": colombia_time.isoformat()
        }

    @staticmethod
    def _handle_greeting(colombia_time) -> dict:
        """Maneja saludos contextuales según la hora"""
        hour = colombia_time.hour
        if 5 <= hour < 12:
            greeting = "¡Buenos días! ☀️"
            time_context = "¡Perfecto para empezar el día!"
        elif 12 <= hour < 18:
            greeting = "¡Buenas tardes! 🌤️"  
            time_context = "¡Espero que tengas una excelente tarde!"
        else:
            greeting = "¡Buenas noches! 🌙"
            time_context = "¡Que tengas una linda noche!"
            
        return {
            "type": "chat_response",
            "message": f"""{greeting} {time_context}

🤖 Soy tu **Asistente Meteorológico Inteligente** para Colombia.

🎯 **¿En qué puedo ayudarte?**
• 🌡️ Clima actual de Bogotá y Medellín
• 💧 Niveles de humedad
• 📊 Comparaciones entre ciudades
• 👕 Recomendaciones de vestimenta
• 🕐 Hora y fecha actual

💡 **Escribe "ayuda" para ver todos los comandos disponibles.**""",
            "timestamp": colombia_time.isoformat()
        }

    @staticmethod
    def _get_help_message(colombia_time) -> dict:
        """Proporciona menú completo de ayuda"""
        return {
            "type": "chat_response",
            "message": f"""🤖 **MENÚ DE COMANDOS DISPONIBLES**

🌡️ **CLIMA:**
• "¿Qué temperatura hace en Bogotá?"
• "¿Cómo está el clima en Medellín?"
• "¿Qué temperatura hace?" (ambas ciudades)

💧 **HUMEDAD:**
• "¿Cuál es la humedad en Bogotá?"
• "¿Está muy húmedo en Medellín?"
• "¿Cómo está la humedad?" (comparación)

📊 **COMPARACIONES:**
• "Compara el clima de ambas ciudades"
• "¿Dónde hace más calor?"
• "¿Cuál es la diferencia de temperatura?"

🕐 **TIEMPO:**
• "¿Qué hora es?"
• "¿Qué día es hoy?"
• "¿En qué fecha estamos?"

👕 **RECOMENDACIONES:**
• "¿Qué me recomiendas llevar?"
• "¿Cómo debo vestirme para Bogotá?"
• "¿Qué ropa usar en Medellín?"

🏃 **ACTIVIDADES:**
• "¿Es buen día para hacer ejercicio?"
• "¿Puedo salir a correr?"

📍 **INFORMACIÓN:**
• "¿Dónde están ubicadas las ciudades?"
• "¿Cómo funciona el sistema?"

💡 **¡Prueba cualquiera de estos comandos!**""",
            "timestamp": colombia_time.isoformat()
        }

    @staticmethod
    def _get_location_info(colombia_time) -> dict:
        """Proporciona información detallada de ubicaciones"""
        bogota_info = settings.CITIES["bogota"]
        medellin_info = settings.CITIES["medellin"]
        
        return {
            "type": "chat_response",
            "message": f"""📍 **INFORMACIÓN DE UBICACIONES MONITOREADAS**

🏔️ **BOGOTÁ (Distrito Capital):**
   • **Coordenadas:** {bogota_info['lat']}°N, {bogota_info['lon']}°W
   • **Altitud:** {bogota_info['altitude']} metros sobre el nivel del mar
   • **Población:** ~8 millones (área metropolitana)
   • **Clima:** Subtropical de altitud (frío de montaña)
   • **Temperatura promedio:** {bogota_info['avg_temp_range']}

🌺 **MEDELLÍN (Antioquia):**
   • **Coordenadas:** {medellin_info['lat']}°N, {medellin_info['lon']}°W
   • **Altitud:** {medellin_info['altitude']} metros sobre el nivel del mar
   • **Población:** ~4 millones (área metropolitana)
   • **Clima:** Tropical de montaña (eterna primavera)
   • **Temperatura promedio:** {medellin_info['avg_temp_range']}

🌍 **Ambas ciudades están en zona horaria UTC-5**
📡 **Datos obtenidos en tiempo real de OpenWeatherMap API**""",
            "timestamp": colombia_time.isoformat()
        }

    @staticmethod
    async def _handle_clothing_advice(content_lower: str, colombia_time) -> dict:
        """Proporciona consejos personalizados de vestimenta"""
        if "bogota" in content_lower or "bogotá" in content_lower:
            weather = await WeatherService.get_weather_data("bogota")
            advice = get_detailed_clothing_advice(weather.temperature, weather.humidity, "bogota")
            return {
                "type": "chat_response",
                "message": f"""👕 **RECOMENDACIÓN PARA BOGOTÁ**
🌡️ **Temperatura:** {weather.temperature}°C
💧 **Humedad:** {weather.humidity}%

{advice}""",
                "timestamp": colombia_time.isoformat()
            }
        elif "medellin" in content_lower or "medellín" in content_lower:
            weather = await WeatherService.get_weather_data("medellin")
            advice = get_detailed_clothing_advice(weather.temperature, weather.humidity, "medellin")
            return {
                "type": "chat_response",
                "message": f"""👕 **RECOMENDACIÓN PARA MEDELLÍN**
🌡️ **Temperatura:** {weather.temperature}°C  
💧 **Humedad:** {weather.humidity}%

{advice}""",
                "timestamp": colombia_time.isoformat()
            }
        else:
            bogota = await WeatherService.get_weather_data("bogota")
            medellin = await WeatherService.get_weather_data("medellin")
            advice_bog = get_detailed_clothing_advice(bogota.temperature, bogota.humidity, "bogota")
            advice_med = get_detailed_clothing_advice(medellin.temperature, medellin.humidity, "medellin")
            
            return {
                "type": "chat_response",
                "message": f"""👕 **RECOMENDACIONES DE VESTIMENTA**

🏔️ **BOGOTÁ ({bogota.temperature}°C):**
{advice_bog}

🌺 **MEDELLÍN ({medellin.temperature}°C):**
{advice_med}""",
                "timestamp": colombia_time.isoformat()
            }

    @staticmethod
    def _get_system_info(colombia_time) -> dict:
        """Proporciona información técnica del sistema"""
        return {
            "type": "chat_response",
            "message": f"""🤖 **INFORMACIÓN DEL SISTEMA**

⚡ **Tecnología:**
• Backend: Python + FastAPI + WebSockets
• Frontend: React + TypeScript
• API Externa: OpenWeatherMap (datos reales)
• Comunicación: WebSocket en tiempo real

🔄 **Funcionamiento:**
• Los robots obtienen datos cada {settings.ROBOT_INTERVALS['bogota']}s (Bogotá) y {settings.ROBOT_INTERVALS['medellin']}s (Medellín)
• Datos reales de temperatura, humedad y condiciones
• Sistema de fallback a datos simulados
• Zona horaria de Colombia (UTC-5)

📡 **Fuentes de datos:**
• OpenWeatherMap API (datos meteorológicos)
• Coordenadas precisas de ambas ciudades
• Actualización automática en tiempo real

🛡️ **Características:**
• Reconexión automática de WebSocket
• Manejo inteligente de errores
• Múltiples usuarios simultáneos
• Autenticación con Google OAuth

💡 **¿Tienes alguna pregunta técnica específica?**""",
            "timestamp": colombia_time.isoformat()
        }

    @staticmethod
    async def _handle_activity_suggestions(content_lower: str, colombia_time) -> dict:
        """Proporciona sugerencias de actividades según el clima"""
        if "bogota" in content_lower or "bogotá" in content_lower:
            weather = await WeatherService.get_weather_data("bogota")
            suggestions = get_activity_suggestions(weather.temperature, weather.humidity, weather.description, "bogota")
            return {
                "type": "chat_response",
                "message": f"""🏃 **ACTIVIDADES RECOMENDADAS PARA BOGOTÁ**
🌡️ **Condiciones:** {weather.temperature}°C, {weather.description}

{suggestions}""",
                "timestamp": colombia_time.isoformat()
            }
        elif "medellin" in content_lower or "medellín" in content_lower:
            weather = await WeatherService.get_weather_data("medellin")
            suggestions = get_activity_suggestions(weather.temperature, weather.humidity, weather.description, "medellin")
            return {
                "type": "chat_response",
                "message": f"""🏃 **ACTIVIDADES RECOMENDADAS PARA MEDELLÍN**  
🌡️ **Condiciones:** {weather.temperature}°C, {weather.description}

{suggestions}""",
                "timestamp": colombia_time.isoformat()
            }
        else:
            bogota = await WeatherService.get_weather_data("bogota")
            medellin = await WeatherService.get_weather_data("medellin")
            
            suggestions_bog = get_activity_suggestions(bogota.temperature, bogota.humidity, bogota.description, "bogota")
            suggestions_med = get_activity_suggestions(medellin.temperature, medellin.humidity, medellin.description, "medellin")
            
            return {
                "type": "chat_response",
                "message": f"""🏃 **ACTIVIDADES RECOMENDADAS**

🏔️ **BOGOTÁ ({bogota.temperature}°C):**
{suggestions_bog}

🌺 **MEDELLÍN ({medellin.temperature}°C):**
{suggestions_med}""",
                "timestamp": colombia_time.isoformat()
            }

    @staticmethod
    async def _handle_weather_calculations(content_lower: str, colombia_time) -> dict:
        """Maneja cálculos simples relacionados con el clima"""
        bogota = await WeatherService.get_weather_data("bogota")
        medellin = await WeatherService.get_weather_data("medellin")
        
        temp_diff = abs(bogota.temperature - medellin.temperature)
        temp_avg = round((bogota.temperature + medellin.temperature) / 2, 1)
        humidity_diff = abs(bogota.humidity - medellin.humidity)
        humidity_avg = round((bogota.humidity + medellin.humidity) / 2, 1)
        
        return {
            "type": "chat_response",
            "message": f"""🧮 **CÁLCULOS CLIMÁTICOS**

🌡️ **Temperaturas:**
• Diferencia: {temp_diff}°C
• Promedio: {temp_avg}°C
• Bogotá: {bogota.temperature}°C | Medellín: {medellin.temperature}°C

💧 **Humedad:**
• Diferencia: {humidity_diff}%
• Promedio: {humidity_avg}%
• Bogotá: {bogota.humidity}% | Medellín: {medellin.humidity}%

📊 **Conversiones útiles:**
• Bogotá en Fahrenheit: {round(bogota.temperature * 9/5 + 32, 1)}°F
• Medellín en Fahrenheit: {round(medellin.temperature * 9/5 + 32, 1)}°F""",
            "timestamp": colombia_time.isoformat()
        }

    @staticmethod
    def _get_default_response_with_suggestions(original_content: str, colombia_time) -> dict:
        """Respuesta por defecto inteligente con sugerencias contextuales"""
        return {
            "type": "chat_response",
            "message": f"""🤖 No reconocí tu pregunta: "{original_content}"

💡 **PERO PUEDO AYUDARTE CON:**

🌡️ **Clima actual:** "¿Qué temperatura hace?"
💧 **Humedad:** "¿Cómo está la humedad?"
📊 **Comparaciones:** "Compara el clima"
👕 **Vestimenta:** "¿Qué me recomiendas llevar?"
🏃 **Actividades:** "¿Es buen día para ejercicio?"
🕐 **Tiempo:** "¿Qué hora es?"
📍 **Ubicaciones:** "¿Dónde están las ciudades?"
❓ **Ayuda completa:** "ayuda"

🎯 **EJEMPLOS ESPECÍFICOS:**
• "¿Hace calor en Medellín?"
• "¿Necesito chaqueta en Bogotá?"
• "¿Dónde llueve más?"
• "¿Puedo salir a correr?"

💬 **¡Intenta una de estas preguntas!**""",
            "timestamp": colombia_time.isoformat()
        }
