We are aiming to answer 5 remaining rounds with 10 questions each. 
We have a set number of coins which we need to fully utilise each round.
Each question we can bet between 250 and 2500 coins on an answer.
The questions are getting us to estimate a real world future event. 
The range of acceptable answers varies per question, and the returns from it vary too.
Typically though, the returns follow a structure of getting your bet * 2.5 for an answer in the 'bullseye' range, abd your bet * 1.75 for an answer in the 'partial' range.
Any answer outside these ranges will result in losing all coins placed on that bet.
Find each screenshot with the exact details in the week2qs folder of this repository.

We aim to either find reliable models that already predict the value we aim to find, or train our own models by finding good data sources and training a basic machine learning model on it.
The models will also need variance of answers, as we need a likelihood of our given answer falling in each range, bullseye partial or failure. 
The models should return our value as well as these likelihoods.

We then aim to price our bets using a modified kelly criterion, allowing us to apply an x scale factor to each answer, using our likelihoods of each range for each answer.

HOW TO REPLY:
Be detailed in all replies, assume little understanding of machine learning models and kelly criterion.

HOW TO IMPLEMENT:
Find good data sources online, and plan using Opus 5.5 agents on Extra High to plan the best model for us. Then implement the code using a lower cost sonnet agent, before verifying it against the plan with an Opus agent again to ensure it compiles correctly and follows the necessary plan. 

FINAL OUTPUT:
Present the exact values per question we need to enter as well as the bet we should put on for each question.

BEFORE TOUCHING THE CODEBASE:
Read through this file, and report any clarifiying questions back to us.