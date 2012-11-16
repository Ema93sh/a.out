-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 16, 2012 at 09:03 PM
-- Server version: 5.5.24
-- PHP Version: 5.3.10-1ubuntu3.2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `online_judge`
--

-- --------------------------------------------------------

--
-- Table structure for table `jobQueue`
--

CREATE TABLE IF NOT EXISTS `jobQueue` (
  `submissionId` bigint(20) NOT NULL AUTO_INCREMENT,
  UNIQUE KEY `submissionId` (`submissionId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `problems`
--

CREATE TABLE IF NOT EXISTS `problems` (
  `problemId` bigint(20) NOT NULL AUTO_INCREMENT,
  `problemName` varchar(40) NOT NULL,
  `problemCode` varchar(10) NOT NULL,
  `content` text NOT NULL,
  `sourceLimit` int(11) NOT NULL,
  `timeLimit` float NOT NULL,
  `memoryLimit` int(11) NOT NULL,
  PRIMARY KEY (`problemId`),
  UNIQUE KEY `problemCode` (`problemCode`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `problems`
--

INSERT INTO `problems` (`problemId`, `problemName`, `problemCode`, `content`, `sourceLimit`, `timeLimit`, `memoryLimit`) VALUES
(1, 'testing judge', 'TEST', 'first line: t\r\nthen t lines follow each with a number n\r\nprint the square of each number ''n''\r\n\r\nall the input and output will fit in 32 bit integer', 2000, 1, 1024),
(2, 'TLECHECK', 'TLECHECK', 'checking for timelimit by running a slooow program', 20000, 2, 1024);

-- --------------------------------------------------------

--
-- Table structure for table `submissions`
--

CREATE TABLE IF NOT EXISTS `submissions` (
  `submissionId` bigint(20) NOT NULL AUTO_INCREMENT,
  `problemCode` varchar(10) NOT NULL,
  `language` varchar(15) NOT NULL,
  `status` varchar(30) NOT NULL DEFAULT 'waiting',
  `time` float NOT NULL,
  `memory` int(11) NOT NULL,
  PRIMARY KEY (`submissionId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `submissions`
--

INSERT INTO `submissions` (`submissionId`, `problemCode`, `language`, `status`, `time`, `memory`) VALUES
(1, 'TEST', 'CPP', 'waiting', 0, 0),
(2, 'TLECHECK', 'Python', 'waiting', 0, 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
