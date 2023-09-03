# Heart Disease Fuzzy Expert System

This is one of my final projects in the "Computational Intelligence" course at AUT. In this project, I've implemented a fuzzy intelligent system that can decide whether a person has a heart problem or not and at what grade is the problem.

```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

Localhost:8448

![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/main_page.png)

## Input Parameters & Fuzzification

- ### Age
  
  Age of the patient in range of [0,100]
  
  ![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/age.png)

- ### Blood Pressure
  
  Blood pressure in range of [0, 350]
  
  ![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/bloodPressure.png)

- ### Cholesterol
  
  Amount of cholesterol in range of [0, 600]
  
  ![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/cholesterol.png) 

- ### Blood Sugar
  
  Amount of blood sugar in range of [0, 200]
  
  ![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/bloodSugar.png)

- ### ECG
  
  A simple test that can be used to check your heart's rhythm and electrical activity. Its value is in range of [-0.5, 2.5]
  
  ![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/ECG.png)

- ### Maximum Heart Rate
  
  Maximum heart rate of the patient in past 24 hours in range of [0, 600].
  
  ![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/heartRate.png)

- ### Exerciese
  
  A crisp set inidicating that exercise is allowed for the patient or not. If it has 0 value it means that exercise is not allowed for the patient and vice verca for 1 value.
  
  ![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/exercise.png)

- ### Old Peak
  
  Degree of oldpeak in range of [0,10].
  
  ![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/oldPeak.png)

- ### Thallium
  
  Amount of thallium in patient's body which can be 3 crisp values. (3, 6, 7)
  
  ![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/thallium.png)

- ### Sex
  
  Sex of the patient. 1 for women and 0 for men.
  
  ![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/sex.png)

## Output Fuzzysets

We have one output parameter which is the health of the patient. It has 5 fuzzysets containing healty, sick1, sick2, sick3 and sick4.

![](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/fuzzysets/health.png)

## Rules

There is a [file](https://github.com/Amirparsa-Sal/Heart-Disease-Fuzzy-Intelligent-System/blob/master/rules.fcl) cotaining all rules of the inference engine. The rules can only contain and/or operators.




