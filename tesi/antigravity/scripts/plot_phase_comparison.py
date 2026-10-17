#!/usr/bin/env python3
"""
plot_phase_comparison.py

Generates bar graphs comparing execution times across test lifecycle phases
for M=5, N=10 vs M=10, N=5 (50 live containers / 100 peak containers).
Produces graphs for Alpine Linux, Ubuntu Heavy, and a combined comparison figure.
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
ANTIGRAVITY_DIR = SCRIPT_DIR.parent
DATA_DIR = ANTIGRAVITY_DIR / 'data' / 'processed'
FIG_DIR = ANTIGRAVITY_DIR / 'figures'
SRC_IMG_DIR = REPO_ROOT / 'src' / 'images'

FIG_DIR.mkdir(parents=True, exist_ok=True)
SRC_IMG_DIR.mkdir(parents=True, exist_ok=True)

# Phase definitions and labels
PHASES = [
    ('provision_teams', 'B1: Provision\nTeams (OVN)'),
    ('deploy_challenges', 'B2: Deploy\nChallenges'),
    ('verify_setup', 'B3: Verify\nSetup (CoW)'),
    ('verify_cleanup', 'B4: Verify\nCleanup'),
    ('teardown_machines', 'B5: Teardown\nMachines'),
    ('teardown_teams', 'B6: Teardown\nTeams (OVN)'),
]

PHASE_KEYS = [p[0] for p in PHASES]
PHASE_LABELS = [p[1] for p in PHASES]


def load_data(csv_path):
    df = pd.read_csv(csv_path)
    # Filter for M=5, N=10 and M=10, N=5
    df_m5_n10 = df[(df['teams_m'] == 5) & ((df['containers_per_team_n'] == 10) | (df.get('containers_n') == 10))]
    df_m10_n5 = df[(df['teams_m'] == 10) & ((df['containers_per_team_n'] == 5) | (df.get('containers_n') == 5))]
    
    # Extract wall times
    def get_times(row):
        return [
            row['provision_wall_sec'].values[0],
            row['deploy_wall_sec'].values[0],
            row['verify_setup_wall_sec'].values[0],
            row['verify_cleanup_wall_sec'].values[0],
            row['teardown_machines_wall_sec'].values[0],
            row['teardown_teams_wall_sec'].values[0],
        ]
    
    times_m5_n10 = get_times(df_m5_n10)
    times_m10_n5 = get_times(df_m10_n5)
    return times_m5_n10, times_m10_n5


def plot_single(times_m5, times_m10, title, out_prefix, color_m5='#1d3557', color_m10='#457b9d', subtitle=None):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    x = np.arange(len(PHASE_LABELS))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, times_m5, width, label='M=5, N=10 (5 Teams × 10 Cts)', color=color_m5, edgecolor='black', linewidth=0.8, zorder=3)
    rects2 = ax.bar(x + width/2, times_m10, width, label='M=10, N=5 (10 Teams × 5 Cts)', color=color_m10, edgecolor='black', linewidth=0.8, zorder=3)
    
    ax.set_ylabel('Execution Time (seconds)', fontweight='semibold')
    ax.set_xlabel('Lifecycle Test Phases', fontweight='semibold', labelpad=10)
    
    full_title = title if not subtitle else f"{title}\n{subtitle}"
    ax.set_title(full_title, fontsize=12, pad=14)
    
    ax.set_xticks(x)
    ax.set_xticklabels(PHASE_LABELS)
    ax.legend(frameon=True, facecolor='white', framealpha=0.92, loc='upper right')
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    
    # Value annotations on top of bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}s',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
            
    autolabel(rects1)
    autolabel(rects2)
    
    # Adjust y-limit to provide headroom
    max_h = max(max(times_m5), max(times_m10))
    ax.set_ylim(0, max_h * 1.18)
    
    fig.tight_layout()
    
    for ext in ['png', 'pdf']:
        fig_path = FIG_DIR / f'{out_prefix}.{ext}'
        fig.savefig(fig_path)
        print(f"Saved: {fig_path}")
        if ext == 'png':
            src_path = SRC_IMG_DIR / f'{out_prefix}.png'
            fig.savefig(src_path)
            print(f"Copied to thesis: {src_path}")
            
    plt.close(fig)


def plot_combined_side_by_side(alp_m5, alp_m10, ubu_m5, ubu_m10):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), sharey=True, dpi=300)
    
    x = np.arange(len(PHASE_LABELS))
    width = 0.35
    
    # Subplot 1: Alpine
    r1 = ax1.bar(x - width/2, alp_m5, width, label='M=5, N=10 (50 cts)', color='#2b5c8f', edgecolor='black', linewidth=0.8, zorder=3)
    r2 = ax1.bar(x + width/2, alp_m10, width, label='M=10, N=5 (50 cts)', color='#5c88b8', edgecolor='black', linewidth=0.8, zorder=3)
    ax1.set_title('Alpine Linux (3.2 MB Rootfs)', fontweight='bold', pad=12)
    ax1.set_xlabel('Lifecycle Test Phases', fontweight='semibold', labelpad=10)
    ax1.set_ylabel('Execution Time (seconds)', fontweight='semibold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(PHASE_LABELS)
    ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.92)
    ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    
    # Subplot 2: Ubuntu Heavy
    r3 = ax2.bar(x - width/2, ubu_m5, width, label='M=5, N=10 (50 cts)', color='#b7094c', edgecolor='black', linewidth=0.8, zorder=3)
    r4 = ax2.bar(x + width/2, ubu_m10, width, label='M=10, N=5 (50 cts)', color='#e05780', edgecolor='black', linewidth=0.8, zorder=3)
    ax2.set_title('Ubuntu Heavy (~1.5 GB Rootfs, systemd, PostgreSQL)', fontweight='bold', pad=12)
    ax2.set_xlabel('Lifecycle Test Phases', fontweight='semibold', labelpad=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels(PHASE_LABELS)
    ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.92)
    ax2.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    
    def autolabel_ax(ax, rects):
        for rect in rects:
            h = rect.get_height()
            ax.annotate(f'{h:.1f}s',
                        xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold')
            
    autolabel_ax(ax1, r1)
    autolabel_ax(ax1, r2)
    autolabel_ax(ax2, r3)
    autolabel_ax(ax2, r4)
    
    max_h = max(max(ubu_m5), max(ubu_m10))
    ax1.set_ylim(0, max_h * 1.18)
    
    fig.suptitle('Lifecycle Phase Timing Comparison: Deep (M=5, N=10) vs. Wide (M=10, N=5) Topologies', fontsize=14, fontweight='bold', y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    
    for ext in ['png', 'pdf']:
        fig_path = FIG_DIR / f'graph_phases_comparison.{ext}'
        fig.savefig(fig_path)
        print(f"Saved: {fig_path}")
        if ext == 'png':
            src_path = SRC_IMG_DIR / f'graph_phases_comparison.png'
            fig.savefig(src_path)
            print(f"Copied to thesis: {src_path}")
            
    plt.close(fig)



def main():
    alp_csv = DATA_DIR / 'thesis_alpine_results.csv'
    ubu_csv = DATA_DIR / 'thesis_ubuntu_results.csv'
    
    alp_m5, alp_m10 = load_data(alp_csv)
    ubu_m5, ubu_m10 = load_data(ubu_csv)
    
    print("Generating Alpine Linux Phase Comparison Graph...")
    plot_single(
        alp_m5, alp_m10,
        title='Lifecycle Phase Execution Times: Alpine Linux (50 Containers Total)',
        out_prefix='graph_phases_alpine',
        color_m5='#1d3557',
        color_m10='#457b9d',
        subtitle='Comparison between Deep Topology (M=5, N=10) and Wide Topology (M=10, N=5)'
    )
    
    print("Generating Ubuntu Heavy Phase Comparison Graph...")
    plot_single(
        ubu_m5, ubu_m10,
        title='Lifecycle Phase Execution Times: Ubuntu Heavy (50 Containers Total)',
        out_prefix='graph_phases_ubuntu',
        color_m5='#7209b7',
        color_m10='#b5179e',
        subtitle='Comparison between Deep Topology (M=5, N=10) and Wide Topology (M=10, N=5)'
    )
    
    print("Generating Side-by-Side Unified Comparison Graph...")
    plot_combined_side_by_side(alp_m5, alp_m10, ubu_m5, ubu_m10)
    
    print("All phase comparison graphs generated successfully!")


if __name__ == '__main__':
    main()
