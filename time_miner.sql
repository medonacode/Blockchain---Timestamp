-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 13, 2025 at 07:34 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `time_miner`
--

-- --------------------------------------------------------

--
-- Table structure for table `tm_admin`
--

CREATE TABLE `tm_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tm_admin`
--

INSERT INTO `tm_admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `tm_register`
--

CREATE TABLE `tm_register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `ip_address` varchar(30) NOT NULL,
  `mac_address` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tm_register`
--

INSERT INTO `tm_register` (`id`, `name`, `mobile`, `email`, `create_date`, `status`, `ip_address`, `mac_address`) VALUES
(1, 'Vijay', 9654254885, 'vijay@gmail.com', '12-04-2025', 0, '192.168.1.44', 'fb:88:df:b3:31:9b');

-- --------------------------------------------------------

--
-- Table structure for table `tm_selected`
--

CREATE TABLE `tm_selected` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `file_path` varchar(100) NOT NULL,
  `filetype` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `hash_val` varchar(200) NOT NULL,
  `backup_id` int(11) NOT NULL,
  `hash_val2` varchar(200) NOT NULL,
  `atime` varchar(20) NOT NULL,
  `mtime` varchar(20) NOT NULL,
  `ctime` varchar(20) NOT NULL,
  `atime2` varchar(20) NOT NULL,
  `mtime2` varchar(20) NOT NULL,
  `ctime2` varchar(20) NOT NULL,
  `dstatus` int(11) NOT NULL,
  `mstatus` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tm_selected`
--

INSERT INTO `tm_selected` (`id`, `uname`, `file_path`, `filetype`, `status`, `hash_val`, `backup_id`, `hash_val2`, `atime`, `mtime`, `ctime`, `atime2`, `mtime2`, `ctime2`, `dstatus`, `mstatus`) VALUES
(1, 'admin', 'D:\\evidence1\\case_info.docx', 'file', 0, 'd9d7e0cd4904a782a42a3ab3fda4824ea0befaf7b3782a9ddc441735c9c89ea1', 0, '', '2025-04-13 00:59:15', '2024-03-11 18:40:22', '2025-02-14 17:30:33', '', '', '', 0, 0),
(2, 'admin', 'D:\\evidence1\\cctv-footage.mp4', 'file', 0, 'be2787043a34b7662d072dd655ffa88d033083e8d98d6a1add495d5dc3fb0816', 0, '', '2025-04-13 00:59:15', '2025-03-20 11:25:34', '2025-03-20 11:25:34', '', '', '', 0, 0),
(3, 'admin', 'D:\\evidence1\\crimes.csv', 'file', 0, '1387a6b83224251f2681c5388dc789d76fdbfd43db7e6b2eee6f99c721ca38a2', 0, '', '2025-04-13 00:59:16', '2024-04-02 10:40:35', '2025-04-12 22:50:05', '', '', '', 0, 0),
(4, 'admin', 'D:\\evidence1\\D4r57_proof.png', 'file', 0, '850b38b6badbf497bb5e81e6c926934a8ef043484b7e10517873d34db476edd1', 0, '', '2025-04-13 00:59:16', '2025-01-03 19:52:38', '2025-04-12 22:51:39', '2025-04-13 01:00:02', '', '', 0, 0),
(5, 'admin', 'D:\\evidence1\\personal_info.txt', 'file', 0, '90344534068ac804d56f9e1d23b002bf6362e99934feef86ff8657b2f0df3f49', 0, '', '2025-04-13 00:59:16', '2025-01-17 16:50:26', '2025-04-12 22:55:29', '', '', '', 0, 0),
(6, 'admin', 'D:\\evidence1\\report.pdf', 'file', 0, '3a96230d126bdbcefd3a6bbf78020b47bc93dd0c13d104170c4fdcfbe0bf0188', 0, '', '2025-04-13 00:59:16', '2024-12-25 16:01:14', '2025-04-12 22:51:14', '', '', '', 0, 0),
(7, 'admin', 'D:\\evidence1\\report2.pdf', 'file', 0, '8e84883ffd24cf9d437c4ffa126e8d3cdf50246ffd34dffa97b023ea0788366f', 0, '', '2025-04-13 00:59:16', '2024-05-03 16:48:23', '2025-04-12 22:54:54', '', '', '', 1, 0),
(8, 'admin', 'D:\\evidence2\\data1.txt', 'file', 0, 'a85c36f2a2ab85f1ac23c92b3701395d85e84abbfc64d43b5431209e8982d337', 0, '', '2025-04-13 00:59:16', '2023-12-21 18:20:06', '2025-04-13 00:59:02', '', '', '', 0, 0),
(9, 'admin', 'D:\\evidence2\\test22.html', 'file', 0, '6bad5da5850a45d5ef9a64946de0c35229a1b89f48d01ed86b5697337081da01', 0, '', '2025-04-13 00:59:16', '2024-01-22 12:44:42', '2025-04-13 00:59:02', '', '', '', 0, 0),
(10, 'admin', 'D:\\evidence2\\report2.pdf', 'file', 0, '8e84883ffd24cf9d437c4ffa126e8d3cdf50246ffd34dffa97b023ea0788366f', 0, '', '2025-04-13 01:00:10', '2024-05-03 16:48:23', '2025-04-12 22:54:54', '', '', '', 0, 0);
