var express = require('express');
var bodyParser = require('body-parser');
var mysql = require('mysql2');
var path = require('path');
const multer = require('multer');
const upload = multer();

//connect database
var connection = mysql.createConnection({
    host: '34.42.226.55',
    user: 'root',
    password: 'razenly64',
    database: 'cs411db'
});
connection.connect(function(err) {
    if (err) {
        console.error('error with connection: ' + err.stack);
        return;
    }
    console.log(' connected ' + connection.threadId);
});

//create express app and set up ejs view engine
var app = express();
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(__dirname + '../public'));

// GET home page, respond by rendering index.ejs 
app.get('/', function(req, res) {
    res.render('index', { title: 'Game Data Management' });
});

//the following are CRUD operations
//create
app.post('/game_data', upload.none(), function(req, res) {
    var sql = 'INSERT INTO game_data (QueryID, ResponseID, GameName, ResponseName, ReleaseDate, Recommendation, Price, SupportURL, AboutText, HeaderImage, PlatformID, CategoryID, GenreID, Players) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)';
    var values = [
        req.body.QueryID, req.body.ResponseID, req.body.GameName,req.body.ResponseName, req.body.ReleaseDate, req.body.Recommendation,req.body.Price, 
        req.body.SupportURL, req.body.AboutText,req.body.HeaderImage, req.body.PlatformID, req.body.CategoryID, req.body.GenreID, req.body.Players
    ];
    connection.query(sql, values, function(err, result) {
        if (err) {
            console.error('error in adding gmae: ' + err);
            return;
        }
        res.json({ message: 'Game added successfully' });
    });
});

//read
app.get('/games', function(req, res) {
    var sql = 'SELECT * FROM game_data';
    connection.query(sql, function(err, results) {
        if (err) {
            console.error('Server error: ' + err);
            return;
        }
        let html = `<table border="1"><tr>`;
        for (let column in results[0]) {
            html += `<th>${column}</th>`;
        }
        html += `</tr>`;
        for (let row of results) {
            html += `<tr>`;
            for (let column in row) {
                html += `<td>${row[column]}</td>`;
            }
            html += `</tr>`;
        }
        html += `</table>`;
        res.send(html);
    });
});

//read by ID
app.get('/search-game', function(req, res) {
    var queryID = req.query.QueryID;
    var sql = 'SELECT * FROM game_data WHERE QueryID = ?';
    connection.query(sql, [queryID], function(err, results) {
        if (err) {
            console.error('Server error: ' + err);
            return;
        }
        if (results.length === 0) {
            res.send('<p>No game found with this QueryID</p>');
            return;
        }
        let html = '<table border="1"><tr>';
        for (let column in results[0]) html += `<th>${column}</th>`;
        html += '</tr>';
        results.forEach(row => {
            html += '<tr>';
            for (let column in row) html += `<td>${row[column]}</td>`;
            html += '</tr>';
        });
        html += '</table>';
        res.send(html);
    });
});

//update
app.post('/update-game/:queryID', upload.none(), function(req, res) {
    const queryID = req.params.queryID;
    const updateData = req.body;
    let updates = [];
    let values = [];
    let sql = 'UPDATE game_data SET ';
    for (let key in updateData) {
        if (updateData[key] && key !== 'QueryID') {
            updates.push(`${key} = ?`);
            values.push(updateData[key]);
        }
    }
    sql += updates.join(', ');
    sql += ' WHERE QueryID = ?';
    values.push(queryID);
    connection.query(sql, values, function(err, result) {
        if (err) {
            console.error('Error updating game: ' + err);
            return;
        }
        res.json({ message: 'Game updated successfully' });
    });
});

//delete
app.post('/delete-game', function(req, res) {
    var gameId = req.body.QueryID;
    var sql = 'DELETE FROM game_data WHERE QueryID = ?'; 
    connection.query(sql, [gameId], function(err, result) {
        if (err) {
            console.error('error: ' + err);
            return;
        }
        if (result.affectedRows === 0) {
            res.json({ message: 'No game found with the provided ID' });
        } else {
            res.json({ message: 'Game deleted successfully' });
        }
    });
});

//the following are search operations
//search by name
app.get('/search-game-by-name', function(req, res) {
    var nameKeyword = req.query.name;
    var sql = 'SELECT * FROM game_data WHERE GameName LIKE ?';
    var values = [`%${nameKeyword}%`];
    connection.query(sql, values, function(err, results) {
        if (err) {
            console.error('Server error: ' + err);
            return;
        }
        if (results.length === 0) {
            res.send('<p>No game found with the provided name keyword</p>');
            return;
        }
        let html = '<table border="1"><tr>';
        for (let column in results[0]) {
            html += `<th>${column}</th>`;
        }
        html += '</tr>';
        results.forEach(row => {
            html += '<tr>';
            for (let column in row) {
                html += `<td>${row[column]}</td>`;
            }
            html += '</tr>';
        });
        html += '</table>';
        res.send(html);
    });
});

//the following are advanced operations
app.post('/like-game', function(req, res) {
    var queryID = req.query.QueryID;
    var sql = 'UPDATE game_data SET Recommendation = Recommendation + 1 WHERE QueryID = ?';
    connection.query(sql, [queryID], function(err, result) {
        if (err) {
            res.status(500).json({ message: 'Error liking the game' });
            return;
        }
        if (result.affectedRows === 0) {
            res.json({ message: 'No game found with the provided QueryID' });
        } else {
            res.json({ message: 'Game liked successfully' });
        }
    });
});

//the following are for extra credit
app.get('/top-games-by-genre', function(req, res) {
    var genreID = req.query.GenreID;
    var sql = `
        SELECT GameName, Recommendation 
        FROM game_data 
        WHERE GenreID = ? 
        ORDER BY Recommendation DESC 
        LIMIT 10
    `;
    connection.query(sql, [genreID], function(err, results) {
        if (err) {
            console.error('Server error: ' + err);
            return;
        }
        res.json(results); 
    });
});

app.get('/top-games-by-price', function(req, res) {
    var price = req.query.Price;
    var sql = `
        SELECT GameName, Recommendation 
        FROM game_data 
        WHERE Price <= ? 
        ORDER BY Recommendation DESC 
        LIMIT 10
    `;
    connection.query(sql, [price], function(err, results) {
        if (err) {
            console.error('Server error: ' + err);
            return;
        }
        res.json(results);
    });
});

app.post('/assign-game-ratings', function(req, res) {
    connection.query('CALL AssignGameRatings()', function(err, result) {
        if (err) {
            console.error('Server error: ' + err);
            return;
        }
        connection.query('SELECT * FROM Ranking', function(err, rankings) {
            if (err) {
                console.error('Server error: ' + err);
                return;
            }
            res.json(rankings);
        });
    });
});


//start server
app.listen(80, function () {
    console.log('Node app is running on port 80');
});

