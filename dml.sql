INSERT INTO users (username, role,email) VALUES
	('admin', 'admin','admin@admin.com'),
	('Pengdi', 'user','test1@test.com'),
	('David', 'user','test2@test.com'),
	('Tony', 'user','test3@test.com'),
	('Five', 'user','test4@test.com'),
	('Terry', 'user','test5@test.com');

INSERT INTO transaction(sender, receiver, timestamp, amount, message) VALUES 
	('David', 'Terry',20190911160812, 750, 'nice bro'),
	('David', 'Pengdi',20191021163413, 800, 'nice work'),
	('Pengdi', 'David',20190911180812, 1000, 'cool'),
	('Pengdi', 'Tony',20191021203413, 120, 'nice'),
	('Terry', 'Tony',20190911090812, 130, 'efficient'),
	('Terry', 'Tony',20191021123413, 150, 'nice thanks'),
	('Tony', 'David',20190911140812, 1000, 'nice appreciate it'),
	('Tony', 'Pengdi',20191021103013, 300, 'haha'),
	('Five', 'Tony',20190911181812, 1000, 'Take it, take it all');

INSERT INTO redemption (username, timestamp,amount) VALUES
	('Terry', 20190915090812,1);


INSERT INTO account (username, to_give,to_receive, to_redeem) VALUES
	('David', 1000,0, 0),
	('Pengdi', 1000,0, 0),
	('Terry', 1000,0, 1),
	('Tony', 1000,0, 0),
	('Five', 1000,0, 0);

--find transcation history
select * from transaction where sender='{name}' or receiver = '{name}'

