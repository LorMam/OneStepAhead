# OneStepAhead
Repository for the One Step Ahead (working Title) Team of the CodeVsCovid19 Hackathon

![alt text][logo]

[logo]: https://github.com/ChristophAl/OneStepAhead/blob/master/resources/OSA_logo.png "One Step Ahead (working title)"

## Intro

We are a group of passionate createives and coders who want to help fighting the spread and the consquences of the Spread of Sars-Cov-2 better known as Corona virus or under the disease it is causing - COVID-19.

### Problem description

Many problems arise with COVID-19 and the battle against it. We can only address one.
We believe that one huge issue is **uncertainty**. How to deal with uncertainty? By planning. But for what shall we plan?

### Solution description

We do not have a fortune teller sphere but we have the powerfull tools of **Machine-** and **Deep Learning**.
So we gonne face this problem with **prediction**. 

#### what is new about this approach?

Yes, nothing to special here. Anyway, we see another huge problem ahead of us. The Spread of the virus in **developing countries** and **refugees camps**. Where we see only few cases today. So just applying *time-series forecasting* is not good enough here. We want to add more features to the model. This way we can not only
+ predict the number of cases
but also
+ explain how effective activities taken are
We will accomplish this by *explaining the model*. Some models are explainable by default (like regression or logistic regression). Other models can be explained by special tools like *lime* for example.

### Data

#### Data Sources

+ Data Repository by Johns Hopkins
...https://github.com/CSSEGISandData/COVID-19
+ Wikipedia
+ tbd.

#### Features for prediction

Normally if you are doing time series forecast you need to get your data from a form lik this:

Country | 01.03.2020 | 02.03.2020 | ... | 27.03.2020
Italy | 20 | 35 | ... | 1247
France | 15 | 28 | ... | 968
... | ... | ... | ... 

into a form like this:

Country | sum cases last 14 days | sum cases last 7 days | sum cases next 7 days
Italy | 340 | 538 | ?
France | 290 | 421 | ?
... | ... | ... | ?

we also want to add additional features (features are the explanatory or independet variables) to better predict the label (the variable to explain or dependent variable)

##### additional features to use

+ population of the countries
+ mean age of the population of the countries
+ 'closing of schools since `x` days'
+ 'quarantine since `x` days'
+ sentiment of citizens about the quarantine
+  ...

#### some thoughts about statistics

in time-series we have autocorrelated variables, as 'sum of cases last 7 days' is not independent of 'sum of cases last 14 days'. This is also true for other features (variables) we will add to the data model.
Anyhow in Machine- and Deep Learning contraints that do normally count for hypothesis to be valid are neglected most of the time. (yes. That actaully is something experts of statistics argue a lot.)

### Solution Architecture
