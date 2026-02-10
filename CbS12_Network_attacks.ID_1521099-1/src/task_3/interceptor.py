from mitmproxy import http

# Эта функция вызывается mitmproxy каждый раз, когда проходит HTTP-запрос
def request(flow: http.HTTPFlow):
    
    # 1. Проверяем, является ли метод запроса POST
    # HTML-формы обычно отправляются методом POST
    if flow.request.method == "POST":
        
        # 2. Выводим красивое уведомление в лог
        print("\n[+] Перехвачен POST запрос!")
        print(f"URL: {flow.request.url}")

        # 3. Пытаемся получить данные формы
        # flow.request.urlencoded_form возвращает словарь с данными
        if flow.request.urlencoded_form:
            print("[*] Данные формы:")
            
            # Проходимся по всем полям формы и выводим их
            for key, value in flow.request.urlencoded_form.items():
                print(f"    {key}: {value}")
        else:
            # Если это не стандартная форма, а например raw data (JSON и т.д.)
            print("[*] Тело запроса (не стандартная форма):")
            print(flow.request.get_text())
            
        print("-" * 50 + "\n")