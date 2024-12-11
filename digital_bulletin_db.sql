-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 03, 2024 at 10:51 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `digital_bulletin_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `category` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `pinned` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`id`, `title`, `content`, `category`, `date`, `created_at`, `pinned`) VALUES
(1, 'hello', 'hello', 'Announcements', '2024-11-29', '2024-11-29 03:47:14', 0),
(3, 'test ulit', 'f noisfweruvnewugcwercnuwren wrt8unowntmhwrc ntercpmrtcinewnt ccjcpwmetmh vwnecmt wecrcnutpmewrctuwipjmne tnpejkujnp g', 'Announcements', '2024-11-29', '2024-11-29 03:51:53', 0),
(4, 'hello', 'helloooooooooooo', 'Announcements', '2024-11-29', '2024-11-29 03:54:52', 0),
(7, 'final na', 'pag ito di parin gumana', 'Announcements', '2024-11-29', '2024-11-29 04:04:33', 0),
(8, 'latest', 'latest', 'Announcements', '2024-11-29', '2024-11-29 04:13:51', 0),
(11, 'announcement', 'announcement', 'Announcements', '2024-11-29', '2024-11-29 04:18:39', 0),
(13, 'IMPORTANT', 'HELLO\n\n\nTESTINGAN, KAILANGAN UMALIS NA KAYO DITO\n\n\n\nTHANK YOU PO', 'Announcements', '2024-11-29', '2024-11-29 04:19:15', 1),
(14, 'testing event', 'hello\n\n\nhello hello hello\n\nhello\n\n\nhello,\nhello', 'Events', '2024-11-29', '2024-11-29 05:01:12', 1),
(17, 'tangina mo', 'hello', 'Events', '2024-11-29', '2024-11-29 05:29:56', 0),
(18, 'latest news', 'hello hello PATAY', 'News', '2024-11-29', '2024-11-29 09:29:09', 1),
(19, 'last testingan', 'hello hello,\n\n\nhello hello hello hello hello hello\n\nhello hello\n\n\nhello', 'Announcements', '2024-11-30', '2024-11-30 04:30:45', 1),
(20, 'test post', 'test post', 'Announcements', '2024-11-30', '2024-11-30 04:59:30', 0),
(21, 'testing', 'testing testing', 'Announcements', '2024-11-30', '2024-11-30 09:01:01', 0),
(22, 'titeng malaki', 'tite ko malaki', 'Events', '2024-12-02', '2024-12-02 03:09:03', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `created_at`) VALUES
(1, 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin@gmail.com', '2024-11-29 03:26:50'),
(4, 'user1', '0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90', 'user1@gmail.com', '2024-11-29 03:28:00'),
(6, 'user2', '6025d18fe48abd45168528f18a82e265dd98d421a7084aa09f61b341703901a3', 'user2@gmail.com', '2024-11-29 03:32:54'),
(7, 'user3', '5860faf02b6bc6222ba5aca523560f0e364ccd8b67bee486fe8bf7c01d492ccb', 'user3@gmail.com', '2024-11-29 03:33:59'),
(8, 'user4', '5269ef980de47819ba3d14340f4665262c41e933dc92c1a27dd5d01b047ac80e', 'user4@gmail.com', '2024-11-29 03:35:42'),
(9, 'user5', '5a39bead318f306939acb1d016647be2e38c6501c58367fdb3e9f52542aa2442', 'user5@gmail.com', '2024-11-29 03:35:59'),
(10, 'user6', 'ecb48a1cc94f951252ec462fe9ecc55c3ef123fadfe935661396c26a45a5809d', 'user6@gmail.com', '2024-11-29 04:29:32'),
(11, 'user7', '3268151e52d97b4cacf97f5b46a5c76c8416e928e137e3b3dc447696a29afbaa', 'user7@gmail.com', '2024-11-29 04:48:24'),
(12, 'user8', 'f60afa4989a7db13314a2ab9881372634b5402c30ba7257448b13fa388de1b78', 'user8@gmail.com', '2024-11-29 05:00:21'),
(13, 'user9', '0fb8d3c5dfaf81a387bf0ba439ab40e6343d2155fb4ddf6978a52d9b9ea8d0f8', 'user9@gmail.com', '2024-11-29 09:29:40'),
(14, 'user10', '5bbf1a9e0de062225a1bb7df8d8b3719591527b74950810f16b1a6bc6d7bd29b', 'user10@gmail.com', '2024-11-30 04:59:48');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
