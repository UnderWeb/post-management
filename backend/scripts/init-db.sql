IF NOT EXISTS (
    SELECT name 
    FROM sys.databases 
    WHERE name = 'posts_db'
)
BEGIN
    CREATE DATABASE posts_db;
END
GO
