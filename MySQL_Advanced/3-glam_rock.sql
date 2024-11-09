-- List Glam rock bands ranked by their longevity
SELECT band_name,
       IFNULL(split - formed, YEAR(CURDATE()) - formed) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
