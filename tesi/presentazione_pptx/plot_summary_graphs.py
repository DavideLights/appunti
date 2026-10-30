"""Regenerate graphs 2-5 in a compact horizontal layout for the PPTX summary slide.

Same data and plotting logic as antigravity/scripts/plot_thesis_graphs.py and
plot_graphs_3_4_5.py; differences: no "Graph N:" title (the slide card provides
the caption), fixed aspect ratio matching the slide card, Arial-metric font.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

DATA = Path('/home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch')
OUT = Path(__file__).resolve().parent / 'figures'
OUT.mkdir(exist_ok=True)

# Liberation Sans is metrically identical to Arial
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Liberation Sans', 'DejaVu Sans'],
    'font.size': 12,
    'axes.labelsize': 12,
    'axes.titlesize': 12.5,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 10.5,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'savefig.dpi': 300,
})

FIGSIZE = (9.6, 3.95)  # ~2.43:1, matches the image area of each slide card

df_alpine = pd.read_csv(DATA / 'thesis_alpine_results.csv')
df_ubuntu = pd.read_csv(DATA / 'thesis_ubuntu_results.csv')


def save(fig, name):
    fig.savefig(OUT / f'{name}.png', facecolor='white')
    plt.close(fig)
    print('[+]', OUT / f'{name}.png')


def graph_2():
    sel = [(1, 1), (2, 5), (5, 5), (5, 10), (10, 2), (10, 5)]
    rows, labels = [], []
    for m, n in sel:
        match = df_ubuntu[(df_ubuntu['teams_m'] == m) & (df_ubuntu['containers_per_team_n'] == n)]
        if not match.empty:
            rows.append(match.iloc[0])
            labels.append(f'M={m},N={n}\n({2*m*n} Peak)')
    df = pd.DataFrame(rows).reset_index(drop=True)
    x = np.arange(len(df))
    w = 0.6

    fig, (a, b) = plt.subplots(1, 2, figsize=FIGSIZE, layout='constrained')

    stack = [('deploy_validation_avg_sec', 'Validation', '#90be6d'),
             ('deploy_create_avg_sec', 'Instance Create (Image Unpack)', '#f94144'),
             ('deploy_push_avg_sec', 'Config File Push', '#f8961e'),
             ('deploy_start_avg_sec', 'Instance Start (systemd boot)', '#f3722c'),
             ('deploy_runtime_net_avg_sec', 'Runtime Network Setup', '#277da1'),
             ('deploy_db_record_avg_sec', 'DB Record State', '#4d908e')]
    bottom = np.zeros(len(df))
    for col, lab, c in stack:
        a.bar(x, df[col], w, bottom=bottom, label=lab, color=c, edgecolor='black', linewidth=0.5)
        bottom += df[col].values
    for i, tot in enumerate(bottom):
        a.text(x[i], tot + 1.2, f'{tot:.1f}s', ha='center', va='bottom', fontsize=9.5, fontweight='bold')
    a.set_title('A: Challenge Deploy (Cold Provisioning)', fontweight='bold')
    a.set_ylabel('Avg Wall Time per Team (s)')
    a.set_xticks(x, labels, fontsize=8.5)
    a.grid(True, axis='y')
    a.legend(loc='upper left', framealpha=0.95, fontsize=8.5)
    a.set_ylim(0, 112)

    stack = [('ovn_create_avg_sec', 'OVN Dark Switch Create', '#43aa8b'),
             ('cow_clone_avg_sec', 'ZFS CoW Snapshot Clone', '#577590'),
             ('clone_connect_avg_sec', 'NIC Rebind to OVN Switch', '#90be6d'),
             ('clone_start_avg_sec', 'Clone Start (boot)', '#f9c74f'),
             ('clone_runtime_net_avg_sec', 'Clone Runtime Route Apply', '#6a4c93')]
    bottom = np.zeros(len(df))
    for col, lab, c in stack:
        b.bar(x, df[col], w, bottom=bottom, label=lab, color=c, edgecolor='black', linewidth=0.5)
        bottom += df[col].values
    for i, tot in enumerate(bottom):
        b.text(x[i], tot + 0.8, f'{tot:.1f}s', ha='center', va='bottom', fontsize=9.5, fontweight='bold')
    b.set_title('B: Verify Sandbox Setup (Ephemeral)', fontweight='bold')
    b.set_xticks(x, labels, fontsize=8.5)
    b.grid(True, axis='y')
    b.legend(loc='upper left', framealpha=0.95, fontsize=8.5)
    b.set_ylim(0, 90)
    save(fig, 'summary_graph2_microphase')


def graph_3():
    fig, ax = plt.subplots(figsize=FIGSIZE, layout='constrained')
    alp = df_alpine.sort_values('peak_verify_containers')
    ubu = df_ubuntu.sort_values('peak_verify_containers')
    xa, ya = alp['peak_verify_containers'].values, alp['steady_peak_net_delta_mb'].values
    xu, yu = ubu['peak_verify_containers'].values, ubu['steady_peak_net_delta_mb'].values
    ax.scatter(xa, ya, color='#2b5c8f', s=55, zorder=5, label='Alpine Empirical Measurements')
    ax.scatter(xu, yu, color='#d90429', s=55, zorder=5, label='Ubuntu Heavy Empirical Measurements')
    sa, _ = np.polyfit(xa, ya, 1)
    su, _ = np.polyfit(xu, yu, 1)
    xt = np.linspace(0, 105, 100)
    ax.plot(xt, sa * xt, '--', color='#2b5c8f', linewidth=2, label=f'Alpine Linear Model (Slope: {sa:.1f} MB / Container)')
    ax.plot(xt, su * xt, '--', color='#d90429', linewidth=2, label=f'Ubuntu Heavy Linear Model (Slope: {su:.1f} MB / Container)')
    ax.annotate('Peak 100 Containers\n+1,533 MB (15.3 MB/ct)', xy=(100, 1533), xytext=(78, 2300),
                arrowprops=dict(facecolor='#2b5c8f', shrink=0.08, width=1.5, headwidth=7),
                fontsize=10, fontweight='bold', color='#1b3b5f',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef4fb', edgecolor='#2b5c8f', alpha=0.9))
    ax.annotate('Peak 100 Containers\n+5,247 MB (52.5 MB/ct)', xy=(100, 5247), xytext=(66, 5250),
                arrowprops=dict(facecolor='#d90429', shrink=0.08, width=1.5, headwidth=7),
                fontsize=10, fontweight='bold', color='#8b0000',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#fdeeed', edgecolor='#d90429', alpha=0.9))
    ax.set_xlabel('Peak Concurrent Containers in Verification Sandbox (2 × M × N)')
    ax.set_ylabel('Net Memory Growth (MB)')
    ax.set_xlim(-2, 108)
    ax.set_ylim(-100, 6300)
    ax.grid(True)
    ax.legend(loc='upper left', framealpha=0.95)
    save(fig, 'summary_graph3_memory')


def graph_4():
    ts = pd.read_csv(DATA / 'thesis_ubuntu_timeseries.csv')
    d = ts[ts['test_name'] == 'Tier M=10 N=5'].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=FIGSIZE, layout='constrained')
    ram_ax = ax.twinx()
    t = d['elapsed_sec'].values
    cpu = pd.Series(d['cpu_pct'].values).rolling(window=5, min_periods=1).mean()
    ram = d['net_ram_mb'].values - d['net_ram_mb'].values[0]
    l1 = ax.plot(t, cpu, color='#264653', linewidth=1.3, label='Host CPU Utilization (%)')
    ax.fill_between(t, 0, cpu, color='#264653', alpha=0.15)
    l2 = ram_ax.plot(t, ram, color='#e76f51', linewidth=2.3, label='Net Container RAM Delta (+MB)')

    trans, cur = [], None
    for _, r in d.iterrows():
        if r['step_name'] != cur:
            trans.append((r['elapsed_sec'], r['step_name']))
            cur = r['step_name']
    names = {'deploy_challenges': 'Barrier 2:\nDeploy Challenges',
             'verify_setup': 'Barrier 3:\nVerify Setup',
             'verify_cleanup': 'Barrier 4:\nCleanup',
             'teardown_machines': 'Barrier 5:\nTeardown'}
    ypos = {'deploy_challenges': 96, 'verify_setup': 96, 'verify_cleanup': 96, 'teardown_machines': 96}
    for i, (t0, s) in enumerate(trans):
        t1 = trans[i + 1][0] if i + 1 < len(trans) else t[-1]
        ax.axvline(t0, color='gray', linestyle=':', alpha=0.7)
        if s in names:
            ax.text((t0 + t1) / 2, ypos[s], names[s], ha='center', va='top', fontsize=9.5, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.9))
    ax.set_xlabel('Elapsed Time from Scenario Start (s) — M=10, N=5, Peak 100 Containers')
    ax.set_ylabel('CPU (% of 8 Cores)', color='#264653', fontweight='bold')
    ram_ax.set_ylabel('Net RAM Delta (+MB)', color='#e76f51', fontweight='bold')
    ax.set_ylim(0, 100)
    ram_ax.set_ylim(-200, 6000)
    ax.tick_params(axis='y', labelcolor='#264653')
    ram_ax.tick_params(axis='y', labelcolor='#e76f51')
    ax.grid(True)
    lines = l1 + l2
    fig.legend(lines, [l.get_label() for l in lines], loc='outside upper center', ncol=2, frameon=False)
    save(fig, 'summary_graph4_timeline')


def graph_5():
    su = pd.read_csv(DATA / 'thesis_ubuntu_step_resources.csv')
    sa = pd.read_csv(DATA / 'thesis_alpine_step_resources.csv')
    su = su[su['test_name'] == 'Tier M=10 N=5'].reset_index(drop=True)
    sa = sa[sa['test_name'] == 'Tier M=10 N=5'].reset_index(drop=True)
    steps = ['1. Provision\nTeams', '2. Deploy\nChallenges', '3. Verify\nSetup',
             '4. Verify\nCleanup', '5. Teardown\nMachines', '6. Teardown\nTeams']
    fig, ax = plt.subplots(figsize=FIGSIZE, layout='constrained')
    x = np.arange(len(steps))
    w = 0.2
    series = [(sa['cpu_avg_pct'], -1.5, 'Alpine CPU Avg (%)', '#264653', 'normal'),
              (sa['iowait_avg_pct'], -0.5, 'Alpine I/O Wait (%)', '#2a9d8f', 'normal'),
              (su['cpu_avg_pct'], 0.5, 'Ubuntu Heavy CPU Avg (%)', '#e76f51', 'bold'),
              (su['iowait_avg_pct'], 1.5, 'Ubuntu Heavy I/O Wait (%)', '#f4a261', 'bold')]
    for vals, off, lab, c, fw in series:
        ax.bar(x + off * w, vals, w, label=lab, color=c, edgecolor='black', linewidth=0.6)
        for i, v in enumerate(vals):
            ax.text(x[i] + off * w, v + 0.7, f'{v:.0f}', ha='center', va='bottom', fontsize=8.5, fontweight=fw)
    ax.set_ylabel('Host Capacity (%)')
    ax.set_xticks(x, steps)
    ax.set_ylim(0, 58)
    ax.grid(True, axis='y')
    ax.legend(loc='upper right', framealpha=0.95, ncol=2)
    save(fig, 'summary_graph5_cpu_iowait')


if __name__ == '__main__':
    graph_2()
    graph_3()
    graph_4()
    graph_5()
