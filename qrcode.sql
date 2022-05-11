-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 11, 2022 at 05:31 AM
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
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `user` int(11) DEFAULT NULL,
  `name` varchar(24) CHARACTER SET utf8 DEFAULT NULL,
  `agency` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `Phase` varchar(6) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`user`, `name`, `agency`, `Phase`) VALUES
(370480, 'นายบุญส่ง มีแย้ม', 'Operation 1 TOG', 'Phase2'),
(380701, 'นายกิจจา โกศล', 'Operation 1 TOG', 'Phase1'),
(350159, 'น.ส.สมคิด ยวงลำใย', 'OP1 Phase1 Uncoat DL Mould', 'Phase1'),
(380540, 'น.ส.บุษบา หวานฉ่ำ', 'OP1 Phase1 Uncoat DL Mould', 'Phase1'),
(431708, 'นางอรุณ ไทยทรงธรรม', 'OP1 Phase1 Uncoat DL Mould', 'Phase1'),
(514055, 'น.ส.ศิราณี สนภู่', 'OP1 Phase1 Uncoat DL Mould', 'Phase1'),
(545111, 'นางมะลิ รักหอม', 'OP1 Phase1 Uncoat DL Mould', 'Phase1'),
(597415, 'นายธีระ ต้อนแก้ว', 'OP1 Phase1 Uncoat DL Mould', 'Phase1'),
(597723, 'นายศักดิ์ดา เยื่องเสือ', 'OP1 Phase1 Uncoat DL Mould', 'Phase1'),
(620335, 'น.ส.วนิดา ลูกภูเขียว', 'OP1 Phase1 Uncoat DL Mould', 'Phase1'),
(360218, 'น.ส.บังอร นาคศรีจันทร์', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(391028, 'นายณรงค์ศักดิ์ ดีเดิน', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(421233, 'น.ส.กัญญา สนธิศรี', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(441923, 'นายสมเกียรติ สะมันยี', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(534657, 'น.ส.สุรีรัตน์ คนตรง', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(555812, 'น.ส.อาภรณ์รัตน์ สว่างศรี', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(576839, 'น.ส.วันวิสา คนตรง', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(587026, 'นายประสาน ประกาทอง', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(587248, 'น.ส.สุริสาย บุตรสีสี', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(597581, 'นายธนวัฒน์ เรืองณรงค์', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(597724, 'น.ส.ปรียานุช บุญนาดี', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(608137, 'นายจำลอง ฉลุนรัมย์', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(608222, 'น.ส.สุดาพร แสงดาว', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(620155, 'นายพลากร วงศ์คำผิว', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(620327, 'นายชุติพนธ์ อินทรทัต', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(620328, 'น.ส.นลพรรณ ไชยมา', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(630050, 'น.ส.ณัชชา งามเลิศ', 'OP1 Phase1 Uncoat DL Before Oven', 'Phase1'),
(370467, 'นางจำเนียร ดีเดิน', 'OP1 Phase1 Uncoat DL After Oven', 'Phase1'),
(411160, 'น.ส.ประยอม โต๊ะกา', 'OP1 Phase1 Uncoat DL After Oven', 'Phase1');

-- --------------------------------------------------------

--
-- Table structure for table `result`
--

CREATE TABLE `result` (
  `id` int(11) NOT NULL,
  `Date` varchar(255) NOT NULL,
  `Van01` int(255) NOT NULL,
  `Van02` int(255) NOT NULL,
  `Van03` int(255) NOT NULL,
  `Van04` int(255) NOT NULL,
  `Van05` int(255) NOT NULL,
  `Van06` int(255) NOT NULL,
  `Van07` int(255) NOT NULL,
  `Bus01` int(255) NOT NULL,
  `Bus02` int(255) NOT NULL,
  `Bus03` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `result`
--

INSERT INTO `result` (`id`, `Date`, `Van01`, `Van02`, `Van03`, `Van04`, `Van05`, `Van06`, `Van07`, `Bus01`, `Bus02`, `Bus03`) VALUES
(400, '2022-04-28', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
(401, '2022-04-28', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(402, '2022-04-28', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `resultvisitor`
--

CREATE TABLE `resultvisitor` (
  `id` int(11) NOT NULL,
  `date` varchar(255) NOT NULL,
  `marketing` int(11) NOT NULL,
  `sales` int(11) NOT NULL,
  `hr` int(11) NOT NULL,
  `customerservice` int(11) NOT NULL,
  `accounting` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `Username` varchar(255) DEFAULT NULL,
  `Container` varchar(255) DEFAULT NULL,
  `Time` varchar(255) DEFAULT NULL,
  `Date` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `Username`, `Container`, `Time`, `Date`) VALUES
(400, '545111', 'Bus02', '14:31:10', '2022-04-28'),
(401, '597415', 'Van01', '14:37:26', '2022-04-28'),
(402, '350159', 'Van01', '14:35:51', '2022-04-28');

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
  `employeeid` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `visitor`
--

INSERT INTO `visitor` (`i`, `ip`, `name`, `detail`, `date`, `timein`, `timeout`, `department`, `phonenumber`, `employeeid`, `status`) VALUES
(114, '119.76.14.172', 'ศราวุธ อ่อนศรี', 'มาทำธุระ', '2022-05-10', '16:45:49', '17:00:00', 'ฝ่ายการตลาด', '0653103809', 'S650002', 'ระบบตัด session ตอน 17.00 น.'),
(115, '118.46.45.761', 'ช้อปปี้ ส่งฟรีทั่วไทย\r\n', 'มาหาใครไม่รู้', '2022-05-12', '15:00:01', '17:00:00', 'ฝ่ายขาย', '0922354621', 'S650003', 'ระบบตัด session ตอน 17.00 น.'),
(116, '220.44.57.546', 'นาย ก', 'มาหานาย ข', '2022-06-13', '08:45:51', '17:00:00', 'ฝ่ายบุคคล', '0912354352', 'S650004', 'ระบบตัด session ตอน 17.00 น.'),
(117, '114.55.44.516', 'นาย ข', 'มาหานาย ง', '2022-05-11', '10:59:21', '17:00:00', 'ฝ่ายลูกค้าสัมพันธ์', '0645257998', 'T52111', 'ระบบตัด session ตอน 17.00 น.'),
(118, '785.54.54.716', 'นาย ค', 'มาหานาย ก', '2022-05-15', '12:11:11', '17:00:00', 'ฝ่ายบัญชี/การเงิน', '0512842348', 'T15612', 'ระบบตัด session ตอน 17.00 น.');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `result`
--
ALTER TABLE `result`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `resultvisitor`
--
ALTER TABLE `resultvisitor`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `visitor`
--
ALTER TABLE `visitor`
  ADD PRIMARY KEY (`i`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `result`
--
ALTER TABLE `result`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=403;

--
-- AUTO_INCREMENT for table `resultvisitor`
--
ALTER TABLE `resultvisitor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=403;

--
-- AUTO_INCREMENT for table `visitor`
--
ALTER TABLE `visitor`
  MODIFY `i` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=119;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
