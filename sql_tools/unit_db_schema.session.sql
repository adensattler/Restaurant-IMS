
-- DATABASE CREATION BLOCK(S)
-- --------------------------------------------------------------------
-- @block
CREATE TABLE Units (
    unit_id INT NOT NULL AUTO_INCREMENT,
    unit_name VARCHAR(100) NOT NULL,
    unit_abbreviation VARCHAR(10) NOT NULL,
    precision_value INT DEFAULT 2,                 -- Precision for calculations
    PRIMARY KEY (unit_id)
);

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
CREATE TABLE InventoryItems (
    inventory_item_id INT NOT NULL AUTO_INCREMENT,
    location_id INT,
    name VARCHAR(255),
    description TEXT,
    GTIN VARCHAR(50),
    SKU VARCHAR(255),
    unit_id INT,
    weight DECIMAL(10, 2),
    price DECIMAL(10, 2),
    stock DECIMAL(10, 2),
    low_stock_level DECIMAL(10, 2),
    PRIMARY KEY (inventory_item_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id),
    FOREIGN KEY (unit_id) REFERENCES Units(unit_id)
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
    PRIMARY KEY (component_id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id),
    FOREIGN KEY (inventory_item_id) REFERENCES InventoryItems(inventory_item_id)
);



-- DATABASE INITIALIZATION/POPULATION BLOCK(S)
-- --------------------------------------------------------------------
-- @block
-- Populate Units table with common units and their conversions
INSERT INTO Units (unit_name, unit_abbreviation, precision_value)
VALUES
-- Common Units
('Pound', 'lb', 2),
('Ounce', 'oz', 2),
('Kilogram', 'kg', 3),
('Gram', 'g', 3),
('Cup', 'cup', 3),
('Liters', 'L', 3),
('Milliliter', 'L', 2),
('Gallon', 'gal', 2),

-- Custom Units
('Per item', 'ea', 0);

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
INSERT INTO InventoryItems (location_id, name, description, unit_id, price, stock, low_stock_level)
VALUES
-- Great Granny's Green Beans Ingredients
(1, 'Canned Green Beans', 'Standard canned green beans', 9, 0.99, 50, 5), -- 'Per item'
(1, 'Bullion', 'Chicken bullion', 5, 0.10, 30, 5), -- 'Cup'
(1, 'Potatoes', 'Fresh potatoes', 9, 0.50, 40, 10), -- 'Per item'
(1, 'Bacon', 'Bacon strips', 9, 0.75, 100, 10), -- 'Per item'

-- Sweet Baby Baked Beans Ingredients
(1, 'Baked Beans', 'Canned baked beans', 9, 1.20, 40, 5), -- 'Per item'
(1, 'BBQ Sauce', 'Sweet Baby Ray BBQ sauce', 5, 0.75, 25, 5), -- 'Cup'
(1, 'Brown Sugar', 'Brown sugar', 2, 0.05, 100, 10), -- 'Ounce'
(1, 'Jimmy Dean Sausage', 'Breakfast sausage', 1, 3.50, 25, 5), -- 'Pound'

-- Green Chili Mac & Cheese Ingredients
(1, 'Butter', 'Unsalted butter', 9, 1.50, 50, 5), -- 'Per item'
(1, 'Flour', 'All-purpose flour', 5, 0.10, 100, 10), -- 'Cup'
(1, 'Milk', 'Whole milk', 8, 3.00, 30, 5), -- 'Gallon'
(1, 'Salt', 'Salt', 5, 0.50, 100, 10), -- 'Cup'
(1, 'Black Pepper', 'Ground black pepper', 5, 1.00, 50, 5), -- 'Cup'
(1, 'Garlic Powder', 'Garlic powder', 5, 0.50, 40, 5), -- 'Cup'
(1, 'Green Chili', 'Canned green chili', 9, 1.50, 30, 5), -- 'Per item'
(1, 'Cheddar Cheese', 'Shredded cheddar cheese', 9, 5.00, 20, 5), -- 'Per item'
(1, 'Parmesan Cheese', 'Shredded Parmesan cheese', 5, 3.50, 25, 5), -- 'Cup'
(1, 'Blue Cheese', 'Crumbled blue cheese', 5, 4.50, 20, 5), -- 'Cup'
(1, 'Macaroni Noodles', 'Macaroni pasta', 2, 0.75, 40, 10), -- 'Ounce'

-- Ribs Ingredients
(1, 'Pork Ribs', 'Fresh pork ribs', 9, 10.00, 15, 5), -- 'Per item'
(1, 'Apple Cider Vinegar', 'Apple cider vinegar', 2, 0.05, 100, 10), -- 'Ounce'
(1, 'Paprika', 'Ground paprika', 5, 1.00, 40, 5), -- 'Cup'
(1, 'Cayenne Pepper', 'Ground cayenne pepper', 5, 1.50, 30, 5), -- 'Cup'

-- Wings Ingredients
(1, 'Chicken Wings', 'Fresh chicken wings', 1, 2.00, 30, 10), -- 'Pound'

-- Hotlinks Ingredients
(1, 'Hotlinks', 'Spicy hotlink sausage', 9, 4.50, 20, 5), -- 'Per item'

-- Catfish Ingredients
(1, 'Catfish Fillet', 'Fresh catfish fillet', 9, 5.00, 10, 5), -- 'Per item'

-- Seasonings
(1, 'Seasoning Mix', 'House seasoning mix', 5, 2.00, 20, 5); -- 'Cup'



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
INSERT INTO MenuItemComponents (menu_item_id, inventory_item_id, quantity_required)
VALUES
-- Sweet Baby Baked Beans (Menu Item ID: 1)
(1, 5, 0.5), -- Baked Beans
(1, 6, 0.1), -- BBQ Sauce
(1, 7, 0.1), -- Brown Sugar
(1, 8, 0.1), -- Jimmy Dean Sausage

-- Teriyaki Parmesean Corn (Menu Item ID: 2)
-- None for now

-- Great Granny's Green Beans (Menu Item ID: 3)
(3, 1, 0.5), -- Canned Green Beans
(3, 2, 0.25), -- Bullion
(3, 3, 3.0), -- Potatoes
(3, 4, 3.0), -- Bacon

-- Green Chili Mac & Cheese (Menu Item ID: 4)
(4, 9, 0.25), -- Butter
(4, 10, 0.25), -- Flour
(4, 11, 0.25), -- Milk
(4, 12, 0.25), -- Salt
(4, 13, 0.25), -- Black Pepper
(4, 14, 0.25), -- Garlic Powder
(4, 15, 0.25), -- Green Chili
(4, 16, 0.25), -- Cheddar Cheese
(4, 17, 0.25), -- Parmesan Cheese
(4, 18, 0.25), -- Blue Cheese
(4, 19, 0.25), -- Macaroni Noodles

-- Wing Wednesday (Menu Item ID: 5)

-- Wings a la Carte (Menu Item ID: 6)

-- extra sauce (Menu Item ID: 7)

-- Ribs a la Carte (Menu Item ID: 8)

-- Hotlink a la Carte (Menu Item ID: 9)

-- Fountain Drinks (Menu Item ID: 10)

-- Cooler Drinks (Menu Item ID: 11)

-- Little Man Ice Cream (Menu Item ID: 12)

-- Wing Plate (Menu Item ID: 13)
(13, 25, 6.0), -- Chicken Wings

-- Rib Plate (Menu Item ID: 14)
(14, 20, 4.0), -- Pork Ribs
(14, 21, 0.25), -- Apple Cider Vinegar
(14, 22, 0.25), -- Paprika
(14, 23, 0.25), -- Cayenne Pepper

-- Hotlink Plate (Menu Item ID: 15)
(15, 24, 1.0), -- Hotlink

-- Catfish Plate (Menu Item ID: 16)
(16, 25, 1.0); -- Catfish Fillet

-- @block
SELECT * FROM MenuItems;

-- @block
SELECT * FROM InventoryItems;

-- @block
SELECT * FROM MenuItemComponents;


-- DROP TABLES BLOCKS
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