-- Only Creates tables if they have not already been created

-- Table for storing display mode
CREATE TABLE IF NOT EXISTS display_mode (
    rowid INTEGER PRIMARY KEY AUTOINCREMENT,
    mode TEXT NOT NULL CHECK (mode IN ('light', 'dark'))
);

-- Table for storing favourite teams
CREATE TABLE IF NOT EXISTS favourite_teams (
    rowid INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id TEXT NOT NULL UNIQUE,
    team_name TEXT NOT NULL UNIQUE
);