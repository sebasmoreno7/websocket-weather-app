"""
Utility functions for date/time and general helpers
"""
from datetime import datetime, timezone, timedelta

def get_colombia_time() -> datetime:
    """Get current time in Colombia timezone (UTC-5)"""
    colombia_tz = timezone(timedelta(hours=-5))
    return datetime.now(colombia_tz)

def get_humidity_description(humidity: int) -> str:
    """Describe el nivel de humedad en términos comprensibles"""
    if humidity < 30:
        return "Muy seco"
    elif 30 <= humidity < 50:
        return "Seco"
    elif 50 <= humidity < 70:
        return "Cómodo"
    elif 70 <= humidity < 85:
        return "Húmedo"
    else:
        return "Muy húmedo"

def get_detailed_clothing_advice(temperature: int, humidity: int, city: str) -> str:
    """Consejos detallados de vestimenta considerando temperatura y humedad"""
    base_advice = ""
    
    # Consejos por temperatura
    if temperature < 10:
        base_advice = "🧥 **Ropa de abrigo:** Chaqueta gruesa, suéter, gorro y guantes"
    elif 10 <= temperature < 15:
        base_advice = "🧥 **Ropa abrigada:** Chaqueta o suéter, puede hacer frío"
    elif 15 <= temperature < 20:
        base_advice = "👕 **Ropa intermedia:** Camiseta de manga larga o suéter ligero"
    elif 20 <= temperature < 25:
        base_advice = "👕 **Ropa cómoda:** Camiseta, clima ideal para cualquier ropa"
    elif 25 <= temperature < 30:
        base_advice = "🩳 **Ropa ligera:** Shorts, camiseta fresca, ropa transpirable"
    else:
        base_advice = "🏖️ **Ropa muy ligera:** Ropa mínima, busca sombra y mantente hidratado"
    
    # Consejos adicionales por humedad
    humidity_advice = ""
    if humidity > 70:
        humidity_advice = "\n💧 **Alta humedad:** Usa ropa transpirable, evita telas sintéticas"
    elif humidity < 30:
        humidity_advice = "\n🏜️ **Baja humedad:** Usa crema hidratante, bebe mucha agua"
    
    # Consejos específicos por ciudad
    city_advice = ""
    if city == "bogota":
        city_advice = "\n🏔️ **Tip para Bogotá:** El clima cambia rápido, lleva una chaqueta extra"
    else:
        city_advice = "\n🌺 **Tip para Medellín:** Ciudad de eterna primavera, ropa ligera pero elegante"
    
    return base_advice + humidity_advice + city_advice

def get_activity_suggestions(temperature: int, humidity: int, description: str, city: str) -> str:
    """Sugerencias de actividades basadas en las condiciones climáticas"""
    activities = []
    
    # Actividades por temperatura
    if 15 <= temperature <= 25:
        activities.append("✅ **Perfecto para:** Correr, caminar, ciclismo")
        activities.append("🏃 **Ejercicio al aire libre:** Condiciones ideales")
    elif temperature < 15:
        activities.append("🏠 **Mejor interior:** Gimnasio, yoga, actividades en casa")
        activities.append("🧥 **Si sales:** Abrígate bien y calienta antes")
    elif temperature > 25:
        activities.append("🌅 **Ejercicio temprano:** Evita las horas de más calor")
        activities.append("💧 **Mantente hidratado:** Lleva agua extra")
    
    # Consideraciones por humedad
    if humidity > 75:
        activities.append("💦 **Alta humedad:** Ejercicio suave, evita sobresfuerzo")
    elif humidity < 40:
        activities.append("🏜️ **Baja humedad:** Bebe más agua, usa protector labial")
    
    # Consideraciones por condición climática
    if "lluvia" in description.lower():
        activities.append("☔ **Lluvia:** Actividades bajo techado")
    elif "despejado" in description.lower() or "soleado" in description.lower():
        activities.append("☀️ **Día despejado:** Perfecto para actividades al aire libre")
    
    return "\n".join(activities) if activities else "🤔 Condiciones variables, usa tu criterio"
