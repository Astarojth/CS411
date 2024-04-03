The following are our desciption of stage4:

1. We fixed some issues that existed in stage3
The main issues we had in stage3 were a mismatch between the ER diagram and the actual situation and forgetting to document the DDL for creating the game_data table. re-uploading the documentation for stage2 and stage3, we fixed these issues. The new documentation has a "new" suffix.

2. We completed the front-end interface with front-end and database connectivity functionality
Following workshop3's instruction, we completed writing nodejs, js, and html code on gcp to design a clean interface that smoothly interacts with the database and accomplishes the functions we designed.

3. Introduction to the functions of our website
Our website is designed as a database of games built by players. Players can add games, recommend games, search for games, and much more. Our advanced database operations and creative features are all related to better game recommendations for players.

4. Advanced SQL
For our database system we included a stored procedure + trigger. The function of the stored procedure is to calculate the recommendation score based on their prices and users' preferences and assign ratings (A, B, C) for each entries based on their rankings in the table. The trigger checks whether the user set their account name the same as their password. If so, the trigger will attach their ID behind their account name to avoid possible privacy leak. 

5. Creative Function
With our creative function, we can filter the eligible games by the game type code or the highest price of the game entered by the player, and sort them according to the number of recommendations from high to low, and finally, the top 10 games with the highest number of recommendations are very graphically represented in a bar chart. We think this can be more intuitive to help players choose games that meet their requirements.


Appendix

Here is the IP of our website: 35.208.47.156

The code of our stage4 is in the "code" dir and the nodejs part is server.js, while html and javascript part is in the ./views/index.ejs.

The code of the advanced SQL part is following:
DELIMITER $$

CREATE PROCEDURE AssignGameRatings()
BEGIN

DECLARE done INT DEFAULT FALSE;
DECLARE vQueryID INT;
DECLARE vGameName VARCHAR(255);
DECLARE vRecommend DECIMAL(10,2);
DECLARE totalGames INT;
DECLARE counter INT DEFAULT 0;
DECLARE rating CHAR(1);

DECLARE game_cursor CURSOR FOR
(SELECT
gd.QueryID,
gd.GameName,
(gd.Recommendation + COUNT(ugp.QueryID)) / (gd.Price + 1) AS Recommend
FROM
game_data gd
LEFT JOIN UserGamePreference ugp ON gd.QueryID = ugp.QueryID
GROUP BY
gd.QueryID, gd.GameName
HAVING
Recommend != 0)
INTERSECT
(SELECT
gd.QueryID,
gd.GameName,
(gd.Recommendation + COUNT(ugp.QueryID)) / (gd.Price + 1) AS Recommend
FROM
game_data gd
LEFT JOIN UserGamePreference ugp ON gd.QueryID = ugp.QueryID
WHERE ReleaseDate <= CURDATE()
GROUP BY
gd.QueryID, gd.GameName)
ORDER BY
Recommend DESC;

DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

SELECT COUNT(*) INTO totalGames
FROM game_data gd
WHERE gd.QueryID IN (
SELECT gd_inner.QueryID
FROM game_data gd_inner
LEFT JOIN (
SELECT QueryID, COUNT(QueryID) as QueryCount
FROM UserGamePreference
GROUP BY QueryID
) ugp ON gd_inner.QueryID = ugp.QueryID
WHERE gd_inner.Recommendation + COALESCE(ugp.QueryCount, 0) != 0
GROUP BY gd_inner.QueryID
UNION
SELECT QueryID
FROM game_data
WHERE ReleaseDate > CURDATE()
);


OPEN game_cursor;

TRUNCATE TABLE Ranking;

read_loop: LOOP
FETCH game_cursor INTO vQueryID, vGameName, vRecommend;
IF done THEN
LEAVE read_loop;
END IF;

SET counter = counter + 1;
IF counter <= totalGames * 0.10 THEN
SET rating = 'A';
ELSEIF counter <= totalGames * 0.30 THEN
SET rating = 'B';
ELSE
SET rating = 'C';
END IF;

INSERT INTO Ranking (QueryID, GameName, Recommend, Rating)
VALUES (vQueryID, vGameName, vRecommend, rating)
ON DUPLICATE KEY UPDATE
Recommend = vRecommend,
Rating = rating;
END LOOP;

CLOSE game_cursor;
END$$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER CheckUserAccount BEFORE INSERT ON Users
FOR EACH ROW
BEGIN
IF NEW.UserAccount = NEW.UserPassword AND NEW.UserID NOT BETWEEN 1000 AND 5000 THEN
SET NEW.UserAccount = CONCAT(NEW.UserAccount, '_', NEW.UserID);
END IF;
END$$

DELIMITER ;