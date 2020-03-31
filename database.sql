CREATE DATABASE IF NOT EXISTS `stay` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `stay`;

CREATE TABLE IF NOT EXISTS `user` (
    `user_id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `mail` varchar(255) NOT NULL,
    `ip` varchar(255) NOT NULL,
    `day` int(11) NOT NULL,
    `date` varchar(255) NOT NULL,
    `timer` varchar(255) NOT NULL, -- Ajouté
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `username` (`username`)
)DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `partner` (
    `partner_id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `mail` varchar(255) NOT NULL,
    `phone` int(11) NOT NULL,
    `address` varchar(255) NOT NULL,
    `offer` varchar(510) NOT NULL,
    `quantity` int(11) NOT NULL,
    PRIMARY KEY (`partner_id`),
    UNIQUE KEY `name` (`name`)
)DEFAULT CHARSET=utf8;