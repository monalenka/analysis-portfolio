import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

df = pd.read_csv("data.csv", sep=";")

df = df[df["Дата"] != "Итого"]

num_cols = [
    "Установки", "Регистрации", "Открыли поиск",
    "Просмотрели авто", "Забронировали", "Первая поездка"
]
for col in num_cols:
    df[col] = df[col].astype(str).str.replace(" ", "").astype(int)

weekly = df.groupby("Неделя")[num_cols].sum().reset_index()

weekly["U->R"] = weekly["Регистрации"] / weekly["Установки"]
weekly["R->S"] = weekly["Открыли поиск"] / weekly["Регистрации"]
weekly["S->V"] = weekly["Просмотрели авто"] / weekly["Открыли поиск"]
weekly["V->B"] = weekly["Забронировали"] / weekly["Просмотрели авто"]
weekly["B->T"] = weekly["Первая поездка"] / weekly["Забронировали"]

conv_cols = ["U->R", "R->S", "S->V", "V->B", "B->T"]
base = weekly[conv_cols].iloc[0]
norm = weekly[conv_cols].div(base) * 100

fig, ax = plt.subplots(figsize=(14, 7))

colors = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd"]
labels = [
    "Установка → Регистрация",
    "Регистрация → Поиск",
    "Поиск → Просмотр авто",
    "Просмотр → Бронь",
    "Бронь → Первая поездка"
]

for i, col in enumerate(conv_cols):
    ax.plot(weekly["Неделя"], norm[col], marker="o", color=colors[i],
            label=labels[i], linewidth=2.5 if col == "R->S" else 1.5,
            alpha=1.0 if col == "R->S" else 0.6)

ax.axhline(100, color="gray", linestyle="--", alpha=0.5, label="Уровень Недели 1 (100%)")


ax.set_title("Динамика конверсии по этапам воронки (нормировано к Неделе 1)", fontsize=14)
ax.set_ylabel("Конверсия, % от Недели 1")
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
ax.legend(loc="lower left", frameon=True)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()