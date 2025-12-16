from tqdm import tqdm
import requests
from api import landmark_to_coords


data = ["hungary", "Strait of Gibraltar", "Alaska", "caribbean sea", "Mississippi Plains", "Volga", "Panama-canal",
        "Kamchatka Peninsula", "North Europe", "Vienna Basin", "Iberian Peninsula", "Mátra",
        "Pécsi ókeresztény sírkamrák",
        "Early Christian tombs of Pécs", "Szabolcs-Szatmár-Bereg megye", "Dunántúl", "Kis-Balaton", "Soproni-hegység",
        "Salgótarján", "Duna", "Aggteleki Nemzeti Park", "Middle East Asia"]


landmarks = []
# for i in data:
# landmarks.append([i, landmark_to_coords(i)])

titles = {"A földrész részei": "Parts of the continent", "Tájak": "Landscapes", "Vízrajz": "Waterscape",
          "Országok": "Countries",
          "Városok": "Cities"}

markers = {"Parts of the continent": ["red", "cloud"], "Landscapes": ["green", "cloud"],
           "Waterscape": ["blue", "cloud"],
           "Countries": ["orange", "cloud"],
           "Cities": ["pink", "cloud"]}
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
        asia_dict.append([list(titles.items())[i][1], {asia[i][j]: asia_eng[i][j]}])

print(*asia_dict, sep="\n")
print(list(asia_dict[0][1].items())[0])

for i in tqdm(asia_dict):
    print(list(i[1].items())[0])
    landmarks.append([i, landmark_to_coords(list(i[1].items())[0][0], list(i[1].items())[0][1])])

with open("asia-save.txt", "w", encoding="utf-8") as file:
    file.write(str(landmarks))
