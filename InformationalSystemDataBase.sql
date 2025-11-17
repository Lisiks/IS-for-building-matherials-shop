-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Хост: MySQL-8.0
-- Время создания: Ноя 17 2025 г., 14:05
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

-- --------------------------------------------------------

--
-- Структура таблицы `ClientSales`
--

CREATE TABLE `ClientSales` (
  `Sales_ID` int NOT NULL,
  `Clients_DiscountCardNumber` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Структура таблицы `MeasurmentUnits`
--

CREATE TABLE `MeasurmentUnits` (
  `MeasurmentUnitName` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

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

-- --------------------------------------------------------

--
-- Структура таблицы `ProductsBuyingPriceChanges`
--

CREATE TABLE `ProductsBuyingPriceChanges` (
  `DateOfChange` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `OldPrice` decimal(10,2) NOT NULL DEFAULT '0.00',
  `Products_ProductArticle` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Структура таблицы `ProductsSellingPriceChanges`
--

CREATE TABLE `ProductsSellingPriceChanges` (
  `DateOfChange` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `OldPrice` decimal(10,2) NOT NULL DEFAULT '0.00',
  `Products_ProductArticle` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Структура таблицы `ProductTypes`
--

CREATE TABLE `ProductTypes` (
  `ProductType` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Структура таблицы `Purchases`
--

CREATE TABLE `Purchases` (
  `ID` int NOT NULL,
  `PurchaseDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Suppliers_INN` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `LandingBillNumber` varchar(30) DEFAULT NULL,
  `Products_ProductArticle` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `ProductCount` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Структура таблицы `Sales`
--

CREATE TABLE `Sales` (
  `ID` int NOT NULL,
  `SaleDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Products_ProductArticle` varchar(10) NOT NULL,
  `ProductCount` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

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

-- --------------------------------------------------------

--
-- Структура таблицы `WriteOffs`
--

CREATE TABLE `WriteOffs` (
  `ID` int NOT NULL,
  `WriteOffDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Products_ProductArticle` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `ProductCount` int NOT NULL,
  `OperationReason` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

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
  ADD PRIMARY KEY (`Sales_ID`),
  ADD KEY `fk_ClientSales_Sales1_idx` (`Sales_ID`),
  ADD KEY `fk_ClientSales_Clients1_idx` (`Clients_DiscountCardNumber`);

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
-- Индексы таблицы `Purchases`
--
ALTER TABLE `Purchases`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `idPurchases_UNIQUE` (`ID`),
  ADD KEY `fk_Purchases_Products1_idx` (`Products_ProductArticle`),
  ADD KEY `fk_Purchases_Suppliers1_idx` (`Suppliers_INN`),
  ADD KEY `Purchases_date_index` (`PurchaseDate`);

--
-- Индексы таблицы `Sales`
--
ALTER TABLE `Sales`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `idSales_UNIQUE` (`ID`),
  ADD KEY `fk_Sales_Products1_idx` (`Products_ProductArticle`),
  ADD KEY `Sales_date_index` (`SaleDate`);

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
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT для таблицы `Sales`
--
ALTER TABLE `Sales`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT для таблицы `WriteOffs`
--
ALTER TABLE `WriteOffs`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `ClientSales`
--
ALTER TABLE `ClientSales`
  ADD CONSTRAINT `fk_ClientSales_Clients` FOREIGN KEY (`Clients_DiscountCardNumber`) REFERENCES `Clients` (`DiscountCardNumber`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_ClientSales_Sales` FOREIGN KEY (`Sales_ID`) REFERENCES `Sales` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

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
-- Ограничения внешнего ключа таблицы `Purchases`
--
ALTER TABLE `Purchases`
  ADD CONSTRAINT `fk_Purchases_Products` FOREIGN KEY (`Products_ProductArticle`) REFERENCES `Products` (`ProductArticle`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Purchases_Suppliers` FOREIGN KEY (`Suppliers_INN`) REFERENCES `Suppliers` (`INN`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `Sales`
--
ALTER TABLE `Sales`
  ADD CONSTRAINT `fk_Sales_Products1` FOREIGN KEY (`Products_ProductArticle`) REFERENCES `Products` (`ProductArticle`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `WriteOffs`
--
ALTER TABLE `WriteOffs`
  ADD CONSTRAINT `fk_WriteOffs_Products` FOREIGN KEY (`Products_ProductArticle`) REFERENCES `Products` (`ProductArticle`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
