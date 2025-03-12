import roadrunner
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
from typing import List


def get_steady_state(fax: float) -> List[float]:
    rr.reset()
    rr.M_FAx = fax
    rr.steadyStateSelections = ["M_LD", "M_TAG", "M_FA"]
    return rr.getSteadyStateValues()


rr = roadrunner.RoadRunner("SimpleFALiver.xml")
rr.reset()
rr.simulate(
    0, 5, 200,
    selections=["time", "M_LD", "M_TAG", "M_FA"]
)
fig, ax = plt.subplots()
rr.plot(show=False)
ax.legend()
ax.set_xlabel("Time")
ax.set_ylabel("Concentration")
fig.tight_layout()

fig.savefig("SimpleFALiver.png")

fax_range = np.arange(0, 5, .01)
result_dict = {
    "M_FAx": list(),
    "M_LD": list(),
    "M_TAG": list(),
    "M_FA": list()
}

with mp.Pool(mp.cpu_count()) as pool:
    results = pool.map(
        get_steady_state,
        fax_range
    )

for fax, res in zip(fax_range, results):
    result_dict["M_FAx"].append(fax)
    result_dict["M_LD"].append(res[0])
    result_dict["M_TAG"].append(res[1])
    result_dict["M_FA"].append(res[2])
fig, ax = plt.subplots()
ax.plot(result_dict["M_FAx"], result_dict["M_LD"], label="LD")
ax.plot(result_dict["M_FAx"], result_dict["M_TAG"], label="TAG")
ax.plot(result_dict["M_FAx"], result_dict["M_FA"], label="FA")
ax.legend()
ax.set_xlabel("FAx")
ax.set_ylabel("Concentration")
fig.tight_layout()
fig.savefig("SimpleFALiver_steady_state.png")
