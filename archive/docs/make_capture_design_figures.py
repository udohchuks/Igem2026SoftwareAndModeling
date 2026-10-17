"""Generate the single-occupancy capture sizing investigation, ISSUES 91."""
from pathlib import Path
import sys,json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src import params,recovery_audit,recovery_chain as rc,capture_design as design,expression
p=recovery_audit.operating_parameters()
c=params.values(params.load("capture_design")["analysis"])
v=params.values(params.load("recovery_process")["volumes"])
feed=p["Au_feed"]*v["feed_volume_L"]
biomass=p["X_max"]*v["feed_volume_L"]
volume=v["capture_volume_L"]
q=p["q_max"]
base=float(rc.capture_equilibrium(feed/volume,q*biomass/volume,p["K_Au"]))*volume
sites=q*biomass
points=np.geomspace(1,c["capacity_multiplier_max"],c["grid_points"])
fractions=rc.capture_equilibrium(feed/volume,q*points*biomass/volume,p["K_Au"])*volume/feed
series=design.fresh_contact_series(feed,volume,p["K_Au"],q,biomass,c["contacts"])
active=expression.steady_state(params.values(params.load("expression")))["A"]
targets=[]
for target in c["target_fractions"]:
    required=design.required_site_amount(feed,volume,p["K_Au"],target)
    reached=np.flatnonzero(series["cumulative_captured_gold_amount_umol"]>=target*feed)
    targets.append(dict(target_fraction=target,required_site_amount_umol=required,
                        required_biomass_g=required/q,required_capacity_umol_per_g=required/biomass,
                        required_active_sites_per_cell=active*required/sites,
                        fresh_contacts=int(reached[0]) if len(reached) else None))
plt.rcParams.update({"font.size":12,"axes.spines.top":False,"axes.spines.right":False})
fig,axes=plt.subplots(2,1,figsize=(8,7))
axes[0].semilogx(points,fractions,color="#087e8b")
axes[0].plot(1,base/feed,'o',color="#bd5932",label="Current site-only model")
for row in targets:
    axes[0].plot(row["required_site_amount_umol"]/sites,row["target_fraction"],'o',color="#bd5932")
axes[0].set(xlabel="Site capacity / current site capacity (fixed biomass)",ylabel="Fraction captured",title="Low capture follows the assumed site inventory")
axes[0].legend(fontsize=10)
axes[1].plot(series["contact_number"],series["cumulative_captured_gold_amount_umol"]/feed,color="#087e8b")
axes[1].set(xlabel=f"Fresh contacts ({biomass:g} g dry cells added for every contact)",ylabel="Cumulative fraction captured",title="Fresh biomass can add capacity; waiting alone cannot")
fig.tight_layout()
out=Path(__file__).resolve().parent/'media'/'recovery_model'
out.mkdir(exist_ok=True,parents=True)
fig.savefig(out/'capture_capacity_investigation.png',dpi=180,bbox_inches='tight')
plt.close(fig)
result=dict(feed_umol=feed,biomass_g=biomass,active_sites_per_cell=active,
            single_occupancy_capacity_umol_per_g=q,site_amount_umol=sites,
            captured_umol=base,site_occupancy=base/sites,targets=targets)
(out/'capture_investigation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
