<!DOCTYPE html>
<html>
<head>
    <title>Wordle</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <style>
        .grid-cell {
            width: 30px;
            height: 30px;
            text-align: center;
            padding: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Wordle</h1>
        <p>Guess the five-letter word.</p>

        {% if message %}
            <div class="alert alert-danger">
                {{ message }}
            </div>
        {% endif %}

        <form method="POST" action="/">
            <div class="form-group">
                <label for="guess">Enter your guess:</label>
                <input type="text" class="form-control" id="guess" name="guess" maxlength="5" required>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</body>
</html>