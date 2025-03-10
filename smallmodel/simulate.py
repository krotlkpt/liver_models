import roadrunner
import matplotlib.pyplot as plt


rr = roadrunner.RoadRunner("SimpleFALiver.xml")
rr.reset()
rr.simulate(
    0, 10, 100,
    selections=["time", "M_LD", "M_FAx"]
)
fig, ax = plt.subplots()
# ax.plot(rr.time, rr.M_LD, label="LD")
# ax.plot(rr.time, rr.M_FAx, label="FAx")
# ax.legend()
rr.plot(show=False)
ax.legend()

fig.savefig("SimpleFALiver.png")