-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: myflaskapp
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

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
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `body` text,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `priv` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
INSERT INTO `articles` VALUES (13,'Global link 1','wescules','lmao lmao lmao lmao lmao lmao lmao lmao','2018-11-22 10:23:50',1),(14,'Global Link 2','wescules','<p>minsert into admin_articles(articleid, userid) select 10, id from users where email = &#39;wafermonster@yahoo.com&#39;;insert into admin_articles(articleid, userid) select 10, id from users where email = &#39;wafermonster@yahoo.com&#39;;insert into admin_articles(articleid, userid) select 10, id from users where email = &#39;wafermonster@yahoo.com&#39;;</p>','2018-11-22 10:45:38',0),(15,'lmao','wescules','<p>qwertyuiop</p><p>qwertyuiop</p><p>qwertyuiop</p><p>qwertyuiopqwertyuiopqwertyuiopqwertyuiop</p>','2018-11-22 11:28:11',1),(17,'Internal Link','wescules','<p>select * from articles, admin_articles where priv = 0 or admin_articles.userid =&nbsp;select * from articles, admin_articles where priv = 0 or admin_articles.userid =&nbsp;select * from articles, admin_articles where priv = 0 or admin_articles.userid =&nbsp;select * from articles, admin_articles where priv = 0 or admin_articles.userid =&nbsp;</p>','2018-11-22 13:16:49',1),(18,'Global Link 3','wescules','<p>select * from article</p>','2018-11-22 13:30:06',0);
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fuelquote`
--

DROP TABLE IF EXISTS `fuelquote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fuelquote` (
  `fuelid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `gallonsrequested` int(11) DEFAULT NULL,
  `suggestedprice` int(11) DEFAULT NULL,
  `amountdue` bigint(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`fuelid`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fuelquote`
--

LOCK TABLES `fuelquote` WRITE;
/*!40000 ALTER TABLE `fuelquote` DISABLE KEYS */;
INSERT INTO `fuelquote` VALUES (1,21,1232,5,6160,'2019-02-02'),(2,21,1232,5,6160,'2019-02-13'),(3,23,1234,5,6170,'2019-02-05'),(4,23,1234,5,6170,'2019-02-05'),(5,23,1234,5,6170,'2019-02-05'),(6,23,1234,5,6170,'2019-02-05'),(23,23,1212,5,6060,'2019-03-01'),(28,23,12312,5,61560,'2019-03-08'),(30,23,12312,5,61560,'2019-03-08'),(31,23,12312,5,61560,'2019-03-08');
/*!40000 ALTER TABLE `fuelquote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(50) DEFAULT NULL,
  `address1` varchar(100) DEFAULT NULL,
  `address2` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `zipcode` varchar(9) DEFAULT NULL,
  `ratehistory` varchar(100) DEFAULT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(100) NOT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (23,'Wescules Andraddy','124 Streeet St.','','Sugar Land','TX','908243',NULL,'lmao','$5$rounds=535000$RB5y7qa99/hfIkW4$94aKA8M2jur8BkKucwazYCEFwyxN2xcRPC7S33Re9Y1','2019-03-18 04:28:07'),(88,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'hiepLy','$5$rounds=535000$WrSgGyOO9NvUS0oQ$B0CmRRyOPqTJg3vMzWqVK8hmiwBtCSlgZefZvzmLgo5','2019-03-18 15:36:00');
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

-- Dump completed on 2019-03-18 11:29:58
