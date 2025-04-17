--------------------------------------------------------------------
-- Script Name: DB_Fireworks3.sql
-- Date Created: 02-27-2025
-- Database: FireworksDB
-- Description: The Database for the Hagley Museum and 
--                Library's Fireworks Event 
--------------------------------------------------------------------


CREATE DATABASE IF NOT EXISTS fireworks DEFAULT CHARACTER SET utf8;
USE `fireworks`;
--------------------------------------------------------------------


--------------------------------------------------------------------
-- Table Creation
--------------------------------------------------------------------

CREATE TABLE Orders (
    orderID INT UNIQUE PRIMARY KEY,
    fullname VARCHAR(75) NOT NULL,
    isMember BOOLEAN NOT NULL,
    generalPermitQuantity INT DEFAULT 0 CHECK (generalPermitQuantity >= 0),
	premiumPermitQuantity INT DEFAULT 0 CHECK (premiumPermitQuantity >= 0),
    adultWristbandQuantity INT DEFAULT 0 CHECK (adultWristbandQuantity >= 0),
    youthWristbandQuantity INT DEFAULT 0 CHECK (youthWristbandQuantity >= 0),
	dayOfAttend DATE NOT NULL
);

-- No relationship to orders unless the users get roles departments.
CREATE TABLE Users (
    userID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(25) UNIQUE NOT NULL,
    userPassword VARCHAR(100) NOT NULL -- encrypted field
    -- departmentName VARCHAR(20)
);


--------------------------------------------------------------------
-- Stored Procedure for the Dashboard
--------------------------------------------------------------------

DELIMITER $$

CREATE PROCEDURE DashboardOutDay1()
BEGIN
    DECLARE TotalYouthWristbands1 INT DEFAULT 0;
    DECLARE TotalAdultWristbands1 INT DEFAULT 0;
    DECLARE TotalPremiumPermits1 INT DEFAULT 0;
    DECLARE TotalGeneralPermits1 INT DEFAULT 0;
    DECLARE EventDate1 DATE;

    SELECT DISTINCT dayOfAttend
    INTO EventDate1
    FROM Orders
    WHERE YEAR(dayOfAttend) = YEAR(CURDATE())
    LIMIT 1;

    SELECT 
        COALESCE(SUM(adultWristbandQuantity), 0), 
        COALESCE(SUM(youthWristbandQuantity), 0), 
        COALESCE(SUM(generalPermitQuantity), 0), 
        COALESCE(SUM(premiumPermitQuantity), 0)
    INTO 
        TotalAdultWristbands1, 
        TotalYouthWristbands1, 
        TotalGeneralPermits1, 
        TotalPremiumPermits1
    FROM Orders
    WHERE dayOfAttend = EventDate1;

    SELECT 
        TotalAdultWristbands1 AS TotalAdultWristbands, 
        TotalYouthWristbands1 AS TotalYouthWristbands, 
        TotalGeneralPermits1 AS TotalGeneralPermits, 
        TotalPremiumPermits1 AS TotalPremiumPermits, 
        EventDate1 AS EventDate;
END $$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE DashboardOutDay2()
BEGIN
    DECLARE TotalYouthWristbands2 INT DEFAULT 0;
    DECLARE TotalAdultWristbands2 INT DEFAULT 0;
    DECLARE TotalPremiumPermits2 INT DEFAULT 0;
    DECLARE TotalGeneralPermits2 INT DEFAULT 0;
    DECLARE EventDate2 DATE;

    SELECT DISTINCT dayOfAttend
    INTO EventDate2
    FROM Orders
    WHERE YEAR(dayOfAttend) = YEAR(CURDATE())
    AND dayOfAttend != (SELECT DISTINCT dayOfAttend
                        FROM Orders
                        WHERE YEAR(dayOfAttend) = YEAR(CURDATE())
                        LIMIT 1)
    LIMIT 1;

    SELECT 
        COALESCE(SUM(adultWristbandQuantity), 0), 
        COALESCE(SUM(youthWristbandQuantity), 0), 
        COALESCE(SUM(generalPermitQuantity), 0), 
        COALESCE(SUM(premiumPermitQuantity), 0)
    INTO 
        TotalAdultWristbands2, 
        TotalYouthWristbands2, 
        TotalGeneralPermits2, 
        TotalPremiumPermits2
    FROM Orders
    WHERE dayOfAttend = EventDate2;

    SELECT 
        TotalAdultWristbands2 AS TotalAdultWristbands, 
        TotalYouthWristbands2 AS TotalYouthWristbands, 
        TotalGeneralPermits2 AS TotalGeneralPermits, 
        TotalPremiumPermits2 AS TotalPremiumPermits, 
        EventDate2 AS EventDate;
END $$

DELIMITER ;


