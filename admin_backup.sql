-- MySQL dump 10.13  Distrib 5.5.62, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: myflaskapp
-- ------------------------------------------------------
-- Server version	5.5.62-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_articles`
--

DROP TABLE IF EXISTS `admin_articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_articles` (
  `articleid` int(11) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_articles`
--

LOCK TABLES `admin_articles` WRITE;
/*!40000 ALTER TABLE `admin_articles` DISABLE KEYS */;
INSERT INTO `admin_articles` VALUES (13,12),(13,2),(15,12),(17,13),(17,7);
/*!40000 ALTER TABLE `admin_articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(100) DEFAULT NULL,
  `merchantName` varchar(100) DEFAULT NULL,
  `amount` DECIMAL(13,2) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `reciepts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items` (
  `recieptID` int(11) NOT NULL,
  `itemName` varchar(100) DEFAULT NULL,
  `UPC` varchar(100) DEFAULT NULL,
  `price` DECIMAL(13,2) DEFAULT NULL,
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
INSERT INTO `articles` VALUES (13,'Global link 1','wescules','lmao lmao lmao lmao lmao lmao lmao lmao','2018-11-22 10:23:50',1),(14,'Global Link 2','wescules','<p>minsert into admin_articles(articleid, userid) select 10, id from users where email = &#39;wafermonster@yahoo.com&#39;;insert into admin_articles(articleid, userid) select 10, id from users where email = &#39;wafermonster@yahoo.com&#39;;insert into admin_articles(articleid, userid) select 10, id from users where email = &#39;wafermonster@yahoo.com&#39;;</p>','2018-11-22 10:45:38',0),(15,'lmao','wescules','<p>qwertyuiop</p><p>qwertyuiop</p><p>qwertyuiop</p><p>qwertyuiopqwertyuiopqwertyuiopqwertyuiop</p>','2018-11-22 11:28:11',1),(17,'Internal Link','wescules','<p>select * from articles, admin_articles where priv = 0 or admin_articles.userid =&nbsp;select * from articles, admin_articles where priv = 0 or admin_articles.userid =&nbsp;select * from articles, admin_articles where priv = 0 or admin_articles.userid =&nbsp;select * from articles, admin_articles where priv = 0 or admin_articles.userid =&nbsp;</p>','2018-11-22 13:16:49',1),(18,'Global Link 3','wescules','<p>select * from article</p>','2018-11-22 13:30:06',0);
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Wesley Andrade','wafermonster@yahoo.com','wescules','$5$rounds=535000$K1i1RTO3V7id9pNE$9nFdojQ6gCfH0XawTglU3.W.NJ.D2u0OZ1YbYKY3pB/','2018-10-24 00:12:44',1),(2,'Hiep Ly','hiepfrsibtghuhytrgaheghiuptreshggiup','fag1234','$5$rounds=535000$hBJFJ0FaC0NMu25u$KhY1WPpuTc0xQh5QDvAhmm0cn0WOfNmWRVZivbM2unD','2018-10-24 00:20:34',0),(3,'s Andrade','johnanifa@hotmail.com','egragsergsretg','$5$rounds=535000$suSAhD52.iYDXYPE$a5I0ZtQ6CIg9iCw.p//9iLqhmtUgDK/CGykz4WJtCGB','2018-10-24 00:27:16',1),(4,'John','wafermonster@yahoo.com','lmaoxd','$5$rounds=535000$nsLd.V3ZnWnh79nQ$N65fnxtIFuHRrPX7mWIr7OfIsktd6Celt94VcfVeHMD','2018-10-24 00:55:42',1),(5,'rgtegeargaergaer','aergaergaergaergaerg','argegaergaerg','$5$rounds=535000$/0L46oE0dF/T/mfR$wWjDd1A2/gmaVHOybnhycfz9T6MY.WL5xKyYLnAnti5','2018-10-24 00:56:18',NULL),(6,'n','mnmmmmmmmmmmmm','mmmmmmmmmmmmmm','$5$rounds=535000$LeEl0NvlCM41nuzG$w6PvdXJnDdFDrLmUC.maXVrtIatjVCPB69PRR1joan1','2018-11-02 06:34:08',NULL),(7,'ocean man','ocean man','ocean man','$5$rounds=535000$elsTL.0aoC8mu74b$wR0aYGrsK2YsseeV8/Derjqxd1oAUwoauUr7LGNny17','2018-11-02 06:34:46',NULL),(8,'henry','johnanifa@hotmail.com','henry','$5$rounds=535000$R52F20ajMTfi.jj2$tIm25d8Q4urGFuhVcWvlv1Qymdz47ps1Y1gMgNFYRs6','2018-11-22 08:29:12',NULL),(9,'Wesley Andrade','wafermonster@yahoo.comc','sssssssssss','$5$rounds=535000$bR.0f1EeF2PIZaQ2$ANugHHDfEJ5t740cv057ZE68oinzkwU/oiT7dqkUYN8','2018-11-22 09:25:33',0),(12,'qwertyuiop','qwertyuiop','qwertyuiop','$5$rounds=535000$G7/EQ.EY7A/QOl02$o11HgqlqUVkJw9uLRgssWBUBj6sRPT2oz0KwG7/zHn0','2018-11-22 11:26:32',0),(13,'Hannibal Buress','Hannibal Buress','Hannibal Buress','$5$rounds=535000$yK0lD3JNA8c5F36a$RQSKy7qFnTzPb10DLlasiwhn0rO739NVwOx0/SmkNL2','2018-11-22 15:58:16',0),(14,'Hannibal BuressHannibal Buress','Hannibal BuressHannibal Buress','Hannibal Buressss','$5$rounds=535000$B1reapGS63v875Hs$ATAM3OW1PwwhlipLJ26sSUj3m/DGXrTaq41yThbV6L2','2018-11-23 02:44:08',1),(15,'register','register','register','$5$rounds=535000$IGRUo.j9dBpi6SSP$BKR.hBMSmKDGp9wrqZoNoK0EesRsqJIXrnItOkK0al4','2018-11-24 04:33:13',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-24  2:22:52
