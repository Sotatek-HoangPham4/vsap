import matplotlib.pyplot as plt

df["topic"].value_counts().plot(kind="bar")
plt.title("Topic Distribution")
plt.savefig("reports/topic_distribution.png")