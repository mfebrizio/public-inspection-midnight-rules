# import dependencies
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# set default pixel density
# reference: https://blakeaw.github.io/2020-05-25-improve-matplotlib-notebook-inline-res/
# reference: https://stackoverflow.com/questions/31594549/how-to-change-the-figure-size-of-a-seaborn-axes-or-figure-level-plot
sns.set(rc={"figure.dpi": 300, 
            "savefig.dpi": 300, 
            "figure.figsize": (11.7, 8.27)
            })


def plot_and_save_barh(df, x_var, y_var, cat_var, 
                       color_list: list = None, 
                       xlabel: str = None, ylabel: str = None, 
                       title: str = "", legend_title: str = "", 
                       xlim: tuple = None, xticks: tuple = (None, None), 
                       text_annotation: tuple = (0.1, 0.01, ""), 
                       save_as = Path(__file__) / r"figure.png"):

    xtick_points, xtick_labels = xticks  # unpack tuple for x-axis ticks
    a, b, text = text_annotation  # unpack tuple for text annotation
    sns.set_theme(style="whitegrid")
    g = sns.catplot(x=x_var, y=y_var, data=df, 
                    hue=cat_var, kind="bar", 
                    orient="h", palette=color_list, 
                    legend=False  # add legend manually for no legend title option
                    )

    plt.xticks(xtick_points, xtick_labels)
    g.set(xlim=xlim)
    g.set_xlabels(xlabel)
    g.set_ylabels(ylabel)
    g.tight_layout()
    g.add_legend(title=legend_title)  # default is no legend title
    g.fig.subplots_adjust(top=0.9, bottom=0.15)  # make room for text annontation
    g.fig.suptitle(title, fontsize=14)
    g.figure.text(a, b, text, fontsize=9)
    g.savefig(save_as)

