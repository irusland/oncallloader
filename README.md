# oncallloader 

## Usage

### see examples in [scripts](scripts) folder

each script could be run with 
```bash
python get_user.py
```

## Config

### specify environment variables in [.env](scripts/.env)

example:
```dotenv
ONCALL_SETTINGS_URL=http://127.0.0.1:8080
ONCALL_SETTINGS_USERNAME=root
ONCALL_SETTINGS_PASSWORD=1234
```

### for importing a schedule load it into [import.yaml](scripts%2Fimport.yaml)

example:
```yaml
---
teams:
  - name: "k8s SRE"
    scheduling_timezone: "Europe/Moscow"
    email: "k8s@sre-course.ru"
    slack_channel: "#k8s-team"
    users:
      - name: "o.ivanov"
        full_name: "Oleg Ivanov"
        phone_number: "+1 111-111-1111"
        email: "o.ivanov@sre-course.ru"
        duty:
          - date: "02/12/2024"
            role: "primary"
          - date: "03/12/2024"
            role: "secondary"
          - date: "04/12/2024"
            role: "primary"
          - date: "05/12/2024"
            role: "secondary"
          - date: "06/12/2024"
            role: "primary"
```

## Demo

### use [import_schedule.py](scripts/import_schedule.py) to import schedule

run
```bash
python import_schedule.py
```

imported teams
![Screenshot 2023-09-28 at 00.31.32.png](pics%2FScreenshot%202023-09-28%20at%2000.31.32.png)

imported users
![Screenshot 2023-09-28 at 00.32.05.png](pics%2FScreenshot%202023-09-28%20at%2000.32.05.png)

imported schedule
![Screenshot 2023-09-28 at 00.32.00.png](pics%2FScreenshot%202023-09-28%20at%2000.32.00.png)

## Installation

```bash
poetry install
```

## Credits 

[Ruslan Sirazhetdinov - @irusland](https://github.com/irusland)

