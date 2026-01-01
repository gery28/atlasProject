from tqdm import tqdm
import requests
from api import landmark_to_coords_open, landmark_to_coords_google
import os

data = ["hungary", "Strait of Gibraltar", "Alaska", "caribbean sea", "Mississippi Plains", "Volga", "Panama-canal",
        "Kamchatka Peninsula", "North Europe", "Vienna Basin", "Iberian Peninsula", "Mátra",
        "Pécsi ókeresztény sírkamrák",
        "Early Christian tombs of Pécs", "Szabolcs-Szatmár-Bereg megye", "Dunántúl", "Kis-Balaton", "Soproni-hegység",
        "Salgótarján", "Duna", "Aggteleki Nemzeti Park", "Middle East Asia"]

landmarks_asia = []
landmarks_hun = []
# for i in data:
# landmarks.append([i, landmark_to_coords(i)])

titles_asia = {"A földrész részei": "Parts of the continent", "Tájak": "Landscapes", "Vízrajz": "Waterscape",
               "Országok": "Countries",
               "Városok": "Cities"}

markers_asia = {"Parts of the continent": ["red", "cloud"], "Landscapes": ["green", "cloud"],
                "Waterscape": ["blue", "cloud"],
                "Countries": ["orange", "cloud"],
                "Cities": ["pink", "cloud"]}

titles_hun = {"Fő tájegységek": "Main regions", "Egyéb tájak, területek": "Other landscapes, areas",
              "Vízrajz": "Waterscape", "Települések": "Settlements",
              "Nemzeti parkok,világörökségek": "National parks, world heritage sites",
              "Megyék": "Counties", "Nagyrégiók, régiók": "Large regions, regions"}

markers_hun = {"Main regions": ["red", "cloud"], "Other landscapes, areas": ["green", "cloud"],
               "Waterscape": ["blue", "cloud"],
               "Settlements": ["orange", "cloud"],
               "National parks, world heritage sites": ["pink", "cloud"],
               "Counties": ["purple", "cloud"],
               "Large regions, regions": ["darkred", "cloud"]}

def create_dict_asia():
    asia = []
    with open("asia.txt", "r", encoding="utf-8") as file:
        for i in file.read().split("*"):
            segment = []
            for j in i.split(", "):
                if j != "":
                    segment.append(j.strip("\n").replace("\n", " "))
            if len(segment) != 0:
                asia.append(segment)
    print(*asia, sep="\n")
    print("\n")
    asia_eng = []
    with open("asia-eng.txt", "r", encoding="utf-8") as file:
        for i in file.read().split("*"):
            segment = []
            for j in i.split(", "):
                if j != "":
                    segment.append(j.strip("\n").replace("\n", " "))
            if len(segment) != 0:
                asia_eng.append(segment)
    # print(*asia_eng, sep="\n")
    # print(list(titles.items()))
    asia_dict = []
    for i in range(len(asia)):
        for j in range(len(asia[i])):
            asia_dict.append([list(titles_asia.items())[i][1], {asia[i][j]: asia_eng[i][j]}])

    print(*asia_dict, sep="\n")
    print(list(asia_dict[0][1].items())[0])

    for i in tqdm(asia_dict):
        print(list(i[1].items())[0])
        landmarks_asia.append([i, landmark_to_coords_open(list(i[1].items())[0][0], list(i[1].items())[0][1])])

    with open("asia-save.txt", "w", encoding="utf-8") as file:
        file.write(str(landmarks_asia))


def create_dict_hun():
    hungary = []
    with open("hungary.txt", "r", encoding="utf-8") as file:
        for i in file.read().split("*"):
            segment = []
            for j in i.split(", "):
                if j != "":
                    segment.append(j.strip("\n").replace("\n", " "))
            if len(segment) != 0:
                hungary.append(segment)
    print(*hungary, sep="\n")
    print("\n")
    hun_dict = []
    for i in range(len(hungary)):
        for j in range(len(hungary[i])):
            hun_dict.append([list(titles_hun.items())[i][1], {hungary[i][j]: 1}])

    print(*hun_dict, sep="\n")
    print(list(hun_dict[0][1].items())[0])

    for i in tqdm(hun_dict):
        print(list(i[1].items())[0])
        landmarks_hun.append([i, landmark_to_coords_google(list(i[1].items())[0][0])])
    with open("hun-save.txt", "w", encoding="utf-8") as file:
        file.write(str(landmarks_hun))


if __name__ == '__main__':
    # create_dict_asia()
    create_dict_hun()
