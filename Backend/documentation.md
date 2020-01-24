# Tante truus documentation

# Objects

## User
```python
     {
        'uuid': "2537b65c-c05b-4cc9-841c-21afd99d07e1",
        'name': "tante truus",
        'user_hash': "$2a$12$ET0G1FghQPhHX7fdTQna.oRbK3I.WKiDB7bObvMJRdPV66Y9OM.O",
        'email': "test@tantetruus.com",
        'birthdate': "07/03/1999",
        'schedule': schedule Object,
        'expenses': expenses Object,
        'install_id': "xxxxxxxxxxx:...",
        'created_at': "2019-12-10 20:00:48.839840",
        'last_login': "2019-12-10 "
    }
```

## Schedule
```python
    {
        'schedule': Array[event]
    }
```
## Event
```python
     {
        'event_uuid': "2537b65c-c05b-4cc9-841c-21afd99d07e1",
        'start': "14/12/2019 18:43:00",
        'end': "14/12/2019 19:43:00",
        'title': "Meeting",
        'content': "Details",
        'location': "Company building",
        'created_at': "2019-12-10 20:00:48.839840"
    }
```

## Expenses
```python
    {
        'expenses': Array[Expense]
    }
```
## Event
```python
    {
        'expense_uuid': "2537b65c-c05b-4cc9-841c-21afd99d07e1",
        'title': "Groceries",
        'expense_type': "exp",
        'est_amount': 200,
        'cur_amount': 100
    }
```


# Routes

## Auth
### Register
**URL:** /auth/register

**Methods:** [POST]

**Form data:** 
```
{
    name: string,
    email: string, 
    password: string, 
    birthdate: string [dd/mm/yyyy]
}
```

**Succes response:** 
```json
 {
     'success': True
 }
```

**Error response:** 
```json
{
    'success': False,
    'error': ["Invalid email", "Fields empty", "Invalid datetime format"]
}
```

### Login
**URL:** /auth/login

**Methods:** [POST]

**Form data:** 
```
{
    email: string, 
    password: string
}
```

**Succes response:** 
```json
 {
     'success': True,
     'uuid': "User uuid"
 }
```

**Error response:** 
```json
{
    'success': False,
    'error': ["User not found", "Password does not match"]
}
```

## User
### Get
**URL:** /user/get

**Methods:** [POST]

**Form data:** 
```
{
    uuid
}
```

**Succes response:** 
```json
 {
     'success': True,
     'data':
     {
        'uuid': "2537b65c-c05b-4cc9-841c-21afd99d07e1",
        'name': "tante truus",
        'email': "test@tantetruus.com",
        'birthdate': "07/03/1999",
        'created_at': "2019-12-10 20:00:48.839840",
        'last_login': "2019-12-10"
     }     
 }
```

**Error response:** 
```json
{
    'success': False,
    'error': ["Invalid user UUID", "User not found"]
}
```

### Update
**URL:** /user/update

**Methods:** [POST]

**Form data:** (All data required) 
```
{
    name: string,
    email: string, 
    password: string, 
    birthdate: string [dd/mm/yyyy]
}
```

**Succes response:** 
```json
 {
     'success': True,
     'uuid': "User uuid"
 }
```

**Error response:** 
```json
{
    'success': False,
    'error': ["User not found", "Password does not match"]
}
```

## Schedule
### Get
**URL:** /user/schedule/get

**Methods:** [POST]

**Form data:** 
```
{
    user_uuid
}
```

**Succes response:** 
```json
 {
     'success': True,
     'data':
     {
        'schedule': Array[Event]
     }     
 }
```

**Error response:** 
```json
{
    'success': False,
    'error': ["Invalid user UUID", "User not found"]
}
```

### Update
**URL:** /user/schedule/update

**Methods:** [POST]

**Form data:** (If event_uuid is set the event will be updated, else it will be added) 
```
{
    user_uuid: string
    start: string [dd/mm/yyyy hh:mm:ss]
    end = string [dd/mm/yyyy hh:mm:ss]
    title = string
    content = string
    location = string
    event_uuid = uuid4 (optional)
}
```

**Succes response:** 
```json
 {
     'success': True
 }
```

**Error response:** 
```json
{
    'success': False,
    'error': 
    [
        "Invalid user UUID", 
        "User not found", 
        "Invalid start-/end time format", 
        "Start must be before and in the future", 
        "Invalid event UUID", 
        "Reminder not found", 
        "Fields empty"
    ]
}
```

