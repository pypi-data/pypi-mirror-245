import cv2
import pyautogui
import numpy as np
import time
import os


class process:
    def first(self, image_path):
        # Загрузка изображения кнопки
        button_image = cv2.imread(image_path)

        # Основной цикл обработки событий
        while True:
            # Сделать снимок экрана
            screen = pyautogui.screenshot()

            # Преобразовать снимок экрана в изображение OpenCV
            screen_image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

            # Поиск соответствия между текущим снимком экрана и изображением кнопки
            result = cv2.matchTemplate(screen_image, button_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Если соответствие найдено
            if max_val > 0.8:
                # Нажать на кнопку
                button_width, button_height = button_image.shape[1], button_image.shape[0]
                button_x, button_y = max_loc[0] + button_width // 2, max_loc[1] + button_height // 2
                pyautogui.click(button_x, button_y)
                time.sleep(1.5)
                pyautogui.click(button_x, button_y)

                break

    def clickf(self, image_path):
        # Загрузка изображения кнопки
        button_image = cv2.imread(image_path)

        # Основной цикл обработки событий
        while True:
            # Сделать снимок экрана
            screen = pyautogui.screenshot()

            # Преобразовать снимок экрана в изображение OpenCV
            screen_image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

            # Поиск соответствия между текущим снимком экрана и изображением кнопки
            result = cv2.matchTemplate(screen_image, button_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Если соответствие найдено
            if max_val > 0.8:
                # Нажать на кнопку
                button_width, button_height = button_image.shape[1], button_image.shape[0]
                button_x, button_y = max_loc[0] + button_width // 2, max_loc[1] + button_height // 2
                pyautogui.click(button_x, button_y)
                break

    def click(self, image_path):
        # Загрузка изображения кнопки
        button_image = cv2.imread(image_path)

        # Основной цикл обработки событий
        while True:
            # Сделать снимок экрана
            screen = pyautogui.screenshot()

            # Преобразовать снимок экрана в изображение OpenCV
            screen_image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

            # Поиск соответствия между текущим снимком экрана и изображением кнопки
            result = cv2.matchTemplate(screen_image, button_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Если соответствие найдено
            if max_val > 0.8:
                # Нажать на кнопку
                button_width, button_height = button_image.shape[1], button_image.shape[0]
                button_x, button_y = max_loc[0] + button_width // 2, max_loc[1] + button_height // 2
                pyautogui.click(button_x, button_y)
                time.sleep(0.5)
                pyautogui.click(button_x, button_y)
                time.sleep(0.2)
                pyautogui.click(button_x, button_y)
                time.sleep(0.2)
                pyautogui.click(button_x, button_y)
                time.sleep(0.2)
                pyautogui.click(button_x, button_y)
                time.sleep(0.2)
                pyautogui.click(button_x, button_y)
                time.sleep(1.2)
                pyautogui.click(button_x, button_y)
                time.sleep(0.8)
                pyautogui.click(button_x, button_y)
                break

    def start(self, image_path):
        # Загрузка изображения кнопки
        button_image = cv2.imread(image_path)

        # Основной цикл обработки событий
        while True:
            # Сделать снимок экрана
            screen = pyautogui.screenshot()

            # Преобразовать снимок экрана в изображение OpenCV
            screen_image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

            # Поиск соответствия между текущим снимком экрана и изображением кнопки
            result = cv2.matchTemplate(screen_image, button_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Если соответствие найдено
            if max_val > 0.8:
                # Нажать на кнопку
                button_width, button_height = button_image.shape[1], button_image.shape[0]
                button_x, button_y = max_loc[0] + button_width // 2, max_loc[1] + button_height // 2
                time.sleep(45)
                pyautogui.click(button_x, button_y)
                time.sleep(6)
                pyautogui.click(button_x, button_y)
                time.sleep(6)
                pyautogui.click(button_x, button_y)
                time.sleep(6)
                pyautogui.click(button_x, button_y)
                time.sleep(6)
                pyautogui.click(button_x, button_y)
                time.sleep(6)
                pyautogui.click(button_x, button_y)
                time.sleep(6)
                pyautogui.click(button_x, button_y)
                time.sleep(6)
                pyautogui.click(button_x, button_y)
                break

    def waitfor(self, image_path):
        # Загрузка изображения кнопки
        button_image = cv2.imread(image_path)

        # Основной цикл обработки событий
        while True:
            # Сделать снимок экрана
            screen = pyautogui.screenshot()

            # Преобразовать снимок экрана в изображение OpenCV
            screen_image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

            # Поиск соответствия между текущим снимком экрана и изображением кнопки
            result = cv2.matchTemplate(screen_image, button_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Если соответствие найдено
            if max_val > 0.8:
                time.sleep(10)
                break

    def waitform(self, image_path):
        # Загрузка изображения кнопки
        button_image = cv2.imread(image_path)

        # Основной цикл обработки событий
        while True:
            # Сделать снимок экрана
            screen = pyautogui.screenshot()

            # Преобразовать снимок экрана в изображение OpenCV
            screen_image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

            # Поиск соответствия между текущим снимком экрана и изображением кнопки
            result = cv2.matchTemplate(screen_image, button_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Если соответствие найдено
            if max_val > 0.8:
                time.sleep(1.2)
                break

    def waitford(self, image_path):
        # Загрузка изображения кнопки
        button_image = cv2.imread(image_path)

        # Основной цикл обработки событий
        while True:
            # Сделать снимок экрана
            screen = pyautogui.screenshot()

            # Преобразовать снимок экрана в изображение OpenCV
            screen_image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

            # Поиск соответствия между текущим снимком экрана и изображением кнопки
            result = cv2.matchTemplate(screen_image, button_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Если соответствие найдено
            if max_val > 0.8:
                break

    def off(self, image_path, name_path):
        # Загрузка изображения кнопки
        button_image = cv2.imread(image_path)

        # Основной цикл обработки событий
        while True:
            # Сделать снимок экрана
            screen = pyautogui.screenshot()

            # Преобразовать снимок экрана в изображение OpenCV
            screen_image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

            # Поиск соответствия между текущим снимком экрана и изображением кнопки
            result = cv2.matchTemplate(screen_image, button_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Если соответствие найдено
            if max_val > 0.8:
                # Нажать на кнопку
                button_width, button_height = button_image.shape[1], button_image.shape[0]
                button_x, button_y = max_loc[0] + button_width // 2, max_loc[1] + button_height // 2
                pyautogui.click(button_x, button_y)
                os.system('taskkill /f /im "' + name_path + '.exe"')
                break
