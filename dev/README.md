### Вспомогательные скрипты

#### Пример добавление триграмных индексов

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX IF NOT EXISTS idx_users_first_name_trgm ON users USING gist (first_name gist_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_users_last_name_trgm ON users USING gist (last_name gist_trgm_ops);
```
