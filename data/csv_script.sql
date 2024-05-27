USE netflix;
-- To import data go to DataBase -> Tables -> Right Click ->  Table data import wizard -> Import you table by importing the csv file

TRUNCATE TABLE data;

ALTER TABLE data
ADD PRIMARY KEY(show_id);

alter table data MODIFY show_id INT AUTO_INCREMENT;