# OneStepAhead
Repository for the 1StepAhead Team that started working in the CodeVsCovid19 Hackathon

## Intro

We are a group of passionate creatives and coders who want to help fighting the spread and the consquences of the Spread of the novel Coronavvirus, causing COVID-19.

### Problem description

Many problems arise with COVID-19 and the battle against it. Since there is no Vaccination available, all that can be done are Non-Pharmaceutical Interventions. By the time there is Data available how successfull these Interventions were in managing the spread of Covid19. 
The situation is changing rapidly, so one might not have the time to wait for new scientific paper to be published, just including the newest data.


### Solution description

We develop a Website, which gives stakeholders and interested people the possibility to create regression models for the initial growth rate of the spread in a given country. Also one can use a given Prediction model and play around with the input factors to see which Variables influence the spread in what manner.

Also we provide an event history regression model on the Timing and Type of Interventions. To use this tool might help getting a better understanding of the possibilities to control the spread.

The Data we use is always up to date, so all calculations and predictions are getting more accurate over time.

We plan to improve our Website, so it can be modified for future pandemics and other diseases as well.

#### what is new about this approach?

We can 
+ predict the number of cases from general country Data e.g. GDP, quality of Healthcare system
but also
+ explain how effective governmental measures taken are and provide a tool on planning those

### Data Sources

+ Data Repository by Johns Hopkins
...https://github.com/CSSEGISandData/COVID-19
+ Prosperity Index
+ Human Development Report


### Solution Architecture

We use a python backend with a Data Pipeline, providing our Model with the newest data available. This is Integrated into a Flask-Application. Front End is Programmed in Javascript.
