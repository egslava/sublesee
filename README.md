# health.medm.com python api

A fetcher/parser for
[health.medm.com](https://www.medm.com). It allows you
to access blood pressure, sugar level, heart rhythm and
so on from your python app.

![](docs/_1_medm_bloodpressure_mainpage.png)

# Usage

```bash
pip install git+https://github.com/egslava/pymedm.git#subdirectory=soft
```

```python
from pymedm import load_medm

load_medm(
    os.getenv('MEDM_EMAIL'),
    os.getenv('MEDM_PASSW'),
    from_date='2022-11-05',
    to_date='2022-12-05T20:59:59.999Z',
    type_='bloodpressure'
)
```

```csv
'Medical record,Medical record email,Medical record name,Medical record birthday,Medical record external id label,Medical record external,Medical record provider,Id,Measured at local time,Systolic,Diastolic,Pulse,Body position,Cuff position,Cuff position status,Cuff dressed,Irregular pulse,Measured arm,Measurement postion quality,Movement during measurement,Pulse range,Feeling,Note,Source,Client\n86135c4c-b705-416d-a00c-afda45a753f0,medm@egslava.ru,Medm Developer,-,,,,6befb084-c44d-4ad4-862d-cb7e8bde321d,2022-12-10 10:15:07 +0300,220,110,100,Supine,"","","",Detected,Left,"","","",Bad,Bad,Manual Entry,"{""app_instance_id"":""0f30b004-84e8-481b-88fc-ab1cc97ef3c6"",""app_id"":""medm_bp"",""app_name"":""Blood Pressure"",""app_version"":""2.12.361.95"",""app_utc_offset"":10800,""app_locale"":""en-RU"",""os_family"":""iOS"",""os_version"":""15.7.1"",""os_version_number"":""0"",""os_platform_info"":{""name"":""iPhone"",""model"":""iPhone"",""device"":""iPhone9,3"",""systemName"":""iOS"",""systemVersion"":""15.7.1"",""localizedModel"":""iPhone""},""mobile_equipment"":{}}"\n86135c4c-b705-416d-a00c-afda45a753f0,medm@egslava.ru,Medm Developer,-,,,,0e6acaf9-a726-45c8-b9fc-b52eca841ec4,2022-12-10 10:14:04 +0300,120,70,60,Sitting,"","","",Not detected,Right,"","","",Good,Good,Manual Entry,"{""app_instance_id"":""0f30b004-84e8-481b-88fc-ab1cc97ef3c6"",""app_id"":""medm_bp"",""app_name"":""Blood Pressure"",""app_version"":""2.12.361.95"",""app_utc_offset"":10800,""app_locale"":""en-RU"",""os_family"":""iOS"",""os_version"":""15.7.1"",""os_version_number"":""0"",""os_platform_info"":{""name"":""iPhone"",""model"":""iPhone"",""device"":""iPhone9,3"",""systemName"":""iOS"",""systemVersion"":""15.7.1"",""localizedModel"":""iPhone""},""mobile_equipment"":{}}"\n'
```

`dateutil.parse` is used for date format parsing, so
you can use: timestamp (int) or any various data
formats. Along with the complete list of [examples]
(https://dateutil. readthedocs.io/en/stable/examples.
html#parse-examples), there are:

- "Thu Sep 25 10:36:28 BRST 2003"
- "2003 10:36:28 BRST 25 Sep Thu"
- "Thu 10:36"
- "10:36", "10pm", "12:00am"
- "Thu Sep 25 2003"
- "Sep 25 2003"
- "Sep 2003"
- "Sep"
- "2003"
- "2003-09-25T10:49:41.5-03:00
- "2003-09-25"
- "20030925T104941.5-0300"
- "20030925T104941-0300"
- "20030925"
- "199709020900"
- "2003-09-25"
- "2003-Sep-25" / "25-Sep-2003"/
  "Sep-25-2003"/ "09-25-2003"/
  "25-09-2003"/"2003/09/25"/"2003 Sep 25"/"2003 09 25"
- "10h36m28.5s"/"01s02h03m"/"01h02m03"/"01h02"/"10h am"
- "Wed, July 10, '96", "1996.07.10 AD at 15:08:56 PDT"
  , "Tuesday, April 12, 1952 AD 3:30:42pm PST",
  "November 5, 1994, 8:15:30 am EST"
- "3rd of May 2001", "5:50 A.M. on June 13, 1990"

# Benefits

Why not parse on your own? Primarily, because of
stability.

1. API access can change. This projects has api
   integration tests, so, when the webm server
   implementation changes it will be known instantly.
   The CI/CD pipelines allow shipping fixes quickly.
2. Probably, you're going to use it for medical usage,
   so while the parser code is small, the
   tests/stability take a way more time to maintain.

# Roadmap:
- status/monitor in README.md if API has changed and
  fails