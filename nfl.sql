drop database nfl_dfs;
create database nfl_dfs;
use nfl_dfs;

CREATE TABLE `player_stats` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `player_id` int,
  `game_id` int,
  `completed_passes` int,
  `attempted_passes` int,
  `passing_yards` int,
  `passing_touchdowns` int,
  `interceptions_thrown` int,
  `times_sacked` int,
  `quarterback_rating` decimal(4,1),
  `rush_attempts` int,
  `rush_yards` int,
  `rush_touchdowns` int,
  `times_pass_target` int,
  `receptions` int,
  `receiving_yards` int,
  `receiving_touchdowns` int,
  `kickoff_return_touchdown` int,
  `punt_return_touchdown` int,
  `fumbles_lost` int,
  `fumbles_recovered_for_touchdown` int,
  `field_goals_made` int,
  `extra_points_made` int
);

CREATE TABLE `player` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(50),
  `position` varchar(3),
  `sportsreference_id` varchar(20)
);

CREATE TABLE `game` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `home_id` int,
  `away_id` int,
  `date_` date,
  `sportsreference_id` varchar(20)
);

CREATE TABLE `team` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `sportsreference_abbreviation` varchar(4)
  `name` varchar(50)
);

CREATE TABLE `salary` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `player_id` int,
  `salary` int
);

ALTER TABLE `player_stats` ADD FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);

ALTER TABLE `player_stats` ADD FOREIGN KEY (`game_id`) REFERENCES `game` (`id`);

ALTER TABLE `game` ADD FOREIGN KEY (`home_id`) REFERENCES `team` (`id`);

ALTER TABLE `game` ADD FOREIGN KEY (`away_id`) REFERENCES `team` (`id`);

ALTER TABLE `salary` ADD FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);
