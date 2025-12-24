-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Хост: MySQL-8.0
-- Время создания: Дек 24 2025 г., 12:21
-- Версия сервера: 8.0.43
-- Версия PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `InformationalSystemDataBase`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Clients`
--

CREATE TABLE `Clients` (
  `DiscountCardNumber` varchar(10) NOT NULL,
  `FirstName` varchar(30) NOT NULL,
  `LastName` varchar(30) NOT NULL,
  `TelephoneNumber` varchar(20) NOT NULL,
  `DiscountPercentage` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `Clients`
--

INSERT INTO `Clients` (`DiscountCardNumber`, `FirstName`, `LastName`, `TelephoneNumber`, `DiscountPercentage`) VALUES
('0000000001', 'Петров', 'Иван', '7-656-656-56-56', 10),
('0000000002', 'Ваньковский', 'Аркадий', '17-888-888-88-88', 5),
('2934845856', 'Никитская', 'Алена', '7-655-454-43-43', 5),
('4390439443', 'Вавилов', 'Семен', '7-777-777-77-77', 80),
('4594948594', 'Трифонов', 'Аркадий', '7-656-565-65-56', 5),
('4950444594', 'Ситников', 'Аркадий', '7-655-655-65-65', 10),
('8549494584', 'Платонов', 'Ярослав', '7-565-565-65-56', 5),
('8549855475', 'Костюшкин', 'Стас', '7-656-565-65-65', 5),
('8958958693', 'Меринов', 'Сергей', '7-656-565-65-65', 10),
('9034034934', 'Ливонова', 'Татьяна', '7-565-454-34-34', 5),
('9058443831', 'Советов', 'Владлен', '7-655-655-65-65', 15),
('9504949504', 'Бабуинов', 'Вячеслав', '7-656-656-65-65', 5);

-- --------------------------------------------------------

--
-- Структура таблицы `ClientSales`
--

CREATE TABLE `ClientSales` (
  `fk_sale_id` int NOT NULL,
  `fk_client_card_number` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `ClientSales`
--

INSERT INTO `ClientSales` (`fk_sale_id`, `fk_client_card_number`) VALUES
(14, '0000000001'),
(15, '0000000001'),
(16, '0000000001'),
(22, '2934845856'),
(23, '4390439443'),
(19, '4594948594'),
(21, '4950444594'),
(18, '8549494584'),
(17, '8958958693');

-- --------------------------------------------------------

--
-- Структура таблицы `MeasurmentUnits`
--

CREATE TABLE `MeasurmentUnits` (
  `MeasurmentUnitName` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `MeasurmentUnits`
--

INSERT INTO `MeasurmentUnits` (`MeasurmentUnitName`) VALUES
('Кг.'),
('Л.'),
('Набор'),
('Пакет'),
('Пачка'),
('Рулон'),
('Шт.');

-- --------------------------------------------------------

--
-- Структура таблицы `Products`
--

CREATE TABLE `Products` (
  `ProductArticle` varchar(10) NOT NULL,
  `ProductName` varchar(30) NOT NULL,
  `BuyingPrice` decimal(10,2) NOT NULL DEFAULT '0.00',
  `SellingPrice` decimal(10,2) NOT NULL DEFAULT '0.00',
  `ProductTypes_ProductType` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `MeasurmentUnits_MeasurmentUnitsName` varchar(30) NOT NULL,
  `Count` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `Products`
--

INSERT INTO `Products` (`ProductArticle`, `ProductName`, `BuyingPrice`, `SellingPrice`, `ProductTypes_ProductType`, `MeasurmentUnits_MeasurmentUnitsName`, `Count`) VALUES
('0000000001', 'Молот \"Vischtrung\"', 1200.00, 3400.00, 'Инструмент', 'Шт.', 40),
('0000000002', 'Кисть \"Drofa\" малярная 3df', 230.00, 1000.20, 'Инструмент', 'Шт.', 31),
('0565565654', 'Гвоздь 3мм', 100.00, 200.00, 'Гвозди и шурупы', 'Пачка', 19),
('5049504595', 'Дрель \"Mr Smitt\"', 460.35, 500.00, 'Инструмент', 'Шт.', 38),
('5940459495', 'Черепеца \"Roof\"', 340.00, 500.00, 'Кровельные материалы', 'Кг.', 59),
('8549854854', 'Краска \"Leaf\" зеленая', 340.00, 670.00, 'Краски', 'Л.', 9),
('8595485494', 'Обои \"Радуга\"', 450.00, 670.00, 'Обои', 'Рулон', 105),
('8983747374', 'Шуруп 12мм', 120.00, 200.00, 'Гвозди и шурупы', 'Пачка', 69),
('8984855854', 'Кирпичи \"BhBricks\"', 1200.00, 3450.50, 'Кирпичи и бетонные блоки', 'Набор', 129),
('9230093932', 'Плитка \"Sevella\"', 1200.00, 3200.00, 'Плитка', 'Набор', 40);

-- --------------------------------------------------------

--
-- Структура таблицы `ProductsBuyingPriceChanges`
--

CREATE TABLE `ProductsBuyingPriceChanges` (
  `DateOfChange` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `NewPrice` decimal(10,2) NOT NULL DEFAULT '0.00',
  `Products_ProductArticle` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `ProductsBuyingPriceChanges`
--

INSERT INTO `ProductsBuyingPriceChanges` (`DateOfChange`, `NewPrice`, `Products_ProductArticle`) VALUES
('2025-12-13 15:25:03', 1200.00, '0000000001'),
('2025-12-13 15:25:45', 230.00, '0000000002'),
('2025-12-13 15:26:55', 1500.00, '0000000001'),
('2025-12-13 21:26:21', 1200.00, '0000000001'),
('2025-12-16 16:46:14', 1200.00, '9230093932'),
('2025-12-16 16:46:44', 340.00, '5940459495'),
('2025-12-16 16:47:19', 340.00, '8549854854'),
('2025-12-16 16:48:03', 1200.00, '8984855854'),
('2025-12-16 16:49:06', 450.00, '8595485494'),
('2025-12-16 16:49:52', 100.00, '0565565654'),
('2025-12-16 16:50:13', 120.00, '8983747374'),
('2025-12-24 10:40:56', 455.34, '5049504595'),
('2025-12-24 10:43:36', 455.35, '5049504595'),
('2025-12-24 10:44:09', 460.35, '5049504595');

-- --------------------------------------------------------

--
-- Структура таблицы `ProductsSellingPriceChanges`
--

CREATE TABLE `ProductsSellingPriceChanges` (
  `DateOfChange` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `NewPrice` decimal(10,2) NOT NULL DEFAULT '0.00',
  `Products_ProductArticle` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `ProductsSellingPriceChanges`
--

INSERT INTO `ProductsSellingPriceChanges` (`DateOfChange`, `NewPrice`, `Products_ProductArticle`) VALUES
('2025-12-13 15:25:03', 3400.00, '0000000001'),
('2025-12-13 15:25:45', 500.00, '0000000002'),
('2025-12-13 15:34:09', 1000.00, '0000000002'),
('2025-12-13 15:38:23', 1000.20, '0000000002'),
('2025-12-16 16:46:14', 3200.00, '9230093932'),
('2025-12-16 16:46:44', 500.00, '5940459495'),
('2025-12-16 16:47:19', 670.00, '8549854854'),
('2025-12-16 16:48:03', 3450.50, '8984855854'),
('2025-12-16 16:49:06', 670.00, '8595485494'),
('2025-12-16 16:49:52', 200.00, '0565565654'),
('2025-12-16 16:50:13', 200.00, '8983747374'),
('2025-12-24 10:40:56', 500.00, '5049504595');

-- --------------------------------------------------------

--
-- Структура таблицы `ProductTypes`
--

CREATE TABLE `ProductTypes` (
  `ProductType` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `ProductTypes`
--

INSERT INTO `ProductTypes` (`ProductType`) VALUES
('Бетон'),
('Гвозди и шурупы'),
('Изоляционные материалы'),
('Инструмент'),
('Кирпичи и бетонные блоки'),
('Краски'),
('Кровельные материалы'),
('Обои'),
('Отделочные материалы'),
('Плитка');

-- --------------------------------------------------------

--
-- Структура таблицы `PurchaseProducts`
--

CREATE TABLE `PurchaseProducts` (
  `fk_purchase_id` int NOT NULL,
  `fk_product_article` varchar(10) NOT NULL,
  `ProductCount` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `PurchaseProducts`
--

INSERT INTO `PurchaseProducts` (`fk_purchase_id`, `fk_product_article`, `ProductCount`) VALUES
(20, '0000000001', 2),
(20, '0000000002', 3),
(23, '0000000001', 1),
(24, '0000000001', 10),
(24, '0000000002', 10),
(25, '0565565654', 30),
(25, '8983747374', 30),
(26, '8595485494', 100),
(27, '5940459495', 30),
(27, '8984855854', 120),
(27, '9230093932', 20),
(28, '0000000002', 5),
(28, '8549854854', 12),
(29, '5940459495', 45),
(29, '8983747374', 45),
(29, '9230093932', 10),
(30, '8595485494', 10),
(31, '8984855854', 10),
(31, '9230093932', 10),
(32, '5049504595', 40),
(34, '0000000001', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `Purchases`
--

CREATE TABLE `Purchases` (
  `Id` int NOT NULL,
  `PurchaseDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `fk_supplier_inn` varchar(10) DEFAULT NULL,
  `LandingBillNumber` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `Purchases`
--

INSERT INTO `Purchases` (`Id`, `PurchaseDate`, `fk_supplier_inn`, `LandingBillNumber`) VALUES
(20, '2025-12-15 10:29:28', '6598659865', '346'),
(23, '2025-12-15 10:46:51', '6598659865', 'Add2'),
(24, '2025-12-16 17:00:48', '3456787653', '4576b346'),
(25, '2025-12-16 17:01:24', '3947374737', '485948bg4859'),
(26, '2025-12-16 17:01:39', '5904954768', '445bg5656'),
(27, '2025-12-16 17:02:03', '5645260769', '3435gh56'),
(28, '2025-12-16 17:02:30', '8394754745', '54547b658'),
(29, '2025-12-16 17:02:59', '6598659865', '44545gh46'),
(30, '2025-12-16 17:03:15', '3947374737', '34578jh76'),
(31, '2025-12-16 17:03:40', '8754574585', '5656f3343'),
(32, '2025-12-24 11:56:23', '3456787653', '45984gh954'),
(34, '2025-12-24 12:03:06', '3456787653', '45454lk44');

-- --------------------------------------------------------

--
-- Структура таблицы `SaleProducts`
--

CREATE TABLE `SaleProducts` (
  `fk_sale_id` int NOT NULL,
  `fk_product_article` varchar(10) NOT NULL,
  `ProductCount` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `SaleProducts`
--

INSERT INTO `SaleProducts` (`fk_sale_id`, `fk_product_article`, `ProductCount`) VALUES
(12, '0000000001', 1),
(12, '0000000002', 1),
(13, '0000000002', 1),
(14, '0000000001', 1),
(14, '0000000002', 2),
(15, '0000000002', 2),
(16, '5940459495', 3),
(16, '8984855854', 1),
(17, '0000000002', 1),
(17, '8549854854', 1),
(17, '8595485494', 2),
(18, '0565565654', 10),
(19, '0000000001', 1),
(19, '8595485494', 1),
(20, '0565565654', 10),
(20, '5940459495', 10),
(20, '8983747374', 5),
(21, '0565565654', 1),
(22, '0000000001', 1),
(22, '5940459495', 1),
(23, '8595485494', 1),
(26, '5049504595', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `Sales`
--

CREATE TABLE `Sales` (
  `Id` int NOT NULL,
  `SaleDate` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `Sales`
--

INSERT INTO `Sales` (`Id`, `SaleDate`) VALUES
(12, '2025-12-13 15:28:31'),
(13, '2025-12-13 15:34:36'),
(14, '2025-12-13 19:22:16'),
(15, '2025-12-14 21:51:15'),
(16, '2025-12-16 17:04:42'),
(17, '2025-12-16 17:04:59'),
(18, '2025-12-16 17:05:09'),
(19, '2025-12-16 17:05:24'),
(20, '2025-12-16 17:05:53'),
(21, '2025-12-16 17:06:03'),
(22, '2025-12-16 18:08:38'),
(23, '2025-12-24 11:19:27'),
(26, '2025-12-24 12:13:44');

-- --------------------------------------------------------

--
-- Структура таблицы `Suppliers`
--

CREATE TABLE `Suppliers` (
  `INN` varchar(10) NOT NULL,
  `SupplierCompany` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `TelephoneNumber` varchar(20) NOT NULL,
  `Email` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `Suppliers`
--

INSERT INTO `Suppliers` (`INN`, `SupplierCompany`, `Address`, `TelephoneNumber`, `Email`) VALUES
('3456787653', 'ООО Русский Стандарт', '', '7-654-344-65-60', 'russtandart@ya.com'),
('3947374737', 'ЗАО Боброзубр', 'Г. Киров, Ул. Ленина 45', '7-654-545-34-23', ''),
('5460945954', 'ООО OakCity', 'Польша, г. Варшава, Ул. Вазимская 34', '7-987-453-32-43', ''),
('5645260769', 'ОАО Богатыри', '', '7-656-656-65-43', 'bogAstroy@mail.com'),
('5869568595', 'ООО ВладимерСтрой', 'Г. Владимир, Ул. Мира 12', '7-654-432-32-32', 'VlamirStroy@gmail.com'),
('5904954768', 'ОАО Мир деревьев', '', '7-655-454-54-54', ''),
('6598659865', 'ООО Рога и копыта', '', '7-656-656-65-65', 'test@mail.com'),
('8394754745', 'ИП Владимир Трубецкой', 'Г. Казань, Ул. Хлестная 23', '7-655-655-43-23', ''),
('8754574585', 'ООО Синяя Ромашка', 'Г.Москва Ул.Пушкина 34', '7-656-566-56-65', '');

-- --------------------------------------------------------

--
-- Структура таблицы `WriteOffs`
--

CREATE TABLE `WriteOffs` (
  `ID` int NOT NULL,
  `WriteOffDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Products_ProductArticle` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `ProductCount` int NOT NULL DEFAULT '0',
  `OperationReason` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `WriteOffs`
--

INSERT INTO `WriteOffs` (`ID`, `WriteOffDate`, `Products_ProductArticle`, `ProductCount`, `OperationReason`) VALUES
(9, '2025-12-16 17:07:41', '8549854854', 2, 'Истекший срок годности'),
(10, '2025-12-16 17:08:01', '5940459495', 1, 'Сломан ящик'),
(11, '2025-12-16 17:08:09', '8595485494', 1, 'Порван рулон'),
(12, '2025-12-16 17:08:22', '8983747374', 1, 'Разрыв упаковки'),
(13, '2025-12-16 18:15:54', '0000000001', 1, ''),
(14, '2025-12-24 12:10:12', '0000000002', 10, 'Воровство'),
(15, '2025-12-24 12:10:29', '5940459495', 1, '');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Clients`
--
ALTER TABLE `Clients`
  ADD PRIMARY KEY (`DiscountCardNumber`),
  ADD UNIQUE KEY `DiscountCardNumber_UNIQUE` (`DiscountCardNumber`);

--
-- Индексы таблицы `ClientSales`
--
ALTER TABLE `ClientSales`
  ADD PRIMARY KEY (`fk_sale_id`,`fk_client_card_number`),
  ADD KEY `cientsales_ibfk_2` (`fk_client_card_number`);

--
-- Индексы таблицы `MeasurmentUnits`
--
ALTER TABLE `MeasurmentUnits`
  ADD PRIMARY KEY (`MeasurmentUnitName`),
  ADD UNIQUE KEY `idtable1_UNIQUE` (`MeasurmentUnitName`);

--
-- Индексы таблицы `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`ProductArticle`),
  ADD UNIQUE KEY `ProductArticle_UNIQUE` (`ProductArticle`),
  ADD KEY `fk_Products_MeasurmentUnits1_idx` (`MeasurmentUnits_MeasurmentUnitsName`),
  ADD KEY `fk_Products_ProductTypes1_idx` (`ProductTypes_ProductType`);

--
-- Индексы таблицы `ProductsBuyingPriceChanges`
--
ALTER TABLE `ProductsBuyingPriceChanges`
  ADD PRIMARY KEY (`DateOfChange`,`Products_ProductArticle`),
  ADD KEY `fk_ProductsBuyingPriceChanges_Products1_idx` (`Products_ProductArticle`);

--
-- Индексы таблицы `ProductsSellingPriceChanges`
--
ALTER TABLE `ProductsSellingPriceChanges`
  ADD PRIMARY KEY (`DateOfChange`,`Products_ProductArticle`),
  ADD KEY `fk_ProductsSellingPriceChanges_Products1_idx` (`Products_ProductArticle`);

--
-- Индексы таблицы `ProductTypes`
--
ALTER TABLE `ProductTypes`
  ADD PRIMARY KEY (`ProductType`),
  ADD UNIQUE KEY `ProductType_UNIQUE` (`ProductType`);

--
-- Индексы таблицы `PurchaseProducts`
--
ALTER TABLE `PurchaseProducts`
  ADD PRIMARY KEY (`fk_purchase_id`,`fk_product_article`),
  ADD KEY `purchaseproducts_ibfk_2` (`fk_product_article`);

--
-- Индексы таблицы `Purchases`
--
ALTER TABLE `Purchases`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `purchases_ibfk_1` (`fk_supplier_inn`);

--
-- Индексы таблицы `SaleProducts`
--
ALTER TABLE `SaleProducts`
  ADD PRIMARY KEY (`fk_sale_id`,`fk_product_article`),
  ADD KEY `saleproducts_ibfk_2` (`fk_product_article`);

--
-- Индексы таблицы `Sales`
--
ALTER TABLE `Sales`
  ADD PRIMARY KEY (`Id`);

--
-- Индексы таблицы `Suppliers`
--
ALTER TABLE `Suppliers`
  ADD PRIMARY KEY (`INN`),
  ADD UNIQUE KEY `INN_UNIQUE` (`INN`);

--
-- Индексы таблицы `WriteOffs`
--
ALTER TABLE `WriteOffs`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `idWriteOffs_UNIQUE` (`ID`),
  ADD KEY `fk_WriteOffs_Products1_idx` (`Products_ProductArticle`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Purchases`
--
ALTER TABLE `Purchases`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT для таблицы `Sales`
--
ALTER TABLE `Sales`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT для таблицы `WriteOffs`
--
ALTER TABLE `WriteOffs`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `ClientSales`
--
ALTER TABLE `ClientSales`
  ADD CONSTRAINT `clientsales_ibfk_1` FOREIGN KEY (`fk_sale_id`) REFERENCES `Sales` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `clientsales_ibfk_2` FOREIGN KEY (`fk_client_card_number`) REFERENCES `Clients` (`DiscountCardNumber`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `Products`
--
ALTER TABLE `Products`
  ADD CONSTRAINT `fk_Products_MeasurmentUnits1` FOREIGN KEY (`MeasurmentUnits_MeasurmentUnitsName`) REFERENCES `MeasurmentUnits` (`MeasurmentUnitName`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Products_ProductTypes1` FOREIGN KEY (`ProductTypes_ProductType`) REFERENCES `ProductTypes` (`ProductType`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `ProductsBuyingPriceChanges`
--
ALTER TABLE `ProductsBuyingPriceChanges`
  ADD CONSTRAINT `fk_ProductsBuyingPriceChanges_Products1` FOREIGN KEY (`Products_ProductArticle`) REFERENCES `Products` (`ProductArticle`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `ProductsSellingPriceChanges`
--
ALTER TABLE `ProductsSellingPriceChanges`
  ADD CONSTRAINT `fk_ProductsSellingPriceChanges_Products1` FOREIGN KEY (`Products_ProductArticle`) REFERENCES `Products` (`ProductArticle`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `PurchaseProducts`
--
ALTER TABLE `PurchaseProducts`
  ADD CONSTRAINT `purchaseproducts_ibfk_1` FOREIGN KEY (`fk_purchase_id`) REFERENCES `Purchases` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `purchaseproducts_ibfk_2` FOREIGN KEY (`fk_product_article`) REFERENCES `Products` (`ProductArticle`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `Purchases`
--
ALTER TABLE `Purchases`
  ADD CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`fk_supplier_inn`) REFERENCES `Suppliers` (`INN`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `SaleProducts`
--
ALTER TABLE `SaleProducts`
  ADD CONSTRAINT `saleproducts_ibfk_1` FOREIGN KEY (`fk_sale_id`) REFERENCES `Sales` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `saleproducts_ibfk_2` FOREIGN KEY (`fk_product_article`) REFERENCES `Products` (`ProductArticle`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `WriteOffs`
--
ALTER TABLE `WriteOffs`
  ADD CONSTRAINT `fk_WriteOffs_Products` FOREIGN KEY (`Products_ProductArticle`) REFERENCES `Products` (`ProductArticle`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
