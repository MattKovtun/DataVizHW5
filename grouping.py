import pandas as pd

df = pd.read_csv("population_by_age_sex_year.csv")

groups = [("0 - 20", 20), ("20 - 40", 40), ("40 - 60", 60), ("60 - 80", 80)]

df = df[df["age"] != "Вік невідомий"]
df = df[df["age"] != "80 і старше"]
df["age"] = pd.to_numeric(df["age"])
df["men"] = pd.to_numeric(df["men"])
df["women"] = pd.to_numeric(df["women"])

res = []

for age in df["age"]:
    for g in groups:
        if age < g[1]:
            res.append(g[0])
            break

df["group"] = res

df.to_csv("population_by_age_sex_year_grouped.csv")


