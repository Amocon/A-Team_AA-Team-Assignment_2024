# [AA] Team Assignment 2024/25

**Analytics and Applications M.Sc. Course**  
Faculty of Management, Economics, and Social Sciences  
Department of Information Systems for Sustainable Society  
University of Cologne  
**Date:** October 30, 2024  
**Instructor:** Prof. Dr. Wolfgang Ketter  
**Term:** WS 2025/25  
**TA:** Janik Muires  
**Website:** [www.is3.uni-koeln.de](http://www.is3.uni-koeln.de) and ILIAS

---

This team assignment is designed to test a representative cross-section of the data analytics and machine learning approaches covered during the course. It is based on a real-world problem focused on electric vehicles (EV), with high relevance to current societal and business challenges.

All relevant data can be downloaded from Sciebo: [Sciebo Data Link](https://uni-koeln.sciebo.de/s/59LhTdJ9c8tYgmn)

---

## 1. Introduction

Transport-related greenhouse gas emissions are the second-largest contributor to total EU emissions. Shifting from internal combustion engine (ICE) vehicles to electric vehicles (EV) is essential for meeting decarbonization goals, though it presents challenges in infrastructure and user adaptation.

For operators of EV charging hubs, understanding and predicting utilization is crucial to efficiently manage the charging sessions of connected EVs. In this project, your team will take the role of data scientists working for a charging hub operator. Your work will follow the Cross Industry Standard Process for Data Mining (CRISP-DM) methodology and focus on two main objectives:

1. **Understanding System Metrics:** Develop a comprehensive view of the charging hubs' key metrics and present them to management in an accessible format.
2. **Prediction of Utilization:** Create predictive models to forecast utilization, enabling better planning and potential new business models.

---

## 2. Description of Dataset

You have been provided with data on individual EV charging sessions at two charging sites (one public and one private). Each site has approximately 50 EV charging stations. The dataset includes session data and hourly weather data from a nearby airport. You may also use additional data sources.

### Dataset Fields
| Field                | Type         | Description |
|----------------------|--------------|-------------|
| `id`                 | string       | Unique session identifier |
| `connectionTime`     | datetime (UTC) | Time when the EV plugged in |
| `disconnectTime`     | datetime (UTC) | Time when the EV unplugged |
| `doneChargingTime`   | datetime (UTC) | Time of last recorded current draw |
| `kWhDelivered`       | float        | Energy delivered in the session |
| `sessionID`          | string       | Unique session identifier |
| `siteID`             | string       | Unique site identifier |
| `spaceID`            | string       | Unique parking space identifier |
| `stationID`          | string       | Unique EVSE identifier |
| `timezone`           | string       | Site timezone in pytz format |
| `userID`             | string       | Unique user identifier, if available |
| `userInputs`         | list         | List of inputs by the user over time |
| `WhPerMile`          | float        | EV efficiency in Wh per mile |
| `kWhRequested`       | float        | User-requested energy in kWh |
| `milesRequested`     | float        | User-requested distance in miles |
| `minutesAvailable`   | float        | Estimated session length by user |
| `modifiedAt`         | datetime (UTC) | Time when input was modified |
| `paymentRequired`    | bool         | If payment was required |
| `requestedDeparture` | datetime (UTC) | User-estimated departure time |

---

## 3. Task Description

1. **Data Collection and Preparation:**
    - Import and clean the dataset, identifying and addressing any missing or erroneous data. Describe your process briefly.

2. **Descriptive Analytics:**
    - **Temporal Patterns and Seasonality:** Analyze variations in charging events by time of day, week, and season. Identify and explain any patterns.
    - **Key Performance Indicators (KPIs):** Define and calculate three KPIs relevant to hub utilization and business performance, including rationale for each KPI.
    - **Site Characteristics:** Based on descriptive analytics, deduce which site is public. Explain the reasoning behind your conclusion.

3. **Cluster Analysis:**
    - Perform a cluster analysis to categorize typical charging sessions. Balance explainability and information content and name the clusters. Discuss the benefits of categorizing session types.

4. **Utilization Prediction:**
    - Develop two predictive models (one using neural networks and another method) to forecast hourly utilization. Use cross-validation and compare model performance, recommending an approach.
    - Suggest a business case for utilizing utilization predictions, including limitations and potential risks.

---

## 4. Deliverables

Adhere to Section 2 in the Syllabus for detailed deliverable requirements. Use version-control systems like GitHub for milestone tracking and final submission (please invite Janik Muires at muires@wiso.uni-koeln.de if using a private repository). Final report submission will be through ILIAS.

**Note:** Failure to provide milestone progress will result in failure of the team assignment portion of the portfolio exam, which leads to failing the course.