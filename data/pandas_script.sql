USE netflix;
-- To import data go to DataBase -> Tables -> Right Click ->  Table data import wizard -> Import you table by importing the csv file

TRUNCATE TABLE shows;

ALTER TABLE shows
ADD PRIMARY KEY(show_id);

alter table shows MODIFY show_id INT AUTO_INCREMENT;