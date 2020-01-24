```https://tantetruus.ovh/auth/register: [POST] // registreer gebruiker // NEEDS username, email, password, birthdate // RETURNS uuid```

```https://tantetruus.ovh/auth/login: [POST] // login gebruiker // NEEDS email, password // RETURNS uuid```

```https://tantetruus.ovh/user/[uuid]/schedule: [POST] // add task to the user's schedule // NEEDS date, start, end, title, content // RETURNS True/ False```

```https://tantetruus.ovh/user/[uuid]/schedule: [GET] // get user's schedule // returns json```
