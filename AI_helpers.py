
import random
import matplotlib.pyplot as plt
import pandas as pd
import math

def overgewicht(gewicht, lengte):
    """
    Genereer of iemand overgewicht heeft. Iemand heeft overgewicht bij BMI>25.
    Omdat de klassen linear te scheiden moeten zijn, versimpel ik het kwadratisch
    verband tussen gewicht en lengte naar een lineair verband. Ik neem als waarde
    voor de tweede lengte 1.70m - de gemiddelde lengte in de populatie.
    """
    bmi = 10000 * gewicht / lengte / 170
    if bmi < 25:
        return 0
    elif bmi > 25:
        return 1
    else:
        return 1 if random.uniform(0, 1) > 0.5 else 0

def genereer_data(n = 50):
    """
    Genereer je eigen dataset. Het gemiddelde gewicht is ongeveer 70 kg en
    de gemiddelde lengte is ongeveer 1 meter 70. De dataset is voor iedereen
    verschillend.
    """
    # normaal verdeelde lengte en gewicht:
    gewicht = [random.gauss(68, 5) for _ in range(n)]
    lengte = [random.gauss(170, 10) for _ in range(n)]
    
    # bereken bmi en bepaal of iemand ongezond is of gezond:
    ongezond = [overgewicht(g, l) for g, l in zip(gewicht, lengte)]
    
    return pd.DataFrame({'gewicht': gewicht, 'lengte': lengte, 'overgewicht': ongezond})

def visualiseer_data(data: pd.DataFrame):
    """
    Plot je data. 
    """
    # kijk of de waarden "correct" zijn
    if 'lengte' not in data.columns:
        raise ValueError('Data onjuist. Bevat geen kolom met lengte.')
    elif 'gewicht' not in data.columns:
        raise ValueError('Data onjuist. Bevat geen kolom met gewicht.')
    elif 'overgewicht' not in data.columns:
        raise ValueError('Data onjuist. Bevat geen kolom met overgewicht.')
    
    # creëer plot:
    fig, ax = plt.subplots()
    
    scatter = ax.scatter(
        x = data['lengte'].to_list(),
        y = data['gewicht'].to_list(),
        c = data['overgewicht'].to_list()
    )
    
    # voeg namen toe aan assen
    if data['lengte'].mean() < 1:
        ax.set_xlabel('Lengte (genormaliseerd)')
    else:
        ax.set_xlabel('Lengte (cm)')
        
    if data['gewicht'].mean() < 1:
        ax.set_ylabel('Gewicht (genormaliseerd)')
    else:
        ax.set_ylabel('Gewicht (cm)')
        
    # voeg legenda toe
    legend1 = ax.legend(*scatter.legend_elements(),
                    loc="lower right", title="Wel/geen overgewicht")
    ax.add_artist(legend1)


def visualiseer_voorspelling(data: pd.DataFrame, titel = None):
    if 'lengte' not in data.columns:
        raise ValueError('Data onjuist. Bevat geen kolom met lengte.')
    elif 'gewicht' not in data.columns:
        raise ValueError('Data onjuist. Bevat geen kolom met gewicht.')
    elif 'voorspelling' not in data.columns:
        raise ValueError('Data onjuist. Bevat geen kolom met overgewicht.')
    
    global ax
    fig, ax = plt.subplots()
    
    ax.scatter(
        x = data['lengte'],
        y = data['gewicht'],
        c = data['voorspelling']
    )
    if data['lengte'].mean() < 1:
        ax.set_xlabel('Lengte (genormaliseerd)')
    else:
        ax.set_xlabel('Lengte (cm)')
    if data['gewicht'].mean() < 1:
        ax.set_ylabel('Gewicht (genormaliseerd)')
    else:
        ax.set_ylabel('Gewicht (cm)')
    
    if titel is not None:
        ax.set_title(titel)
    
    fig.show()

def maak_voorspelling(data, b, l, g):
    """
    Doe een voorspelling over de klasse van patiënten in je dataset
    op basis van de parameters b, l en g. Welke patiënten hebben
    overgewicht, en welke niet?
    """
    activatie = [b + l * data['lengte'].loc[i] + g * data['gewicht'].loc[i] for i in range(len(data))]
    data['voorspelling'] = [1 if a > 0 else 0 for a in activatie]
    
    return data

def update_gewichten(data, b, l, g, eta = 0.01):
    """
    Update de parameters b, l en g op basis van je voorspelling en de data.
    Als je voorspelling goed is, worden de parameters maar een klein beetje
    veranderd. Als je voorspelling slecht is, worden de parameters veel
    meer veranderd.
    
    Tot slot: eta is de leersnelheid. Als je het interessant vind om daar
    meer over te lezen, kijk dan naar de bonusvraag.
    """
    for rij in data.iterrows():
        error = rij[1]['overgewicht'] - rij[1]['voorspelling']
        b = b + eta * error
        l = l + eta * error * rij[1]['lengte']
        g = g + eta * error * rij[1]['gewicht']
    
    return b, l, g


def gemiddelde(meetwaarden):
    return sum(meetwaarden) / len(meetwaarden)

def standaard_deviatie(meetwaarden):    
    som = 0
    for x in meetwaarden:
        som = som + (x - gemiddelde(meetwaarden)) ** 2
    
    variantie = som / (len(meetwaarden) - 1)
    
    return math.sqrt(variantie)