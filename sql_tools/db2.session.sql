
-- @block
SELECT * FROM InventoryItems;

-- @block
DROP TABLE Locations;

-- DATABASE CREATION BLOCK(S)
-- --------------------------------------------------------------------
-- @block
CREATE TABLE Locations (
    location_id INT NOT NULL AUTO_INCREMENT,
    location_name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    zipcode VARCHAR(20),
    PRIMARY KEY (location_id)
);

-- @block
CREATE TABLE InventoryItems (
    inventory_item_id INT NOT NULL AUTO_INCREMENT,
    location_id INT,
    name VARCHAR(255),
    description TEXT,
    GTIN VARCHAR(50),
    SKU VARCHAR(255),
    unit VARCHAR(50),
    weight DECIMAL(10, 2),
    price DECIMAL(10, 2),
    current_quantity INT,
    reorder_threshold INT,
    PRIMARY KEY (inventory_item_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
);

-- @block
CREATE TABLE Categories (
    category_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (category_id)
);

-- @block
CREATE TABLE MenuItems (
    menu_item_id INT NOT NULL AUTO_INCREMENT,
    category_id INT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    instructions TEXT,
    price DECIMAL(10, 2),
    PRIMARY KEY (menu_item_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- @block
-- Serves as a junction table to link MenuItems and InventoryItems
CREATE TABLE MenuItemComponents (
    component_id INT NOT NULL AUTO_INCREMENT,
    menu_item_id INT,
    inventory_item_id INT,
    quantity_required DECIMAL(10, 2),
    unit VARCHAR(50),
    PRIMARY KEY (component_id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id),
    FOREIGN KEY (inventory_item_id) REFERENCES InventoryItems(inventory_item_id)
);



-- DATABASE INITIALIZATION/POPULATION BLOCK(S)
-- --------------------------------------------------------------------

-- @block
INSERT INTO Locations (location_name, address, city, state, zipcode)
VALUES
    ('DU', '2100 S University Blvd', 'Denver', 'CO', 80210);


-- @block
-- Populate Categories table
INSERT INTO Categories (name) VALUES
('Sides'), ('Mains'), ('Drinks'), ('Desserts'), ('A La Carte');

-- @block
-- Populate InventoryItems table (sample ingredients)
INSERT INTO InventoryItems (location_id, name, unit, price, current_quantity, reorder_threshold)
VALUES
(1, 'Baked Beans', 'oz', 2.50, 100, 20),
(1, 'Corn', 'oz', 1.50, 100, 20),
(1, 'Green Beans', 'oz', 1.50, 100, 20),
(1, 'Macaroni', 'oz', 1.00, 100, 20),
(1, 'Chicken Wings', 'lb', 5.00, 50, 10),
(1, 'Ribs', 'lb', 8.00, 30, 5),
(1, 'Hotlink', 'each', 2.00, 50, 10),
(1, 'Fountain Drink Syrup', 'gallon', 20.00, 10, 2),
(1, 'Bottled Drinks', 'each', 1.50, 100, 20),
(1, 'Ice Cream', 'oz', 3.00, 50, 10),
(1, 'Catfish', 'lb', 6.00, 30, 5),
(1, 'BBQ Sauce', 'oz', 1.00, 50, 10),
(1, 'Mustard', 'oz', 0.50, 30, 5);

-- @block
-- Populate MenuItems table
INSERT INTO MenuItems (category_id, name, description, price)
VALUES
(1, 'Sweet baby baked beans', 'Our signature baked beans', 4.00),
(1, 'Teriyaki Parmesan Corn', 'Corn with a twist', 4.00),
(1, 'Great Granny''s Green Beans', 'Classic green beans', 4.00),
(1, 'Green Chili Macaroni', 'Spicy mac and cheese', 4.00),
(2, 'Wing Wednesday', 'Special wing deal on Wednesdays', 1.00),
(5, 'wings a la carte', 'Just the wings', 2.00),
(5, 'extra sauce', 'Additional sauce portion', 0.50),
(5, 'ribs a la carte', 'Just the ribs', 3.00),
(5, 'hotlink a la carte', 'Single hotlink', 4.50),
(3, 'fountain drinks', 'Assorted fountain drinks', 1.75),
(3, 'cooler drinks', 'Assorted bottled drinks', 3.00),
(4, 'little mans ice cream', 'Delicious ice cream', 9.50),
(2, 'Wing Plate', 'Wings with two sides', 16.25),
(2, 'Rib plate', 'Ribs with two sides', 16.25),
(2, 'Hotlink Plate', 'Hotlink with two sides and mustard', 16.25),
(2, 'Catfish plate', 'Catfish with two sides', 16.25),
(2, 'Two Meat Plate', 'Choice of two meats with two sides', 18.25),
(2, 'Three Meat Plate', 'Choice of three meats with two sides', 23.25);

-- @block
-- Populate MenuItemComponents table (sample relationships)
INSERT INTO MenuItemComponents (menu_item_id, inventory_item_id, quantity_required, unit)
VALUES
(1, 1, 6, 'oz'),  -- Baked Beans for Sweet Baby Baked Beans
(2, 2, 6, 'oz'),  -- Corn for Teriyaki Parmesan Corn
(3, 3, 6, 'oz'),  -- Green Beans for Great Granny's Green Beans
(4, 4, 6, 'oz'),  -- Macaroni for Green Chili Macaroni
(5, 5, 1, 'lb'),  -- Chicken Wings for Wing Wednesday Special
(6, 5, 1, 'lb'),  -- Chicken Wings for Wings A La Carte
(8, 6, 1, 'lb'),  -- Ribs for Ribs A La Carte
(9, 7, 1, 'each'),  -- Hotlink for Hotlink A La Carte
(10, 8, 0.25, 'gallon'), -- Fountain Drink Syrup for Fountain Drinks
(12, 10, 6, 'oz'),   -- Ice Cream for Little Man's Ice Cream
(13, 5, 1, 'lb'),    -- Chicken Wings for Wing Plate
(14, 6, 1, 'lb'),    -- Ribs for Rib Plate
(15, 7, 1, 'each'),    -- Hotlink for Hotlink Plate
(15, 13, 1, 'oz');   -- Mustard for Hotlink Plate

-- @block
SELECT * FROM MenuItemComponents;

-- @block 
DROP TABLE MenuItems;