import unittest
from unittest.mock import patch

from app.core.settings import settings
from app.services.weather_service import WeatherService
from app.services.websocket_manager import WebSocketManager


class FakeWebSocket:
    def __init__(self, fail_on_send=False):
        self.fail_on_send = fail_on_send
        self.accepted = False
        self.messages = []

    async def accept(self):
        self.accepted = True

    async def send_text(self, text):
        if self.fail_on_send:
            raise RuntimeError("connection closed")
        self.messages.append(text)


class WebSocketManagerTests(unittest.IsolatedAsyncioTestCase):
    async def test_failed_welcome_does_not_leave_a_stale_observer(self):
        manager = WebSocketManager()
        socket = FakeWebSocket(fail_on_send=True)

        with self.assertRaises(RuntimeError):
            await manager.connect_observer(socket)

        self.assertTrue(socket.accepted)
        self.assertEqual(manager.get_observer_count(), 0)

    async def test_successful_connection_receives_welcome_and_broadcast(self):
        manager = WebSocketManager()
        socket = FakeWebSocket()

        await manager.connect_observer(socket)
        await manager.broadcast_to_observers({"message": "weather update"})

        self.assertEqual(manager.get_observer_count(), 1)
        self.assertEqual(len(socket.messages), 2)


class WeatherServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_weather_request_has_a_bounded_timeout(self):
        class Response:
            status = 200

            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

            async def json(self):
                return {
                    "main": {"temp": 18.4, "humidity": 65},
                    "weather": [{"description": "nublado"}],
                }

        class Session:
            timeout = None

            def __init__(self, timeout):
                Session.timeout = timeout

            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

            def get(self, url, params):
                return Response()

        with patch.object(settings, "OPENWEATHER_API_KEY", "test-key"):
            with patch("app.services.weather_service.aiohttp.ClientSession", Session):
                weather = await WeatherService.get_real_weather_data("bogota")

        self.assertEqual(Session.timeout.total, 10)
        self.assertTrue(weather.real_data)
        self.assertEqual(weather.temperature, 18)

    async def test_unknown_city_is_not_sent_upstream(self):
        self.assertIsNone(await WeatherService.get_real_weather_data("unknown"))


if __name__ == "__main__":
    unittest.main()
