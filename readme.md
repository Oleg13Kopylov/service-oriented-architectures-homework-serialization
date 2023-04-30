# Краткие сведения о проекте

Приложение позволяет сравнить различные форматы сериализации данных по:
1) времени сериализации,
2) времени десериализации,
3) памяти, которую занимает сериализованная структура данных.

Приложение состоит из прокси-сервера и воркеров. 
Прокси-сервер служит посредником в общении клиента с воркерами.
Для каждого метода сериализации отводится свой воркер.

Рассмотрено 7 форматов сериализации, которые тестируются на фиксированной структуре данных.
Подробнее про рассматриваемые форматы сериализации, структуру данных, на которой происходит
тестирование, а также про то, как пользоваться прилоежением, написано ниже.

# Порядок работы с приложением

1. (Выполняется только один раз, в последующие разы этот наш можно пропустить)
Клонировать репозиторий к себе на компьютер:
```git clone git@github.com:Oleg13Kopylov/service-oriented-architectures-homework-serialization.git```

3. Перейти в полученную папку:
```cd service-oriented-architectures-homework-serialization```
4. Запустить докер 
5. Выполнить в терминале команду
```docker-compose --env-file variables.env build && docker-compose --env-file variables.env up```
    Обычно её выполнение занимает от 15 до 40 секунд.

    В результате в терминале должен появиться лог:
    ```service-oriented-architectures-homework-serialization-proxy-1                   | INFO:root:HELLO, I am proxy server and I just started working!!!```

6. Открыть другой терминал, в нем можно вводить запросы. Запросы имеют следующий вид:

    а) Запустить сравнение каких-либо конкретных форматов сериализации данных:
   ```echo -n '{"type" : "get_result", "formats" : ["GOOGLE_PROTOCOL_BUFFER", "APACHE_AVRO",  "YAML", "MESSAGE_PACK", "JSON", "XML", "NATIVE"]}' | nc -u -w2 localhost 2000```
    Требуемые вам форматы данных нужно указать в "formats", как в примере выше. В примере выше указаны все форматы данных.

    Запустить какой-то один формат, например, JSON, можно так:
    ```echo -n '{"type" : "get_result", "formats" : ["JSON"]}' | nc -u -w2 localhost 2000```
    
    б) Запустить сравнение всех форматов данных:
```echo -n '{"type" : "get_result_all"}' | nc -u -w2 localhost 2000```


7. Приложение можно отключить, 3 раза повторив эти два действия:

    а) В терминале с приложением нажать Ctrl + C
   
    б) Подождать секунду.

## Рассмотрены следующие форматы сериализации:
1.   Нативный вариант сериализации (NATIVE)
2.   XML
3.   JSON
4.   Google Protocol Buffers (GOOGLE_PROTOCOL_BUFFER)
5.   Apache Avro (APACHE_AVRO)
6.   YAML
7.   MessagePack (MESSAGE_PACK)

## Тестируемая структура данных:
Находится в файле *to_include.py*. Содержит bool, int, float, строку, список (массив)
строк, список (массив) интов, словарь (ассоциативный массив).

## Пример работы приложения:
В файле _screenshot_example.png_
![](/Users/olegkopylov/Desktop/SOA/testing_first_hw/service-oriented-architectures-homework-serialization/screenshot_example.png)



