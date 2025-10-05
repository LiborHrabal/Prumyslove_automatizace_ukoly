# It creates graph via seaborn library
# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns       

PATH = "datasets\cnc_mill_tool_wear\experiment_01.csv"

# Load the cnc_mill_tool_wear dataset
dataset = pd.read_csv(PATH)

# Rename columns for easier access
dataset.rename(
    columns={
        "X1_ActualPosition": "X1_Pos",
        "X1_ActualVelocity": "X1_Speed",
        "X1_ActualAcceleration": "X1_Acc",
        "Y1_ActualPosition": "Y1_Pos",
        "Y1_ActualVelocity": "Y1_Speed",
        "Y1_ActualAcceleration": "Y1_Acc",
        "Z1_ActualPosition": "Z1_Pos",
        "Z1_ActualVelocity": "Z1_Speed",
        "Z1_ActualAcceleration": "Z1_Acc",
    },
    inplace=True,
)

# Get min and max values for scaling
speedX_min = dataset["X1_Speed"].min()
speedX_max = dataset["X1_Speed"].max() 
accelX_min = dataset["X1_Acc"].min()
accelX_max = dataset["X1_Acc"].max()

speedY_min = dataset["Y1_Speed"].min()
speedY_max = dataset["Y1_Speed"].max()  
accelY_min = dataset["Y1_Acc"].min()
accelY_max = dataset["Y1_Acc"].max()

# Create comparison graphs
fig, (ax1, ax3) = plt.subplots(nrows=2, ncols= 1, figsize=(12, 8))

# First axis Y on first subplot
sns.lineplot(data=dataset, x="X1_Pos", y="X1_Speed", ax=ax1, color="blue")
ax1.set_ylabel("X1_Speed", color="blue")
ax1.tick_params(axis='y', labelcolor='blue')
#ax1.set_xticks(list(range(int(dataset["X1_Pos"].min()), int(dataset["X1_Pos"].max()), 50))) # Set x-ticks with a step of 50
#ax1.set_ylim(speedX_min , speedX_max/10 + 4) # Set y-limits for better visibility

# Second axis Y on first subplot
ax2 = ax1.twinx()
sns.lineplot(data=dataset, x="X1_Pos", y="X1_Acc", ax=ax2, color="red")
ax2.set_ylabel("Acceleration", color="red")
ax2.tick_params(axis='y', labelcolor='red')
#ax2.set_ylim(accelX_min/10, accelX_max/10)

# Manual Legend
custom_lines = [
    plt.Line2D([0], [0], color="blue", lw=2, label="Speed"),
    plt.Line2D([0], [0], color="red", lw=2, label="Acceleration")
]
ax1.legend(handles=custom_lines, loc="upper right")

# First axis Y on second subplot
sns.lineplot(data=dataset, x="Y1_Pos", y="Y1_Speed", ax=ax3, color="blue")
ax3.set_ylabel("Y1_Speed", color="blue")    
ax3.tick_params(axis='y', labelcolor='blue')
ax3.set_ylim(speedY_min , speedY_max)

# Second axis Y on second subplot
ax4 = ax3.twinx()
sns.lineplot(data=dataset, x="Y1_Pos", y="Y1_Acc", ax=ax4, color="red")
ax4.set_ylabel("Acceleration", color="red") 
ax4.tick_params(axis='y', labelcolor='red')
ax4.set_ylim(accelY_min, accelY_max)

# Manual Legend
ax3.legend(handles=custom_lines, loc="upper right")

# Common title for all graphs
fig.suptitle("Comparison of Speed and Acceleration for X and Y axes", fontsize=16)
plt.tight_layout()
plt.show()

