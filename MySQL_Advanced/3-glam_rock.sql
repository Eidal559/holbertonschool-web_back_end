-- Task 3: Old school bandlists - all bands with Glam as their main style
-SELECT
    name AS band_name,
    (split - formed) AS lifespan
FROM
    metal_bands
WHERE
    main_style = 'Glam rock'
ORDER BY
    lifespan DESC;
