import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# Set academic publication style
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

# Order scenarios by peak containers, then by live containers
scenario_order = [
    'Test 1 Baseline (alpine)',
    'Tier M=2 N=5',
    'Tier M=2 N=7',
    'Tier M=2 N=10',
    'Tier M=10 N=2',
    'Tier M=5 N=5',
    'Tier M=5 N=7',
    'Tier M=5 N=10',
    'Tier M=10 N=5',
]

def format_scenario_label(row):
    m = row['teams_m']
    n = row['containers_per_team_n']
    peak = row['peak_verify_containers']
    if m == 1 and n == 1:
        return 'M=1, N=1\n(2 cts)'
    return f'M={m}, N={n}\n({peak} cts)'

# Sort dataframes
df_alpine['sort_key'] = df_alpine['peak_verify_containers'] * 1000 + df_alpine['live_containers']
df_alpine = df_alpine.sort_values('sort_key').reset_index(drop=True)
df_alpine['label'] = df_alpine.apply(format_scenario_label, axis=1)

df_ubuntu['sort_key'] = df_ubuntu['peak_verify_containers'] * 1000 + df_ubuntu['live_containers']
df_ubuntu = df_ubuntu.sort_values('sort_key').reset_index(drop=True)
df_ubuntu['label'] = df_ubuntu.apply(format_scenario_label, axis=1)


# ==============================================================================
# GRAPH 1: Cold Deploy Create vs. ZFS CoW Clone Latency (Alpine vs. Ubuntu)
# ==============================================================================
def generate_graph_1():
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

    # Subplot 1: Alpine
    ax1 = axes[0]
    x = np.arange(len(df_alpine))
    width = 0.38

    bars_dep_alp = ax1.bar(x - width/2, df_alpine['deploy_create_avg_sec'], width,
                           label='Deploy Create (Cold Base Image)', color='#2b5c8f', edgecolor='black', linewidth=0.8)
    bars_cow_alp = ax1.bar(x + width/2, df_alpine['cow_clone_avg_sec'], width,
                           label='Verify CoW Clone (ZFS Snapshot)', color='#e06666', edgecolor='black', linewidth=0.8)

    # Annotate speedup
    for i, row in df_alpine.iterrows():
        dep_val = row['deploy_create_avg_sec']
        cow_val = row['cow_clone_avg_sec']
        speedup = dep_val / cow_val if cow_val > 0 else 1.0
        y_pos = max(dep_val, cow_val) + 1.5
        ax1.text(x[i], y_pos, f'{speedup:.1f}×', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#8b0000')

    ax1.set_title('Alpine Linux (3.21 MiB Rootfs)', fontweight='bold', pad=12)
    ax1.set_xlabel('Scenario (M Teams, N Containers, Peak Concurrent Containers)')
    ax1.set_ylabel('Average Latency per Team (Seconds)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_alpine['label'], rotation=0)
    ax1.grid(True, axis='y')
    ax1.legend(loc='upper left', framealpha=0.95)
    ax1.set_ylim(0, 88)

    # Subplot 2: Ubuntu Heavy
    ax2 = axes[1]
    x = np.arange(len(df_ubuntu))

    bars_dep_ubu = ax2.bar(x - width/2, df_ubuntu['deploy_create_avg_sec'], width,
                           label='Deploy Create (Cold Base Image)', color='#1b4965', edgecolor='black', linewidth=0.8)
    bars_cow_ubu = ax2.bar(x + width/2, df_ubuntu['cow_clone_avg_sec'], width,
                           label='Verify CoW Clone (ZFS Snapshot)', color='#d90429', edgecolor='black', linewidth=0.8)

    # Annotate speedup
    for i, row in df_ubuntu.iterrows():
        dep_val = row['deploy_create_avg_sec']
        cow_val = row['cow_clone_avg_sec']
        speedup = dep_val / cow_val if cow_val > 0 else 1.0
        y_pos = max(dep_val, cow_val) + 1.5
        ax2.text(x[i], y_pos, f'{speedup:.1f}×', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#8b0000')

    ax2.set_title('Ubuntu Heavy (~1.5 GB Rootfs with systemd, nginx, postgresql)', fontweight='bold', pad=12)
    ax2.set_xlabel('Scenario (M Teams, N Containers, Peak Concurrent Containers)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_ubuntu['label'], rotation=0)
    ax2.grid(True, axis='y')
    ax2.legend(loc='upper left', framealpha=0.95)

    plt.suptitle('Graph 1: Deploy Create vs. ZFS Copy-on-Write (CoW) Clone Latency Across Scaling Tiers', fontsize=15, fontweight='bold', y=0.98)
    plt.tight_layout()

    png_path = OUTPUT_DIR / 'graph1_cow_vs_deploy.png'
    pdf_path = OUTPUT_DIR / 'graph1_cow_vs_deploy.pdf'
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.close()
    print(f'[+] Graph 1 saved to {png_path} and {pdf_path}')


# ==============================================================================
# GRAPH 2: Micro-Phase Latency Breakdown at Scale (Stacked Bar Chart)
# ==============================================================================
def generate_graph_2():
    # Select representative key scaling scenarios for comparison
    # e.g., Baseline (1,1), Mid-scale (2,10), Dense Challenge (5,10), Multi-Team Concurrency (10,5)
    selected_scenarios = [
        ('Test 1 Baseline', 1, 1),
        ('Tier M=2 N=5', 2, 5),
        ('Tier M=5 N=5', 5, 5),
        ('Tier M=5 N=10', 5, 10),
        ('Tier M=10 N=2', 10, 2),
        ('Tier M=10 N=5', 10, 5),
    ]

    # Filter Ubuntu rows for these scenarios
    rows_ubuntu = []
    labels = []
    for title, m, n in selected_scenarios:
        match = df_ubuntu[(df_ubuntu['teams_m'] == m) & (df_ubuntu['containers_per_team_n'] == n)]
        if not match.empty:
            rows_ubuntu.append(match.iloc[0])
            labels.append(f'M={m}, N={n}\n({2*m*n} Peak)')

    df_sub = pd.DataFrame(rows_ubuntu).reset_index(drop=True)
    x = np.arange(len(df_sub))

    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))

    # -------------------------------------------------------------------------
    # Panel A: Deploy Micro-Phases
    # -------------------------------------------------------------------------
    ax_dep = axes[0]
    p_val = df_sub['deploy_validation_avg_sec']
    p_create = df_sub['deploy_create_avg_sec']
    p_push = df_sub['deploy_push_avg_sec']
    p_start = df_sub['deploy_start_avg_sec']
    p_net = df_sub['deploy_runtime_net_avg_sec']
    p_db = df_sub['deploy_db_record_avg_sec']

    w = 0.55
    b0 = np.zeros(len(df_sub))
    b_val = ax_dep.bar(x, p_val, w, bottom=b0, label='Validation', color='#90be6d', edgecolor='black', linewidth=0.6)
    b0 += p_val
    b_create = ax_dep.bar(x, p_create, w, bottom=b0, label='Instance Create (Image Unpack)', color='#f94144', edgecolor='black', linewidth=0.6)
    b0 += p_create
    b_push = ax_dep.bar(x, p_push, w, bottom=b0, label='Config File Push', color='#f8961e', edgecolor='black', linewidth=0.6)
    b0 += p_push
    b_start = ax_dep.bar(x, p_start, w, bottom=b0, label='Instance Start (systemd boot)', color='#f3722c', edgecolor='black', linewidth=0.6)
    b0 += p_start
    b_net = ax_dep.bar(x, p_net, w, bottom=b0, label='Runtime Network Setup', color='#277da1', edgecolor='black', linewidth=0.6)
    b0 += p_net
    b_db = ax_dep.bar(x, p_db, w, bottom=b0, label='DB Record State', color='#4d908e', edgecolor='black', linewidth=0.6)
    b0 += p_db

    # Total labels
    for i in range(len(df_sub)):
        tot = b0[i]
        ax_dep.text(x[i], tot + 1.2, f'{tot:.1f}s', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax_dep.set_title('A: Challenge Deployment Lifecycle (Cold Provisioning)', fontweight='bold', pad=12)
    ax_dep.set_xlabel('Scenario (Teams M, Containers N, Peak Scale)')
    ax_dep.set_ylabel('Average Wall Time per Team (Seconds)')
    ax_dep.set_xticks(x)
    ax_dep.set_xticklabels(labels)
    ax_dep.grid(True, axis='y')
    ax_dep.legend(loc='upper left', framealpha=0.95)
    ax_dep.set_ylim(0, 105)

    # -------------------------------------------------------------------------
    # Panel B: Verify Setup Micro-Phases
    # -------------------------------------------------------------------------
    ax_ver = axes[1]
    v_ovn = df_sub['ovn_create_avg_sec']
    v_clone = df_sub['cow_clone_avg_sec']
    v_conn = df_sub['clone_connect_avg_sec']
    v_start = df_sub['clone_start_avg_sec']
    v_net = df_sub['clone_runtime_net_avg_sec']

    vb0 = np.zeros(len(df_sub))
    vb_ovn = ax_ver.bar(x, v_ovn, w, bottom=vb0, label='OVN Dark Switch Create', color='#43aa8b', edgecolor='black', linewidth=0.6)
    vb0 += v_ovn
    vb_clone = ax_ver.bar(x, v_clone, w, bottom=vb0, label='ZFS CoW Snapshot Clone', color='#577590', edgecolor='black', linewidth=0.6)
    vb0 += v_clone
    vb_conn = ax_ver.bar(x, v_conn, w, bottom=vb0, label='NIC Rebind to OVN Switch', color='#90be6d', edgecolor='black', linewidth=0.6)
    vb0 += v_conn
    vb_start = ax_ver.bar(x, v_start, w, bottom=vb0, label='Clone Start (boot)', color='#f9c74f', edgecolor='black', linewidth=0.6)
    vb0 += v_start
    vb_net = ax_ver.bar(x, v_net, w, bottom=vb0, label='Clone Runtime Route Apply', color='#6a4c93', edgecolor='black', linewidth=0.6)
    vb0 += v_net

    # Total labels
    for i in range(len(df_sub)):
        tot = vb0[i]
        ax_ver.text(x[i], tot + 0.8, f'{tot:.1f}s', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax_ver.set_title('B: Verify Sandbox Setup Lifecycle (Ephemeral Sandboxing)', fontweight='bold', pad=12)
    ax_ver.set_xlabel('Scenario (Teams M, Containers N, Peak Scale)')
    ax_ver.set_ylabel('Average Wall Time per Team (Seconds)')
    ax_ver.set_xticks(x)
    ax_ver.set_xticklabels(labels)
    ax_ver.grid(True, axis='y')
    ax_ver.legend(loc='upper left', framealpha=0.95)
    ax_ver.set_ylim(0, 85)

    plt.suptitle('Graph 2: Micro-Phase Latency Breakdown (Ubuntu Heavy ~1.5 GB Service Stack)', fontsize=15, fontweight='bold', y=0.98)
    plt.tight_layout()

    png_path = OUTPUT_DIR / 'graph2_microphase_breakdown.png'
    pdf_path = OUTPUT_DIR / 'graph2_microphase_breakdown.pdf'
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.close()
    print(f'[+] Graph 2 saved to {png_path} and {pdf_path}')


if __name__ == '__main__':
    generate_graph_1()
    generate_graph_2()
