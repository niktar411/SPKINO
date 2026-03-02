import os
import sys
import subprocess
import venv
import shutil
from pathlib import Path

def main():
    # Имя виртуального окружения
    venv_name = "fastproj"
    
    # Проверяем существование виртуального окружения
    if not os.path.exists(venv_name):
        print("Создание виртуального окружения...")
        venv.create(venv_name, with_pip=True)
        print(f"Виртуальное окружение '{venv_name}' создано.")
    else:
        print(f"Виртуальное окружение '{venv_name}' уже существует.")

    # Определяем путь к интерпретатору Python в виртуальном окружении
    python_executable = os.path.join(venv_name, "Scripts", "python.exe")
    pip_executable = os.path.join(venv_name, "Scripts", "pip.exe")

    # Проверяем существование requirements.txt
    requirements_file = "requirements.txt"

    # Устанавливаем зависимости
    print("Установка зависимостей...")
    try:
        subprocess.run(
            [python_executable, "-m", "pip", "install", "-r", requirements_file],
            check=True,
            capture_output=True,
            text=True
        )
        print("Зависимости успешно установлены.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке зависимостей:\n{e.stderr}")
        sys.exit(1)

    app_file = "main.py"

    # Запускаем приложение
    print("Запуск FastAPI приложения...")
    try:
        subprocess.run(
            [python_executable, "-m", "uvicorn", "main:app", "--reload"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Ошибка запуска приложения: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nПриложение остановлено пользователем.")
        sys.exit(0)

if __name__ == "__main__":
    main()