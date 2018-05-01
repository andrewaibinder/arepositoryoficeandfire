create table CHARACTERS(
	id int(10) NOT NULL,
	name VARCHAR(255) NOT NULL,
	gender VARCHAR(255),
	culture VARCHAR(255),
	born VARCHAR(255),
	born_start_pre_rough int(10),
	born_end_pre_rough int(10),	
	born_start int(10),
	born_end int(10),
	died VARCHAR(255),
	father VARCHAR(255),
	mother VARCHAR(255),
	spouse VARCHAR(255),
	PRIMARY KEY(id)
	);


create table HOUSES(
	id int(10) NOT NULL,
	name VARCHAR(255) NOT NULL,
	region VARCHAR(255),
	coatOfArms VARCHAR(255),
	words VARCHAR(255),
	currentLord VARCHAR(255),
	heir VARCHAR(255),
	founder VARCHAR(255),
	diedOut VARCHAR(255),
	PRIMARY KEY(id)
	);


create table FACT(
	house_id int(10) NOT NULL,
	character_id int(10) NOT NULL,
	UNIQUE (house_id, character_id)
	);
