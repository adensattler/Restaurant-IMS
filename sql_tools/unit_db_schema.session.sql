
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
CREATE TABLE Categories (
    category_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (category_id)
);

-- @block
INSERT INTO Units (unit_name, unit_abbreviation, conversion_to_pounds, precision)
VALUES
('Pounds', 'lbs', 1, 0),                    -- 1 pound equals 1 pound
('Ounces', 'oz', 0.0625, 2),                -- 1 ounce equals 0.0625 pounds
('Kilograms', 'kg', 2.20462, 2),            -- 1 kilogram equals 2.20462 pounds
('Grams', 'g', 0.00220462, 3),              -- 1 gram equals 0.00220462 pounds
('Cups', 'cups', 0.52159, 3),               -- 1 cup of water (as an example) equals 0.52159 pounds
('Liters', 'L', 2.20462, 3),                -- 1 liter of water equals 2.20462 pounds
('Cans', 'cans', NULL, 0),                  -- Non-convertible custom unit (NULL for conversion)
('Packages', 'pkgs', NULL, 0);              -- Non-convertible custom unit


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
    stock DECIMAL(10, 2),
    low_stock_level DECIMAL(10, 2),
    PRIMARY KEY (inventory_item_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
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
INSERT INTO InventoryItems (location_id, name, description, unit, price, stock, low_stock_level)
VALUES
-- Great Granny's Green Beans Ingredients
(1, 'Canned Green Beans', 'Standard canned green beans', 'cans', 0.99, 50, 5),
(1, 'Bullion', 'Chicken bullion', 'cups', 0.10, 30, 5),
(1, 'Potatoes', 'Fresh potatoes', 'pieces', 0.50, 40, 10),
(1, 'Bacon', 'Bacon strips', 'strips', 0.75, 100, 10),

-- Sweet Baby Baked Beans Ingredients
(1, 'Baked Beans', 'Canned baked beans', 'cans', 1.20, 40, 5),
(1, 'BBQ Sauce', 'Sweet Baby Ray BBQ sauce', 'cups', 0.75, 25, 5),
(1, 'Brown Sugar', 'Brown sugar', 'oz', 0.05, 100, 10),
(1, 'Jimmy Dean Sausage', 'Breakfast sausage', 'lb', 3.50, 25, 5),

-- Green Chili Mac & Cheese Ingredients
(1, 'Butter', 'Unsalted butter', 'sticks', 1.50, 50, 5),
(1, 'Flour', 'All-purpose flour', 'cups', 0.10, 100, 10),
(1, 'Milk', 'Whole milk', 'gallons', 3.00, 30, 5),
(1, 'Salt', 'Salt', 'cups', 0.50, 100, 10),
(1, 'Black Pepper', 'Ground black pepper', 'cups', 1.00, 50, 5),
(1, 'Garlic Powder', 'Garlic powder', 'cups', 0.50, 40, 5),
(1, 'Green Chili', 'Canned green chili', 'cans', 1.50, 30, 5),
(1, 'Cheddar Cheese', 'Shredded cheddar cheese', 'bags', 5.00, 20, 5),
(1, 'Parmesan Cheese', 'Shredded Parmesan cheese', 'cups', 3.50, 25, 5),
(1, 'Blue Cheese', 'Crumbled blue cheese', 'cups', 4.50, 20, 5),
(1, 'Macaroni Noodles', 'Macaroni pasta', 'oz', 0.75, 40, 10),

-- Ribs Ingredients
(1, 'Pork Ribs', 'Fresh pork ribs', 'slabs', 10.00, 15, 5),
(1, 'Apple Cider Vinegar', 'Apple cider vinegar', 'oz', 0.05, 100, 10),
(1, 'Paprika', 'Ground paprika', 'cups', 1.00, 40, 5),
(1, 'Cayenne Pepper', 'Ground cayenne pepper', 'cups', 1.50, 30, 5),
-- (1, 'Brown Sugar', 'Brown sugar', 'cups', 0.05, 100, 10),

-- Wings Ingredients
(1, 'Chicken Wings', 'Fresh chicken wings', 'lbs', 2.00, 30, 10),

-- Hotlinks Ingredients
(1, 'Hotlinks', 'Spicy hotlink sausage', 'link', 4.50, 20, 5),

-- Catfish Ingredients
(1, 'Catfish Fillet', 'Fresh catfish fillet', 'pieces', 5.00, 10, 5),

-- Seasonings
(1, 'Seasoning Mix', 'House seasoning mix', 'cups', 2.00, 20, 5);



-- @block
-- Populate MenuItems table
INSERT INTO MenuItems (category_id, name, description, price)
VALUES
(1, 'Sweet baby baked beans', 'Our signature baked beans', 4.00),
(1, 'Teriyaki Parmesean Corn', 'Corn with a twist', 4.00),
(1, 'Great Granny''s Green Beans', 'Classic green beans', 4.00),
(1, 'Green Chili Macaronni', 'Spicy mac and cheese', 4.00),
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
-- Great Granny's Green Beans (Menu Item ID: 3)
(3, 1, 2.0, 'cans'), -- Canned Green Beans
(3, 2, 1.25, 'cups'), -- Bullion
(3, 3, 3.0, 'pieces'), -- Potatoes
(3, 4, 3.0, 'strips'), -- Bacon

-- Sweet Baby Baked Beans (Menu Item ID: 1)
(1, 5, 2.0, 'cans'), -- Baked Beans
(1, 6, 1.25, 'cups'), -- BBQ Sauce
(1, 7, 1.5, 'oz'), -- Brown Sugar
(1, 8, 1.0, 'lb'), -- Jimmy Dean Sausage

-- Green Chili Mac & Cheese (Menu Item ID: 4)
(4, 9, 2.5, 'sticks'), -- Butter
(4, 10, 2.0, 'cups'), -- Flour
(4, 11, 4.0, 'gallons'), -- Milk
(4, 12, 1.25, 'cups'), -- Salt
(4, 13, 0.5, 'cups'), -- Black Pepper
(4, 14, 0.75, 'cups'), -- Garlic Powder
(4, 15, 1.0, 'can'), -- Green Chili
(4, 16, 1.0, 'bag'), -- Cheddar Cheese
(4, 17, 5.0, 'cups'), -- Parmesan Cheese
(4, 18, 4.0, 'cups'), -- Blue Cheese
(4, 19, 8.0, 'oz'), -- Macaroni Noodles

-- Rib Plate (Menu Item ID: 14)
(14, 20, 4.0, 'slabs'), -- Pork Ribs
(14, 21, 1.0, 'oz'), -- Apple Cider Vinegar
(14, 22, 8.0, 'cups'), -- Paprika
(14, 23, 1.5, 'cups'), -- Cayenne Pepper
(14, 24, 4.0, 'cups'), -- Brown Sugar

-- Wing Plate (Menu Item ID: 13)
(13, 25, 6.0, 'lbs'), -- Chicken Wings

-- Hotlink Plate (Menu Item ID: 15)
(15, 26, 1.0, 'link'), -- Hotlink

-- Catfish Plate (Menu Item ID: 16)
(16, 27, 1.0, 'pieces'); -- Catfish Fillet

-- @block
SELECT * FROM MenuItems;

-- @block
SELECT * FROM InventoryItems;

-- @block
SELECT * FROM MenuItemComponents;

-- @block 
DROP TABLE MenuItemComponents;

-- @block 
DROP TABLE MenuItems;

-- @block 
DROP TABLE InventoryItems;

-- @block
 SELECT InventoryItems.name AS inventory_item_name, MenuItemComponents.quantity_required
        FROM MenuItemComponents
        JOIN InventoryItems ON MenuItemComponents.inventory_item_id = InventoryItems.inventory_item_id
        WHERE MenuItemComponents.menu_item_id = 4