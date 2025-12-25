
CREATE TABLE IF NOT EXISTS match_team_stats (
    fixture_id INTEGER NOT NULL,
    team_name TEXT NOT NULL,
    side TEXT CHECK (side IN ('home', 'away')),
    stat_name TEXT NOT NULL,
    stat_value NUMERIC,

    PRIMARY KEY (fixture_id, team_name, side, stat_name),

    CONSTRAINT fk_stats_match
        FOREIGN KEY (fixture_id) REFERENCES matches(fixture_id)
);

