-- @block
SELECT * FROM Items;

-- @block
DROP TABLE Items;



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

-- @block NEW ITEMS
CREATE TABLE Items (
    item_id INT NOT NULL AUTO_INCREMENT,
    location_id INT,
    name VARCHAR(255),
    description TEXT,
    GTIN VARCHAR(50),
    SKU VARCHAR(255),
    unit VARCHAR(50),
    weight DECIMAL(10, 2),
    price DECIMAL(10, 2),
    stock INT,
    low_stock_level INT,
    PRIMARY KEY (item_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
);



-- @block
CREATE TABLE Recipes (
    recipe_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    instructions TEXT,
    PRIMARY KEY (recipe_id)
);

-- @block
-- Serves as a junction table to link Recipes and Items
CREATE TABLE RecipeItems (
    recipe_item_id INT NOT NULL AUTO_INCREMENT,
    recipe_id INT,
    item_id INT,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50),
    PRIMARY KEY (recipe_item_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id),
    FOREIGN KEY (item_id) REFERENCES Items(item_id)
);


-- @block
INSERT INTO Locations (location_name, address, city, state, zipcode)
VALUES
    ('DU', '2100 S University Blvd', 'Denver', 'CO', 80210);

-- @block
-- Inserting data into Items table
INSERT INTO Items (location_id, name, description, GTIN, SKU, unit, weight, price, stock, low_stock_level)
VALUES 
    (1, 'Pork Ribs', 'Description of Pork Ribs', '1234567890123', 'SKU123', 'lbs', 0.00, 0.00, 20, 5),
    (1, 'Chicken Wings', 'Description of Chicken Wings', '1234567890124', 'SKU124', 'lbs', 0.00, 0.00, 15, 5),
    (1, 'Beef Brisket', 'Description of Beef Brisket', '1234567890125', 'SKU125', 'lbs', 0.00, 0.00, 25, 5),
    (1, 'Pulled Pork', 'Description of Pulled Pork', '1234567890126', 'SKU126', 'lbs', 0.00, 0.00, 18, 5),
    (1, 'BBQ Sauce', 'Description of BBQ Sauce', '1234567890127', 'SKU127', 'bottles', 0.00, 0.00, 10, 5),
    (1, 'Potato Salad', 'Description of Potato Salad', '1234567890128', 'SKU128', 'servings', 0.00, 0.00, 30, 10),
    (1, 'Cornbread', 'Description of Cornbread', '1234567890129', 'SKU129', 'pieces', 0.00, 0.00, 40, 15),
    (1, 'Cole Slaw', 'Description of Cole Slaw', '1234567890130', 'SKU130', 'servings', 0.00, 0.00, 25, 10);

-- @block
-- Inserting data into Recipes table
INSERT INTO Recipes (name, description, instructions)
VALUES
    ('Classic BBQ Pork Ribs', 'Slow-cooked pork ribs with a smoky BBQ flavor.', '1. Rub ribs with seasoning mix. 2. Smoke at 225°F for 4-6 hours. 3. Brush with BBQ sauce. 4. Serve hot.'),
    ('Southern Fried Chicken Wings', 'Crispy fried chicken wings seasoned to perfection.', '1. Season wings with spices. 2. Coat in flour mixture. 3. Fry until golden brown. 4. Serve hot with dipping sauce.'),
    ('Texas Style Beef Brisket', 'Tender slow-cooked beef brisket with a savory dry rub.', '1. Rub brisket with dry rub. 2. Smoke at 250°F for 8-10 hours. 3. Slice thinly. 4. Serve with BBQ sauce.'),
    ('Pulled Pork Sandwiches', 'Juicy pulled pork sandwiches with tangy BBQ sauce.', '1. Slow-cook pork shoulder until tender. 2. Shred pork. 3. Mix with BBQ sauce. 4. Serve on buns with coleslaw.'),
    ('Homemade BBQ Sauce', 'A tangy and sweet homemade BBQ sauce perfect for ribs and chicken.', '1. Combine ketchup, vinegar, brown sugar, and spices. 2. Simmer until thickened. 3. Let cool. 4. Use as desired.'),
    ('Creamy Potato Salad', 'Classic potato salad with a creamy mayo dressing.', '1. Boil potatoes until tender. 2. Chop potatoes and mix with mayo, mustard, and seasonings. 3. Chill before serving.'),
    ('Southern Cornbread', 'Moist and crumbly cornbread with a touch of sweetness.', '1. Mix cornmeal, flour, sugar, and baking powder. 2. Add eggs, milk, and melted butter. 3. Bake at 375°F until golden brown.'),
    ('Classic Cole Slaw', 'Crunchy coleslaw with a tangy vinegar-based dressing.', '1. Shred cabbage, carrots, and onions. 2. Mix with vinegar, mayo, sugar, and seasonings. 3. Chill before serving.');

-- Inserting data into RecipeItems table
INSERT INTO RecipeItems (recipe_id, item_id, quantity, unit)
VALUES
    (1, 1, 10, 'lbs'),   -- Classic BBQ Pork Ribs: Pork Ribs
    (1, 5, 2, 'cups'),   -- Classic BBQ Pork Ribs: BBQ Sauce
    (2, 2, 15, 'lbs'),   -- Southern Fried Chicken Wings: Chicken Wings
    (2, 7, 4, 'cups'),   -- Southern Fried Chicken Wings: Cornbread
    (3, 3, 20, 'lbs'),   -- Texas Style Beef Brisket: Beef Brisket
    (3, 5, 3, 'cups'),   -- Texas Style Beef Brisket: BBQ Sauce
    (4, 4, 15, 'lbs'),   -- Pulled Pork Sandwiches: Pulled Pork
    (4, 5, 2, 'cups'),   -- Pulled Pork Sandwiches: BBQ Sauce
    (5, 6, 4, 'cups'),   -- Homemade BBQ Sauce: Potato Salad
    (5, 3, 5, 'cups'),   -- Homemade BBQ Sauce: Beef Brisket
    (6, 6, 10, 'lbs'),   -- Creamy Potato Salad: Potato Salad
    (7, 8, 5, 'cups'),   -- Southern Cornbread: Cole Slaw
    (7, 5, 2, 'cups');   -- Southern Cornbread: BBQ Sauce

-- @block
Select * FROM Items;

-- @block 
SELECT * FROM Recipes;

-- @block
-- Select all Items in a recipe
SELECT Items.name, RecipeItems.quantity, RecipeItems.unit
FROM Recipes
JOIN RecipeItems ON Recipes.recipe_id = RecipeItems.recipe_id
JOIN Items ON RecipeItems.item_id = Items.item_id
WHERE Recipes.name = 'Classic BBQ Pork Ribs';