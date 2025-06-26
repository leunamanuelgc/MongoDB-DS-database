import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set up visual styling
sns.set(style="whitegrid")

# --- DATA ---

data = {
    ("NO INDEX", "VERSION 1"): [
        504, 573, 429, 540, 420, 503, 603, 559, 590, 512, 676, 2575, 586, 755,
        2254, 500, 862, 1705, 631, 704, 901, 630, 614, 567, 803
    ],
    ("NO INDEX", "VERSION 2"): [
        684, 610, 610, 618, 848, 591, 652, 766, 607, 713, 677, 566, 1879, 1139,
        875, 1130, 633, 1356, 958, 883
    ],
    ("NO INDEX", "VERSION 1.5"): [
        1288, 801, 1104, 1262, 1453, 1299, 1446, 1601
    ],

    ("INDEX nombre_1_manchas_sangre.tiempo_muerte_-1", "VERSION 1"): [
        1771, 894, 1316, 1766, 735, 533, 601, 596, 610, 792, 838, 684
    ],
    ("INDEX nombre_1_manchas_sangre.tiempo_muerte_-1", "VERSION 2"): [
        612, 593, 773, 828, 1784, 1171, 805, 779, 707, 731, 696, 1001, 905
    ],

    ("INDEX manchas_sangre.tiempo_muerte_1_nombre_1", "VERSION 1"): [
        746, 1086, 1086, 671, 553, 669, 638, 507, 1193, 759, 511, 927, 784
    ],
    ("INDEX manchas_sangre.tiempo_muerte_1_nombre_1", "VERSION 2"): [
        660, 540, 722, 592, 811, 1166, 773, 742, 774, 590, 625, 650, 705
    ],

    ("INDEX manchas_sangre.tiempo_muerte_1", "VERSION 1"): [
        511, 933, 666, 462, 917, 661, 574, 662, 581, 561, 803, 508, 743,
        599, 593, 691, 515, 566, 627, 543, 535
    ],
    ("INDEX manchas_sangre.tiempo_muerte_1", "VERSION 2"): [
        624, 723, 696, 648, 608, 697, 774, 760, 760
    ],
    ("INDEX manchas_sangre.tiempo_muerte_1", "VERSION 1.5"): [
        562, 582, 592, 637, 702, 1102, 1569, 754, 834, 760, 1011, 671
    ],
}

# --- Flatten and load into a DataFrame ---

rows = []
for (index_type, version), times in data.items():
    for t in times:
        rows.append({"Index": index_type, "Version": version, "Tiempo (ms)": t})
df = pd.DataFrame(rows)

# --- Plotting ---

plt.figure(figsize=(14, 8))
ax = sns.boxplot(data=df, x="Index", y="Tiempo (ms)", hue="Version")

# Highlight best choice (VERSION 1 + index)
highlight = (df["Index"] == "INDEX manchas_sangre.tiempo_muerte_1") & (df["Version"] == "VERSION 1")
mean_v1 = df[highlight]["Tiempo (ms)"].mean()
plt.axhline(mean_v1, color="green", linestyle="--", linewidth=1.5, label=f"Mean of Best: {mean_v1:.0f} ms")

plt.title("T. de ejecución consulta longevidad jugadores, según Version y Index", fontsize=14)
plt.xticks(rotation=15)
plt.legend()
plt.tight_layout()
plt.show()
