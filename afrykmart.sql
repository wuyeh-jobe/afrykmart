-- phpMyAdmin SQL Dump
-- version 4.8.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 07, 2018 at 02:28 AM
-- Server version: 10.1.34-MariaDB
-- PHP Version: 7.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `afrykmart`
--

-- --------------------------------------------------------

--
-- Table structure for table `brands`
--

CREATE TABLE `brands` (
  `brand_id` int(11) NOT NULL,
  `brand_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `brands`
--

INSERT INTO `brands` (`brand_id`, `brand_name`) VALUES
(1, 'Ubuntu'),
(2, 'Maasai Market'),
(3, 'Bantu Cloth'),
(4, 'Kente'),
(5, 'Gele Wear'),
(6, 'Ultimate Turban');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `p_id` int(10) NOT NULL,
  `ip_add` varchar(255) NOT NULL,
  `qty` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`p_id`, `ip_add`, `qty`) VALUES
(1, '127.0.0.1', 2),
(2, '127.0.0.1', 3),
(2, '127.0.0.1', 3),
(2, '127.0.0.1', 3);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `cat_id` int(11) NOT NULL,
  `cat_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`cat_id`, `cat_name`) VALUES
(1, 'Afryk Toiletry'),
(2, 'Afryk Print Clothes'),
(3, 'Afryk Footwear'),
(4, 'Afryk Jewellery '),
(5, 'Men'),
(6, 'Women'),
(7, 'West-African'),
(8, 'Eastern-Africa'),
(9, 'Sourvinirs-Africa');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `emp_id` int(11) NOT NULL,
  `cost` double NOT NULL,
  `details` text NOT NULL,
  `status` enum('Successful','Pending','Failed') NOT NULL,
  `date_ordered` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `product_cat` int(11) NOT NULL,
  `product_brand` int(11) NOT NULL,
  `product_title` varchar(255) NOT NULL,
  `product_price` int(11) NOT NULL,
  `product_desc` text NOT NULL,
  `product_image` text NOT NULL,
  `product_keywords` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_cat`, `product_brand`, `product_title`, `product_price`, `product_desc`, `product_image`, `product_keywords`) VALUES
(1, 1, 1, 'Fancy African Blazer', 40, 'African made Blazer', 'blazer.jpg', 'blazer, women, african'),
(2, 3, 4, 'Kente Suit', 458, 'The best in town!!', 'kentesuit.jpg', 'kente, men, Nothern Ghana'),
(3, 3, 3, 'Maasai Shirt', 350, 'Maasai touch shirt', 'maasaishirt.jpg', 'maasai, men, shirt'),
(4, 2, 3, 'Fancy Necklace', 200, 'a fancy necklace for your neck', 'maasaibag.jpeg', 'necklace,jewelclass'),
(5, 2, 3, 'Fancy Necklace', 200, 'a fancy necklace for your neck', 'dress.jpg', 'necklace,jewelclass'),
(6, 2, 3, 'Fancy Necklace', 200, 'a fancy necklace for your neck', 'shuka.jpg', 'necklace,jewelclass'),
(7, 2, 3, 'Fancy Necklace', 200, 'a fancy necklace for your neck', 'heavyneck.jpg', 'necklace,jewelclass'),
(8, 2, 3, 'Fancy Necklace', 200, 'a fancy necklace for your neck', 'necklace.jpg', 'necklace,jewelclass'),
(9, 2, 3, 'Fancy Necklace', 200, 'a fancy necklace for your neck', 'fancyheels.jpg', 'necklace,jewelclass'),
(10, 2, 3, 'Fancy Necklace', 200, 'a fancy necklace for your neck', 'slippers.jpg', 'necklace,jewelclass'),
(11, 2, 3, 'Fancy Necklace', 200, 'a fancy necklace for your neck', 'jewelset.jpg', 'necklace,jewelclass'),
(12, 2, 3, 'Fancy Women Tops', 400, 'fancy tops for your body', 'tops.jpg', 'tops, ladies, african,cloth'),
(13, 2, 3, 'Lingerie', 250, 'a fancy lingerie for girls and wome', 'lingerie.jpg', 'lingerie, innerwear'),
(14, 2, 3, 'Shea Butter', 200, 'perfect for natural hair', 'hairoil.jpg', 'African beauty'),
(15, 2, 3, 'Body Oil', 240, 'Oil for skin, very good', 'bodyoil.jpg', 'body oil, african, skin,'),
(16, 2, 3, 'Dashiki Dress', 260, 'a real african wears the pride of Africa Dashiki.', 'dashiki.jpg', 'dashiki, purely african, pride of africa'),
(17, 2, 3, 'Fancy Body Wear', 500, 'a fancy necklace for your neck', 'banner03.jpg', 'necklace,jewelclass'),
(18, 2, 3, 'Fancy Necklace', 100, 'a fancy necklace for your neck', 'banner02.jpg', 'necklace,jewelclass'),
(19, 2, 3, 'Fancy Necklace', 1000, 'a fancy necklace for your neck', 'banner01.jpg', 'necklace,jewelclass');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `gender` enum('Male','Female') NOT NULL,
  `date_of_birth` date NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Admin','Standard') NOT NULL DEFAULT 'Standard',
  `status` enum('Active','Inactive') NOT NULL DEFAULT 'Active',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `full_name`, `gender`, `date_of_birth`, `email`, `password`, `role`, `status`, `date_created`) VALUES
(3, 'Wuyeh Jobe', 'Male', '2018-11-03', 'jwuyeh@gmail.com', '1122', 'Standard', 'Active', '2018-11-03 23:04:07'),
(4, 'Faith Kilonzi', 'Female', '2018-10-28', 'lcaromin@asu.edu', '7877', 'Standard', 'Active', '2018-11-03 23:06:33'),
(5, 'Rahmat', 'Female', '2018-11-05', 'rahmat@gmail.com', '1122', 'Standard', 'Active', '2018-11-05 15:51:11'),
(6, 'Nanis Kanana', 'Female', '2018-11-05', 'jwuyeh@gmail.com', '1122', 'Standard', 'Active', '2018-11-05 19:20:50');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `brands`
--
ALTER TABLE `brands`
  ADD PRIMARY KEY (`brand_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`cat_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `product_cat` (`product_cat`),
  ADD KEY `product_brand` (`product_brand`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `brands`
--
ALTER TABLE `brands`
  MODIFY `brand_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `cat_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`product_cat`) REFERENCES `categories` (`cat_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`product_brand`) REFERENCES `brands` (`brand_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
