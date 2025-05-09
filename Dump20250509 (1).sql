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
-- Table structure for table `activity_log`
--

DROP TABLE IF EXISTS `activity_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `action` text,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_log`
--

LOCK TABLES `activity_log` WRITE;
/*!40000 ALTER TABLE `activity_log` DISABLE KEYS */;
INSERT INTO `activity_log` VALUES (1,'admin','Просмотрел список пользователей','2025-05-02 14:06:15'),(2,'admin','Удалил пользователя 11 (Бухгалтер)','2025-05-02 14:06:44'),(3,'admin','Удалил пользователя qw (Кладовщик)','2025-05-02 14:06:50'),(4,'admin','Добавил пользователя qwqw с ролью Кладовщик','2025-05-02 14:07:00'),(5,'admin','Добавил пользователя zxzx с ролью Кладовщик','2025-05-02 14:07:09'),(6,'admin','Просмотрел список пользователей','2025-05-02 14:07:12'),(7,'admin','Удалил пользователя zxzx (Кладовщик)','2025-05-02 14:07:16'),(8,'admin','Добавил пользователя zx с ролью Бухгалтер','2025-05-02 14:07:22'),(9,'admin','Просмотрел список пользователей','2025-05-02 14:07:25'),(10,'admin','Просмотрел журнал действий','2025-05-02 14:14:34'),(11,'qwqw','Просмотрел склад','2025-05-02 15:04:28'),(12,'qwqw','Создал отчет по складу: Отчет_по_складу_2025-05-02_15-06-12.pdf','2025-05-02 15:06:12'),(13,'qwqw','Создал отчет по складу: Отчет_по_складу_2025-05-02_15-06-18.pdf','2025-05-02 15:06:18'),(14,'qwqw','Проверил штрих-код: результат — Ошибка проверки в ЕГАИС!','2025-05-02 15:06:38'),(15,'qwqw','Принял поставку #20','2025-05-02 15:06:58'),(16,'qwqw','Просмотрел склад','2025-05-02 15:07:09'),(17,'qwqw','Списал 1 шт. товара \'Водка \"Белый медведь\"\' по причине: Повреждение упаковки','2025-05-02 15:14:06'),(18,'qwqw','Списал 2 шт. товара \'Водка \"Белый медведь\"\' по причине: Просроченный срок годности','2025-05-02 15:14:23'),(19,'qwqw','Просмотрел склад','2025-05-02 15:14:41'),(20,'zx','Бухгалтер zx выполнил(а) закупку товаров (покупка ID: 23)','2025-05-02 16:41:45'),(21,'zx','Бухгалтер zx продал(а) товар: Вино \"Красное сухое\" - 2 шт. по 800.0 руб. Итог: 1600.0 руб.','2025-05-02 16:42:25'),(22,'zx','Бухгалтер zx открыл(а) окно финансового отчёта','2025-05-02 16:42:49'),(23,'admin','Просмотрел журнал действий','2025-05-02 16:51:14'),(24,'admin','Просмотрел журнал действий','2025-05-02 16:54:48'),(25,'admin','Просмотрел журнал действий','2025-05-02 17:29:14'),(26,'admin','Просмотрел журнал действий','2025-05-02 17:29:27'),(27,'admin','Просмотрел список пользователей','2025-05-09 14:53:01'),(28,'admin','Просмотрел журнал действий','2025-05-09 14:53:08'),(29,'admin','Просмотрел журнал действий','2025-05-09 14:53:33'),(30,'admin','Просмотрел журнал действий','2025-05-09 14:54:13'),(31,'qwqw','Просмотрел склад','2025-05-09 15:01:26'),(32,'qwqw','Создал отчет по складу: Отчет_по_складу_2025-05-09_15-02-05.pdf','2025-05-09 15:02:05'),(33,'admin','Просмотрел список пользователей','2025-05-09 15:06:48'),(34,'admin','Просмотрел список пользователей','2025-05-09 15:06:48'),(35,'zx','Бухгалтер zx выполнил(а) закупку товаров (покупка ID: 24)','2025-05-09 15:18:37'),(36,'zx','Бухгалтер zx продал(а) товар: Ликёр \"Шоколадный аромат\" - 5 шт. по 1100.0 руб. Итог: 5500.0 руб.','2025-05-09 15:19:33'),(37,'zx','Бухгалтер zx создал финансовый отчёт','2025-05-09 15:19:54'),(38,'qwqw','Просмотрел склад','2025-05-09 15:20:35'),(39,'qwqw','Принял поставку #24','2025-05-09 15:36:07'),(40,'qwqw','Принял поставку #23','2025-05-09 15:36:17'),(41,'qwqw','Принял поставку #19','2025-05-09 15:36:24'),(42,'qwqw','Просмотрел склад','2025-05-09 15:36:34'),(43,'qwqw','Создал отчет по складу: Отчет_по_складу_2025-05-09_15-36-43.pdf','2025-05-09 15:36:43'),(44,'qwqw','Списал 1 шт. товара: Текила \"Эсполон\", причина: Повреждение упаковки','2025-05-09 16:00:29'),(45,'qwqw','Списал товар \'Водка \"Белый медведь\"\' в количестве 1. Причина: Повреждение упаковки','2025-05-09 16:06:30'),(46,'qwqw','Списал товар \'Текила \"Эсполон\"\' в количестве 1. Причина: Повреждение упаковки','2025-05-09 16:07:09'),(47,'qwqw','Просмотрел склад','2025-05-09 16:07:16'),(48,'zx','Бухгалтер zx продал(а) товар: Вино \"Красное сухое\" - 7 шт. по 750.0 руб. Итог: 5250.0 руб.','2025-05-09 16:07:54'),(49,'qwqw','Просмотрел склад','2025-05-09 16:08:00'),(50,'zx','Бухгалтер zx продал(а) товар: Текила \"Эсполон\" - 8 шт. по 1400.0 руб. Итог: 11200.0 руб.','2025-05-09 16:26:39'),(51,'qwqw','Списал товар \'Водка \"Белый медведь\"\' в количестве 1. Причина: Нарушение условий хранения','2025-05-09 16:27:01'),(52,'qwqw','Просмотрел склад','2025-05-09 16:27:03'),(53,'zx','Бухгалтер zx продал(а) товар: Текила \"Эсполон\" - 12 шт. по 1400.0 руб. Итог: 16800.0 руб.','2025-05-09 16:27:17'),(54,'admin','Просмотрел список пользователей','2025-05-09 16:27:40'),(55,'admin','Просмотрел список пользователей','2025-05-09 16:27:40'),(56,'admin','Просмотрел журнал действий','2025-05-09 16:27:43'),(57,'qwqw','Принял поставку #18','2025-05-09 20:05:01'),(58,'admin','Просмотрел список пользователей','2025-05-09 20:14:03'),(59,'admin','Просмотрел список пользователей','2025-05-09 20:14:03'),(60,'admin','Добавил пользователя 12 с ролью Кладовщик','2025-05-09 20:14:13'),(61,'admin','Просмотрел список пользователей','2025-05-09 20:14:14'),(62,'admin','Просмотрел список пользователей','2025-05-09 20:14:14'),(63,'admin','Удалил пользователя 12 (Кладовщик)','2025-05-09 20:14:20'),(64,'admin','Просмотрел список пользователей','2025-05-09 20:14:21'),(65,'admin','Просмотрел список пользователей','2025-05-09 20:14:21'),(66,'admin','Просмотрел журнал действий','2025-05-09 20:14:24'),(67,'admin','Добавил пользователя 2 с ролью Бухгалтер','2025-05-09 20:14:42'),(68,'admin','Просмотрел список пользователей','2025-05-09 20:14:43'),(69,'admin','Просмотрел список пользователей','2025-05-09 20:14:43'),(70,'admin','Просмотрел журнал действий','2025-05-09 20:14:47'),(71,'zx','Бухгалтер zx выполнил(а) закупку товаров (покупка ID: 25)','2025-05-09 20:15:30'),(72,'zx','Бухгалтер zx продал(а) товар: Текила \"Эсполон\" - 4 шт. по 1400.0 руб. Итог: 5600.0 руб.','2025-05-09 20:15:39'),(73,'zx','Бухгалтер zx создал финансовый отчёт','2025-05-09 20:15:46'),(74,'qwqw','Просмотрел склад','2025-05-09 20:15:54'),(75,'qwqw','Принял поставку #25','2025-05-09 20:16:01'),(76,'qwqw','Создал отчет по складу: Отчет_по_складу_2025-05-09_20-16-11.pdf','2025-05-09 20:16:11'),(77,'qwqw','Просмотрел склад','2025-05-09 20:16:13'),(78,'qwqw','Списал товар \'Шампанское \"Кристалл\"\' в количестве 1. Причина: Повреждение упаковки','2025-05-09 20:16:31');
/*!40000 ALTER TABLE `activity_log` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchases`
--

LOCK TABLES `purchases` WRITE;
/*!40000 ALTER TABLE `purchases` DISABLE KEYS */;
INSERT INTO `purchases` VALUES (1,'2025-03-24 16:31:35'),(2,'2025-03-24 17:06:02'),(3,'2025-03-24 17:39:24'),(4,'2025-03-24 19:10:15'),(5,'2025-03-25 00:19:00'),(6,'2025-03-25 00:20:22'),(7,'2025-03-25 00:21:51'),(8,'2025-03-25 00:24:17'),(9,'2025-03-25 00:35:04'),(10,'2025-03-25 00:49:53'),(11,'2025-03-25 00:52:42'),(12,'2025-03-25 00:53:36'),(13,'2025-03-25 13:15:39'),(14,'2025-03-25 13:18:35'),(15,'2025-03-25 13:19:13'),(16,'2025-03-30 22:00:27'),(17,'2025-04-24 15:30:53'),(18,'2025-05-01 21:22:21'),(19,'2025-05-01 21:22:33'),(20,'2025-05-01 21:22:40'),(21,'2025-05-01 21:22:46'),(22,'2025-05-02 13:30:00'),(23,'2025-05-02 16:41:45'),(24,'2025-05-09 15:18:37'),(25,'2025-05-09 20:15:30');
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
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock`
--

LOCK TABLES `stock` WRITE;
/*!40000 ALTER TABLE `stock` DISABLE KEYS */;
INSERT INTO `stock` VALUES (6,'Водка \"Белый медведь\"',0.5,40,35,45000.00,6),(13,'Ликёр \"Шоколадный аромат\"',0.7,20,15,18000.00,10),(14,'Виски \"Талискер\"',0.7,45,13,50000.00,11),(15,'Водка \"Белый медведь\"',0.5,40,1,450.00,6),(16,'Водка \"Белый медведь\"',0.5,40,12,5400.00,6),(18,'Коньяк \"Золотая выдержка\"',0.7,40,1,1200.00,7),(20,'Пиво \"Хмельное настроение\"',0.5,5,1,150.00,9),(21,'Ром \"Карибский бриз\"',0.7,37.5,1,800.00,12),(24,'Джин \"Bombay Sapphire\"',0.7,47,1,1600.00,15),(25,'Водка \"Белый медведь\"',0.5,40,1,450.00,6),(26,'Вино \"Красное сухое\"',0.75,13,23,25500.00,8),(30,'Водка \"Белый медведь\"',0.5,40,1,450.00,6),(31,'Водка \"Белый медведь\"',0.5,40,1,450.00,6),(32,'Ликёр \"Шоколадный аромат\"',0.7,20,23,20700.00,10),(33,'Ром \"Карибский бриз\"',0.7,37.5,2,1600.00,12),(34,'Водка \"Белый медведь\"',0.5,40,22,9900.00,6),(35,'Ликёр \"Шоколадный аромат\"',0.7,20,1,900.00,10),(36,'Ром \"Карибский бриз\"',0.7,37.5,12,9600.00,12),(37,'Коньяк \"Золотая выдержка\"',0.7,40,1,1200.00,7),(38,'Ром \"Карибский бриз\"',0.7,37.5,5,4000.00,12),(39,'Текила \"Эсполон\"',0.7,38,1,7000.00,14),(40,'Джин \"Bombay Sapphire\"',0.7,47,1,1600.00,15);
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
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,'purchase',2,2,2400.00,'received',1,'2025-03-28 14:07:06'),(2,'purchase',5,1,900.00,'received',1,'2025-03-28 14:07:06'),(3,'purchase',5,1,900.00,'pending',2,'2025-03-28 14:07:06'),(4,'purchase',1,12,5400.00,'pending',2,'2025-03-28 14:07:06'),(5,'purchase',4,100,15000.00,'pending',3,'2025-03-28 14:07:06'),(6,'purchase',15,1,1600.00,'received',4,'2025-03-28 14:07:06'),(7,'purchase',6,12,5400.00,'received',4,'2025-03-28 14:07:06'),(8,'purchase',9,3,450.00,'received',4,'2025-03-28 14:07:06'),(9,'purchase',6,100,45000.00,'received',5,'2025-03-28 14:07:06'),(10,'purchase',6,100,45000.00,'pending',6,'2025-03-28 14:07:06'),(11,'purchase',14,1,1400.00,'received',7,'2025-03-28 14:07:06'),(12,'purchase',12,20,16000.00,'pending',8,'2025-03-28 14:07:06'),(13,'purchase',8,34,25500.00,'pending',9,'2025-03-28 14:07:06'),(14,'purchase',14,1,1400.00,'received',10,'2025-03-28 14:07:06'),(15,'purchase',14,10,14000.00,'received',11,'2025-03-28 14:07:06'),(16,'purchase',8,10,7500.00,'received',11,'2025-03-28 14:07:06'),(17,'purchase',14,20,28000.00,'received',12,'2025-03-28 14:07:06'),(18,'purchase',6,1,450.00,'received',13,'2025-03-28 14:07:06'),(19,'purchase',6,12,5400.00,'received',13,'2025-03-28 14:07:06'),(20,'purchase',10,1,900.00,'received',14,'2025-03-28 14:07:06'),(21,'purchase',11,2,5000.00,'received',14,'2025-03-28 14:07:06'),(22,'purchase',10,20,18000.00,'received',15,'2025-03-28 14:07:06'),(23,'purchase',11,20,50000.00,'received',15,'2025-03-28 14:07:06'),(26,'sale',6,50,22500.00,'completed',NULL,'2025-03-28 14:21:45'),(27,'purchase',7,1,1200.00,'received',16,'2025-03-30 19:00:27'),(28,'purchase',8,1,750.00,'received',16,'2025-03-30 19:00:27'),(29,'purchase',9,1,150.00,'received',16,'2025-03-30 19:00:27'),(30,'purchase',12,1,800.00,'received',16,'2025-03-30 19:00:27'),(31,'purchase',13,1,3500.00,'received',16,'2025-03-30 19:00:27'),(32,'purchase',13,1,3500.00,'received',16,'2025-03-30 19:00:27'),(33,'purchase',15,1,1600.00,'received',16,'2025-03-30 19:00:27'),(34,'purchase',6,1,450.00,'received',16,'2025-03-30 19:00:27'),(35,'purchase',14,1,1400.00,'received',17,'2025-04-24 12:30:53'),(36,'purchase',8,1,750.00,'received',17,'2025-04-24 12:30:53'),(37,'sale',13,1,3500.00,'completed',NULL,'2025-04-24 12:32:51'),(38,'purchase',12,5,4000.00,'received',18,'2025-05-01 18:22:21'),(39,'purchase',14,5,7000.00,'received',18,'2025-05-01 18:22:21'),(40,'purchase',15,1,1600.00,'received',18,'2025-05-01 18:22:21'),(41,'purchase',7,1,1200.00,'received',19,'2025-05-01 18:22:33'),(42,'purchase',6,1,450.00,'received',20,'2025-05-01 18:22:40'),(43,'purchase',6,1,450.00,'received',21,'2025-05-01 18:22:46'),(44,'sale',11,2,5000.00,'completed',NULL,'2025-05-01 18:23:11'),(45,'purchase',6,1,450.00,'received',22,'2025-05-02 10:30:00'),(46,'purchase',10,1,900.00,'received',23,'2025-05-02 13:41:45'),(47,'purchase',12,12,9600.00,'received',23,'2025-05-02 13:41:45'),(48,'sale',8,2,1600.00,'completed',NULL,'2025-05-02 13:42:25'),(49,'purchase',10,23,20700.00,'received',24,'2025-05-09 12:18:37'),(50,'purchase',12,2,1600.00,'received',24,'2025-05-09 12:18:37'),(51,'purchase',6,22,9900.00,'received',24,'2025-05-09 12:18:37'),(52,'sale',10,5,5500.00,'completed',NULL,'2025-05-09 12:19:33'),(53,'sale',8,7,5250.00,'completed',NULL,'2025-05-09 13:07:54'),(54,'sale',14,8,11200.00,'completed',NULL,'2025-05-09 13:26:39'),(55,'sale',14,12,16800.00,'completed',NULL,'2025-05-09 13:27:17'),(56,'purchase',13,1,3500.00,'received',25,'2025-05-09 17:15:30'),(57,'sale',14,4,5600.00,'completed',NULL,'2025-05-09 17:15:39');
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'admin','admin123','Администратор'),(13,'qwqw','qwqw','Кладовщик'),(15,'zx','zxzx','Бухгалтер'),(17,'2','2','Бухгалтер');
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `write_offs`
--

LOCK TABLES `write_offs` WRITE;
/*!40000 ALTER TABLE `write_offs` DISABLE KEYS */;
INSERT INTO `write_offs` VALUES (1,14,1,'Повреждение упаковки','2025-03-28 15:40:46'),(2,13,1,'Просроченный срок годности','2025-03-28 15:45:45'),(4,14,3,'Несоответствие маркировки','2025-03-28 15:53:15'),(5,26,2,'Просроченный срок годности','2025-03-30 21:40:22'),(6,6,8,'Нарушение условий хранения','2025-04-24 12:31:37'),(8,6,1,'Повреждение упаковки','2025-05-02 12:14:06'),(9,6,2,'Просроченный срок годности','2025-05-02 12:14:23');
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

-- Dump completed on 2025-05-09 20:18:27
