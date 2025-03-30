-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: distillery_db
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `volume` float NOT NULL,
  `strength` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Водка \"Белый медведь\"',450.00,0,0),(2,'Коньяк \"Золотая выдержка\"',1200.00,0,0),(3,'Вино \"Красное сухое\"',750.00,0,0),(4,'Пиво \"Хмельное настроение\"',150.00,0,0),(5,'Ликёр \"Шоколадный аромат\"',900.00,0,0),(6,'Водка \"Белый медведь\"',450.00,0.5,40),(7,'Коньяк \"Золотая выдержка\"',1200.00,0.7,40),(8,'Вино \"Красное сухое\"',750.00,0.75,13),(9,'Пиво \"Хмельное настроение\"',150.00,0.5,5),(10,'Ликёр \"Шоколадный аромат\"',900.00,0.7,20),(11,'Виски \"Талискер\"',2500.00,0.7,45),(12,'Ром \"Карибский бриз\"',800.00,0.7,37.5),(13,'Шампанское \"Кристалл\"',3500.00,0.75,12),(14,'Текила \"Эсполон\"',1400.00,0.7,38),(15,'Джин \"Bombay Sapphire\"',1600.00,0.7,47);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchases`
--

DROP TABLE IF EXISTS `purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `purchase_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchases`
--

LOCK TABLES `purchases` WRITE;
/*!40000 ALTER TABLE `purchases` DISABLE KEYS */;
INSERT INTO `purchases` VALUES (1,'2025-03-24 16:31:35'),(2,'2025-03-24 17:06:02'),(3,'2025-03-24 17:39:24'),(4,'2025-03-24 19:10:15'),(5,'2025-03-25 00:19:00'),(6,'2025-03-25 00:20:22'),(7,'2025-03-25 00:21:51'),(8,'2025-03-25 00:24:17'),(9,'2025-03-25 00:35:04'),(10,'2025-03-25 00:49:53'),(11,'2025-03-25 00:52:42'),(12,'2025-03-25 00:53:36'),(13,'2025-03-25 13:15:39'),(14,'2025-03-25 13:18:35'),(15,'2025-03-25 13:19:13'),(16,'2025-03-30 22:00:27');
/*!40000 ALTER TABLE `purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock`
--

DROP TABLE IF EXISTS `stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '1',
  `volume` float NOT NULL DEFAULT '1',
  `strength` float NOT NULL DEFAULT '1',
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '1.00',
  `product_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_product` (`product_id`),
  CONSTRAINT `fk_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock`
--

LOCK TABLES `stock` WRITE;
/*!40000 ALTER TABLE `stock` DISABLE KEYS */;
INSERT INTO `stock` VALUES (6,'Водка \"Белый медведь\"',0.5,40,48,45000.00,6),(7,'Текила \"Эсполон\"',0.7,38,1,1400.00,14),(8,'Текила \"Эсполон\"',0.7,38,8,14000.00,14),(9,'Вино \"Красное сухое\"',0.75,13,9,7500.00,8),(10,'Текила \"Эсполон\"',0.7,38,20,28000.00,14),(11,'Ликёр \"Шоколадный аромат\"',0.7,20,1,900.00,10),(12,'Виски \"Талискер\"',0.7,45,2,5000.00,11),(13,'Ликёр \"Шоколадный аромат\"',0.7,20,20,18000.00,10),(14,'Виски \"Талискер\"',0.7,45,15,50000.00,11),(15,'Водка \"Белый медведь\"',0.5,40,1,450.00,6),(16,'Водка \"Белый медведь\"',0.5,40,12,5400.00,6),(17,'Текила \"Эсполон\"',0.7,38,1,1400.00,14),(18,'Коньяк \"Золотая выдержка\"',0.7,40,1,1200.00,7),(19,'Вино \"Красное сухое\"',0.75,13,1,750.00,8),(20,'Пиво \"Хмельное настроение\"',0.5,5,1,150.00,9),(21,'Ром \"Карибский бриз\"',0.7,37.5,1,800.00,12),(22,'Шампанское \"Кристалл\"',0.75,12,1,3500.00,13),(23,'Шампанское \"Кристалл\"',0.75,12,1,3500.00,13),(24,'Джин \"Bombay Sapphire\"',0.7,47,1,1600.00,15),(25,'Водка \"Белый медведь\"',0.5,40,1,450.00,6),(26,'Вино \"Красное сухое\"',0.75,13,32,25500.00,8);
/*!40000 ALTER TABLE `stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `transaction_type` varchar(50) DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `purchase_id` int DEFAULT NULL,
  `sale_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `purchase_id` (`purchase_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`purchase_id`) REFERENCES `purchases` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,'purchase',2,2,2400.00,'received',1,'2025-03-28 14:07:06'),(2,'purchase',5,1,900.00,'received',1,'2025-03-28 14:07:06'),(3,'purchase',5,1,900.00,'pending',2,'2025-03-28 14:07:06'),(4,'purchase',1,12,5400.00,'pending',2,'2025-03-28 14:07:06'),(5,'purchase',4,100,15000.00,'pending',3,'2025-03-28 14:07:06'),(6,'purchase',15,1,1600.00,'received',4,'2025-03-28 14:07:06'),(7,'purchase',6,12,5400.00,'received',4,'2025-03-28 14:07:06'),(8,'purchase',9,3,450.00,'received',4,'2025-03-28 14:07:06'),(9,'purchase',6,100,45000.00,'received',5,'2025-03-28 14:07:06'),(10,'purchase',6,100,45000.00,'pending',6,'2025-03-28 14:07:06'),(11,'purchase',14,1,1400.00,'received',7,'2025-03-28 14:07:06'),(12,'purchase',12,20,16000.00,'pending',8,'2025-03-28 14:07:06'),(13,'purchase',8,34,25500.00,'pending',9,'2025-03-28 14:07:06'),(14,'purchase',14,1,1400.00,'received',10,'2025-03-28 14:07:06'),(15,'purchase',14,10,14000.00,'received',11,'2025-03-28 14:07:06'),(16,'purchase',8,10,7500.00,'received',11,'2025-03-28 14:07:06'),(17,'purchase',14,20,28000.00,'received',12,'2025-03-28 14:07:06'),(18,'purchase',6,1,450.00,'received',13,'2025-03-28 14:07:06'),(19,'purchase',6,12,5400.00,'received',13,'2025-03-28 14:07:06'),(20,'purchase',10,1,900.00,'received',14,'2025-03-28 14:07:06'),(21,'purchase',11,2,5000.00,'received',14,'2025-03-28 14:07:06'),(22,'purchase',10,20,18000.00,'received',15,'2025-03-28 14:07:06'),(23,'purchase',11,20,50000.00,'received',15,'2025-03-28 14:07:06'),(26,'sale',6,50,22500.00,'completed',NULL,'2025-03-28 14:21:45'),(27,'purchase',7,1,1200.00,'received',16,'2025-03-30 19:00:27'),(28,'purchase',8,1,750.00,'received',16,'2025-03-30 19:00:27'),(29,'purchase',9,1,150.00,'received',16,'2025-03-30 19:00:27'),(30,'purchase',12,1,800.00,'received',16,'2025-03-30 19:00:27'),(31,'purchase',13,1,3500.00,'received',16,'2025-03-30 19:00:27'),(32,'purchase',13,1,3500.00,'received',16,'2025-03-30 19:00:27'),(33,'purchase',15,1,1600.00,'received',16,'2025-03-30 19:00:27'),(34,'purchase',6,1,450.00,'received',16,'2025-03-30 19:00:27');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Администратор','Кладовщик','Бухгалтер') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'admin','admin123','Администратор'),(9,'qw','qwqw','Кладовщик'),(10,'zx','zxzx','Бухгалтер');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `write_offs`
--

DROP TABLE IF EXISTS `write_offs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `write_offs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stock_id` int NOT NULL,
  `quantity` int NOT NULL,
  `reason` text NOT NULL,
  `write_off_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `stock_id` (`stock_id`),
  CONSTRAINT `write_offs_ibfk_1` FOREIGN KEY (`stock_id`) REFERENCES `stock` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `write_offs`
--

LOCK TABLES `write_offs` WRITE;
/*!40000 ALTER TABLE `write_offs` DISABLE KEYS */;
INSERT INTO `write_offs` VALUES (1,14,1,'Повреждение упаковки','2025-03-28 15:40:46'),(2,13,1,'Просроченный срок годности','2025-03-28 15:45:45'),(3,9,1,'Повреждение упаковки','2025-03-28 15:49:35'),(4,14,3,'Несоответствие маркировки','2025-03-28 15:53:15'),(5,26,2,'Просроченный срок годности','2025-03-30 21:40:22');
/*!40000 ALTER TABLE `write_offs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-31  0:51:19
