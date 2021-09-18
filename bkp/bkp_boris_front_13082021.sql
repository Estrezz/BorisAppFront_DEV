-- MySQL dump 10.13  Distrib 5.7.35, for Linux (x86_64)
--
-- Host: localhost    Database: boris
-- ------------------------------------------------------
-- Server version	5.7.35-0ubuntu0.18.04.1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `atributo`
--

DROP TABLE IF EXISTS `atributo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `atributo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orden` int(11) DEFAULT NULL,
  `descripcion` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_atributo_descripcion` (`descripcion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atributo`
--

LOCK TABLES `atributo` WRITE;
/*!40000 ALTER TABLE `atributo` DISABLE KEYS */;
/*!40000 ALTER TABLE `atributo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `store_id` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `company_name` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `admin_email` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `logo` varchar(200) COLLATE utf8_bin DEFAULT NULL,
  `contact_name` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `contact_phone` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `contact_email` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `correo_usado` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `correo_apikey` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `correo_id` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `shipping_address` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_number` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_floor` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_zipcode` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_city` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_province` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_country` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_info` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `communication_email` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `company_country` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `company_main_currency` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `company_main_language` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `correo_apikey_test` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `correo_id_test` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `correo_test` tinyint(1) DEFAULT NULL,
  `platform_access_token` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `platform_token_type` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `company_url` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_company_store_id` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=390 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `email` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `address` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `city` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `country` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `floor` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `identification` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `locality` varchar(150) COLLATE utf8_bin DEFAULT NULL,
  `number` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `phone` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `province` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `zipcode` varchar(8) COLLATE utf8_bin DEFAULT NULL,
  `instructions` varchar(150) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_customer_name` (`name`),
  KEY `ix_customer_identification` (`identification`),
  KEY `company_id` (`company_id`),
  KEY `ix_customer_email` (`email`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70554713 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_number` int(11) DEFAULT NULL,
  `order_original_id` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `gastos_cupon` float DEFAULT NULL,
  `gastos_gateway` float DEFAULT NULL,
  `gastos_promocion` float DEFAULT NULL,
  `gastos_shipping_customer` float DEFAULT NULL,
  `gastos_shipping_owner` float DEFAULT NULL,
  `metodo_de_pago` varchar(35) COLLATE utf8_bin DEFAULT NULL,
  `order_fecha_compra` datetime DEFAULT NULL,
  `tarjeta_de_pago` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  KEY `ix_order_timestamp` (`timestamp`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=461554584 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `producto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `variant` int(11) DEFAULT NULL,
  `accion` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `accion_cantidad` int(11) DEFAULT NULL,
  `motivo` varchar(150) COLLATE utf8_bin DEFAULT NULL,
  `image` varchar(200) COLLATE utf8_bin DEFAULT NULL,
  `promo_descuento` float DEFAULT NULL,
  `promo_nombre` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `accion_reaccion` tinyint(1) DEFAULT NULL,
  `prod_id` int(11) DEFAULT NULL,
  `accion_cambiar_por` int(11) DEFAULT NULL,
  `accion_cambiar_por_desc` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `promo_precio_final` float DEFAULT NULL,
  `politica_valida` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `politica_valida_motivo` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `ix_producto_prod_id` (`prod_id`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=603202591 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `store_id` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `store_name` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `admin_email` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `param_logo` varchar(200) COLLATE utf8_bin DEFAULT NULL,
  `param_fondo` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `param_config` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `contact_name` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `contact_phone` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `contact_email` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `correo_usado` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `correo_apikey` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `correo_id` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `shipping_address` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_number` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_floor` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_zipcode` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_city` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_province` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_country` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `shipping_info` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `communication_email` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `correo_apikey_test` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `correo_id_test` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `correo_test` tinyint(1) DEFAULT NULL,
  `platform_access_token` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `platform_token_type` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `store_country` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `store_main_currency` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `store_main_language` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `store_address` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  `store_phone` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `store_plan` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `store_url` varchar(120) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_store_platform` (`platform`),
  KEY `ix_store_store_id` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store`
--

LOCK TABLES `store` WRITE;
/*!40000 ALTER TABLE `store` DISABLE KEYS */;
INSERT INTO `store` VALUES (9,'tiendanube','1447373','Demo Boris','erezzonico@borisreturns.com','https://frontprod.borisreturns.com/static/images/Demo_boris.png','','app/static/conf/boris.json','','','erezzonico@borisreturns.com','Moova','b23920003684e781d87e7e5b615335ad254bdebc','b22bc380-439f-11eb-8002-a5572ae156e7','Cuba','1865','','1428','CABA','CABA','','Dejar en Porteria','soporte@borisreturns.com','b23920003684e781d87e7e5b615335ad254bdebc','b22bc380-439f-11eb-8002-a5572ae156e7',1,'cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16','bearer','','','','','',NULL,'https://demoboris.mitiendanube.com'),(10,'tiendanube','138327','Abundancia por designio','lucia@abundanciapordesignio.com','//frontprod.borisreturns.com/static/images/abundancia.png','','app/static/conf/abundancia.json','Lucia Ferreira','11 31140270','info@abundanciapordesignio.com','Moova','a492fe617421dcf9c2658cd4f4ba4dceb7eba63b','99bb0440-97ab-11eb-9a96-43c1af99baa0','','','','','','','','','info@borisreturns.com','','',0,'89a5ea6c862b1955d4e42f111f2685a0584c5de7','bearer','AR','ARS','es','Showroon Balvanera  - Por ahora sólo envíos.','',NULL,'https://www.abundancia.com.ar'),(12,'tiendanube','1631829','demo-debocaenboca','leilasaid@hotmail.com','//d2r9epyceweg5n.cloudfront.net/stores/001/631/829/themes/common/logo-343539575-1617381511-501e7beeaea7770b915d4300c320ad871617381511.png?0','','app/static/conf/1631829.json',NULL,NULL,NULL,'Ninguno',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'ARG',NULL,'info@borisreturns.com',NULL,NULL,1,'c5e4b74803a72b6b84f4b3cafc71d3c43994111d','bearer','AR','ARS','es',NULL,NULL,NULL,'https://demodebocaenboca.mitiendanube.com'),(13,'tiendanube','1448797','Pidebis','pidebis@gmail.com','//d2r9epyceweg5n.cloudfront.net/stores/001/448/797/themes/common/logo-1672919836-1609005682-33b0fdbdb949ab5dae8616d7fcfb9e891609005683.png?0',NULL,'app/static/conf/1448797.json','','','pidebis@gmail.com','Ninguno',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'ARG',NULL,'info@borisreturns.com',NULL,NULL,1,'a78c13a46afb19349f184a2dc2e28b4257ca6887','bearer','AR','ARS','es','Ambrosetti 242','+54 011 30639618',NULL,'https://pidebis.mitiendanube.com'),(14,'tiendanube','962628','KILL','tienda@kill.com.ar','//d2r9epyceweg5n.cloudfront.net/stores/962/628/themes/common/logo-444853454-1608665108-19714e3db78dff93053c5f7a01f53ed11608665109.jpg?0','','app/static/conf/962628.json',NULL,NULL,'tienda@kill.com.ar','Moova','a492fe617421dcf9c2658cd4f4ba4dceb7eba63b','99bb0440-97ab-11eb-9a96-43c1af99baa0','colombia','251','','1603','Villa Martelli','Buenos Aires','ARG','','info@borisreturns.com','','',0,'a2a0f51e918e791bb59a9f11145ab4d486a969c4','bearer','AR','ARS','es','COLOMBIA 251','+54 011 33035356',NULL,'https://tienda.kill.com.ar'),(15,'tiendanube','630942','BATHINDA','info@bathinda.com.ar','//frontprod.borisreturns.com/static/images/bathinda.png','','app/static/conf/630942.json',NULL,NULL,'info@bathinda.com.ar','Moova','a492fe617421dcf9c2658cd4f4ba4dceb7eba63b','99bb0440-97ab-11eb-9a96-43c1af99baa0','Uruguay','1342','','1016','CABA','CABA','ARG','','info@borisreturns.com','','',0,'907ca431ffc80b712641b0d565eada6efd9e860f','bearer','AR','ARS','es','URUGUAY 1342','+54 11 48135697',NULL,'https://www.bathinda.com.ar');
/*!40000 ALTER TABLE `store` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-13 20:16:02
