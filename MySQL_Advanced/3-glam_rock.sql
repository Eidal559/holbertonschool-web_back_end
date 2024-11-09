-- Task 3: Old school bandlists - all bands with Glam as their main style
-- SQL script that lists all bands with Glam rock as their main style, ranked by their longevity

SELECT band_name, COALESCE(split, 2020) - formed as lifespan FROM metal_bands
WHERE style LIKE '%Glam rock%' ;
