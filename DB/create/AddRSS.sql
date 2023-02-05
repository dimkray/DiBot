-- �������: RSS
CREATE TABLE RSS (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    rssUrl TEXT NOT NULL UNIQUE,
    title TEXT,
    subtitle TEXT,
    date TEXT,
    link TEXT,
    author TEXT,
    lang TEXT,
    post TEXT,
    titleU TEXT,
    ubtitleU TEXT
);