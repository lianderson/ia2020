CREATE TABLE `equipe2_palavra` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`palavra` VARCHAR(9999) NOT NULL COLLATE 'latin1_swedish_ci',
	`quantidade` INT(255) NOT NULL,
	`noticia_id` INT(255) NOT NULL,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;
