---
title: Analysis of Chess Game and Player Data
description: Creating a clean pipline for data analysis of chess games and players from chess data.
author: Yazid Abusultan
---
# GSG PSSAR Advanced Course Session 5
## Data Quality Report

### Chess Games Data 

#### Raw Data 
| Column            |   Non-Null Count | Data Type   |
|:------------------|-----------------:|:------------|
| Unnamed: 0        |            20058 | int64       |
| game_id           |            20058 | int64       |
| rated             |            20058 | bool        |
| turns             |            20058 | int64       |
| victory_status    |            20058 | str         |
| winner            |            20058 | str         |
| time_increment    |            20058 | str         |
| white_id          |            20058 | str         |
| white_rating      |            20058 | int64       |
| black_id          |            20058 | str         |
| black_rating      |            20058 | int64       |
| moves             |            20058 | str         |
| opening_code      |            20058 | str         |
| opening_moves     |            20058 | int64       |
| opening_fullname  |            20058 | str         |
| opening_shortname |            20058 | str         |
| opening_response  |             1207 | str         |
| opening_variation |            14398 | str         |

**Chess games dataframe has 0 duplicated rows out of 20058**

### Cleaned Data 
| Column            |   Non-Null Count | Data Type   |
|:------------------|-----------------:|:------------|
| game_id           |            20058 | int64       |
| rated             |            20058 | bool        |
| turns             |            20058 | int64       |
| victory_status    |            20058 | str         |
| winner            |            20058 | str         |
| time_increment    |            20058 | str         |
| white_id          |            20058 | str         |
| white_rating      |            20058 | int64       |
| black_id          |            20058 | str         |
| black_rating      |            20058 | int64       |
| moves             |            20058 | str         |
| opening_code      |            20058 | str         |
| opening_moves     |            20058 | int64       |
| opening_fullname  |            20058 | str         |
| opening_shortname |            20058 | str         |
| opening_variation |            14398 | str         |
| time_base         |            20058 | int64       |
| time_inc          |            20058 | int64       |
| rating_diff       |            20058 | int64       |
| opening_family    |            20058 | str         |
| is_suspicious     |            20058 | bool        |

#### Important Changes:
* Removed 'Unnamed: 0' since it does not serve a purpose and game_id can be used as an index instead.
* Removed opening_response since it is mostly nulls.
* Splited time_increment into time base and time increment for cleaner time view.
* Added a rating difference column to highlight the difference between the two players of any game.
* Extracted an opening family column to group openings within each family.
* Added is_suspicious column to detect fake games (eg. a player won after 1 turn in the game).

### Analytics Outcomes

Win Rates
| winner   |        0 |
|:---------|---------:|
| Black    | 45.4033  |
| Draw     |  4.73626 |
| White    | 49.8604  |

Most common victory status is Resign 

Games were classed into Short, Medium, Long based on the histogram of turn counts.
 Medium Games are between 30 to 70 turns since the majority of games fall into that range.

### Players Registry Data 

#### Raw Data 
| Column               |   Non-Null Count | Data Type   |
|:---------------------|-----------------:|:------------|
| Unnamed: 0           |              215 | int64       |
| username             |              215 | str         |
| display_name         |              215 | str         |
| country              |              201 | str         |
| registered_year      |              208 | float64     |
| rating_registry      |              215 | int64       |
| total_games_registry |              215 | int64       |
| account_status       |              169 | str         |
| email_verified       |              215 | bool        |
| join_platform        |              215 | str         |

Players registry has 0 duplicated rows

### Merged Data 

**Merged chess games and players registry dataframes.**
| Column               |   Non-Null Count | Data Type   |
|:---------------------|-----------------:|:------------|
| game_id              |             4433 | int64       |
| white_id             |             4433 | str         |
| white_rating         |             4433 | int64       |
| winner               |             4433 | str         |
| Unnamed: 0           |             4433 | int64       |
| display_name         |             4433 | str         |
| country              |             4159 | str         |
| registered_year      |             4290 | float64     |
| rating_registry      |             4433 | int64       |
| total_games_registry |             4433 | int64       |
| account_status       |             3465 | str         |
| email_verified       |             4433 | bool        |
| join_platform        |             4433 | str         |

**There are 200 registered players and 9238 unregistered ones.**

Registered players join from the following countries
* Brazil
* France
* Germany
* India
* Poland
* Russia
* Spain
* Ukraine
* United Kingdom
* United States
