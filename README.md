# hacs-polaris 
![all](https://github.com/samoswall/hass-polaris/blob/main/logo&icon.png)

## Polaris IQ Home devices integration to Home Assistant
## Интеграция Home Assistant для техники Polaris.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
![](https://img.shields.io/github/watchers/samoswall/hacs-polaris.svg)
![](https://img.shields.io/github/stars/samoswall/hacs-polaris.svg)

[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)

> [!WARNING]
> Устройство Polaris должно быть подключено к вашему mqtt брокеру! <br>
> Подключить к mqtt брокеру можно в приложении в настройках. Если такой настройки нет, значит у вас старая версия прошивки в устройстве.<br>
> Новую версию прошивки можно запросить в техподдержке Polaris через приложение.<br>
> Если по какой-то причине нет возможности обновить прошивку или ее ещё не существует, или это устройство Русклимат (Hommyn), то можно вам необходимо перенаправить трафик в роутере на локальный брокер mqtt.<br>
> Суть перенаправления трафика заключается в установке частного DNS (не глобального) с именем  <br>`mqtt.cloud.polaris-iot.com` и/или `mqtt.cloud.rusklimat.ru` на IP вашего локального mqtt брокера.<br>
> Есть одна особенность:
> - должен быть в брокере действующий сертификат для SSL подключения на 8883 порт
> - должна быть включена анонимная авторизация на 8883 порту
> Проще всего это реализуется с использованием брокера EMQX.

ℹ️ **Добавлены**: <br>
✔️ Устройста Polaris (см. таблицу) <br>
✔️ Устройства РУСКЛИМАТ (Hommyn) (см. таблицу)<br>

ℹ️ **Как добавить новое устройство**: <br>
Создаем issues - Добавить ...  <br>
Или пишем в чате Telegram <br>
Обязательно указать type(ID) устройства и желательно развернутый mqtt топик для понимания, что добавлять. <br>

ℹ️ **Возможные проблемы**: <br>
В устройствах - может отсутствовать(быть лишним) сенсор или переключатель. Так же может не работать Ночник в чайнике (потому что в чайнике его нет)<br>
Проблема - есть одинаковые модели как с весом так и без, с ночником и без. Отличаются type(ID). <br>
Не стесняемся, пишем - отсутствует(лишний) сенсор ... type ... <br>
По другим предложениям (проблемам, логике работы, иконкам, переводам) тоже пишем, по возможности оперативно исправлю<br>

ℹ️ **Планы для доработок**: <br>
⬛ Добавить пылесосы и т.д.<br>

Доступно обсуждение тут: [Telegram](https://t.me/polarishomeassistant)

<details>
  <summary>Инструкция по подключению устройства к MQTT на примере чайника.</summary>

  1. Зайти в устройство в приложении и нажать на значок шестерёнки, чтобы перейти в настройки
     
     <img src='https://github.com/user-attachments/assets/187fc45c-2705-4111-845b-68cd21d9ff2c' width='200' alt='app screen 1'>
       
     Проверить, есть ли в настройках пункт "Настройки MQTT".
          
     <img src='https://github.com/user-attachments/assets/3b300b9b-02f5-457c-8e69-a9406d235270' width='200' alt='app screen 2'>
          
     Если его нет, то запросить прошивку в поддержке.
     Прошивка устанавливается долгим нажатием на строку с версией прошивки (не MCU).
  2. Открыть Home Assistant и установить дополнение Mosquitto broker (если он не установлен) и интеграцию MQTT (если она не установлена).
  3. Настройки брокера можно оставить по умолчанию, но необходимо добавить пользователя для доступа к брокеру, для этого нужно перейти во вкладку "Люди" в Home Assistant и добавить пользователя.
  4. В приложении Polaris зайти в пункт "Настройки MQTT", сдвинуть переключатель "Включено", указать адрес Home Assistant (это и есть адрес брокера, если используете дополнение Mosquitto broker) и порт (по умолчанию 1883). Ниже ввести учётные данные созданного пользователя для доступа к mqtt брокеру, SSL не включать, и в верхнем правом углу нажать галочку, для сохранения настроек.

     <img src='https://github.com/user-attachments/assets/bed0ff7b-6322-4a4d-bc89-b3e7bbfacae1' width='200' alt='app screen 3: mqtt settings'>
     
  5. Зайти в HomeAssistant и установить интеграцию Polaris. Поскольку интеграции в репозитории HACS нет, то надо в ручную добавить этот репозиторий в HACS (три точки в верхнем правом углу).
  6. Добавить эту интеграцию в HomeAssistant (раздел Настройки - Интеграции) и в ней, добавить устройство. Оно определится автоматически, достаточно указать пространство.

Устройство так же может находиться во внешней сети, и если до сети с брокером есть маршрут, оно будет найдено.
</details>

<details>
  <summary>Инструкция по добавлению своих рецептов (напитков) в мультиварку (кофемашину/чайник).</summary>

  1. Необходимо создать файл `polaris_custom_select.js` в папке `www/polaris` (в корне конфигурации, папка www, в ней polaris) любым удобным способом и открыть его для редактирования (например с помощью дополнения File editor)
  2. Скопировать пример и вставить в файл `polaris_custom_select.js`
  3. Максимальный пример: <br>
```yaml
{
  "SELECT_KETTLE_options": {
    "Мой чай": 94
  },
  "SELECT_COOKER_options": {
    "Мой рецепт 1": {"mode": 1, "time": 1200, "temperature": 115},
    "Мой рецепт 2": {"mode": 2, "time": 1300, "temperature": 105}
  },
  "SELECT_COFFEEMAKER_options": {
    "Мой кофе": {"mode": 2, "amount": 30, "weight": 11, "tank": 0, "pressure": 0, "speed": 0, "temperature": 92}
  },
  "SELECT_COFFEEMAKER_ROG_options": {
    "Мой кофе": {"mode": 3, "amount": 65, "tank": 32, "temperature": 95}
  },
  "SELECT_AIRFRYER_options": {
    "Мой рецепт 1": {"mode": 1, "time": 1200, "temperature": 115},
    "Мой рецепт 2": {"mode": 2, "time": 1300, "temperature": 105}
  },
  "SELECT_VACUUM_rooms": {
  	"Коридор": {"id": "01", "coordinate": [-72, 64, -71, -6, 16, -4, 15, 66]},
    "Зал":     {"id": "02", "coordinate": [21, 26, 24, -155, 140, -153, 137, 28]},
    "Кухня":   {"id": "03", "coordinate": [-71, -10, -68, -196, 22, -194, 19, -8]}
  }
}
```
(значение 0 у кофемашин и кофеварок обозначает, что параметр не используется и этот регулятор блокируется<br>
"mode" - Режим, "time" - Время приготовления, "amount" - Объём кофе, "weight" - Крепкость напитка, "tank" - Объём напитка (молока для кофеварок рожкового типа), "pressure" - Объём пенки, "speed" - Объём молока, "temperature" - Температура напитка)
4. Отредактировать файл под свои нужды.
Пояснения:
```yaml
{
  "SELECT_KETTLE_options": {
    Напитки для чайников
  },
  "SELECT_COOKER_options": {
    Рецепты для мультиварок
  },
  "SELECT_COFFEEMAKER_options": {
    Напитки для кофемашин
  },
  "SELECT_COFFEEMAKER_ROG_options": {
    Напитки для кофеварок рожкового типа
  },
  "SELECT_AIRFRYER_options": {
    Рецепты для аэрогрилей
  },
  "SELECT_VACUUM_rooms": {
  	Списки комнат с координатами
  }
}
```
Количество напитков/рецептов может быть минимум 1.
Если для устройства не добавляются напитки/рецепты, то раздел удалить. Например добавление только для мультиварки:
```yaml
{
  "SELECT_COOKER_options": {
    "Мой рецепт 1": {"mode": 1, "time": 1200, "temperature": 115}
  }
}
```
ВАЖНО! Валидация ваших напитков/рецептов не осуществляется! Поэтому внимательно отнеситесь к значению параметров и синтаксису json (запятые и фигурные скобки).
Сохраняем изменения в файле. После перезагрузки Home Assistant в меню будет новый рецепт.<br>
</details>

<details>
  <summary>Устройства Polaris</summary>

| ID    | Модель           | Тип устройства | Поддержка | Функции | Изображение |
| :---: |------------------|----------------|-----------|---------|    :---:    |
|37|PWK -7111CGLD-WIFI-(old)|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/d/ec/850f5-5943-4845-bd40-0884cfd497f0/60.webp)
|245|PWK-0105|kettle|✔️|volume, backlight, child_lock, water_tank, temperature, weight|![all](https://images.cdn.polaris-iot.com/a/c5/db790-4ed6-4dc6-a17b-639eb334e3ec/60.webp)
|205|PWK-1538CC|kettle|✔️|night, volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/b/1c/2f620-bcdd-49a0-b321-c9e25433febd/60.webp)
|271|PWK-1701CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/5/cd/b1677-8f3f-4b28-8b8c-103756cd6c9f/60.webp)
|36|PWK-17107CGLD-WIFI-(old)|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/a6/0a0ae-769d-44cf-ae1d-039dad4be304/60.webp)
|29|PWK-1712CGLD|kettle|✔️|child_lock, temperature|![all](https://images.cdn.polaris-iot.com/2/1e/87fb9-b3ab-4fc1-a184-1008e57064fb/60.webp)
|38|PWK-1712CGLD|kettle|✔️|volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/e/cc/ddf2f-070d-4867-8099-938bf6a3a084/60.webp)
|54|PWK-1712CGLD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/e/cc/ddf2f-070d-4867-8099-938bf6a3a084/60.webp)
|59|PWK-1712CGLD|kettle|✔️|volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/0/80/2044e-71b1-4143-80f5-79ccf1dbff96/60.webp)
|63|PWK-1712CGLD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/4/06/6d215-dfe6-4211-8260-8a72cb50f30e/60.webp)
|97|PWK-1712CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/1/4d/812d2-9cd5-473c-8670-865b6fa8cdbe/60.webp)
|117|PWK-1712CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/c/1c/4ff8e-7a0e-400c-9e50-43c6d45d300e/60.webp)
|208|PWK-1712CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/4/06/6d215-dfe6-4211-8260-8a72cb50f30e/60.webp)
|83|PWK-1712CGLD-RGB|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/e/cc/ddf2f-070d-4867-8099-938bf6a3a084/60.webp)
|253|PWK-1715|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/5/cd/b1677-8f3f-4b28-8b8c-103756cd6c9f/60.webp)
|244|PWK-1716CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/2/5c/a4518-3133-4e76-96fe-abd18089351f/60.webp)
|67|PWK-1720CGLD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/6/41/04018-94b4-4ae7-be02-1375b22e39e2/60.webp)
|84|PWK-1720CGLD-RGB|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/6/41/04018-94b4-4ae7-be02-1375b22e39e2/60.webp)
|6|PWK-1725CGLD|kettle|✔️|child_lock, temperature|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)
|52|PWK-1725CGLD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)
|57|PWK-1725CGLD|kettle|✔️|volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)
|61|PWK-1725CGLD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)
|82|PWK-1725CGLD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)
|86|PWK-1725CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/a/8c/aad08-4d13-489c-9b0f-028486297ac1/60.webp)
|105|PWK-1725CGLD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)
|106|PWK-1725CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)
|177|PWK-1725CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)
|194|PWK-1725CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/a/8c/aad08-4d13-489c-9b0f-028486297ac1/60.webp)
|196|PWK-1725CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/a/8c/aad08-4d13-489c-9b0f-028486297ac1/60.webp)
|164|PWK-1728CGLDA|kettle|✔️|night, volume, backlight, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)
|209|PWK-1729CAD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/1e/63e7d-332e-42de-96a4-2b393463b78b/60.webp)
|189|PWK-1746CA|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/1e/63e7d-332e-42de-96a4-2b393463b78b/60.webp)
|260|PWK-1746CA|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/1e/63e7d-332e-42de-96a4-2b393463b78b/60.webp)
|308|PWK-1746CA|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/1e/63e7d-332e-42de-96a4-2b393463b78b/60.webp)
|8|PWK-1755CAD|kettle|✔️|child_lock, temperature|![all](https://images.cdn.polaris-iot.com/4/52/2f530-8ebb-426d-98d1-5922508ecbbc/60.webp)
|53|PWK-1755CAD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/4/52/2f530-8ebb-426d-98d1-5922508ecbbc/60.webp)
|58|PWK-1755CAD|kettle|✔️|volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/4/52/2f530-8ebb-426d-98d1-5922508ecbbc/60.webp)
|62|PWK-1755CAD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/4/52/2f530-8ebb-426d-98d1-5922508ecbbc/60.webp)
|185|PWK-1755CAD|kettle|✔️|volume, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/4/52/2f530-8ebb-426d-98d1-5922508ecbbc/60.webp)
|165|PWK-1755CAD-VOICE|kettle|✔️|volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/96/c40d6-068b-4a17-9e9c-f912ee1e70c2/60.webp)
|121|PWK-1774CAD|kettle|✔️|volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/3/25/790d4-2ead-4c4a-a440-a8be89765e90/60.webp)
|2|PWK-1775CGLD|kettle|✔️|child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|51|PWK-1775CGLD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|56|PWK-1775CGLD|kettle|✔️|volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|60|PWK-1775CGLD|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|98|PWK-1775CGLD|kettle|✔️|volume, backlight, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|188|PWK-1775CGLD|kettle|✔️|volume, backlight, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|223|PWK-1775CGLD|kettle|✔️|volume, backlight, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|262|PWK-1775CGLD|kettle|✔️|volume, backlight, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|263|PWK-1775CGLD|kettle|✔️|volume, backlight, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|275|PWK-1775CGLD|kettle|✔️|volume, backlight, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|294|PWK-1775CGLD|kettle|✔️|volume, backlight, child_lock, temperature, weight|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|85|PWK-1775CGLD-SMART|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|139|PWK-1775CGLD-VOICE|kettle|✔️|volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)
|175|PWK-1823CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/5/f2/5158d-edd3-4018-a391-2a97626f3bb9/60.webp)
|254|PWK-1823CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/5/f2/5158d-edd3-4018-a391-2a97626f3bb9/60.webp)
|176|PWK-1841CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/5/cd/b1677-8f3f-4b28-8b8c-103756cd6c9f/60.webp)
|255|PWK-1841CGLD|kettle|✔️|night, volume, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/5/cd/b1677-8f3f-4b28-8b8c-103756cd6c9f/60.webp)
|147|PUH-0205|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/5/77/d82d4-6e9c-4794-8a6b-4d6893f9b297/60.webp)
|71|PUH-1010|humidifier|✔️|speed, timer, volume, humidity, backlight, child_lock|![all](https://images.cdn.polaris-iot.com/7/6d/75075-23c8-44c0-a582-d91919da426d/60.webp)
|72|PUH-2300|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/6/ee/0c47e-a3d6-4f99-840b-5a74f85e056e/60.webp)
|73|PUH-3030|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock|![all](https://images.cdn.polaris-iot.com/3/a9/c2d1c-e416-45f5-8a7b-e2ac59c9b164/60.webp)
|75|PUH-4040|humidifier|✔️|speed, timer, volume, humidity, backlight, child_lock|![all](https://images.cdn.polaris-iot.com/0/79/caa3f-4b4d-4092-9a9e-c02ca79d8c4a/60.webp)
|99|PUH-4040|humidifier|✔️|speed, timer, volume, humidity, backlight, child_lock|![all](https://images.cdn.polaris-iot.com/0/79/caa3f-4b4d-4092-9a9e-c02ca79d8c4a/60.webp)
|153|PUH-4055|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock|![all](https://images.cdn.polaris-iot.com/8/bc/dbc40-1588-48cd-80ce-3fa2c10c0d10/60.webp)
|137|PUH-4066|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock|![all](https://images.cdn.polaris-iot.com/a/d3/3934a-32a1-44b5-b0f2-1be2951cb7d4/60.webp)
|157|PUH-4550|humidifier|✔️|night, speed, timer, turbo, volume, ioniser, humidity, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/e/15/86a99-602c-4c6b-b204-43551b37d358/60.webp)
|158|PUH-6060|humidifier|✔️|night, speed, timer, turbo, volume, ioniser, humidity, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/7/6f/07d82-8dea-42eb-b092-ae7a1bec1a22/60.webp)
|25|PUH-6090|humidifier|✔️|speed, timer, volume, humidity, backlight, child_lock|![all](https://images.cdn.polaris-iot.com/9/03/6eada-d5f2-4d60-bcfa-d4c9b2669852/60.webp)
|15|PUH-7406|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/2/49/d53fe-3e9d-4229-9900-8f621b54ca23/60.webp)
|87|PUH-8080/PUH-4606|humidifier|✔️|speed, timer, volume, humidity, backlight, child_lock|![all](https://images.cdn.polaris-iot.com/9/3a/2e628-d005-4ce2-be29-93aa56e1d315/60.webp)
|155|PUH-8802|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock|![all](https://images.cdn.polaris-iot.com/6/b1/2ddff-8f41-4fd2-8e33-6cfc60090332/60.webp)
|74|PUH-9009|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/a/a7/7bb37-25b8-4d03-99d2-775794af20dc/60.webp)
|4|PUH-9105/PUH-2709|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, stream_warm|![all](https://images.cdn.polaris-iot.com/c/9d/27f85-2e01-4cd7-85d8-a034e81c5be4/60.webp)
|17|PUH-9105/PUH-2709|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, stream_warm|![all](https://images.cdn.polaris-iot.com/c/9d/27f85-2e01-4cd7-85d8-a034e81c5be4/60.webp)
|18|PUH-9105/PUH-2709|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/c/9d/27f85-2e01-4cd7-85d8-a034e81c5be4/60.webp)
|44|PUH-9105/PUH-2709|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/c/9d/27f85-2e01-4cd7-85d8-a034e81c5be4/60.webp)
|70|PUH-9105/PUH-2709|humidifier|✔️|speed, timer, volume, ioniser, humidity, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/c/9d/27f85-2e01-4cd7-85d8-a034e81c5be4/60.webp)
|1|EVO-0225|cooker|✔️|timer, keep_warm, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/b/8f/ae138-e3b2-448a-8a8e-ca60eb7c3cc5/60.webp)
|95|PMC-00000|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)
|303|PMC-0510|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/a/50/c33c6-d8ec-487b-ba32-1740dc233577/60.webp)
|301|PMC-0515|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)
|10|PMC-0521WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/1/31/fc82e-50af-430e-8d71-043bd7aeb5d2/60.webp)
|41|PMC-0521WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/1/31/fc82e-50af-430e-8d71-043bd7aeb5d2/60.webp)
|267|PMC-0521WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/1/31/fc82e-50af-430e-8d71-043bd7aeb5d2/60.webp)
|55|PMC-0524WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/e/5f/51204-817a-46fb-a477-c80cad89f019/60.webp)
|206|PMC-0524WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/3/32/d6c82-2ebc-4519-8b71-05de8097756a/60.webp)
|9|PMC-0526WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)
|40|PMC-0526WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)
|138|PMC-0526WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)
|39|PMC-0528WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/4/ce/e930f-5b1b-444f-96e2-04b4d9314231/60.webp)
|48|PMC-0528WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/4/ce/e930f-5b1b-444f-96e2-04b4d9314231/60.webp)
|268|PMC-0528WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/4/ce/e930f-5b1b-444f-96e2-04b4d9314231/60.webp)
|47|PMC-0530WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/2/d9/64dfb-b93e-49b8-874c-766c212698c8/60.webp)
|270|PMC-0530WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/2/d9/64dfb-b93e-49b8-874c-766c212698c8/60.webp)
|210|PMC-0590AD|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/4/cc/bd7d5-385a-4edb-bb43-7a686dcffa2f/60.webp)
|302|PMC-0597|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/1/31/fc82e-50af-430e-8d71-043bd7aeb5d2/60.webp)
|215|PMC-5001WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/1/31/fc82e-50af-430e-8d71-043bd7aeb5d2/60.webp)
|79|PMC-5017WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/7/41/24cf9-cb91-431c-a5cb-183d2594a5af/60.webp)
|192|PMC-5017WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/7/41/24cf9-cb91-431c-a5cb-183d2594a5af/60.webp)
|80|PMC-5020WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/d/da/5a3c8-b17a-4d94-83cd-24bd2e8562d6/60.webp)
|266|PMC-5020WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/d/da/5a3c8-b17a-4d94-83cd-24bd2e8562d6/60.webp)
|77|PMC-5040WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/0/40/bbd11-87b7-47ae-9432-74b78d904d74/60.webp)
|78|PMC-5050WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/1/87/4d6af-60c0-48d3-8939-60400805fca9/60.webp)
|89|PMC-5055WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/a/67/edd4c-9a92-4cfe-b17e-53a76d282475/60.webp)
|114|PMC-5060 Smart Motion|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)
|240|PMC-5060-Smart-Motion|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)
|162|PMC-5063WIFI|cooker|✔️|timer, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/e/5f/51204-817a-46fb-a477-c80cad89f019/60.webp)
|169|PPC-1505 Wi-FI|cooker|✔️|timer, volume, pressure, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)
|183|PPC-1505-Wi-FI*|cooker|✔️|timer, volume, pressure, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)
|235|AM7310-(test)|coffeemaker|✔️|turbo, amount, volume, child_lock, water_tank, stream_warm, temperature|![all](https://images.cdn.polaris-iot.com/d/05/16bab-b852-4e03-afa6-41a892d93205/60.webp)
|305|PACM-2072|coffeemaker|✔️|speed, turbo, amount, volume, weight, pressure, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/b/2b/8c952-9291-4c02-bce2-4d73f853452d/60.webp)
|103|PACM-2080AC|coffeemaker|✔️|speed, amount, volume, weight, pressure, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/b/2b/8c952-9291-4c02-bce2-4d73f853452d/60.webp)
|261|PACM-2080AC|coffeemaker|✔️|speed, amount, volume, weight, pressure, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/b/2b/8c952-9291-4c02-bce2-4d73f853452d/60.webp)
|276|PACM-2080AC|coffeemaker|✔️|speed, turbo, amount, volume, weight, pressure, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/b/2b/8c952-9291-4c02-bce2-4d73f853452d/60.webp)
|277|PACM-2080AC|coffeemaker|✔️|speed, turbo, amount, volume, weight, pressure, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/b/2b/8c952-9291-4c02-bce2-4d73f853452d/60.webp)
|200|PACM-2081AC|coffeemaker|✔️|speed, timer, amount, volume, weight, pressure, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/c/11/747d1-b6ce-417f-980d-665512b3a6ad/60.webp)
|265|PACM-2081AC|coffeemaker|✔️|speed, timer, turbo, amount, volume, weight, pressure, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/c/11/747d1-b6ce-417f-980d-665512b3a6ad/60.webp)
|280|PACM-2081AC|coffeemaker|✔️|speed, timer, turbo, amount, weight, pressure, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/c/11/747d1-b6ce-417f-980d-665512b3a6ad/60.webp)
|166|PACM-2085GC|coffeemaker|✔️|speed, amount, volume, weight, pressure, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/a/64/4d650-b0b1-46f7-879e-394b688fa34f/60.webp)
|278|PACM-2085GC|coffeemaker|✔️|speed, turbo, amount, volume, weight, pressure, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/c/e1/e7862-3e89-40c4-a92a-ca1d5c0bae9c/60.webp)
|247|PCM-1255|coffeemaker|✔️|timer, amount, volume, weight, ioniser, child_lock|![all](https://images.cdn.polaris-iot.com/6/7e/b8e87-9593-4023-b339-3fb6da5df931/60.webp)
|45|PCM-1540WIFI|coffeemaker|✔️|amount, volume, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/a/44/ec0b3-ea7f-4d75-bd2a-ba174bf1817d/60.webp)
|222|PCM-1540WIFI|coffeemaker|✔️|amount, volume, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/a/44/ec0b3-ea7f-4d75-bd2a-ba174bf1817d/60.webp)
|274|PCM-1540WIFI|coffeemaker|✔️|amount, volume, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/a/44/ec0b3-ea7f-4d75-bd2a-ba174bf1817d/60.webp)
|279|PCM-1540WIFI|coffeemaker|✔️|amount, volume, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/a/44/ec0b3-ea7f-4d75-bd2a-ba174bf1817d/60.webp)
|190|PCM-1560|coffeemaker|✔️|amount, volume, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/6/77/a31a0-34d7-4343-a37e-0fbd5af7ceaa/60.webp)
|207|PCM-2070CG|coffeemaker|✔️|turbo, amount, volume, child_lock, water_tank, stream_warm, temperature|![all](https://images.cdn.polaris-iot.com/2/72/b2f22-3608-40b7-b435-7485fe68dfc2/60.webp)
|172|PAW-0804|air-cleaner|✔️|speed, timer, volume, backlight|![all](https://images.cdn.polaris-iot.com/6/8d/81a02-893f-467d-a375-1c004bb31548/60.webp)
|140|PAW-0804(c3-test)|air-cleaner|✔️|speed, timer, turbo, volume, ioniser, backlight|![all](https://images.cdn.polaris-iot.com/0/f0/440b3-27bd-49f8-81e4-0af6f8e13dee/60.webp)
|151|PPA-2025|air-cleaner|✔️|speed, timer, volume, ioniser, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/5/de/94ac7-2530-446f-a4bd-566ddc4edd16/60.webp)
|203|PPA-2025|air-cleaner|✔️|speed, timer, volume, ioniser, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/d/fb/9d0c9-ddaf-405a-8ae7-19b1ccf27fa3/60.webp)
|250|PPA-2025|air-cleaner|✔️|speed, timer, volume, ioniser, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/d/fb/9d0c9-ddaf-405a-8ae7-19b1ccf27fa3/60.webp)
|152|PPA-4050|air-cleaner|✔️|speed, timer, volume, ioniser, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/9/3d/a90f0-137c-414c-aa15-df9f395e1cb1/60.webp)
|204|PPA-4050|air-cleaner|✔️|speed, timer, volume, ioniser, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/8/93/ca1e0-f8de-4b42-938f-6f803eb7d982/60.webp)
|251|PPA-4050|air-cleaner|✔️|speed, timer, volume, ioniser, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/8/93/ca1e0-f8de-4b42-938f-6f803eb7d982/60.webp)
|236|PPAT-02A|air-cleaner|✔️|speed, timer, turbo, volume, ioniser, humidity, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/a/88/251fb-764d-4891-9a52-0e5a58bc93a0/60.webp)
|238|PPAT-80P|air-cleaner|✔️|speed, timer, volume, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/f/66/2b72c-ed43-456e-9524-245e229bb667/60.webp)
|239|PPAT-90GDi|air-cleaner|✔️|speed, timer, turbo, volume, humidity, child_lock, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/f/66/2b72c-ed43-456e-9524-245e229bb667/60.webp)
|132|PWF-2005|irrigator|✔️|speed, timer, ioniser, smart_mode|![all](https://images.cdn.polaris-iot.com/5/bd/1a68b-9fb5-46e9-acbd-c086748b72bb/60.webp)
|252|PWF-2005|irrigator|✔️|speed, timer, ioniser, smart_mode|![all](https://images.cdn.polaris-iot.com/5/bd/1a68b-9fb5-46e9-acbd-c086748b72bb/60.webp)
|273|PAF-4001WIFI|air_fryer|❌|timer, child_lock, multi_step, temperature|![all](https://images.cdn.polaris-iot.com/c/e3/6185e-c768-4283-95d4-07fa5ffe7448/60.webp)
|290|PAF-6003WIFI|air_fryer|✔️|timer, backlight, child_lock, multi_step, temperature|![all](https://images.cdn.polaris-iot.com/1/c6/acb0e-5312-44e2-b155-5c3148f0a07d/60.webp)
|291|PAF-8003WIFI|air_fryer|✔️|timer, backlight, child_lock, multi_step, temperature|![all](https://images.cdn.polaris-iot.com/2/99/6942a-ce57-4824-888d-56ac8c6a15b5/60.webp)
|292|PAF-8005WIFI|air_fryer|✔️|timer, backlight, child_lock, multi_step, temperature|![all](https://images.cdn.polaris-iot.com/f/29/7c5ae-57fa-4394-b9f0-8243ce56d852/60.webp)
|31|ENIGMA-WI-FI|boiler|❌|speed, timer, keep_warm, child_lock, smart_mode, temperature|![all](https://images.cdn.polaris-iot.com/5/e6/60f0f-98be-44ea-bea4-42cc3a27d340/60.webp)
|11|PWH-IDF06|boiler|❌|speed, timer, keep_warm, child_lock, smart_mode, temperature|![all](https://images.cdn.polaris-iot.com/5/e6/60f0f-98be-44ea-bea4-42cc3a27d340/60.webp)
|30|SIGMA-WI-FI|boiler|❌|speed, timer, keep_warm, child_lock, smart_mode, temperature|![all](https://images.cdn.polaris-iot.com/6/f1/21910-973b-4796-ab35-7bad5b9fb87e/60.webp)
|249|VEKTOR-WI-FI|boiler|❌|speed, volume, keep_warm, child_lock, water_tank, temperature|![all](https://images.cdn.polaris-iot.com/6/f1/21910-973b-4796-ab35-7bad5b9fb87e/60.webp)
|46|PCH-0320WIFI|heater|❌|timer, temperature|![all](https://images.cdn.polaris-iot.com/2/ef/6cb11-25b4-4c82-adcf-33f0e01302b8/60.webp)
|65|PCH-0320WIFI|heater|❌|timer, temperature|![all](https://images.cdn.polaris-iot.com/2/ef/6cb11-25b4-4c82-adcf-33f0e01302b8/60.webp)
|16|PHV-1401|heater|❌|timer, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/e/3b/3615d-0d9d-4107-9783-df4e9655cdd1/60.webp)
|49|PMH-21XX|heater|❌|timer, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/2/30/eb6b9-5ed3-4536-9e54-b380fd25c178/60.webp)
|64|PMH-21XX|heater|❌|timer, backlight, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/6/e0/263c0-2c33-4a8a-929c-e998568a5606/60.webp)
|246|PRWC-3001|cleaner|✔️|turbo, water_tank|![all](https://images.cdn.polaris-iot.com/f/91/8cc80-f16e-4ac8-b075-cdf8270801b6/60.webp)
|101|PVCR-0726-Aqua|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/1/20/da178-0a48-405d-83f5-c17300f23b5d/60.webp)
|108|PVCR-0726-GYRO|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/c/61/4b62b-f6f8-47fc-bd48-0112b56e9977/60.webp)
|21|PVCR-0735|cleaner|✔️|speed, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/9/89/721c8-9edb-49f0-8016-9b6fefb7b096/60.webp)
|163|PVCR-0735|cleaner|✔️|speed, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/9/89/721c8-9edb-49f0-8016-9b6fefb7b096/60.webp)
|19|PVCR-0833|cleaner|✔️|speed, find_me|![all](https://images.cdn.polaris-iot.com/0/48/35580-64af-42e7-9994-55ef1407d591/60.webp)
|43|PVCR-0833|cleaner|✔️|speed, find_me|![all](https://images.cdn.polaris-iot.com/0/48/35580-64af-42e7-9994-55ef1407d591/60.webp)
|104|PVCR-0905|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank|![all](https://images.cdn.polaris-iot.com/6/de/c37ad-21d9-4f15-8c7f-ed8410babd7f/60.webp)
|156|PVCR-0905|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank|![all](https://images.cdn.polaris-iot.com/f/eb/7cc05-b47a-4646-acc0-ad7d17ce8cc9/60.webp)
|107|PVCR-0926|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/1/20/da178-0a48-405d-83f5-c17300f23b5d/60.webp)
|23|PVCR-1028|cleaner|✔️|speed, battery, child_lock|![all](https://images.cdn.polaris-iot.com/8/a3/68430-8088-404f-af1f-6d79cf4512d0/60.webp)
|22|PVCR-1050|cleaner|✔️|speed, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/4/ec/06465-b9e3-4e02-a27c-797fdcf182d1/60.webp)
|102|PVCR-1226-Aqua|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/1/20/da178-0a48-405d-83f5-c17300f23b5d/60.webp)
|109|PVCR-1226-GYRO|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/1/26/3ac2c-ce5a-4c4e-8f2b-d9cfc8653ed7/60.webp)
|24|PVCR-1229|cleaner|✔️|speed, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/1/25/f2359-b5a6-4e32-a1b5-88283a97c662/60.webp)
|68|PVCR-3100|cleaner|✔️|speed, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/4/80/6b6e6-6ecd-437e-b01c-2f14e2cf5b56/60.webp)
|7|PVCR-3200|cleaner|✔️|speed, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/4/27/7e198-dede-4ea1-a1a7-1cb9b6ce2888/60.webp)
|76|PVCR-3200|cleaner|✔️|speed, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/5/6d/bdc04-52f8-4092-a827-c1455e2a11f8/60.webp)
|115|PVCR-3200|cleaner|✔️|speed, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/5/6d/bdc04-52f8-4092-a827-c1455e2a11f8/60.webp)
|12|PVCR-3300|cleaner|✔️|speed, volume, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/5/7a/903fd-3c1e-4c17-a396-97d6a5eb32bd/60.webp)
|81|PVCR-3400|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/7/78/12125-b314-4cba-96dd-b394da015482/60.webp)
|130|PVCR-3600|cleaner|✔️|speed, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/6/24/ee896-0ec7-428c-8704-82f446107a45/60.webp)
|112|PVCR-3700|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/5/b6/684e6-a94d-4fc8-aa61-5a3efef92a92/60.webp)
|88|PVCR-3800|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/1/20/da178-0a48-405d-83f5-c17300f23b5d/60.webp)
|66|PVCR-3900|cleaner|✔️|speed, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/5/ba/bd543-ba02-4399-ac4a-be7bc65fd4d6/60.webp)
|131|PVCR-3900|cleaner|✔️|speed, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/5/ba/bd543-ba02-4399-ac4a-be7bc65fd4d6/60.webp)
|113|PVCR-4000|cleaner|✔️|speed, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/2/bb/d79e5-72a9-44f7-8921-46427cc4beab/60.webp)
|197|PVCR-4000|cleaner|✔️|speed, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/2/bb/d79e5-72a9-44f7-8921-46427cc4beab/60.webp)
|110|PVCR-4105|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/7/2f/6679a-5e9c-4aa1-81dd-80b370c34631/60.webp)
|127|PVCR-4105|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/7/2f/6679a-5e9c-4aa1-81dd-80b370c34631/60.webp)
|199|PVCR-4250|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/5/57/282da-d799-4c8d-80e6-dbd133cd9611/60.webp)
|241|PVCR-4250|cleaner|✔️|speed, turbo, volume, find_me, ioniser, child_lock, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/9/c9/430a9-5335-42c1-b6e8-2fb3a62f3274/60.webp)
|211|PVCR-4260|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/c/ce/591f4-223e-48b7-b01c-7d8efa0111c7/60.webp)
|269|PVCR-4260|cleaner|✔️|speed, turbo, volume, find_me, ioniser, child_lock, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/c/ce/591f4-223e-48b7-b01c-7d8efa0111c7/60.webp)
|142|PVCR-4500|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/9/38/99c96-80f5-4858-a1f1-322456498104/60.webp)
|195|PVCR-4500|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/e/6c/7638c-3e9c-4551-85e5-a0b9138961cd/60.webp)
|307|PVCR-4750|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/8/6b/1da86-4db7-4410-93a7-f0b952d8eb1c/60.webp)
|119|PVCR-5001|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/8/f2/f2957-fb7e-4ac4-b644-8eedfeff61d7/60.webp)
|146|PVCR-5001|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/8/f2/f2957-fb7e-4ac4-b644-8eedfeff61d7/60.webp)
|154|PVCR-5001|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/8/f2/f2957-fb7e-4ac4-b644-8eedfeff61d7/60.webp)
|201|PVCR-5003|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/9/19/84a49-0f78-40d1-9f6c-c3ad1c77c8ae/60.webp)
|242|PVCR-5005|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/8/6b/1da86-4db7-4410-93a7-f0b952d8eb1c/60.webp)
|123|PVCR-6001|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/8/f7/b2aa9-56ab-4ef0-b19e-bc78c9492809/60.webp)
|148|PVCR-6001|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/8/f7/b2aa9-56ab-4ef0-b19e-bc78c9492809/60.webp)
|221|PVCR-6001|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/8/f7/b2aa9-56ab-4ef0-b19e-bc78c9492809/60.webp)
|187|PVCR-6003|cleaner|✔️|speed, turbo, volume, find_me, backlight, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/f/4f/8dec1-d948-4d6c-b09c-e8cfe71f0408/60.webp)
|256|PVCR-7026|cleaner|✔️|speed, turbo, volume, find_me, backlight, child_lock, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/f/4f/8dec1-d948-4d6c-b09c-e8cfe71f0408/60.webp)
|128|PVCRAC-7050|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank|![all](https://images.cdn.polaris-iot.com/6/a8/f5bc0-5cb6-423a-b51e-34e02b1dcd9d/60.webp)
|212|PVCRAC-7290|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank|![all](https://images.cdn.polaris-iot.com/c/3c/7649b-aaa6-4e74-9293-7f8efeaf5746/60.webp)
|178|PVCRAC-7750|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/d/70/0218c-9a0e-4d00-b104-3979316f231c/60.webp)
|198|PVCRAC-7790|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank|![all](https://images.cdn.polaris-iot.com/3/21/b6739-f68c-4039-86a0-bdd72c4daf5b/60.webp)
|264|PVCRAC-7790|cleaner|✔️|speed, turbo, amount, volume, find_me, ioniser, water_tank|![all](https://images.cdn.polaris-iot.com/3/21/b6739-f68c-4039-86a0-bdd72c4daf5b/60.webp)
|126|PVCRDC-0101|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank|![all](https://images.cdn.polaris-iot.com/a/e3/2643f-16a9-445a-bef6-67e2990b95b2/60.webp)
|160|PVCRDC-0101|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank|![all](https://images.cdn.polaris-iot.com/1/9b/495af-1edb-42f6-9d07-ea6dff1327b9/60.webp)
|124|PVCRDC-5002|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/5/da/761dd-4d18-4958-89e5-cb391aa3238c/60.webp)
|149|PVCRDC-5002|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/5/da/761dd-4d18-4958-89e5-cb391aa3238c/60.webp)
|213|PVCRDC-5002|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/5/da/761dd-4d18-4958-89e5-cb391aa3238c/60.webp)
|202|PVCRDC-5004|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/c/10/8ae2a-7f37-46e6-8f46-c2f9c0d916eb/60.webp)
|181|PVCRDC-5006|cleaner|✔️|speed, turbo, volume, find_me, ioniser, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/8/32/4dc97-320a-4f52-92b7-a188ac71c434/60.webp)
|125|PVCRDC-6002|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/d/e6/0b12b-1c6d-4143-a7f1-acaf586d0499/60.webp)
|150|PVCRDC-6002|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/d/e6/0b12b-1c6d-4143-a7f1-acaf586d0499/60.webp)
|186|PVCRDC-6004|cleaner|✔️|speed, turbo, volume, find_me, ioniser, backlight, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/9/5f/5f965-16b3-4c8c-a449-bd8a0a3a476b/60.webp)
|257|PVCRDC-7028|cleaner|✔️|speed, turbo, volume, find_me, ioniser, backlight, child_lock, water_tank, stream_warm|![all](https://images.cdn.polaris-iot.com/9/5f/5f965-16b3-4c8c-a449-bd8a0a3a476b/60.webp)
|217|PVCRDC-G2-5002|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/c/40/4bdb3-7ccb-4b2e-b131-835d0c563624/60.webp)
|218|PVCRDC-G2-6002|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/7/1e/9eaa3-227e-4fb2-92bf-cb969f7db86e/60.webp)
|133|PVCR-G2-0726W|cleaner|✔️|speed, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/1/bd/019c4-56b4-4986-a037-81dd7c5db320/60.webp)
|193|PVCR-G2-0826|cleaner|✔️|speed, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/2/de/d787e-8ca3-4a1b-aeee-c192c7986381/60.webp)
|134|PVCR-G2-0926W|cleaner|✔️|speed, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/2/d1/933a9-c624-449e-b0e9-a66638fbab63/60.webp)
|135|PVCR-G2-1226|cleaner|✔️|speed, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/d/94/beec6-89df-4e44-a943-eba7cc79bfde/60.webp)
|129|PVCR-G2-3200|cleaner|✔️|speed, turbo, volume, battery, find_me, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/7/24/796ea-4e2f-499c-90ff-582e2fc74685/60.webp)
|122|PVCR-G2-3600|cleaner|✔️|speed, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/6/24/ee896-0ec7-428c-8704-82f446107a45/60.webp)
|219|PVCR-G2-5001|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/8/f2/f2957-fb7e-4ac4-b644-8eedfeff61d7/60.webp)
|220|PVCR-G2-6001|cleaner|✔️|speed, turbo, volume, find_me, water_tank|![all](https://images.cdn.polaris-iot.com/4/99/7b1b4-0e0d-4cf1-b307-a14e0a80636d/60.webp)
|100|PVCR-Wave-15|cleaner|✔️|speed, turbo, battery, child_lock, water_tank|![all](https://images.cdn.polaris-iot.com/7/4d/dbdab-a1ec-46e0-a669-57e4e4c24ae8/60.webp)
|93|PHB-1350-WIFI|blender|❌|speed, timer, multi_step|![all](https://images.cdn.polaris-iot.com/e/f8/22f01-dd2f-40e3-8f85-d7dc8f9fddce/60.webp)
|35|PHB-1503-WIFI-(old)|blender|❌|speed, timer, child_lock, multi_step|![all](https://images.cdn.polaris-iot.com/3/a6/45180-5e03-4e43-9de9-a0948262c226/60.webp)
|34|PHB-1551-WIFI|blender|❌|speed, timer, child_lock, multi_step|![all](https://images.cdn.polaris-iot.com/a/c1/c2911-605b-4450-8376-761b01062507/60.webp)
|282|induction-hob|cooktop|❌|timer, volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/2/05/9f53d-0b17-4a53-8fd1-271d887d85a5/60.webp)
|286|XFC302I-B3SF|cooktop|❌|timer, volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/c/10/9eaed-501d-49a8-828a-7201dc5c7998/60.webp)
|288|XFC302T-B1D|cooktop|❌|timer, volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/8/dc/c8916-f800-4b1b-acfb-30970eb2f99b/60.webp)
|285|XFC604I|cooktop|❌|timer, volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/0/09/d23d9-dd9c-42ce-9900-fd1e5a477d84/60.webp)
|304|XFC604I-(test)|cooktop|❌|timer, volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/0/09/d23d9-dd9c-42ce-9900-fd1e5a477d84/60.webp)
|284|XFC604I-B8F|cooktop|❌|timer, volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/6/5b/cdb75-b846-4fc5-a581-40d5832c51f7/60.webp)
|287|XFC604T-B7D|cooktop|❌|timer, volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/4/d9/329b8-fb1e-48de-b4e6-0aade487b5e2/60.webp)
|289|XFG640F-B3P|cooktop|❌|timer, volume, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/e/28/c833d-c977-4371-b547-6feee50de77c/60.webp)
|111|PVCS-1150|cordless_cleaner|❌|speed, timer|![all](https://images.cdn.polaris-iot.com/1/27/36f11-5225-478f-bbc2-fed844a33639/60.webp)
|90|PVCS-2090|cordless_cleaner|❌|speed, timer|![all](https://images.cdn.polaris-iot.com/3/9d/8bcaf-38fa-4168-b71e-cf201171e719/60.webp)
|136|PVCS-4070|cordless_cleaner|❌|speed, timer|![all](https://images.cdn.polaris-iot.com/0/5c/3078f-88c4-4f8b-8bbf-7a1f1db794fd/60.webp)
|229|PVCS-4070|cordless_cleaner|❌|speed, timer|![all](https://images.cdn.polaris-iot.com/0/5c/3078f-88c4-4f8b-8bbf-7a1f1db794fd/60.webp)
|232|PVCS-6020|cordless_cleaner|❌|speed, timer|![all](https://images.cdn.polaris-iot.com/0/6f/5034e-1de1-46c9-8828-c95895afae40/60.webp)
|281|PVCS-6020|cordless_cleaner|❌|speed, timer, amount|![all](https://images.cdn.polaris-iot.com/0/6f/5034e-1de1-46c9-8828-c95895afae40/60.webp)
|230|PVCS-8200|cordless_cleaner|❌|speed, timer, amount|![all](https://images.cdn.polaris-iot.com/6/11/0626d-1b12-4603-a4aa-dae77478c40b/60.webp)
|234|PVCSDC-3000|cordless_cleaner|❌|speed, timer, amount|![all](https://images.cdn.polaris-iot.com/d/6d/009a7-1427-4527-821e-b9b38c8aec9c/60.webp)
|233|PVCSDC-3005|cordless_cleaner|❌|speed, timer|![all](https://images.cdn.polaris-iot.com/8/5e/6e656-7813-4d03-b0c4-0bc96a3d38c4/60.webp)
|306|PVCSDC-3005|cordless_cleaner|❌|speed, timer, amount|![all](https://images.cdn.polaris-iot.com/8/5e/6e656-7813-4d03-b0c4-0bc96a3d38c4/60.webp)
|180|PSF-3315|fan|✔️|speed, timer, turbo, amount, volume, child_lock, smart_mode|![all](https://images.cdn.polaris-iot.com/0/b0/6a48d-34d0-4ca9-b6da-13836486400b/60.webp)
|248|PSF-4025|fan|❌|speed, timer, volume, child_lock|![all](https://images.cdn.polaris-iot.com/a/00/d21fb-2149-43cb-8426-2f99cfb3580d/60.webp)
|5|PWS1830/1883|floor-scales|❌ bluetooth||![all](https://images.cdn.polaris-iot.com/f/cc/49dba-e496-44af-9d44-a657109675c5/60.webp)
|3|PWS18XX|floor-scales|❌ bluetooth||![all](https://images.cdn.polaris-iot.com/2/16/8d351-214b-4c16-8c52-09a4e9b568a6/60.webp)
|167|Scales-collection|floor-scales|❌ bluetooth||![all](https://images.cdn.polaris-iot.com/f/c4/584c3-3ee5-4f5f-bee7-10b99626a70c/60.webp)
|141|SLG-V3|generator|❌ bluetooth||![all](https://images.cdn.polaris-iot.com/4/14/8b312-c022-494a-86ce-0091e37168f2/60.webp)
|144|SLG-V4|generator|❌ bluetooth||![all](https://images.cdn.polaris-iot.com/4/14/8b312-c022-494a-86ce-0091e37168f2/60.webp)
|179|PGP-3010-SMOKELESS|grill|❌|speed, timer, turbo, volume, child_lock|![all](https://images.cdn.polaris-iot.com/2/ea/c9dfe-cd3d-4f04-bd55-67b14f6e8c84/60.webp)
|96|PGP-4001|grill|❌|timer, child_lock, temperature|![all](https://images.cdn.polaris-iot.com/6/71/a0394-5753-4bd7-abcc-963f34fb79a9/60.webp)
|120|PHD-4000|hair_care|❌|speed, stream_warm, temperature|![all](https://images.cdn.polaris-iot.com/b/6c/73ab1-d25f-44d7-98a7-7f91e6d40628/60.webp)
|184|PHS-1300|hair_care|❌|child_lock, temperature|![all](https://images.cdn.polaris-iot.com/7/97/7f835-fabd-4221-b90c-f32cf4a5bd1d/60.webp)
|171|PHSB-5000DF|hair_care|❌|speed, pressure, water_tank, stream_warm, temperature|![all](https://images.cdn.polaris-iot.com/4/54/d75e0-7363-4aad-8f8e-e55d83052fd9/60.webp)
|145|PHSC-1234|hair_care|❌|ioniser, humidity, temperature|![all](https://images.cdn.polaris-iot.com/2/fe/425f6-be9b-47ca-a34b-5fc12dbf8443/60.webp)
|297|8006|hood|❌|speed, volume, backlight|![all](https://images.cdn.polaris-iot.com/9/90/76d89-cfd0-4cd7-bb9e-d10ab3581e75/60.webp)
|296|8029|hood|❌|speed, timer, volume, backlight|![all](https://images.cdn.polaris-iot.com/7/6d/2a005-b939-4d6b-98cb-d0779bc19fff/60.webp)
|295|6065A-600|hood|❌|speed, timer, volume, backlight|![all](https://images.cdn.polaris-iot.com/d/bb/2810a-837e-4959-9793-7af2ef933c42/60.webp)
|283|PGS-2250VA|iron|❌|volume, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/f/e8/84ba2-8592-412d-b067-ce36ad9442d4/60.webp)
|91|PIR-2624AK-3m|iron|❌|timer, child_lock|![all](https://images.cdn.polaris-iot.com/d/ab/4f72f-088f-44fe-9f78-81c36244a657/60.webp)
|161|PIR-3074SG|iron|❌|speed, timer, volume, humidity, child_lock|![all](https://images.cdn.polaris-iot.com/d/ab/4f72f-088f-44fe-9f78-81c36244a657/60.webp)
|173|PIR-3210AK-3m|iron|❌|speed, timer, volume, child_lock|![all](https://images.cdn.polaris-iot.com/3/69/57212-fd8d-4a7a-a0aa-fcd954becb28/60.webp)
|174|PIR-3225AK-3m|iron|❌|speed, timer, turbo, volume, humidity, child_lock|![all](https://images.cdn.polaris-iot.com/4/d1/793cf-adc8-4342-9e5d-447a0c8b1724/60.webp)
|191|PSS-2002K|iron|❌|volume, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/f/e8/84ba2-8592-412d-b067-ce36ad9442d4/60.webp)
|259|PSS-8010K|iron|❌|volume, backlight, child_lock, stream_warm|![all](https://images.cdn.polaris-iot.com/5/5e/6ef87-83d0-4089-be9a-b240be7273f6/60.webp)
|159|PSS-9090K|iron|❌|speed, turbo, volume, child_lock, stream_warm, temperature|![all](https://images.cdn.polaris-iot.com/4/ba/f6029-12bf-4598-87e0-06a4ca6fe68b/60.webp)
|237|SM-8095|kitchen_machine|❌|speed, timer, child_lock, multi_step|![all](https://images.cdn.polaris-iot.com/c/da/ab2e1-775a-4bc4-9a18-fe004ffafdc7/60.webp)
|272|SM-8095|kitchen_machine|❌|speed, timer, child_lock, multi_step|![all](https://images.cdn.polaris-iot.com/c/da/ab2e1-775a-4bc4-9a18-fe004ffafdc7/60.webp)
|32|PMG-2580|meat_grinder|❌|speed, turbo, volume, child_lock|![all](https://images.cdn.polaris-iot.com/7/68/d874e-389d-49e6-8901-705740dbedc8/60.webp)
|216|PMG-3060|meat_grinder|❌|speed, timer, volume, child_lock|![all](https://images.cdn.polaris-iot.com/f/47/83e05-570f-4ccd-9455-612611d6568c/60.webp)
|116|Smart-Lid|other|❌|speed, battery|![all](https://images.cdn.polaris-iot.com/f/fc/274e8-7ddf-4429-b827-f63b141c6db9/60.webp)
|182|Voice-Ring|other|❌ bluetooth||![all](https://images.cdn.polaris-iot.com/7/ca/7d669-ba3a-4549-b264-ddae6380d505/60.webp)
|170|Watch|other|❌ bluetooth||![all](https://images.cdn.polaris-iot.com/c/a2/d9565-3316-4613-9b02-5ec661fc15d6/60.webp)
|258|Watch(new)|other|❌ bluetooth||![all](https://images.cdn.polaris-iot.com/c/a2/d9565-3316-4613-9b02-5ec661fc15d6/60.webp)
|299|xbcook55|oven|❌|timer, backlight, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/7/85/de907-82ba-4d53-8ace-8b69cca67b19/60.webp)
|300|xbcook56|oven|❌|timer, backlight, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/e/ed/5db11-cb6f-46b0-8dd7-ce0d2be619fc/60.webp)
|298|xbcook62|oven|❌|timer, turbo, backlight, keep_warm, child_lock, multi_step, delay_start, temperature|![all](https://images.cdn.polaris-iot.com/e/e4/15875-9874-4209-bc43-0dc80ce11b01/60.webp)
|92|PGS-1450CWIFI|steamer|❌|speed, child_lock|![all](https://images.cdn.polaris-iot.com/1/00/43d2d-5a4b-4de7-a60a-767a007b7f5c/60.webp)
|94|PSS-7070KWIFI|steamer|❌|water_tank, temperature|![all](https://images.cdn.polaris-iot.com/1/00/43d2d-5a4b-4de7-a60a-767a007b7f5c/60.webp)
|50|PETB-0202TC|toothbrush|❌|timer, smart_mode|![all](https://images.cdn.polaris-iot.com/d/d5/14363-6a8e-4d0d-bee1-658994b95305/60.webp)
</details>

<details>
  <summary>Устройства РУСКЛИМАТ</summary>

| ID    | Модель           | Тип устройства | Поддержка | Функции | Изображение |
| :---: |------------------|----------------|-----------|---------|    :---:    |
|801|Electrolux EAP-1040D/1055D|air-cleaner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/d/6e/53e7d-b244-4fa3-aab6-4edc79c83fc3/60.webp)
|826|Electrolux EAP-2050D/2075D|air-cleaner|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/e/ec/989e2-3a9b-4c7f-ab45-f2397174c878/60.webp)
|803|Ballu ONEAIR ASP-200|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/a/7b/b36b0-70aa-4799-bbf6-c5faf24e038d/60.webp)
|830|Ballu ONEAIR ASP-200S|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/a/7b/b36b0-70aa-4799-bbf6-c5faf24e038d/60.webp)
|832|Ballu ASP-100 / Electrolux EASP-100|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/c/4f/be8b5-5208-4205-a402-b2da3f6db563/60.webp)
|834|Electrolux EPVS / ERVX inv|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/1/4a/3c6c3-30d6-4dfa-b3f4-fc0743f24304/60.webp)
|836|Electrolux EPVS / ERVX inv|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/1/4a/3c6c3-30d6-4dfa-b3f4-fc0743f24304/60.webp)
|859|Ballu ONEAIR ASP-200S|ventilation|✔️ WiFi|fan speed, damper, volume, sound, backlight |![all](https://images.cdn.rusklimat.ru/a/7b/b36b0-70aa-4799-bbf6-c5faf24e038d/60.webp)
|869|Ballu ASP-100 / Electrolux EASP-100 with music|ventilation|✔️ WiFi|fan speed, volume, sound, backlight |![all](https://images.cdn.rusklimat.ru/7/24/0e706-f264-4635-8fa8-715ab6a2a9b1/60.webp)
|898|Shuft Allston-VH/ERV Комплектный пульт|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/2/ec/fca9a-e694-48ad-85f9-3ed9eac3eaba/60.webp)
|900|Shuft Allston-VH/ERV Пульт AirPad 7|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/2/a8/4b8c3-e36c-4701-9c8f-e43c6fbbee07/60.webp)
|902|Ballu ONEAIR ASP-90|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/7/24/0e706-f264-4635-8fa8-715ab6a2a9b1/60.webp)
|905|Ballu ONEAIR ASP-90|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/7/24/0e706-f264-4635-8fa8-715ab6a2a9b1/60.webp)
|906|Ballu ONEAIR ASP-90|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/7/24/0e706-f264-4635-8fa8-715ab6a2a9b1/60.webp)
|907|Ballu ONEAIR ASP-90|ventilation|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/7/24/0e706-f264-4635-8fa8-715ab6a2a9b1/60.webp)
|827|Ballu RDU ANTICOVIDgenerator WiFi|recirculator|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/6/b3/c8e39-e547-4bc8-88eb-786a6e50cb06/60.webp)
|808|Electrolux Atrium DC / Zanussi Siena DC / Ballu Lagoon|air-conditioner|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/d/a7/5ab4d-2ce4-4b23-a441-7abd441a832d/60.webp)
|810|Zanussi Massimo Solar|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/5/7e/85f4a-2572-484b-9acf-3ed07aa085f5/60.webp)
|813|Electrolux Smartline/ Ballu Eco Smart/ Ice Peak|air-conditioner|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/4/b8/462f8-ce2b-466f-a3fd-19f10b09ddb4/60.webp)
|815|Electrolux Viking DC / Zanussi Perfecto DC / Ballu Greenland DC|air-conditioner|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/7/be/01024-1bc0-4591-9820-cfee40ff3efc/60.webp)
|820|Ballu Platinum Evol. DC/Olympio Legend|air-conditioner|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/c/2f/bf74f-cf56-454a-8131-86cb4ca6be11/60.webp)
|821|Zanussi Moderno DC/Electrolux Loft DC|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/f/7e/a2a32-9cba-452e-b8ad-0ca146ef34d5/60.webp)
|838|Toshiba Shorai EE|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/5/b1/30a44-26ae-40b1-aa01-2050bcf54111/60.webp)
|841|Electrolux Monaco DC|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/d/f1/5a9ab-521d-424d-b09a-51fa341a1b42/60.webp)
|851|Zanussi Massimo Solar 2023|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/9/5f/0f996-7c0b-4347-8b66-837ce254bf8b/60.webp)
|855|Zanussi Barocco DC/ Royal Thermo Barocco DC|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/d/25/1ed97-c608-45be-9c9e-4ed15f5f27e9/60.webp)
|856|Toshiba|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/b/ae/2fadb-de06-4d04-bcd9-e49ffc849f7b/60.webp)
|857|Shuft Berg/ MBO M-1|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/c/24/90a69-8ec9-4ae4-9d1a-76a91286c1e0/60.webp)
|860|Ballu Discovery DC|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/5/80/16337-6860-4cfe-a4f3-76c58a6e6bdd/60.webp)
|868|Electrolux Loft DC/Ballu Platinum Black DC|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/8/3d/084c3-decd-4af1-bb0c-479c20bd5965/60.webp)
|870|Ballu Universal 3, DC, Free Match|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/2/09/9639a-fb15-4ab4-803f-846eaa6376f2/60.webp)
|872|Zanussi Barocco/ Royal Thermo Barocco|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/d/25/1ed97-c608-45be-9c9e-4ed15f5f27e9/60.webp)
|882|Goldstar GSAC/GSACI|air-conditioner|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/d/f9/55d2b-71e6-4767-b1db-5475175bc517/60.webp)
|883|Ballu Aura|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/f/72/25330-705f-4a6c-9593-89a938edf245/60.webp)
|884|Ballu Aura|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/8/82/0d9e0-a1ab-4522-b220-544515bd7fec/60.webp)
|885|Aurus D|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/5/98/ef4ab-c310-42d6-bdcd-abc8186c397f/60.webp)
|895|Climer Dresden|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/7/6c/66e82-0b1b-4034-9c45-81d7f95567e0/60.webp)
|899|AURUS A|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/c/37/873be-aa4d-4b99-a6f8-d3c6dc6aed47/60.webp)
|908|Royal Thermo Diamond DC|air-conditioner|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/3/dc/5fcf5-e6fb-48c0-9841-ac4f20800e57/60.webp)
|802|SmartInverter|boiler|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/2/05/e77f7-5d89-42bb-b4ea-c5ae77872c5b/60.webp)
|807|Zanussi Artendo WiFi/ Azurro PRO WiFi|boiler|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/3/5e/5aa2e-de87-4ab6-9d55-da7ce2b2f07d/60.webp)
|812|Electrolux Centurio IQ 2.0/ Maximus WiFi|boiler|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/4/7d/052d7-a4b4-4b59-b906-39dd8e2dc6bc/60.webp)
|816|Ballu Smart WiFi|boiler|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/6/ae/dbe41-2195-47a3-90bb-41592329be83/60.webp)
|818|Electrolux Maximus/ Megapolis WiFi/ Zanussi Splendore XP 2.0/ Artendo PRO-C WiFi|boiler|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/4/77/fa842-cb9a-4d98-a875-2dfc11be1232/60.webp)
|819|Electrolux Regency|boiler|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/0/df/38bde-b7f9-44a2-ab2f-f8530e745fb2/60.webp)
|833|Electrolux Centurio IQ 3.0|boiler|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/4/7d/052d7-a4b4-4b59-b906-39dd8e2dc6bc/60.webp)
|844|Royal Thermo Aqua Inverter/ Royal Thermo Aqua Inox Inverter|boiler|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/4/a4/4efd3-7b6c-4e56-92c7-41b5f2a2a4f7/60.webp)
|874|Aurus S|boiler|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/b/7d/f1e52-2725-44b4-99e0-8eb0231f9f74/60.webp)
|876|Electrolux Royal Flash/ Centurio IQ Inverter|boiler|✔️ WiFi|mode, temperature, smart, bss, child_lock |![all](https://images.cdn.rusklimat.ru/4/7d/052d7-a4b4-4b59-b906-39dd8e2dc6bc/60.webp)
|877|Royal Thermo Major Inverter/ Smalto Inverter|boiler|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/c/8d/27904-4db3-4bfb-92f5-fedfe051d5f2/60.webp)
|880|Aurus F|boiler|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/6/9f/a9f33-729b-43e1-9bc9-dba9460d6457/60.webp)
|890|Ballu Cetrion Inverter/ Ballu Cetrion Inox Inverter|boiler|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/c/8d/27904-4db3-4bfb-92f5-fedfe051d5f2/60.webp)
|891|Royal Thermo Regency|boiler|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/f/fc/fc57a-c3f4-4b16-a751-f5bbfdd3b77d/60.webp)
|850|Electrolux 3D Fireplace|fireplace|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/2/d3/1670a-7e6f-4b3b-b8cd-0eb90b13685a/60.webp)
|806|Transformer DI 3.0|heater|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/5/9b/4b0d8-9d7a-4d07-bb46-6880703cb814/60.webp)
|809|Transformer DI 3.0 S|heater|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/5/9b/4b0d8-9d7a-4d07-bb46-6880703cb814/60.webp)
|811|Ballu Rapid|heater|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/6/d5/3c5f6-2e58-4885-b83b-84542d2419cd/60.webp)
|814|Transformer DI|heater|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/5/9b/4b0d8-9d7a-4d07-bb46-6880703cb814/60.webp)
|817|Wi-Fi Convection Heater|heater|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/5/9b/4b0d8-9d7a-4d07-bb46-6880703cb814/60.webp)
|828|Transformer DI 4.0|heater|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/5/9b/4b0d8-9d7a-4d07-bb46-6880703cb814/60.webp)
|831|Transformer 4.0|heater|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/5/9b/4b0d8-9d7a-4d07-bb46-6880703cb814/60.webp)
|842|Transformer DI 3.0 XS|heater|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/5/9b/4b0d8-9d7a-4d07-bb46-6880703cb814/60.webp)
|846|Transformer DI 4.0|heater|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/d/9e/3c438-8eeb-49f6-827b-41f93b081088/60.webp)
|847|Wi-Fi Convection Heater|heater|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/4/8c/a707d-12f9-4f91-8781-3e410dbcd0be/60.webp)
|849|Transformer 4.0|heater|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/5/9b/4b0d8-9d7a-4d07-bb46-6880703cb814/60.webp)
|871|Transformer DI 4.0|heater|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/d/9e/3c438-8eeb-49f6-827b-41f93b081088/60.webp)
|889|Aurus|heater|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/c/2d/b8971-21ce-4228-a8d0-d5d0b186f456/60.webp)
|804|Electrolux EHU-3910D/EHU-3915D|humidifier|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/c/be/6c6d6-8aa0-479a-bd5d-3490e5f937e1/60.webp)
|835|Electrolux YOGAhealthline 2.0.|humidifier|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/c/be/6c6d6-8aa0-479a-bd5d-3490e5f937e1/60.webp)
|881|UHB-960 ET|humidifier|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/3/2a/6e189-dbf5-43bf-9b5d-e6a0c5b40a0a/60.webp)
|875|Aurus Infrared|ir-heater|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/e/d9/4cb80-d083-4dca-9ce9-bbe5a05e7ad2/60.webp)
|805|WFN-02|other|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/b/db/3ec7d-b5c0-4a51-ba4f-e7508b5eacfc/60.webp)
|825|WFN-02 D4|other|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/b/db/3ec7d-b5c0-4a51-ba4f-e7508b5eacfc/60.webp)
|843|WFN-02-01/02|other|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/b/db/3ec7d-b5c0-4a51-ba4f-e7508b5eacfc/60.webp)
|866|Smart valve manipulator WZB400W|other|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/c/d0/ca21d-fd6a-4e09-b9f0-08b331afe306/60.webp)
|893|Smart valve manipulator WZB400W|other|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/c/d0/ca21d-fd6a-4e09-b9f0-08b331afe306/60.webp)
|822|Hommyn Hub HH-01|other|❌ WiFi+Zigbee| |![all](https://images.cdn.rusklimat.ru/5/61/29639-3761-4a68-9356-3541a1909ae4/60.webp)
|897|Hommyn Hub HH-01*|other|❌ WiFi+Zigbee| |![all](https://images.cdn.rusklimat.ru/5/61/29639-3761-4a68-9356-3541a1909ae4/60.webp)
|837|Water leak sensor WS-20-Z|sensor|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/b/5e/92015-ca65-46c9-8740-89bf3d374c4f/60.webp)
|839|Temperature sensor TS-20-Z|sensor|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/0/dd/a5a7f-5c86-4372-b8c6-14a4cbf66d79/60.webp)
|840|Motion and Light sensor MS-21-Z|sensor|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/a/79/cfe16-889c-444b-b3d7-23570c373b6b/60.webp)
|852|Water leak sensor WS-30-Z|sensor|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/d/30/796ed-1009-4281-8b98-2115205a393d/60.webp)
|853|Temperature sensor HTSZ-01|sensor|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/9/52/7210c-44c3-45e7-9dc2-6ddf7b8602a2/60.webp)
|854|Opening sensor DS-20-Z|sensor|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/d/d1/90b96-4c65-4d6e-aaf8-ffbb69f24104/60.webp)
|879|Opening sensor OS30ZB|sensor|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/6/66/15349-082b-4157-a5d4-fa30037b27d1/60.webp)
|886|Motion and Light sensor MBS30ZB|sensor|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/b/c5/8c38b-2311-45e8-beba-4b6aeda79f41/60.webp)
|887|Water leak sensor WLS30ZB|sensor|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/9/78/5e913-7196-4eca-a1a7-3a5e686d6b5d/60.webp)
|892|Temperature and Humidity sensor THS30ZB|sensor|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/e/80/df347-477a-4771-b825-c42eb007cfe8/60.webp)
|858|Smart socket RKNZ01|socket|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/6/14/c9972-9bb6-459b-9029-9d6e535987f1/60.webp)
|861|One-channel relay|socket|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/b/5e/4f553-bc02-427f-a076-c808d850c653/60.webp)
|862|Two-channel relay|socket|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/e/92/3f75e-7c53-4b6d-a4b6-24a96f9b467b/60.webp)
|863|One-key switch SWZBNN01W|socket|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/5/f5/de1ce-f185-4961-aaa8-8e3bf6fa871c/60.webp)
|864|Two-key switch SWZBNN02W|socket|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/f/b6/0dd4b-8317-468a-b9a9-13fc945d416e/60.webp)
|888|1-channel AC/DC relay DCRLZBN01|socket|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/9/92/5da45-45f0-4e83-b54a-5b1fb1d24a87/60.webp)
|894|Smart socket RKNZ02|socket|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/f/3f/1473b-253c-4aa7-bc4c-4c62f8142009/60.webp)
|903|Inwall outlet RKNWOZ01W|socket|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/3/78/7d451-9a6f-4e97-90b9-8720ababb20e/60.webp)
|904|Dimmer switch rotary DSWZBN01W|socket|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/7/5d/f64b2-b2c0-4df2-ac09-c7058e12d938/60.webp)
|829|Electrolux/Royal Thermo|thermostat|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/4/6d/834bb-ca32-45d4-9b00-2009e9035816/60.webp)
|865|SmartControl|thermostat|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/6/fa/b75ab-2e92-49eb-9c1a-38eb03a4853e/60.webp)
|867|Electrolux/Royal Thermo|thermostat|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/1/37/4f271-8d3b-4e8e-a598-dfdfcfbacbbb/60.webp)
|873|SmartControl Pro|thermostat|❌ WiFi| |![all](https://images.cdn.rusklimat.ru/6/fa/b75ab-2e92-49eb-9c1a-38eb03a4853e/60.webp)
|878|Electrolux/Royal Thermo|thermostat|✔️ WiFi| |![all](https://images.cdn.rusklimat.ru/4/6d/834bb-ca32-45d4-9b00-2009e9035816/60.webp)
|823|TZE200|thermostatic-radiator|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/8/92/8a703-7713-41c4-a74a-c5b47df67a84/60.webp)
|824|Royal Thermo Smart Heat|thermostatic-radiator|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/f/b0/61277-8a08-468e-9619-f8b0305c0a66/60.webp)
|901|Royal Thermo Smart Heat schedule modes|thermostatic-radiator|❌ Zigbee| |![all](https://images.cdn.rusklimat.ru/f/b0/61277-8a08-468e-9619-f8b0305c0a66/60.webp)


</details>

