from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# Настройка параметров Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Запуск в фоновом режиме
chrome_options.add_argument('--no-sandbox')  # Отключение песочницы
chrome_options.add_argument('--disable-dev-shm-usage')  # Отключение использования общего разделяемого хранилища
chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15')  # Установка пользовательского агента

# Создание экземпляра драйвера
driver = webdriver.Chrome(options=chrome_options)

def wait_and_find_element(by, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
    except TimeoutException:
        return None

try:
    # Шаг 1: Открытие главной страницы Одноклассников
    driver.get("https://ok.ru")
    print(f"Текущий URL: {driver.current_url}")
    print(f"Заголовок страницы: {driver.title}")
    assert "Одноклассники" in driver.title, "Неожиданный заголовок страницы"
    print("Шаг 1: Успешно открыта главная страница Одноклассников")

    # Шаг 2: Проверка наличия логотипа Одноклассников
    logo = wait_and_find_element(By.CSS_SELECTOR, "img[src*='ok-logo']")
    if logo:
        print("Шаг 2: Логотип Одноклассников найден")
    else:
        raise AssertionError("Логотип Одноклассников не найден")

    # Шаг 3: Проверка наличия формы входа
    login_form = wait_and_find_element(By.CSS_SELECTOR, "form#login-form")
    if login_form:
        print("Шаг 3: Форма входа найдена")
    else:
        raise AssertionError("Форма входа не найдена")

    # Шаг 4: Проверка наличия кнопки "Зарегистрироваться"
    register_button = wait_and_find_element(By.XPATH, "//a[contains(text(), 'Зарегистрироваться')]")
    if register_button:
        print("Шаг 4: Кнопка 'Зарегистрироваться' найдена")
    else:
        raise AssertionError("Кнопка 'Зарегистрироваться' не найдена")

    # Шаг 5: Проверка наличия ссылки на политику конфиденциальности
    privacy_link = wait_and_find_element(By.XPATH, "//a[contains(text(), 'Политика конфиденциальности')]")
    if privacy_link:
        print("Шаг 5: Ссылка на политику конфиденциальности найдена")
    else:
        raise AssertionError("Ссылка на политику конфиденциальности не найдена")

    # Шаг 6: Проверка наличия текста о безопасности
    security_text = wait_and_find_element(By.XPATH, "//*[contains(text(), 'безопасность')]")
    if security_text:
        print("Шаг 6: Найден текст о безопасности")
    else:
        raise AssertionError("Текст о безопасности не найден")

    print("Тест успешно завершен!")

except AssertionError as e:
    print(f"Тест не пройден: {str(e)}")
except Exception as e:
    print(f"Произошла ошибка: {str(e)}")

finally:
    print(f"Финальный URL: {driver.current_url}")
    print("Структура страницы:")
    elements = driver.find_elements(By.XPATH, "//*")
    for element in elements[:10]:  # Выводим первые 10 элементов
        print(f"Тег: {element.tag_name}, Класс: {element.get_attribute('class')}, Текст: {element.text[:30]}...")
    driver.quit()
