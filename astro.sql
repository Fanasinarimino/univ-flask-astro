/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.5.29-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: astro_community
-- ------------------------------------------------------
-- Server version	10.5.29-MariaDB-0+deb11u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cameras`
--

DROP TABLE IF EXISTS `cameras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cameras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `marque` varchar(80) NOT NULL,
  `modele` varchar(80) NOT NULL,
  `date_sortie` varchar(20) NOT NULL,
  `score` int(11) NOT NULL,
  `categorie` varchar(50) NOT NULL,
  `url_image` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cameras`
--

LOCK TABLES `cameras` WRITE;
/*!40000 ALTER TABLE `cameras` DISABLE KEYS */;
INSERT INTO `cameras` VALUES (1,'Canon','EOS 2000D','2018',3,'Amateur','images/appareil/canonEOS2000D.jpg'),(2,'Sony','A7 III','2018',5,'Amateur sérieux','images/appareil/sonyALPHA.jpg'),(3,'Canon','EOS R5','2020',5,'Professionnel','images/appareil/canon.jpg');
/*!40000 ALTER TABLE `cameras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `photos`
--

DROP TABLE IF EXISTS `photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `photos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titre` varchar(120) NOT NULL,
  `url_image` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `photos`
--

LOCK TABLES `photos` WRITE;
/*!40000 ALTER TABLE `photos` DISABLE KEYS */;
INSERT INTO `photos` VALUES (1,'Voie Lactée','images/photographie/voieLactee.jpg'),(2,'Nébuleuse d\'Orion','images/photographie/nebuluse.jpg'),(3,'Lune','images/photographie/lune.jpg');
/*!40000 ALTER TABLE `photos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `telescopes`
--

DROP TABLE IF EXISTS `telescopes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `telescopes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `marque` varchar(80) NOT NULL,
  `modele` varchar(80) NOT NULL,
  `date_sortie` varchar(20) NOT NULL,
  `score` int(11) NOT NULL,
  `categorie` varchar(50) NOT NULL,
  `url_image` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telescopes`
--

LOCK TABLES `telescopes` WRITE;
/*!40000 ALTER TABLE `telescopes` DISABLE KEYS */;
INSERT INTO `telescopes` VALUES (1,'Celestron','FirstScope','2010',3,'Enfants','images/telescope/enfant.PNG'),(2,'Sky-Watcher','Star Discovery','2015',4,'Automatisés','images/telescope/automatisee.PNG'),(3,'Meade','LX200','2012',5,'Complets','images/telescope/complets.PNG');
/*!40000 ALTER TABLE `telescopes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','fanasina@test','scrypt:32768:8:1$0AxDUFwUMHL8GPAt$ef9052e70115112fa877ab5f8aa7f5a63cd48e59376fe6605a3d164fe65ee6649d4e4bd85f333fdd15f5f50798d0cb9035abcae53757c3085efbe93d5e38e65b'),(3,'test','test@test','scrypt:32768:8:1$7sOC8YtlJd1fH299$03f6f1b959ca586fafaea0bb8896aa44de153826270e013081696816fb4410f5dd059a099c1ce8b23404d0c694ce4b4773a2cdda5a4885742469b947f943f45a'),(4,'hh','hh@hh','scrypt:32768:8:1$cVqZJskA2xGza3PE$1bed1f702a37c7ad33d6f629919899bed968efa4534a7c83191ed8af07a267dea3311d9b56858bd5b29d4ce2b77746f0f8a2b02ba433332591fd7a0a9183360b'),(5,'jjj','jjj@jjj','scrypt:32768:8:1$cKK7YMM3IauhqUB5$703e6e8ba41406fb5887928016577c311efedfc795de81666352d66475b7809de1a2c0772a0744171a98efcbc2b7ade0e46b2e8cdddf5bfa954352d9cbe13b20'),(6,'jean','jean@test','scrypt:32768:8:1$MQ0TkLkW1Pgcx58E$2ced581bbb30b871139428a018d1a5b57d763f779865baa01d58a15e1a7760aae7d8c46ea2e94e6843a53918e527a005c117aafd9ad6e4c50b5b9a6b16cfb321'),(7,'fanasina','fanasina@admin','scrypt:32768:8:1$2y0cqe53jPctp7yp$5491c5956a9518c21c30b81d9c7da45e5f26e89db50cd0cd23afa78cf6d5287a68d400c7b30dded0228e5bdd822d3b10c24a2c916452b542c59e79cf40d10c7c');
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

-- Dump completed on 2026-04-17 19:20:33
