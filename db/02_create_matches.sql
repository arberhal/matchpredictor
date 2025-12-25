
CREATE TABLE IF NOT EXISTS matches (
    fixture_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    season INTEGER NOT NULL,
    venue TEXT,

    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,

    home_goals INTEGER,
    away_goals INTEGER
);

