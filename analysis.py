from pylab import np, plt

result_folder = "results"

last = open("{}/last.txt".format(result_folder)).read()
print("Last session", last)

print(open("{}/save{}.txt".format(result_folder, last)).read())
data = np.load("{}/indirect_strategies{}.npy".format(result_folder, last))

x = np.arange(len(data[:]))

plt.plot(x, data[:, 0], c="red")
plt.plot(x, data[:, 1], c="blue")
plt.plot(x, data[:, 2], c="green")

plt.show()
