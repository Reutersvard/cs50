SELECT title
FROM (SELECT title, rating FROM (SELECT id, title FROM movies WHERE id IN (SELECT movie_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = "Chadwick Boseman"))) JOIN ratings ON id = ratings.movie_id)
ORDER BY rating DESC
LIMIT 5;