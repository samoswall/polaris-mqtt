# hacs-polaris 
![all](https://github.com/samoswall/hass-polaris/blob/main/logo&icon.png)

## Polaris IQ Home devices integration to Home Assistant
## Интеграция Home Assistant для техники Polaris.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
![](https://img.shields.io/github/watchers/samoswall/hacs-polaris.svg)
![](https://img.shields.io/github/stars/samoswall/hacs-polaris.svg)

[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://yoomoney.ru/fundraise/b8GYBARCVRE.230309)

> [!NOTE]
> ### Интеграция для техники Polaris c поддержкой mqtt на этапе тестирования!
> ### Устройства без поддержки mqtt в приложении пока не поддерживаются.
> :information_source: **Добавлены**: <br>
:heavy_check_mark: Чайники <br>
:heavy_check_mark: Увлажнители <br>
> :information_source: **Как добавить новое устройство**: <br>
Создаем issues - Добавить ...  <br>
Обязательно указать type(ID) устройства и желательно развернутый mqtt топик для понимания, что добавлять. <br>
> :information_source: **Возможные проблемы**: <br>
В чайниках с поддержкой веса - может отсутствовать(быть лишним) сенсор веса и сенсор на базе.  <br>
Проблема - есть одинаковые модели как с весом так и без. Отличаются type(ID). <br>
Не стесняемся, создаем issues - отсутствует(лишний) сенсор ... type ... <br>
По другим предложениям (проблемам, логике работы, иконкам, переводам) пишем issues <br>
> :information_source: **Планы для доработок**: <br>
:black_large_square: Добавить поддержку старых устройств (со старой структурой топика) <br>
:black_large_square: Добавить сенсор ошибок (описание ошибки в атрибут) <br>
:black_large_square: Добавить устройсто online/offline <br>


## Устройства Polaris

| ID    | Модель           | Тип устройства | Поддержка | Изображение |
| :---: |------------------|----------------|-----------|    :---:    |
|2|PWK 1775CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)|
|6|PWK 1725CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)|
|8|PWK 1755CAD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/4/52/2f530-8ebb-426d-98d1-5922508ecbbc/60.webp)|
|29|PWK-1712CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/2/1e/87fb9-b3ab-4fc1-a184-1008e57064fb/60.webp)|
|35|PWK 1775CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)|
|36|PWK 1725CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)|
|37|PWK 1755CAD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/4/52/2f530-8ebb-426d-98d1-5922508ecbbc/60.webp)|
|38|PWK-1712CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/e/cc/ddf2f-070d-4867-8099-938bf6a3a084/60.webp)|
|51|PWK 1775CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)|
|52|PWK 1725CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)|
|53|PWK 1755CAD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/4/52/2f530-8ebb-426d-98d1-5922508ecbbc/60.webp)|
|54|PWK-1712CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/e/cc/ddf2f-070d-4867-8099-938bf6a3a084/60.webp)|
|56|PWK 1775CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)|
|57|PWK 1725CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)|
|58|PWK 1755CAD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/4/52/2f530-8ebb-426d-98d1-5922508ecbbc/60.webp)|
|59|PWK-1712CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/0/80/2044e-71b1-4143-80f5-79ccf1dbff96/60.webp)|
|60|PWK 1775CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)|
|61|PWK 1725CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)|
|62|PWK 1755CAD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/4/52/2f530-8ebb-426d-98d1-5922508ecbbc/60.webp)|
|63|PWK-1712CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/4/06/6d215-dfe6-4211-8260-8a72cb50f30e/60.webp)|
|67|PWK-1720CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/6/41/04018-94b4-4ae7-be02-1375b22e39e2/60.webp)|
|82|PWK 1725CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)|
|83|PWK-1712CGLD RGB|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/e/cc/ddf2f-070d-4867-8099-938bf6a3a084/60.webp)|
|84|PWK-1720CGLD RGB|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/6/41/04018-94b4-4ae7-be02-1375b22e39e2/60.webp)|
|85|PWK 1775CGLD SMART|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)|
|86|PWK 1725CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/a/8c/aad08-4d13-489c-9b0f-028486297ac1/60.webp)|
|97|PWK-1712CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/1/4d/812d2-9cd5-473c-8670-865b6fa8cdbe/60.webp)|
|98|PWK 1775CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)|
|105|PWK 1725CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)|
|106|PWK 1725CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)|
|117|PWK-1712CGLD|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/1c/4ff8e-7a0e-400c-9e50-43c6d45d300e/60.webp)|
|139|PWK 1775CGLD VOICE|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/8/08/f91f4-f117-4074-aa8a-d3d177d7c657/60.webp)|
|164|PWK 1728CGLDA|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/38/c5351-2643-4bcf-bd1b-c5d24a7a9b85/60.webp)|
|165|PWK 1755CAD VOICE|kettle|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/8/96/c40d6-068b-4a17-9e9c-f912ee1e70c2/60.webp)|
|4|PUH-9105|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/9d/27f85-2e01-4cd7-85d8-a034e81c5be4/60.webp)|
|15|PUH-7406|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/2/49/d53fe-3e9d-4229-9900-8f621b54ca23/60.webp)|
|17|PUH-9105|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/9d/27f85-2e01-4cd7-85d8-a034e81c5be4/60.webp)|
|18|PUH-9105|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/9d/27f85-2e01-4cd7-85d8-a034e81c5be4/60.webp)|
|25|PUH-6090|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/9/03/6eada-d5f2-4d60-bcfa-d4c9b2669852/60.webp)|
|44|PUH-9105|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/9d/27f85-2e01-4cd7-85d8-a034e81c5be4/60.webp)|
|70|PUH-9105|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/c/9d/27f85-2e01-4cd7-85d8-a034e81c5be4/60.webp)|
|71|PUH-1010|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/7/6d/75075-23c8-44c0-a582-d91919da426d/60.webp)|
|72|PUH-2300|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/6/ee/0c47e-a3d6-4f99-840b-5a74f85e056e/60.webp)|
|73|PUH-3030|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/3/a9/c2d1c-e416-45f5-8a7b-e2ac59c9b164/60.webp)|
|74|PUH-9009|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/a/a7/7bb37-25b8-4d03-99d2-775794af20dc/60.webp)|
|75|PUH-4040|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/0/79/caa3f-4b4d-4092-9a9e-c02ca79d8c4a/60.webp)|
|87|PUH-8080|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/9/3a/2e628-d005-4ce2-be29-93aa56e1d315/60.webp)|
|99|PUH-4040|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/0/79/caa3f-4b4d-4092-9a9e-c02ca79d8c4a/60.webp)|
|140|PAW-0804|humidifier|:x:|![all](https://images.cdn.polaris-iot.com/0/f0/440b3-27bd-49f8-81e4-0af6f8e13dee/60.webp)|
|145|PHSC-1234|humidifier|:x:|![all](https://images.cdn.polaris-iot.com/2/fe/425f6-be9b-47ca-a34b-5fc12dbf8443/60.webp)|
|147|PUH-0205|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/3/34/5f26e-522c-4cc6-a956-3b2d365419ab/60.webp)|
|151|PPA-2025|humidifier|:x:|![all](https://images.cdn.polaris-iot.com/5/c3/171ce-b1b2-4393-82ed-dde91a93a1d8/60.webp)|
|152|PPA-4050|humidifier|:x:|![all](https://images.cdn.polaris-iot.com/1/f5/063f7-4006-4b61-992f-0f2f49f77455/60.webp)|
|155|PUH-8802|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/2/43/7a2e5-ce65-40ee-ac4b-646cf6c91108/60.webp)|
|157|PUH-4550|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/d/b8/9d5a2-a339-47dc-8177-1d0f3561504f/60.webp)|
|158|PUH-6060|humidifier|:heavy_check_mark:|![all](https://images.cdn.polaris-iot.com/9/1b/9e878-5b9e-4ec4-b464-2451912609f8/60.webp)|
|172|PAW-0804|humidifier|:x:|![all](https://images.cdn.polaris-iot.com/0/f0/440b3-27bd-49f8-81e4-0af6f8e13dee/60.webp)|
|1|EVO-0225|cooker|:x:|![all](https://images.cdn.polaris-iot.com/b/8f/ae138-e3b2-448a-8a8e-ca60eb7c3cc5/60.webp)|
|9|PMC-0526WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)|
|10|PMC-0521WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/1/31/fc82e-50af-430e-8d71-043bd7aeb5d2/60.webp)|
|32|PMC-0524WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/e/5f/51204-817a-46fb-a477-c80cad89f019/60.webp)|
|33|PMC-0530WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/2/d9/64dfb-b93e-49b8-874c-766c212698c8/60.webp)|
|39|PMC-0528WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/4/ce/e930f-5b1b-444f-96e2-04b4d9314231/60.webp)|
|40|PMC-0526WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)|
|41|PMC-0521WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/1/31/fc82e-50af-430e-8d71-043bd7aeb5d2/60.webp)|
|47|PMC-0530WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/2/d9/64dfb-b93e-49b8-874c-766c212698c8/60.webp)|
|48|PMC-0528WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/4/ce/e930f-5b1b-444f-96e2-04b4d9314231/60.webp)|
|55|PMC-0524WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/e/5f/51204-817a-46fb-a477-c80cad89f019/60.webp)|
|77|PMC-5040WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/0/40/bbd11-87b7-47ae-9432-74b78d904d74/60.webp)|
|78|PMC-5050WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/1/87/4d6af-60c0-48d3-8939-60400805fca9/60.webp)|
|79|PMC-5017WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/7/41/24cf9-cb91-431c-a5cb-183d2594a5af/60.webp)|
|80|PMC-5020WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/d/da/5a3c8-b17a-4d94-83cd-24bd2e8562d6/60.webp)|
|89|PMC-5055WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/a/67/edd4c-9a92-4cfe-b17e-53a76d282475/60.webp)|
|95|PMC-00000|cooker|:x:|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)|
|114|PMC-5060 Smart Motion|cooker|:x:|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)|
|138|PMC-0526WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)|
|162|PMC-5063WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/e/5f/51204-817a-46fb-a477-c80cad89f019/60.webp)|
|169|PMC-0526WIFI|cooker|:x:|![all](https://images.cdn.polaris-iot.com/6/fd/f7349-f7c0-46e0-b001-787923872799/60.webp)|
|11|PWH-IDF06|boiler|:x:|![all](https://images.cdn.polaris-iot.com/5/e6/60f0f-98be-44ea-bea4-42cc3a27d340/60.webp)|
|30|SIGMA WI-FI|boiler|:x:|![all](https://images.cdn.polaris-iot.com/6/f1/21910-973b-4796-ab35-7bad5b9fb87e/60.webp)|
|31|ENIGMA WI-FI|boiler|:x:|![all](https://images.cdn.polaris-iot.com/5/e6/60f0f-98be-44ea-bea4-42cc3a27d340/60.webp)|
|45|PCM-1540WIFI|coffeemaker|:x:|![all](https://images.cdn.polaris-iot.com/5/1d/50a72-f324-410d-923e-645c5c164775/60.webp)|
|103|PACM-2080AC|coffeemaker|:x:|![all](https://images.cdn.polaris-iot.com/b/2b/8c952-9291-4c02-bce2-4d73f853452d/60.webp)|
|166|PACM-M8|coffeemaker|:x:|![all](https://images.cdn.polaris-iot.com/b/2b/8c952-9291-4c02-bce2-4d73f853452d/60.webp)|
|7|PVCR-3200|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/4/27/7e198-dede-4ea1-a1a7-1cb9b6ce2888/60.webp)|
|12|PVCR-3300|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/5/7a/903fd-3c1e-4c17-a396-97d6a5eb32bd/60.webp)|
|19|PVCR-0833|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/0/48/35580-64af-42e7-9994-55ef1407d591/60.webp)|
|21|PVCR-0735|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/9/89/721c8-9edb-49f0-8016-9b6fefb7b096/60.webp)|
|22|PVCR-1050|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/4/ec/06465-b9e3-4e02-a27c-797fdcf182d1/60.webp)|
|23|PVCR-1028|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/8/a3/68430-8088-404f-af1f-6d79cf4512d0/60.webp)|
|24|PVCR-1229|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/1/25/f2359-b5a6-4e32-a1b5-88283a97c662/60.webp)|
|43|PVCR-0833|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/0/48/35580-64af-42e7-9994-55ef1407d591/60.webp)|
|66|PVCR-3900|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/5/ba/bd543-ba02-4399-ac4a-be7bc65fd4d6/60.webp)|
|68|PVCR-3100|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/4/80/6b6e6-6ecd-437e-b01c-2f14e2cf5b56/60.webp)|
|76|PVCR-3200|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/5/6d/bdc04-52f8-4092-a827-c1455e2a11f8/60.webp)|
|81|PVCR-3400|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/7/78/12125-b314-4cba-96dd-b394da015482/60.webp)|
|88|PVCR-3800|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/1/20/da178-0a48-405d-83f5-c17300f23b5d/60.webp)|
|90|PVCS-2090|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/3/9d/8bcaf-38fa-4168-b71e-cf201171e719/60.webp)|
|100|PVCR Wave-15|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/7/4d/dbdab-a1ec-46e0-a669-57e4e4c24ae8/60.webp)|
|101|PVCR-0726 Aqua|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/1/20/da178-0a48-405d-83f5-c17300f23b5d/60.webp)|
|102|PVCR-1226 Aqua|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/1/20/da178-0a48-405d-83f5-c17300f23b5d/60.webp)|
|104|PVCR-0905|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/6/de/c37ad-21d9-4f15-8c7f-ed8410babd7f/60.webp)|
|107|PVCR-0926|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/1/20/da178-0a48-405d-83f5-c17300f23b5d/60.webp)|
|108|PVCR-0726 GYRO|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/c/61/4b62b-f6f8-47fc-bd48-0112b56e9977/60.webp)|
|109|PVCR-1226 GYRO|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/1/26/3ac2c-ce5a-4c4e-8f2b-d9cfc8653ed7/60.webp)|
|110|PVCR-4105|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/7/2f/6679a-5e9c-4aa1-81dd-80b370c34631/60.webp)|
|111|PVCS-1150|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/1/27/36f11-5225-478f-bbc2-fed844a33639/60.webp)|
|112|PVCR-3700|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/5/b6/684e6-a94d-4fc8-aa61-5a3efef92a92/60.webp)|
|113|PVCR-4000|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/2/bb/d79e5-72a9-44f7-8921-46427cc4beab/60.webp)|
|115|PVCR-3200|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/5/6d/bdc04-52f8-4092-a827-c1455e2a11f8/60.webp)|
|119|PVCR-5001|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/8/f2/f2957-fb7e-4ac4-b644-8eedfeff61d7/60.webp)|
|123|PVCR-6001|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/8/f7/b2aa9-56ab-4ef0-b19e-bc78c9492809/60.webp)|
|124|PVCRDC-5002|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/5/da/761dd-4d18-4958-89e5-cb391aa3238c/60.webp)|
|125|PVCRDC-6002|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/d/e6/0b12b-1c6d-4143-a7f1-acaf586d0499/60.webp)|
|126|PVCRDC-0101|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/a/e3/2643f-16a9-445a-bef6-67e2990b95b2/60.webp)|
|127|PVCR-4105|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/7/2f/6679a-5e9c-4aa1-81dd-80b370c34631/60.webp)|
|128|PVCRAC-7050|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/4/d0/faeef-30f3-4613-8a01-8274330a9d81/60.webp)|
|129|PVCRAC-7070|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/4/80/6b6e6-6ecd-437e-b01c-2f14e2cf5b56/60.webp)|
|130|PVCR-3600|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/6/24/ee896-0ec7-428c-8704-82f446107a45/60.webp)|
|131|PVCR-3900 test|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/5/ba/bd543-ba02-4399-ac4a-be7bc65fd4d6/60.webp)|
|133|PVCR-G2-0726W|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/1/bd/019c4-56b4-4986-a037-81dd7c5db320/60.webp)|
|134|PVCR-G2-0926W|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/2/d1/933a9-c624-449e-b0e9-a66638fbab63/60.webp)|
|135|PVCR-G2-1226|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/d/94/beec6-89df-4e44-a943-eba7cc79bfde/60.webp)|
|136|PVCS-4070|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/3/9d/8bcaf-38fa-4168-b71e-cf201171e719/60.webp)|
|142|PVCR-4500|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/5/ba/bd543-ba02-4399-ac4a-be7bc65fd4d6/60.webp)|
|146|PVCR-5001|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/8/f2/f2957-fb7e-4ac4-b644-8eedfeff61d7/60.webp)|
|148|PVCR-6001|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/8/f7/b2aa9-56ab-4ef0-b19e-bc78c9492809/60.webp)|
|149|PVCRDC-5002|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/5/da/761dd-4d18-4958-89e5-cb391aa3238c/60.webp)|
|150|PVCRDC-6002|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/d/e6/0b12b-1c6d-4143-a7f1-acaf586d0499/60.webp)|
|154|PVCR-5001|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/8/f2/f2957-fb7e-4ac4-b644-8eedfeff61d7/60.webp)|
|156|PVCR-0905|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/f/eb/7cc05-b47a-4646-acc0-ad7d17ce8cc9/60.webp)|
|160|PVCRDC-0101|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/1/9b/495af-1edb-42f6-9d07-ea6dff1327b9/60.webp)|
|163|PVCR-0735|cleaner|:x:|![all](https://images.cdn.polaris-iot.com/9/89/721c8-9edb-49f0-8016-9b6fefb7b096/60.webp)|
|34|PHB-1551WIFI|blender|:x:|![all](https://images.cdn.polaris-iot.com/e/f8/22f01-dd2f-40e3-8f85-d7dc8f9fddce/60.webp)|
|93|PHB-1350WIFI|blender|:x:|![all](https://images.cdn.polaris-iot.com/e/f8/22f01-dd2f-40e3-8f85-d7dc8f9fddce/60.webp)|
|3|PWS18XX|floor-scales|:x:bluetooth|![all](https://images.cdn.polaris-iot.com/2/16/8d351-214b-4c16-8c52-09a4e9b568a6/60.webp)|
|5|PWS1830/1883|floor-scales|:x:bluetooth|![all](https://images.cdn.polaris-iot.com/f/cc/49dba-e496-44af-9d44-a657109675c5/60.webp)|
|167|PWS-1894|floor-scales|:x:bluetooth|![all](https://images.cdn.polaris-iot.com/a/0b/680a4-e1b5-4bc2-8dcf-3d89df9419fa/60.webp)|
|141|SLG-V3|generator|:x:bluetooth|![all](https://images.cdn.polaris-iot.com/4/14/8b312-c022-494a-86ce-0091e37168f2/60.webp)|
|144|SLG-V4|generator|:x:bluetooth|![all](https://images.cdn.polaris-iot.com/4/14/8b312-c022-494a-86ce-0091e37168f2/60.webp)|
|96|PGP-4001|grill|:x:|![all](https://images.cdn.polaris-iot.com/f/e7/e9db2-e3d7-443f-838b-735c66e67b93/60.webp)|
|122|PGP-4001-DEV|grill|:x:|![all](https://images.cdn.polaris-iot.com/f/e7/e9db2-e3d7-443f-838b-735c66e67b93/60.webp)|
|16|PHV-1401|heater|:x:|![all](https://images.cdn.polaris-iot.com/e/3b/3615d-0d9d-4107-9783-df4e9655cdd1/60.webp)|
|46|PCH-0320WIFI|heater|:x:|![all](https://images.cdn.polaris-iot.com/2/ef/6cb11-25b4-4c82-adcf-33f0e01302b8/60.webp)|
|49|PMH-21XX|heater|:x:|![all](https://images.cdn.polaris-iot.com/2/30/eb6b9-5ed3-4536-9e54-b380fd25c178/60.webp)|
|64|PMH-21XX|heater|:x:|![all](https://images.cdn.polaris-iot.com/6/e0/263c0-2c33-4a8a-929c-e998568a5606/60.webp)|
|65|PCH-0320WIFI|heater|:x:|![all](https://images.cdn.polaris-iot.com/2/ef/6cb11-25b4-4c82-adcf-33f0e01302b8/60.webp)|
|91|PIR-2624AK 3m|iron|:x:|![all](https://images.cdn.polaris-iot.com/d/ab/4f72f-088f-44fe-9f78-81c36244a657/60.webp)|
|161|PIR-3074SG|iron|:x:|![all](https://images.cdn.polaris-iot.com/d/ab/4f72f-088f-44fe-9f78-81c36244a657/60.webp)|
|92|PGS-1450CWIFI|steamer|:x:|![all](https://images.cdn.polaris-iot.com/1/00/43d2d-5a4b-4de7-a60a-767a007b7f5c/60.webp)|
|94|PSS-7070KWIFI|steamer|:x:|![all](https://images.cdn.polaris-iot.com/1/00/43d2d-5a4b-4de7-a60a-767a007b7f5c/60.webp)|
|159|PSS-9090K|steamer|:x:|![all](https://images.cdn.polaris-iot.com/1/00/43d2d-5a4b-4de7-a60a-767a007b7f5c/60.webp)|
|26|PTB-RMST201811|toothbrush|:x:bluetooth|![all](https://images.cdn.polaris-iot.com/d/bf/defdd-706b-44fe-9c81-0d9c7b478434/60.webp)|
|27|PTB-RMST201908|toothbrush|:x:bluetooth|![all](https://images.cdn.polaris-iot.com/6/8f/f5141-c7c8-4243-939c-28cdf6423f51/60.webp)|
|28|PTB-RMST201906|toothbrush|:x:bluetooth|![all](https://images.cdn.polaris-iot.com/e/0d/b02c3-8d15-4c4e-842a-1055e7277c7f/60.webp)|
|50|PETB-0202TC|toothbrush|:x:|![all](https://images.cdn.polaris-iot.com/d/d5/14363-6a8e-4d0d-bee1-658994b95305/60.webp)|
|132|PWF-2005|toothbrush|:x:|![all](https://images.cdn.polaris-iot.com/a/a9/fcac0-cc30-4f2f-a1c1-cb38cf77f6db/60.webp)|
|116|Smart-Lid|lid|:x:|![all](https://images.cdn.polaris-iot.com/f/fc/274e8-7ddf-4429-b827-f63b141c6db9/60.webp)|
|120|HAIR-DRYER|hair-dryer|:x:|![all](https://images.cdn.polaris-iot.com/b/6c/73ab1-d25f-44d7-98a7-7f91e6d40628/60.webp)|
|168|Spice Mixer|mixer|:x:|![all](https://images.cdn.polaris-iot.com/f/fc/274e8-7ddf-4429-b827-f63b141c6db9/60.webp)|
|171|HOT BRUSH|brush|:x:|![all](https://images.cdn.polaris-iot.com/b/6c/73ab1-d25f-44d7-98a7-7f91e6d40628/60.webp)|




