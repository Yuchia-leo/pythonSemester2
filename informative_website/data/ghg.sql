CREATE TABLE drought  (
  category INT PRIMARY KEY,
  netherlands_x  DATE NOT NULL,
  netherlands_y  FLOAT NOT NULL
);

CREATE TABLE emission (
  category DATE PRIMARY KEY,
  Total_emissions_excluding_LULUCF FLOAT NOT NULL,
  LULUCF FLOAT NOT NULL,
  Total_emissions_including_LULUCF FLOAT NOT NULL
);

CREATE TABLE emissionpp (
  category DATE PRIMARY KEY,
  netherlands FLOAT NOT NULL
);

CREATE TABLE extremeprecipitation (
  category INT PRIMARY KEY,
  less_than_1_week_x DATE NOT NULL,
  less_than_1_week_y FLOAT NOT NULL,
  from_1_to_2_weeks_x DATE NOT NULL,
  from_1_to_2_weeks_y INT NOT NULL,
  over_2_weeks_x DATE NOT NULL,
  over_2_weeks_y INT NOT NULL
);

CREATE TABLE policy (
  category DATE PRIMARY KEY,
  Number_of_policies_adopted INT NOT NULL,
  Number_of_measured_policies_in_CAPMF_2023 INT NOT NULL
);

CREATE TABLE precipitation (
  category DATE PRIMARY KEY,
  netherlands FLOAT NOT NULL
);

CREATE TABLE temperature(
  category DATE PRIMARY KEY,
  OECD_Total FLOAT NOT NULL
);

CREATE TABLE dutchghg (
    category INTEGER PRIMARY KEY,
    emission FLOAT NOT NULL,
    emission_pp FLOAT NOT NULL,
    precipitation FLOAT NOT NULL,
    extreme_precipitation FLOAT NOT NULL,
    drought FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    policy INT NOT NULL,

    FOREIGN KEY(emission) REFERENCES emission(Total_emissions_including_LULUCF),
    FOREIGN KEY(emission_pp) REFERENCES emissionpp(netherlands),
    FOREIGN KEY(precipitation) REFERENCES precipitation(netherlands),
    FOREIGN KEY(extreme_precipitation) REFERENCES extremeprecipitation(less_than_1_week_y),
    FOREIGN KEY(drought) REFERENCES drought(netherlands_y),
    FOREIGN KEY(temperature) REFERENCES temperature(OECD_Total),
    FOREIGN KEY(policy) REFERENCES policy(Number_of_policies_adopted) 
);

.mode csv
.import /Users/yuchia/Library/CloudStorage/OneDrive-UvA/individual_assignment_sm2/informative_website/data/dutch_drought.csv drought
.import /Users/yuchia/Library/CloudStorage/OneDrive-UvA/individual_assignment_sm2/informative_website/data/dutch_emission.csv emission
.import /Users/yuchia/Library/CloudStorage/OneDrive-UvA/individual_assignment_sm2/informative_website/data/dutch_emissionpp.csv emissionpp
.import /Users/yuchia/Library/CloudStorage/OneDrive-UvA/individual_assignment_sm2/informative_website/data/dutch_policy.csv policy
.import /Users/yuchia/Library/CloudStorage/OneDrive-UvA/individual_assignment_sm2/informative_website/data/dutch_precipitation.csv precipitation
.import /Users/yuchia/Library/CloudStorage/OneDrive-UvA/individual_assignment_sm2/informative_website/data/dutch_extreprecipitation.csv extremeprecipitation
.import /Users/yuchia/Library/CloudStorage/OneDrive-UvA/individual_assignment_sm2/informative_website/data/dutch_temperature.csv temperature

DELETE FROM drought WHERE category < 2000 OR category = 2022;
DELETE FROM extremeprecipitation WHERE category = 2022;
DELETE FROM emissionpp WHERE DATE(category) < '1999-01-01 00:00:00' OR DATE(category) > '2021-01-01 00:00:00';
DELETE FROM emission WHERE DATE(category) < '1999-01-01 00:00:00';
DELETE FROM policy WHERE DATE(category) < '1999-01-01 00:00:00' OR DATE(category) > '2021-01-01 00:00:00';
DELETE FROM precipitation WHERE DATE(category) < '1999-01-01 00:00:00' OR DATE(category) > '2021-01-01 00:00:00';
DELETE FROM temperature WHERE DATE(category) < '1999-01-01 00:00:00' OR DATE(category) > '2021-01-01 00:00:00';

INSERT INTO dutchghg (category,emission,emission_pp,precipitation,extreme_precipitation,drought,temperature,policy)
SELECT drought.category,emission.Total_emissions_including_LULUCF,emissionpp.netherlands,precipitation.netherlands,extremeprecipitation.less_than_1_week_y,drought.netherlands_y,temperature.OECD_Total,policy.Number_of_policies_adopted
FROM drought,emission,emissionpp,precipitation,extremeprecipitation,temperature,policy
WHERE drought.netherlands_x=emission.category AND drought.netherlands_x=emissionpp.category AND drought.netherlands_x=precipitation.category AND drought.netherlands_x=extremeprecipitation.less_than_1_week_x AND drought.netherlands_x=temperature.category AND drought.netherlands_x=policy.category;