CREATE TABLE flowers (
    id_flower SERIAL PRIMARY KEY,
    common_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255) NOT NULL,
    family VARCHAR(255) NOT NULL,
    plant_type VARCHAR(50) NOT NULL,
    blooming_period VARCHAR(255) NOT NULL,
    colors VARCHAR(255) NOT NULL,
    pollinators VARCHAR(255) NOT NULL,
    possessed BOOLEAN NOT NULL DEFAULT FALSE, -- Default value set to FALSE
    CONSTRAINT chk_plant_type CHECK (plant_type IN ('annual', 'biennial', 'perennial'))
);
-- Insert multiple entries into the flowers table
INSERT INTO flowers (common_name, scientific_name, family, plant_type, blooming_period, colors, pollinators, possessed) VALUES
('Sunflower', 'Helianthus annuus', 'Asteraceae', 'annual', 'Summer', 'Yellow', 'Bees, Birds', TRUE),
('Rose', 'Rosa', 'Rosaceae', 'perennial', 'Spring-Summer', 'Red, Pink, White, Yellow', 'Bees',FALSE),
('Lavender', 'Lavandula', 'Lamiaceae', 'perennial', 'Summer', 'Purple', 'Bees, Butterflies',FALSE),
('Tulip', 'Tulipa', 'Liliaceae', 'perennial', 'Spring', 'Red, Yellow, Pink, White', 'Bees',FALSE),
('Daisy', 'Bellis perennis', 'Asteraceae', 'perennial', 'Spring', 'White, Pink', 'Bees, Butterflies',FALSE),
('Peony', 'Paeonia', 'Paeoniaceae', 'perennial', 'Spring', 'Pink, Red, White', 'Bees',FALSE),
('Marigold', 'Tagetes', 'Asteraceae', 'annual', 'Summer-Fall', 'Yellow, Orange', 'Bees, Butterflies',FALSE),
('Daffodil', 'Narcissus', 'Amaryllidaceae', 'perennial', 'Spring', 'Yellow, White', 'Bees',FALSE),
('Snapdragon', 'Antirrhinum', 'Plantaginaceae', 'annual', 'Spring-Fall', 'Pink, Red, Yellow, White', 'Bees',FALSE),
('Aster', 'Aster', 'Asteraceae', 'perennial', 'Summer-Fall', 'Purple, Blue, White', 'Bees, Butterflies',TRUE),
('Forget-me-not', 'Myosotis', 'Boraginaceae', 'perennial', 'Spring', 'Blue, Pink, White', 'Bees',FALSE),
('Lily of the Valley', 'Convallaria majalis', 'Asparagaceae', 'perennial', 'Spring', 'White', 'Bees',FALSE),
('Hibiscus', 'Hibiscus', 'Malvaceae', 'perennial', 'Summer-Fall', 'Red, Pink, Orange, Yellow', 'Hummingbirds, Bees',FALSE),
('Zinnia', 'Zinnia elegans', 'Asteraceae', 'annual', 'Summer-Fall', 'Red, Pink, Yellow, Orange, White', 'Butterflies, Hummingbirds, Bees',FALSE),
('Bluebell', 'Hyacinthoides non-scripta', 'Asparagaceae', 'perennial', 'Spring', 'Blue', 'Bees',FALSE),
('Foxglove', 'Digitalis', 'Plantaginaceae', 'biennial', 'Summer', 'Pink, Purple, White', 'Bees',FALSE),
('Cosmos', 'Cosmos', 'Asteraceae', 'annual', 'Summer-Fall', 'Pink, White, Red', 'Bees, Butterflies',FALSE),
('Iris', 'Iris', 'Iridaceae', 'perennial', 'Spring-Summer', 'Blue, Purple, White, Yellow', 'Bees',FALSE),
('Poppy', 'Papaver', 'Papaveraceae', 'annual', 'Spring-Summer', 'Red, Orange, Yellow, White', 'Bees', TRUE),
('Chrysanthemum', 'Chrysanthemum', 'Asteraceae', 'perennial', 'Fall', 'Pink, Yellow, White', 'Bees',FALSE),
('Violet', 'Viola', 'Violaceae', 'perennial', 'Spring', 'Purple, Blue, Yellow, White', 'Bees',FALSE),
('Magnolia', 'Magnolia', 'Magnoliaceae', 'perennial', 'Spring', 'White, Pink', 'Beetles',FALSE),
('Geranium', 'Geranium', 'Geraniaceae', 'perennial', 'Spring-Summer', 'Pink, Red, White, Blue', 'Bees',FALSE),
('Begonia', 'Begonia', 'Begoniaceae', 'perennial', 'Summer', 'Pink, Red, White', 'Bees',FALSE),
('Camellia', 'Camellia', 'Theaceae', 'perennial', 'Winter-Spring', 'Pink, Red, White', 'Bees',FALSE),
('Carnation', 'Dianthus caryophyllus', 'Caryophyllaceae', 'perennial', 'Spring-Summer', 'Pink, Red, White, Yellow', 'Bees',FALSE),
('Gardenia', 'Gardenia jasminoides', 'Rubiaceae', 'perennial', 'Spring-Summer', 'White', 'Bees', TRUE),
('Sweet Pea', 'Lathyrus odoratus', 'Fabaceae', 'annual', 'Spring-Summer', 'Pink, Purple, White, Red', 'Bees',FALSE),
('Morning Glory', 'Ipomoea', 'Convolvulaceae', 'annual', 'Summer-Fall', 'Blue, Purple, Pink, White', 'Bees, Hummingbirds',FALSE),
('Dahlia', 'Dahlia', 'Asteraceae', 'perennial', 'Summer-Fall', 'Pink, Purple, Red, White, Yellow', 'Bees, Butterflies',FALSE),
('Rhododendron', 'Rhododendron', 'Ericaceae', 'perennial', 'Spring', 'Pink, Purple, Red, White', 'Bees',FALSE),
('Petunia', 'Petunia × atkinsiana', 'Solanaceae', 'annual', 'Spring-Fall', 'Purple, Pink, Red, White, Yellow', 'Hummingbirds, Bees',FALSE),
('Heather', 'Calluna vulgaris', 'Ericaceae', 'perennial', 'Late Summer-Fall', 'Pink, Purple, White', 'Bees',FALSE),
('Anemone', 'Anemone', 'Ranunculaceae', 'perennial', 'Spring-Fall', 'Pink, Purple, Red, White', 'Bees',FALSE),
('Hydrangea', 'Hydrangea', 'Hydrangeaceae', 'perennial', 'Summer-Fall', 'Blue, Pink, Purple, White', 'Bees',FALSE),
('Black-eyed Susan', 'Rudbeckia hirta', 'Asteraceae', 'perennial', 'Summer-Fall', 'Yellow, Orange, Brown', 'Butterflies, Bees',FALSE),
('Coneflower', 'Echinacea purpurea', 'Asteraceae', 'perennial', 'Summer-Fall', 'Pink, Purple', 'Bees, Butterflies',FALSE),
('Bleeding Heart', 'Lamprocapnos spectabilis', 'Papaveraceae', 'perennial', 'Spring', 'Pink, White', 'Bees',FALSE),
('Lupine', 'Lupinus', 'Fabaceae', 'perennial', 'Spring-Summer', 'Blue, Purple, Pink, White', 'Bees, Butterflies', TRUE),
('Jasmine', 'Jasminum', 'Oleaceae', 'perennial', 'Spring-Summer', 'White, Yellow', 'Bees',FALSE),
('Primrose', 'Primula', 'Primulaceae', 'perennial', 'Winter-Spring', 'Yellow, Pink, Purple, Blue, Red, White', 'Bees',FALSE),
('Lavatera', 'Lavatera', 'Malvaceae', 'perennial', 'Summer-Fall', 'Pink, White', 'Bees, Butterflies',FALSE),
('Bellflower', 'Campanula', 'Campanulaceae', 'perennial', 'Summer', 'Blue, Purple, White', 'Bees, Hummingbirds',FALSE),
('Gazania', 'Gazania', 'Asteraceae', 'perennial', 'Summer', 'Yellow, Orange, Red, Pink', 'Bees',FALSE),
('Foxglove Beardtongue', 'Penstemon digitalis', 'Plantaginaceae', 'perennial', 'Spring-Early Summer', 'White', 'Bees',FALSE),
('Globe Thistle', 'Echinops', 'Asteraceae', 'perennial', 'Summer-Fall', 'Blue', 'Bees, Butterflies',FALSE),
('African Daisy', 'Osteospermum', 'Asteraceae', 'perennial', 'Spring-Fall', 'Purple, Blue, Pink, Yellow, White', 'Bees, Butterflies',FALSE),
('Monkshood', 'Aconitum', 'Ranunculaceae', 'perennial', 'Summer-Fall', 'Blue, Purple', 'Bees',FALSE),
('Coral Bells', 'Heuchera', 'Saxifragaceae', 'perennial', 'Spring-Summer', 'Red, Pink, White', 'Hummingbirds, Bees',FALSE),
('Bee Balm', 'Monarda', 'Lamiaceae', 'perennial', 'Summer', 'Red, Pink, Purple, White', 'Bees, Hummingbirds, Butterflies', TRUE),
('Pasque Flower', 'Pulsatilla vulgaris', 'Ranunculaceae', 'perennial', 'Spring', 'Purple, Blue, Red, White', 'Bees',FALSE),
('Speedwell', 'Veronica', 'Plantaginaceae', 'perennial', 'Spring-Summer', 'Blue, Purple, White', 'Bees, Butterflies',FALSE),
('Yarrow', 'Achillea millefolium', 'Asteraceae', 'perennial', 'Summer', 'White, Yellow, Pink, Red', 'Bees, Butterflies',FALSE),
('Hellebore', 'Helleborus', 'Ranunculaceae', 'perennial', 'Winter-Spring', 'Purple, Green, White, Pink', 'Bees',FALSE),
('Sedum', 'Sedum', 'Crassulaceae', 'perennial', 'Summer-Fall', 'Pink, Yellow, Red', 'Bees, Butterflies',FALSE),
('Columbine', 'Aquilegia', 'Ranunculaceae', 'perennial', 'Spring', 'Blue, Purple, Red, Yellow, White', 'Hummingbirds, Bees',FALSE),
('Statice', 'Limonium', 'Plumbaginaceae', 'perennial', 'Summer', 'Purple, Blue, Yellow, Pink', 'Bees',FALSE),
('Nasturtium', 'Tropaeolum majus', 'Tropaeolaceae', 'annual', 'Summer-Fall', 'Orange, Yellow, Red', 'Bees',FALSE),
('Snapdragon', 'Antirrhinum majus', 'Plantaginaceae', 'annual', 'Spring-Fall', 'Pink, Red, Yellow, White', 'Bees', TRUE),
('Coreopsis', 'Coreopsis', 'Asteraceae', 'perennial', 'Summer-Fall', 'Yellow, Gold', 'Bees, Butterflies',FALSE),
('Allium', 'Allium', 'Amaryllidaceae', 'perennial', 'Spring-Summer', 'Purple, White', 'Bees, Butterflies',FALSE);

CREATE TABLE measures (
    id_measure SERIAL PRIMARY KEY,
    id_flower INT,
    measure_date TIMESTAMP NOT NULL,
    temperature INT,
    humidity INT,
    FOREIGN KEY (id_flower) REFERENCES flowers(id_flower) -- Establishing the foreign key relationship
);

INSERT INTO measures (id_flower, measure_date, temperature, humidity) VALUES
(10, '2024-04-10', 22, 45),
(10, '2024-04-11', 24, 40),

(1, '2024-04-09', 30, 55),
(1, '2024-04-10', 28, 60),
(1, NOW(), 29, 53),
(1, NOW(), 21, 50),

(50, '2024-04-08', 18, 65),
(50, '2024-04-09', 20, 62),
(50, NOW(), 19, 68),

(19, '2024-04-07', 25, 70),
(19, '2024-04-08', 26, 65),
(19, NOW(), 24, 75),

(59, '2024-04-06', 17, 80),

(39, '2024-04-05', 23, 85),
(39, '2024-04-06', 21, 88),
(39, NOW(), 22, 84),

(27, '2024-04-04', 29, 90),
(27, '2024-04-05', 31, 85),
(27, NOW(), 28, 92);



