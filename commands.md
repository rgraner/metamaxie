# Importing Heroku Postgres Databases
```
heroku pg:backups:capture
```
```
heroku pg:backups:download
```

# Restore to local database
```
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U myuser -d mydb latest.dump
,,,