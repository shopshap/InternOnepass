-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 09, 2022 at 09:38 AM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.4.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `qrcode`
--

-- --------------------------------------------------------

--
-- Table structure for table `visitor`
--

CREATE TABLE `visitor` (
  `i` int(11) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `detail` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL,
  `timein` varchar(255) NOT NULL,
  `timeout` varchar(255) NOT NULL,
  `department` varchar(255) NOT NULL,
  `phonenumber` varchar(255) NOT NULL,
  `employeeid` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `visitor`
--

INSERT INTO `visitor` (`i`, `ip`, `name`, `detail`, `date`, `timein`, `timeout`, `department`, `phonenumber`, `employeeid`) VALUES
(26, '119.76.14.172', 'ดชช้อป', 'มาทำธุระ', '2022-05-09', '14:09:04', '12:45:55', 'Feedback', '0945236485', 's650001'),
(27, '119.76.14.172', 'TETHXeRuS', '4asdasdasdasd', '2022-05-09', '14:15:39', 'OUT', 'Feedback', '0621924968', 'S650004'),
(28, '119.76.14.172', 'Pramote Kaewdonmong', '545151', '2022-05-09', '14:19:42', '', 'Auction', '0621924968', 'S650004'),
(29, '119.76.14.172', 'TETHXeRuS', '4845454', '2022-05-09', '14:21:49', '', 'New Buyer', '0621924968', 'S650004'),
(30, '119.76.14.172', 'TETHXeRuS', '545151', '2022-05-09', '14:22:51', '', 'Auction', '0621924968', 'S650004'),
(31, '119.76.14.172', 'ปราโมทย์ แก้วดอนโมง', 'asdasd', '2022-05-09', '14:25:07', '14:28:48', 'New Buyer', '+66621924968', 'S650004'),
(32, '119.76.14.172', 'Date', 'asdasdad', '2022-05-09', '14:26:33', '', 'Auction', 'asdasd', 'S650004'),
(33, '119.76.14.172', 'ปราโมทย์ แก้วดอนโมง', 'asdasdasd', '2022-05-09', '14:28:26', '14:28:48', 'Feedback', '+66621924968', 'S650004'),
(34, '119.76.14.172', 'Dullahan', 'S', '2022-05-09', '14:28:35', '14:30:04', 'Auction', '0653103809', 'S650002');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `visitor`
--
ALTER TABLE `visitor`
  ADD PRIMARY KEY (`i`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `visitor`
--
ALTER TABLE `visitor`
  MODIFY `i` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
