import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# Publication styling
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'sans-serif',
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
})

BASE_DIR = Path('/home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch')
OUTPUT_DIR = BASE_DIR / 'thesis_figures'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df_alpine = pd.read_csv(BASE_DIR / 'thesis_alpine_results.csv')
df_ubuntu = pd.read_csv(BASE_DIR / 'thesis_ubuntu_results.csv')

# ==============================================================================
# GRAPH 3: Net Container Memory Scaling (Alpine vs. Ubuntu Heavy)
# ==============================================================================
def generate_graph_3():
    fig, ax = plt.subplots(figsize=(10, 6))

    # Sort by peak containers
    df_alp_sorted = df_alpine.sort_values('peak_verify_containers').reset_index(drop=True)
    df_ubu_sorted = df_ubuntu.sort_values('peak_verify_containers').reset_index(drop=True)

    x_alp = df_alp_sorted['peak_verify_containers'].values
    y_alp = df_alp_sorted['steady_peak_net_delta_mb'].values

    x_ubu = df_ubu_sorted['peak_verify_containers'].values
    y_ubu = df_ubu_sorted['steady_peak_net_delta_mb'].values

    # Plot empirical points
    ax.scatter(x_alp, y_alp, color='#2b5c8f', s=70, zorder=5, label='Alpine Empirical Measurements')
    ax.scatter(x_ubu, y_ubu, color='#d90429', s=70, zorder=5, label='Ubuntu Heavy Empirical Measurements')

    # Fit linear regression trend lines (forcing intercept near 0)
    slope_alp, _ = np.polyfit(x_alp, y_alp, 1)
    slope_ubu, _ = np.polyfit(x_ubu, y_ubu, 1)

    x_trend = np.linspace(0, 105, 100)
    ax.plot(x_trend, slope_alp * x_trend, '--', color='#2b5c8f', linewidth=2,
            label=f'Alpine Linear Model (Slope: {slope_alp:.1f} MB / Container)')
    ax.plot(x_trend, slope_ubu * x_trend, '--', color='#d90429', linewidth=2,
            label=f'Ubuntu Heavy Linear Model (Slope: {slope_ubu:.1f} MB / Container)')

    # Annotate peak points
    ax.annotate(f'Peak 100 Containers\n+1,533 MB (15.3 MB/ct)',
                xy=(100, 1533), xytext=(80, 2200),
                arrowprops=dict(facecolor='#2b5c8f', shrink=0.08, width=1.5, headwidth=7),
                fontsize=9.5, fontweight='bold', color='#1b3b5f',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#eef4fb', edgecolor='#2b5c8f', alpha=0.9))

    ax.annotate(f'Peak 100 Containers\n+5,247 MB (52.5 MB/ct)',
                xy=(100, 5247), xytext=(70, 5600),
                arrowprops=dict(facecolor='#d90429', shrink=0.08, width=1.5, headwidth=7),
                fontsize=9.5, fontweight='bold', color='#8b0000',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#fdeeed', edgecolor='#d90429', alpha=0.9))

    ax.set_title('Graph 3: Net Container Memory Scaling (Alpine vs. Ubuntu Heavy)', fontweight='bold', pad=14)
    ax.set_xlabel('Peak Concurrent Containers in Verification Sandbox (2 × M × N)')
    ax.set_ylabel('Net Memory Growth Over Baseline (MB, Excluding ZFS ARC)')
    ax.set_xlim(-2, 108)
    ax.set_ylim(-100, 6300)
    ax.grid(True)
    ax.legend(loc='upper left', framealpha=0.95)

    plt.tight_layout()
    png_path = OUTPUT_DIR / 'graph3_memory_scaling.png'
    pdf_path = OUTPUT_DIR / 'graph3_memory_scaling.pdf'
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.close()
    print(f'[+] Graph 3 saved to {png_path} and {pdf_path}')


# ==============================================================================
# GRAPH 4: Lifecycle Timeline: CPU % and Net RAM (Dual-Axis Time-Series)
# ==============================================================================
def generate_graph_4():
    df_ts = pd.read_csv(BASE_DIR / 'thesis_ubuntu_timeseries.csv')
    df_t10 = df_ts[df_ts['test_name'] == 'Tier M=10 N=5'].copy().reset_index(drop=True)

    fig, ax_cpu = plt.subplots(figsize=(14, 6.5))
    ax_ram = ax_cpu.twinx()

    t = df_t10['elapsed_sec'].values
    cpu = df_t10['cpu_pct'].values
    net_ram = df_t10['net_ram_mb'].values
    baseline_ram = net_ram[0]
    net_ram_delta = net_ram - baseline_ram

    # Plot CPU on left axis (smoothed with moving average for clarity)
    cpu_smooth = pd.Series(cpu).rolling(window=5, min_periods=1).mean()
    l1 = ax_cpu.plot(t, cpu_smooth, color='#264653', linewidth=1.8, label='Host CPU Utilization (%)')
    ax_cpu.fill_between(t, 0, cpu_smooth, color='#264653', alpha=0.15)

    # Plot Net RAM Delta on right axis
    l2 = ax_ram.plot(t, net_ram_delta, color='#e76f51', linewidth=2.5, label='Net Container RAM Delta (+MB)')

    # Identify step transitions
    step_transitions = []
    current_step = None
    for _, row in df_t10.iterrows():
        s = row['step_name']
        if s != current_step:
            step_transitions.append((row['elapsed_sec'], s))
            current_step = s

    # Label colors and vertical lines for barriers
    phase_colors = {
        'provision_teams': '#e9c46a',
        'deploy_challenges': '#f4a261',
        'verify_setup': '#e76f51',
        'verify_cleanup': '#2a9d8f',
        'teardown_machines': '#264653',
        'teardown_teams': '#457b9d',
    }

    phase_display_names = {
        'provision_teams': 'Barrier 1:\nProvision Teams',
        'deploy_challenges': 'Barrier 2:\nDeploy Challenges\n(50 Live Containers)',
        'verify_setup': 'Barrier 3:\nVerify Setup\n(100 Containers Alive!)',
        'verify_cleanup': 'Barrier 4:\nVerify Cleanup',
        'teardown_machines': 'Barrier 5:\nTeardown Containers',
        'teardown_teams': 'Barrier 6:\nTeardown Teams',
    }

    # Add phase demarcation lines
    label_y_offsets = {
        'provision_teams': 92,
        'deploy_challenges': 88,
        'verify_setup': 88,
        'verify_cleanup': 76,
        'teardown_machines': 88,
        'teardown_teams': 76,
    }

    for i in range(len(step_transitions)):
        t_start, s_name = step_transitions[i]
        t_end = step_transitions[i+1][0] if i + 1 < len(step_transitions) else t[-1]
        t_mid = (t_start + t_end) / 2

        ax_cpu.axvline(t_start, color='gray', linestyle=':', alpha=0.7)
        if s_name in ('deploy_challenges', 'verify_setup', 'verify_cleanup', 'teardown_machines'):
            y_pos = label_y_offsets.get(s_name, 88)
            ax_cpu.text(t_mid, y_pos, phase_display_names[s_name], ha='center', va='top',
                        fontsize=8.5, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.88))

    ax_cpu.set_title('Graph 4: Host Lifecycle Telemetry Timeline (Tier M=10 Teams, N=5 Containers — Peak 100 Instances)',
                     fontweight='bold', pad=14)
    ax_cpu.set_xlabel('Elapsed Time from Scenario Start (Seconds)')
    ax_cpu.set_ylabel('CPU Utilization (% Across 8 Cores)', color='#264653', fontweight='bold')
    ax_ram.set_ylabel('Net Container RAM Delta (+MB Over Baseline)', color='#e76f51', fontweight='bold')

    ax_cpu.set_ylim(0, 100)
    ax_ram.set_ylim(-200, 6000)

    ax_cpu.tick_params(axis='y', labelcolor='#264653')
    ax_ram.tick_params(axis='y', labelcolor='#e76f51')
    ax_cpu.grid(True)

    # Combined legend
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax_cpu.legend(lines, labels, loc='upper left', framealpha=0.95)

    plt.tight_layout()
    png_path = OUTPUT_DIR / 'graph4_lifecycle_timeline.png'
    pdf_path = OUTPUT_DIR / 'graph4_lifecycle_timeline.pdf'
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.close()
    print(f'[+] Graph 4 saved to {png_path} and {pdf_path}')


# ==============================================================================
# GRAPH 5: Per-Step CPU & I/O Wait Utilization (Grouped Bar Chart)
# ==============================================================================
def generate_graph_5():
    df_step_ubu = pd.read_csv(BASE_DIR / 'thesis_ubuntu_step_resources.csv')
    df_step_alp = pd.read_csv(BASE_DIR / 'thesis_alpine_step_resources.csv')

    # Filter for the peak scale scenario M=10, N=5
    s_ubu = df_step_ubu[df_step_ubu['test_name'] == 'Tier M=10 N=5'].reset_index(drop=True)
    s_alp = df_step_alp[df_step_alp['test_name'] == 'Tier M=10 N=5'].reset_index(drop=True)

    step_labels = [
        '1. Provision\nTeams',
        '2. Deploy\nChallenges',
        '3. Verify\nSetup',
        '4. Verify\nCleanup',
        '5. Teardown\nMachines',
        '6. Teardown\nTeams'
    ]

    fig, ax = plt.subplots(figsize=(13, 6))

    x = np.arange(len(step_labels))
    width = 0.20

    # Bars: Alpine CPU Avg, Alpine I/O Wait, Ubuntu CPU Avg, Ubuntu I/O Wait
    b1 = ax.bar(x - 1.5*width, s_alp['cpu_avg_pct'], width, label='Alpine CPU Avg (%)', color='#264653', edgecolor='black', linewidth=0.7)
    b2 = ax.bar(x - 0.5*width, s_alp['iowait_avg_pct'], width, label='Alpine I/O Wait (%)', color='#2a9d8f', edgecolor='black', linewidth=0.7)
    b3 = ax.bar(x + 0.5*width, s_ubu['cpu_avg_pct'], width, label='Ubuntu Heavy CPU Avg (%)', color='#e76f51', edgecolor='black', linewidth=0.7)
    b4 = ax.bar(x + 1.5*width, s_ubu['iowait_avg_pct'], width, label='Ubuntu Heavy I/O Wait (%)', color='#f4a261', edgecolor='black', linewidth=0.7)

    # Annotate values
    for i in range(len(x)):
        val_alp_cpu = s_alp['cpu_avg_pct'].iloc[i]
        val_alp_io = s_alp['iowait_avg_pct'].iloc[i]
        val_ubu_cpu = s_ubu['cpu_avg_pct'].iloc[i]
        val_ubu_io = s_ubu['iowait_avg_pct'].iloc[i]

        ax.text(x[i] - 1.5*width, val_alp_cpu + 0.7, f'{val_alp_cpu:.1f}%', ha='center', va='bottom', fontsize=7.5)
        ax.text(x[i] - 0.5*width, val_alp_io + 0.7, f'{val_alp_io:.1f}%', ha='center', va='bottom', fontsize=7.5)
        ax.text(x[i] + 0.5*width, val_ubu_cpu + 0.7, f'{val_ubu_cpu:.1f}%', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax.text(x[i] + 1.5*width, val_ubu_io + 0.7, f'{val_ubu_io:.1f}%', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    ax.set_title('Graph 5: Host CPU Utilization & I/O Wait Across the 6 Lifecycle Barriers (Peak 100 Containers)',
                 fontweight='bold', pad=14)
    ax.set_xlabel('Lifecycle Step (Barrier Synchronized)')
    ax.set_ylabel('Percentage of Host Capacity (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(step_labels)
    ax.set_ylim(0, 55)
    ax.grid(True, axis='y')
    ax.legend(loc='upper right', framealpha=0.95, ncol=2)

    plt.tight_layout()
    png_path = OUTPUT_DIR / 'graph5_step_cpu_iowait.png'
    pdf_path = OUTPUT_DIR / 'graph5_step_cpu_iowait.pdf'
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.close()
    print(f'[+] Graph 5 saved to {png_path} and {pdf_path}')


if __name__ == '__main__':
    generate_graph_3()
    generate_graph_4()
    generate_graph_5()
