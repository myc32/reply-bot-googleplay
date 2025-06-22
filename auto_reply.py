from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Подключение к уже запущенному Chrome с remote debugging
chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

answers = [
    "Добрый день. Мы искренне рады, что вам понравилась наша игра. Большое вам спасибо за ваш отзыв и оценку. Похвала, которую мы получаем от наших игроков, поможет нам улучшать наши текущие игры и создавать более интересные игры в будущем.",
    "Добрый день. Спасибо за вашу оценку! Наша команда обязательно рассмотрит ваш отзыв. Мы действительно стараемся делать нашу игру как можно более увлекательной, поэтому отзывы наших игроков очень ценны для нас. Пожалуйста, напишите нам письмо  по адресу support_gokru@mechanist.co с дополнительными предложениями. Хорошего вам времени :)",
    "Добрый день. Наша искренняя благодарность за вашу оценку. Приятно знать, что вам понравилась наша игра, это действительно мотивирует нас на дальнейшее развитие. Мы рассмотрим ваш отзыв. Спасибо за вашу поддержку!",
    "Добрый день. Спасибо вам за ваш обнадеживающий отзыв и оценку! Мы надеемся, что вы продолжите наслаждаться нашей игрой. Если у вас есть какие-либо отзывы или предложения, пожалуйста, напишите в нашу техподдержку в игре или по адресу support_gokru@mechanist.co. Мы будем рады услышать вас!"
]

print("Начинаем обработку отзывов...")

try:
    # Ждём появления всех текстовых полей ответа (textarea)
    textareas = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//review-reply//textarea')))
    print(f"Обнаружено отзывов для ответа: {len(textareas)}")

    for i, textarea in enumerate(textareas[:50]):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", textarea)
            time.sleep(0.3)

            textarea.clear()
            textarea.send_keys(answers[i % len(answers)])
            time.sleep(1.2)  # Ждём появления кнопки

            # Находим блок review-reply, родитель textarea
            review_reply = textarea.find_element(By.XPATH, './ancestor::review-reply')

            # Ждём кнопку Publish reply внутри review-reply и кликаем
            publish_btn = WebDriverWait(review_reply, 4).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    './/console-button-set/div/material-button/button'
                ))
            )
            driver.execute_script("arguments[0].click();", publish_btn)

            print(f"[{i+1}] ✅ Ответ отправлен.")
            time.sleep(1.2)

        except Exception as e:
            print(f"[{i+1}] ❌ Ошибка при ответе: {e}")
            continue

except Exception as e:
    print(f"❌ Ошибка при инициализации: {e}")

finally:
    print("🏁 Работа завершена.")

