use netflix;

-- data Table
select * from users;

SHOW COLUMNS FROM `users`;

SELECT count(id)
FROM users;


-- shows Table
SELECT * FROM shows;

SHOW COLUMNS FROM `shows`;

SELECT count(show_id)
FROM shows;

SELECT *
from shows
WHERE show_id = 6879;