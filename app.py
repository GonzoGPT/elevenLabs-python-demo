import asyncio
import base64
import json
import os
import time
import websockets
import soundfile as sf
from datetime import datetime
import numpy as np
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение переменных окружения
API_KEY = os.getenv("API_KEY")
AGENT_ID = os.getenv("AGENT_ID")
WEBSOCKET_BASE_URI = os.getenv("WEBSOCKET_BASE_URI")
INPUT_AUDIO_FILE = os.getenv("INPUT_AUDIO_FILE", "input.wav") # Значение по умолчанию, если не задано
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
LOG_DIR = os.getenv("LOG_DIR", "log")

# Проверка наличия обязательных переменных
if not API_KEY or not AGENT_ID or not WEBSOCKET_BASE_URI:
    print("Ошибка: Не заданы обязательные переменные окружения API_KEY, AGENT_ID или WEBSOCKET_BASE_URI в файле .env")
    exit()

async def send_audio_and_receive_responses():
    # Создание директории для выходных файлов, если она не существует
    output_dir = OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    # Создание директории для логов, если она не существует
    log_dir = LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_filepath = os.path.join(log_dir, "websocket_log.txt")
    
    # Загрузка входного аудио файла
    try:
        audio_data, sample_rate = sf.read(INPUT_AUDIO_FILE)
        print(f"Аудиофайл загружен: {len(audio_data)} сэмплов, частота дискретизации {sample_rate} Гц")
    except Exception as e:
        print(f"Ошибка при загрузке входного аудиофайла '{INPUT_AUDIO_FILE}': {e}")
        return
    
    # Установка WebSocket соединения
    uri = f"{WEBSOCKET_BASE_URI}?agent_id={AGENT_ID}"
    try:
        async with websockets.connect(uri, additional_headers={"xi-api-key": API_KEY}) as websocket:
            print("WebSocket соединение установлено")
            
            # Подготовка и отправка аудиофайла
            audio_bytes = audio_data.tobytes()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Создание сообщения для отправки (формат может отличаться в зависимости от вашего API)
            message = {
                "audio": audio_base64,
                "sample_rate": sample_rate
            }
            
            await websocket.send(json.dumps(message))
            print("Аудиофайл отправлен")
            
            # Получение и обработка ответов
            while True:
                try:
                    response = await websocket.recv()
                    print(f"Получено сообщение: {response}") # Логирование сырого сообщения

                    try:
                        response_data = json.loads(response)
                        print(f"Распарсенные данные: {response_data}") # Логирование распарсенных данных

                        # Сохранение JSON в лог-файл
                        try:
                            timestamp_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                            with open(log_filepath, "a", encoding="utf-8") as log_file:
                                log_file.write(f"{timestamp_log} - {response}\n")
                        except Exception as log_e:
                            print(f"Ошибка при записи в лог-файл: {log_e}")

                        # Пример обработки разных типов сообщений (адаптируйте под ваше API)
                        if "type" in response_data:
                            message_type = response_data["type"]
                            if message_type == "ping":
                                print("Получен ping, отправка pong...")
                                # Отправка pong, если требуется API (проверьте документацию)
                                # await websocket.send(json.dumps({"type": "pong", ...})) 
                                continue # Пропустить остальную обработку для ping
                            elif message_type == "user_transcript":
                                print(f"Транскрипция пользователя: {response_data.get('user_transcription_event', {}).get('user_transcript', 'N/A')}")
                            elif message_type == "agent_response":
                                print(f"Ответ агента: {response_data.get('agent_response_event', {}).get('agent_response', 'N/A')}")
                            # Добавьте другие типы по необходимости
                        
                        # Извлечение аудио из ответа
                        # Проверяем новую структуру: {"audio_event": {"audio_base_64": "..."}}
                        if "audio_event" in response_data and isinstance(response_data["audio_event"], dict) and "audio_base_64" in response_data["audio_event"] and response_data["audio_event"]["audio_base_64"]:
                            audio_base64 = response_data["audio_event"]["audio_base_64"]
                            try:
                                audio_bytes = base64.b64decode(audio_base64)
                                
                                # Преобразование байтов в массив PCM (int16)
                                audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
                                
                                # Создание имени файла с временной меткой
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                                filepath = os.path.join(output_dir, f"{timestamp}.wav")
                                
                                # Сохраняем аудио в WAV файл с параметрами PCM (16kHz, 16-bit)
                                sf.write(filepath, audio_array, 16000, subtype='PCM_16')
                                print(f"Сохранено аудио в {filepath}")
                            except base64.binascii.Error as b64_error:
                                print(f"Ошибка декодирования Base64: {b64_error}")
                            except Exception as audio_e:
                                print(f"Ошибка при обработке или сохранении аудио: {audio_e}")
                        
                        # Проверка завершения сессии или другой логики завершения
                        if "is_final" in response_data and response_data["is_final"]:
                            print("Получен финальный ответ, завершение сессии")
                            break
                    
                    except json.JSONDecodeError:
                        print("Не удалось распарсрить JSON из сообщения")
                        # Обработка не-JSON сообщений, если они ожидаются

                except websockets.exceptions.ConnectionClosed:
                    print("Соединение WebSocket закрыто")
                    break
                except Exception as e:
                    print(f"Ошибка при обработке ответа: {e}")
                    break
    
    except Exception as e:
        print(f"Ошибка при установке WebSocket соединения: {e}")

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(send_audio_and_receive_responses()) 