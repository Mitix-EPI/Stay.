CREATE DATABASE IF NOT EXISTS `resterchezsoi` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `resterchezsoi`;

CREATE TABLE IF NOT EXISTS `user` (
    `user_id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `mail` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `nb_days_completed` int(11) NOT NULL,
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `username` (`username`)
)DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `day` (
    `day_id` int(11) NOT NULL AUTO_INCREMENT,
    `day` datetime,
    `status` enum('neutral','completde','failed') NOT NULL DEFAULT 'neutral',
    PRIMARY KEY (`day_id`),
    UNIQUE KEY `title` (`title`)
)DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user_has_day` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `fk_user_id` int(11) NOT NULL,
    `fk_day_id` int(11) NOT NULL,
    PRIMARY KEY (`id`)
)DEFAULT CHARSET=utf8;
